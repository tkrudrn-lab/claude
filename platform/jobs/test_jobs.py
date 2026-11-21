# platform/jobs/test_jobs.py — `python -m unittest test_jobs -v` (이 폴더에서)
import os, tempfile, unittest
from pathlib import Path


class EnvFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        os.environ["HERMES_CONFIG_DIR"] = str(self.tmp / "cfg")
        (self.tmp / "cfg").mkdir()
        (self.tmp / "cfg" / "paths.env").write_text(
            f"# 주석\n\nHERMES_LOGS={self.tmp / 'logs'}\nHERMES_VIVA=~/사진 폴더\nODD=a=b\n", encoding="utf-8")


class TestCommon(EnvFixture):
    def test_load_env_parses_and_expands(self):
        import common
        env = common.load_env("paths")
        self.assertEqual(env["HERMES_LOGS"], str(self.tmp / "logs"))
        self.assertEqual(env["HERMES_VIVA"], os.path.expanduser("~/사진 폴더"))
        self.assertEqual(env["ODD"], "a=b")
        self.assertNotIn("# 주석", env)

    def test_load_env_missing_raises_with_hint(self):
        import common
        with self.assertRaises(FileNotFoundError) as cm:
            common.load_env("telegram")
        self.assertIn("telegram.env.example", str(cm.exception))

    def test_log_line_appends(self):
        import common
        p = common.log_line("catalog", "비바 +3 −0")
        p2 = common.log_line("catalog", "둘째")
        self.assertEqual(p, p2)
        self.assertEqual(p, self.tmp / "logs" / "catalog.log")
        lines = p.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].endswith("| 비바 +3 −0"))


import io, json, urllib.error
from contextlib import contextmanager


class FakeTelegram:
    """urlopen 대역. calls 에 (method, body_bytes) 누적. fail_methods 는 HTTP 400 으로 거절."""
    def __init__(self, ok=True, raise_url_error=False, fail_methods=(), raise_exc=None):
        self.ok, self.raise_url_error, self.calls = ok, raise_url_error, []
        self.fail_methods, self.raise_exc = set(fail_methods), raise_exc

    def __call__(self, req, timeout=None):
        if self.raise_exc:
            raise self.raise_exc
        if self.raise_url_error:
            raise urllib.error.URLError("no network")
        method = req.full_url.rsplit("/", 1)[1]
        self.calls.append((method, req.data or b""))
        if method in self.fail_methods:
            raise urllib.error.HTTPError(req.full_url, 400, "Bad Request", None,
                                         io.BytesIO(b'{"ok":false,"description":"PHOTO_INVALID_DIMENSIONS"}'))
        body = json.dumps({"ok": self.ok, "description": "chat not found", "result": {}}).encode()

        @contextmanager
        def resp():
            yield io.BytesIO(body)
        return resp()


class TestNotify(EnvFixture):
    def setUp(self):
        super().setUp()
        (self.tmp / "cfg" / "telegram.env").write_text(
            "TELEGRAM_BOT_TOKEN=123:abc\nTELEGRAM_CHAT_ID=777\n", encoding="utf-8")
        import notify
        self.notify = notify
        self.fake = FakeTelegram()
        notify.urlopen = self.fake

    def _method(self):
        return self.fake.calls[-1][0]

    def test_text_uses_sendMessage(self):
        self.assertTrue(self.notify.send("카탈로그 · 비바 +3", job="catalog"))
        self.assertEqual(self._method(), "sendMessage")
        self.assertIn(b"777", self.fake.calls[-1][1])

    def test_jpg_uses_sendPhoto(self):
        p = self.tmp / "썸네일.jpg"; p.write_bytes(b"\xff\xd8\xff" + b"0" * 10)
        self.assertTrue(self.notify.send("제목", file=p, job="blog"))
        self.assertEqual(self._method(), "sendPhoto")
        self.assertIn(b'name="photo"', self.fake.calls[-1][1])
        self.assertIn("제목".encode(), self.fake.calls[-1][1])

    def test_mp4_uses_sendVideo_and_other_uses_sendDocument(self):
        v = self.tmp / "E03.mp4"; v.write_bytes(b"0" * 10)
        d = self.tmp / "buyers.csv"; d.write_bytes(b"0" * 10)
        self.notify.send("릴스", file=v); self.assertEqual(self._method(), "sendVideo")
        self.notify.send("바이어", file=d); self.assertEqual(self._method(), "sendDocument")

    def test_big_file_falls_back_to_text_with_path(self):
        import urllib.parse
        self.addCleanup(setattr, self.notify, "MAX_FILE_BYTES", self.notify.MAX_FILE_BYTES)
        self.notify.MAX_FILE_BYTES = 5
        v = self.tmp / "big.mp4"; v.write_bytes(b"0" * 10)
        self.assertTrue(self.notify.send("렌더 완료", file=v, job="seocheon"))
        self.assertEqual(self._method(), "sendMessage")
        form = urllib.parse.parse_qs(self.fake.calls[-1][1].decode())
        self.assertIn("파일: ", form["text"][0])
        self.assertIn("big.mp4", form["text"][0])

    def test_long_text_truncated(self):
        import urllib.parse
        self.notify.send("가" * 5000)
        form = urllib.parse.parse_qs(self.fake.calls[-1][1].decode())
        self.assertEqual(len(form["text"][0]), 4096)

    def test_api_not_ok_returns_false_and_logs(self):
        self.notify.urlopen = FakeTelegram(ok=False)
        self.assertFalse(self.notify.send("x", job="inbox"))
        self.assertTrue((self.tmp / "logs" / "inbox.log").exists())

    def test_url_error_returns_false_and_logs(self):
        self.notify.urlopen = FakeTelegram(raise_url_error=True)
        self.assertFalse(self.notify.send("x", job="inbox"))
        self.assertEqual(len((self.tmp / "logs" / "inbox.log").read_text(encoding="utf-8").splitlines()), 1)

    # --- 리뷰 Important 2: 첨부가 없거나 거절돼도 텍스트는 간다, 어떤 예외도 밖으로 안 나간다 ---
    def test_missing_file_falls_back_to_text(self):
        import urllib.parse
        self.assertTrue(self.notify.send("썸네일", file=self.tmp / "없는.jpg", job="blog"))
        self.assertEqual(self._method(), "sendMessage")
        self.assertIn("없는.jpg", urllib.parse.parse_qs(self.fake.calls[-1][1].decode())["text"][0])

    def test_attachment_rejected_falls_back_to_text(self):
        self.notify.urlopen = self.fake = FakeTelegram(fail_methods={"sendPhoto"})
        p = self.tmp / "띠.png"; p.write_bytes(b"\x89PNG" + b"0" * 10)
        self.assertTrue(self.notify.send("서천 스틸", file=p))
        self.assertEqual([m for m, _ in self.fake.calls], ["sendPhoto", "sendMessage"])

    def test_non_urlerror_exception_returns_false_and_logs(self):
        self.notify.urlopen = FakeTelegram(raise_exc=TimeoutError("timed out"))
        self.assertFalse(self.notify.send("x", job="inbox"))
        self.assertEqual(len((self.tmp / "logs" / "inbox.log").read_text(encoding="utf-8").splitlines()), 1)


import csv, shutil, subprocess, sys
from contextlib import redirect_stdout


def _png(path, size=(4, 3), exif_dt=None):
    from PIL import Image
    img = Image.new("RGB", size, "green")
    if exif_dt:
        ex = img.getexif(); ex.get_ifd(0x8769)[0x9003] = exif_dt
        img.save(path, exif=ex.tobytes())
    else:
        img.save(path)


def _rows(folder):
    with open(folder / "_catalog.csv", encoding="utf-8-sig", newline="") as f:
        return {r["rel_path"]: r for r in csv.DictReader(f)}


class TestCatalog(EnvFixture):
    def setUp(self):
        super().setUp()
        import catalog; self.catalog = catalog
        self.folder = self.tmp / "비바 사진"
        (self.folder / "하위 폴더").mkdir(parents=True)
        (self.folder / "_mosaic").mkdir()
        (self.folder / "툴 사본").mkdir(); (self.folder / "툴 사본" / ".nocatalog").touch()
        _png(self.folder / "a.png", exif_dt="2026:10:17 14:03:22")
        _png(self.folder / "b.png")
        _png(self.folder / "하위 폴더" / "ㄱ.jpg")
        _png(self.folder / "_mosaic" / "skip.png")
        _png(self.folder / "툴 사본" / "skip2.png")
        (self.folder / "메모.txt").write_text("x")

    def test_update_adds_media_only_with_exif_and_dims(self):
        self.assertEqual(self.catalog.update_catalog(self.folder), (3, 0))
        rows = _rows(self.folder)
        self.assertEqual(set(rows), {"a.png", "b.png", "하위 폴더/ㄱ.jpg"})
        self.assertEqual(rows["a.png"]["taken"], "2026-10-17 14:03:22")
        self.assertEqual((rows["a.png"]["width"], rows["a.png"]["height"]), ("4", "3"))
        self.assertRegex(rows["b.png"]["taken"], r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")  # mtime 폴백

    def test_rerun_keeps_note_and_drops_removed(self):
        self.catalog.update_catalog(self.folder)
        rows = _rows(self.folder); rows["a.png"]["note"] = "루비 모프 성체"
        with open(self.folder / "_catalog.csv", "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=self.catalog.COLUMNS); w.writeheader(); w.writerows(rows.values())
        self.assertEqual(self.catalog.update_catalog(self.folder), (0, 0))
        self.assertEqual(_rows(self.folder)["a.png"]["note"], "루비 모프 성체")
        (self.folder / "b.png").unlink()
        self.assertEqual(self.catalog.update_catalog(self.folder), (0, 1))
        self.assertNotIn("b.png", _rows(self.folder))

    def test_corrupt_image_row_kept(self):
        (self.folder / "bad.jpg").write_bytes(b"not an image")
        added, _ = self.catalog.update_catalog(self.folder)
        self.assertEqual(added, 4)
        self.assertEqual(_rows(self.folder)["bad.jpg"]["width"], "")

    def test_video_without_ffprobe_gets_empty_dims(self):
        (self.folder / "v.mp4").write_bytes(b"0" * 100)
        self.addCleanup(setattr, self.catalog.shutil, "which", shutil.which)
        self.catalog.shutil.which = lambda name: None
        self.catalog.update_catalog(self.folder)
        r = _rows(self.folder)["v.mp4"]
        self.assertEqual((r["duration_s"], r["width"]), ("", ""))
        self.assertTrue(r["taken"])

    def test_main_missing_folder(self):
        with redirect_stdout(io.StringIO()):  # main() 의 요약 출력이 테스트 로그를 더럽히지 않게
            self.assertEqual(self.catalog.main([str(self.tmp / "없는 폴더")]), 1)
            self.assertEqual(self.catalog.main([str(self.tmp / "없는 폴더"), str(self.folder)]), 0)

    # --- 리뷰 C1: 윈도우에서 stdout 이 파이프면 cp949 라 '−' 에서 죽는다 ---
    def test_cli_survives_piped_stdout_without_utf8_env(self):
        env = {k: v for k, v in os.environ.items() if k not in ("PYTHONIOENCODING", "PYTHONUTF8")}
        r = subprocess.run([sys.executable, "catalog.py", str(self.folder)], capture_output=True,
                           env=env, cwd=Path(__file__).parent)
        self.assertEqual(r.returncode, 0, r.stderr)

    # --- 리뷰 Important 1: 폴더 하나의 예외가 나머지 폴더와 알림을 죽이면 안 된다 ---
    def test_main_reports_folder_failure_and_still_notifies(self):
        import notify
        sent = []
        self.addCleanup(setattr, notify, "send", notify.send)
        notify.send = lambda text, file=None, job="manual": sent.append((text, job)) or True
        bad = self.tmp / "잠긴 폴더"; bad.mkdir()
        real = self.catalog.update_catalog
        self.addCleanup(setattr, self.catalog, "update_catalog", real)

        def boom(folder):
            if Path(folder) == bad:
                raise PermissionError("locked")
            return real(folder)
        self.catalog.update_catalog = boom
        with redirect_stdout(io.StringIO()):
            self.assertEqual(self.catalog.main([str(bad), str(self.folder), "--notify"]), 0)
        self.assertEqual(len(sent), 1)
        self.assertIn("잠긴 폴더 실패", sent[0][0])
        self.assertEqual(sent[0][1], "catalog")

    # --- 리뷰 Important 3: HERMES_CATALOG_DIRS 의 두 번째 경로부터 ~ 가 안 풀린다 ---
    def test_catalog_dirs_tilde_expands_each_path(self):
        for k in ("USERPROFILE", "HOME"):
            old = os.environ.get(k)
            self.addCleanup(lambda k=k, old=old: os.environ.__setitem__(k, old) if old is not None else os.environ.pop(k, None))
            os.environ[k] = str(self.tmp)
        (self.tmp / "cfg" / "paths.env").write_text(
            f"HERMES_LOGS={self.tmp / 'logs'}\nHERMES_CATALOG_DIRS=~/없는; ~/비바 사진\n", encoding="utf-8")
        with redirect_stdout(io.StringIO()) as out:
            self.assertEqual(self.catalog.main([]), 0)
        self.assertIn("비바 사진 +3", out.getvalue())

    # --- 리뷰 Important 4: ffprobe 가 없으면 조용히 영구 빈칸 — 알림 줄에 경고 ---
    def test_main_warns_when_ffprobe_missing(self):
        self.addCleanup(setattr, self.catalog.shutil, "which", shutil.which)
        self.catalog.shutil.which = lambda name: None
        with redirect_stdout(io.StringIO()) as out:
            self.catalog.main([str(self.folder)])
        self.assertIn("ffprobe 없음", out.getvalue())

    # --- 리뷰 Important 5: 영상 taken 은 로컬 시각, epoch 값은 무시 ---
    def test_video_taken_is_local_time_and_epoch_ignored(self):
        from datetime import datetime, timezone
        v = self.folder / "v.mov"; v.write_bytes(b"0" * 10)
        self.addCleanup(setattr, self.catalog.shutil, "which", shutil.which)
        self.catalog.shutil.which = lambda name: "ffprobe"
        self.addCleanup(setattr, self.catalog.subprocess, "run", subprocess.run)
        canned = {"streams": [{"width": 1920, "height": 1080, "side_data_list": [{"rotation": -90}]}],
                  "format": {"duration": "7.56", "tags": {"creation_time": "2025-10-11T19:05:21.000000Z"}}}
        self.catalog.subprocess.run = lambda *a, **k: subprocess.CompletedProcess(a, 0, json.dumps(canned), "")
        r = self.catalog.probe(v)
        expect = datetime(2025, 10, 11, 19, 5, 21, tzinfo=timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual((r["taken"], r["duration_s"], r["width"], r["height"]), (expect, "7.6", "1080", "1920"))
        canned["format"]["tags"]["creation_time"] = "1904-01-01T00:00:00.000000Z"
        self.assertRegex(self.catalog.probe(v)["taken"], r"^20\d\d-")  # mtime 폴백


class FakeOllama:
    """urlopen 대역. requests 에 (url, body dict) 누적, answers 를 모델 응답 content 로 돌려준다."""
    def __init__(self, answers=None, raise_exc=None):
        self.answers, self.raise_exc, self.requests = answers or {}, raise_exc, []

    def __call__(self, req, timeout=None):
        if self.raise_exc:
            raise self.raise_exc
        self.requests.append((req.full_url, json.loads(req.data)))
        body = json.dumps({"message": {"content": json.dumps(self.answers)}}).encode()

        @contextmanager
        def resp():
            yield io.BytesIO(body)
        return resp()


QUESTIONS = {
    "dept": {"type": "choice", "instructions": "어느 팀이 맡나?",
             "criteria": {"billing": "결제·환불", "tech": "버그·장애"}},
    "anger": {"type": "score", "instructions": "고객이 얼마나 화났나?", "criteria": ["차분", "답답", "매우 화남"]},
    "urgent": {"type": "noul", "instructions": "지금 급한가?"},
}


class TestJudge(EnvFixture):
    def setUp(self):
        super().setUp()
        import judge
        self.judge = judge
        self.fake = FakeOllama({"dept": "billing", "anger": 2, "urgent": 0.9})
        self.addCleanup(setattr, judge, "urlopen", judge.urlopen)
        judge.urlopen = self.fake

    def test_returns_jev_shaped_answers(self):
        a = self.judge.judge("결제가 3일째 실패해요", QUESTIONS)
        self.assertEqual(a, {"dept": {"choice": "billing"}, "anger": {"score": 2}, "urgent": {"noul": 0.9}})

    def test_request_goes_to_local_ollama_with_schema(self):
        self.judge.judge("결제가 3일째 실패해요", QUESTIONS)
        url, body = self.fake.requests[0]
        self.assertEqual(url, "http://localhost:11434/api/chat")
        self.assertEqual((body["model"], body["stream"], body["think"]), ("main-64k", False, False))
        props = body["format"]["properties"]
        self.assertEqual(props["dept"]["enum"], ["billing", "tech"])
        self.assertEqual((props["anger"]["minimum"], props["anger"]["maximum"]), (0, 2))
        self.assertIn("결제가 3일째 실패해요", body["messages"][-1]["content"])

    def test_url_and_model_from_paths_env(self):
        (self.tmp / "cfg" / "paths.env").write_text(
            "HERMES_JUDGE_URL=http://100.114.236.66:11434/\nHERMES_JUDGE_MODEL=qwen3:8b\n", encoding="utf-8")
        self.judge.judge("x", QUESTIONS)
        url, body = self.fake.requests[0]
        self.assertEqual((url, body["model"]), ("http://100.114.236.66:11434/api/chat", "qwen3:8b"))

    def test_bad_question_rejected_before_call(self):
        bad = {"anger": {"type": "score", "instructions": "화났나?", "criteria": ["하나뿐"]}}
        with self.assertRaises(ValueError):
            self.judge.judge("x", bad)
        self.assertEqual(self.fake.requests, [])

    def test_out_of_range_answer_raises(self):
        self.fake.answers = {"dept": "sales", "anger": 2, "urgent": 0.9}
        with self.assertRaises(ValueError):
            self.judge.judge("x", QUESTIONS)

    # 리뷰: 스키마를 어긴 답(리스트·bool)은 TypeError·확실한 '예'가 아니라 ValueError
    def test_wrong_typed_answers_raise_value_error(self):
        for bad in ({"dept": ["billing"]}, {"urgent": True}, {"anger": True}):
            self.fake.answers = {"dept": "billing", "anger": 2, "urgent": 0.9, **bad}
            with self.assertRaises(ValueError, msg=bad):
                self.judge.judge("x", QUESTIONS)

    def test_non_object_reply_raises_value_error(self):
        self.fake.answers = ["billing"]
        with self.assertRaises(ValueError):
            self.judge.judge("x", QUESTIONS)

    # 리뷰: 빈 state·이상한 질문은 그럴듯한 판정이 되기 전에 막는다
    def test_empty_state_and_malformed_question_rejected_before_call(self):
        for state, qs in (("", QUESTIONS), (None, QUESTIONS), ("x", {"u": "질문"}),
                          ("x", {"u": {"type": "noul", "instructions": None}})):
            with self.assertRaises(ValueError, msg=(state, qs)):
                self.judge.judge(state, qs)
        self.assertEqual(self.fake.requests, [])

    # 호출 실패는 '아니오'가 아니라 에러다 — 삼키지 않는다
    def test_network_error_propagates(self):
        self.fake.raise_exc = urllib.error.URLError("no route")
        with self.assertRaises(OSError):
            self.judge.judge("x", QUESTIONS)


class TestGemini(EnvFixture):  # 네트워크 없이 — 입력 만들기 · 결과 읽기만
    def setUp(self):
        super().setUp()
        import gemini
        self.g = gemini

    def test_parse_script_joins_continuations_and_ignores_unknown_names(self):
        script = "Alex: 안녕\n이어지는 줄\n\nSam: 메모: 이건 대사\nNote: 대사 안 콜론"
        self.assertEqual(self.g.parse_script(script, {"Alex", "Sam"}), [
            ("Alex", "안녕 이어지는 줄"), ("Sam", "메모: 이건 대사 Note: 대사 안 콜론")])
        with self.assertRaises(ValueError):
            self.g.parse_script("머리말\nAlex: 안녕", {"Alex"})

    def test_secs(self):
        self.assertEqual([self.g.secs(x) for x in ("90", "2:30", "1:02:03")], [90, 150, 3723])

    def test_speech_block_only_annotates_when_needed(self):
        self.assertEqual(self.g.speech_block("hi"), {"type": "text", "text": "hi"})
        self.assertEqual(self.g.speech_block("hi", speaker="Sam")["annotations"],
                         [{"type": "speech_metadata", "speaker": "Sam"}])

    def test_sources_dedupes_citations(self):
        from types import SimpleNamespace as N
        cite = lambda url: N(type="url_citation", url=url, title=None)
        it = N(steps=[N(type="google_search_call"), N(type="model_output", content=[
            N(type="text", annotations=[cite("https://a"), cite("https://b"), cite("https://a")])])])
        self.assertEqual(self.g.sources(it), ["https://a — https://a", "https://b — https://b"])

    def test_media_block_rejects_non_image_audio(self):
        p = self.tmp / "x.png"
        p.write_bytes(b"\x89PNG")
        self.assertEqual(self.g.media_block(str(p))["type"], "image")
        with self.assertRaises(ValueError):
            self.g.media_block(str(self.tmp / "x.txt"))

    def test_video_clip_offsets(self):
        self.assertEqual(self.g.video_block("https://youtu.be/x", 120, 270)["processing"],
                         {"type": "static", "start_offset": "120s", "end_offset": "270s"})
        self.assertNotIn("processing", self.g.video_block("https://youtu.be/x"))

    def test_local_video_uploads_file_object_not_path(self):  # 경로를 주면 한글 파일 이름이 HTTP 헤더에서 깨진다
        from types import SimpleNamespace as N
        p = self.tmp / "씨앗.mp4"
        p.write_bytes(b"x")
        seen = {}
        done = N(state=N(name="ACTIVE"), uri="files/u", mime_type="video/mp4", name="files/1")
        c = N(files=N(upload=lambda file, config: seen.update(file=file, config=config) or done))
        self.assertEqual(self.g.video_block(str(p), c=c)["uri"], "files/u")
        self.assertNotIsInstance(seen["file"], str)
        self.assertEqual(seen["config"], {"mime_type": "video/mp4"})

    def test_image_always_asks_jpeg_and_saves_jpg(self):  # png 요청은 API가 400으로 거절한다
        import base64
        from unittest import mock
        from types import SimpleNamespace as N
        seen = {}
        def create(**kw):
            seen.update(kw)
            return N(output_image=N(data=base64.b64encode(b"jpegbytes").decode()))
        with mock.patch.object(self.g, "client", lambda: N(interactions=N(create=create))):
            out = self.g.image("잎", self.tmp / "a.png", aspect="1:1")
        self.assertEqual(out.suffix, ".jpg")
        self.assertEqual(out.read_bytes(), b"jpegbytes")
        self.assertEqual(seen["response_format"], {"type": "image", "mime_type": "image/jpeg", "aspect_ratio": "1:1"})

    def _fake_voices(self, seen):
        import base64
        from types import SimpleNamespace as N
        mine = N(voices=[N(id="voice_new1", display_name="자연내레이터"), N(id="voice_old2", display_name="샵소개")])
        def create(store, voice):
            seen.update(store=store, voice=voice)
            return N(id="voice_new1", sample_audio=N(data=base64.b64encode(b"RIFFwav").decode()))
        return N(voices=N(list=lambda type_: mine, create=create, delete=lambda id: seen.update(deleted=id)))

    def test_resolve_voice_by_name_and_passthrough(self):
        from unittest import mock
        with mock.patch.object(self.g, "client", lambda: self._fake_voices({})):
            self.assertEqual(self.g.resolve_voice("Kore"), "Kore")
            self.assertEqual(self.g.resolve_voice("voice_abc"), "voice_abc")
            self.assertEqual(self.g.resolve_voice("샵소개"), "voice_old2")
            with self.assertRaises(ValueError) as cm:
                self.g.resolve_voice("없는목소리")
            self.assertIn("자연내레이터", str(cm.exception))

    def test_voice_create_stores_prompted_voice_and_saves_sample(self):
        from unittest import mock
        seen = {}
        with mock.patch.object(self.g, "client", lambda: self._fake_voices(seen)):
            vid = self.g.voice_create("낮고 따뜻한 내레이터", "자연내레이터", gender="male", sample=self.tmp / "p.wav")
            self.g.voice_delete("자연내레이터")
        self.assertEqual(vid, "voice_new1")
        self.assertTrue(seen["store"])
        self.assertEqual(seen["voice"], {"model": self.g.TTS_MODEL, "type": "prompted", "display_name": "자연내레이터",
                                         "language_code": "ko-KR", "prompted": {"input": "낮고 따뜻한 내레이터"},
                                         "gender": "male"})
        self.assertEqual((self.tmp / "p.wav").read_bytes(), b"RIFFwav")
        self.assertEqual(seen["deleted"], "voice_new1")

    def _fake_create(self, calls, fail):
        """fail(model) 이 예외를 주면 던지고, 아니면 그 모델 이름으로 답한다."""
        from types import SimpleNamespace as N
        def create(model, timeout, **kw):
            calls.append((model, timeout))
            if err := fail(model):
                raise err
            return N(output_text=f"answer from {model}", steps=[])
        return lambda: N(interactions=N(create=create))

    def test_text_falls_back_to_lite_when_main_model_busy(self):  # 2026-11-21 기본 모델 503 · 3분 멈춤
        from unittest import mock
        busy = type("InternalServerError", (Exception,), {"status_code": 503})
        calls = []
        fake = self._fake_create(calls, lambda m: busy("high demand") if m == self.g.TEXT_MODEL else None)
        with mock.patch.object(self.g, "client", fake):
            answer, _ = self.g.ask("hi")
        self.assertEqual(answer, f"answer from {self.g.FALLBACK_MODEL}")
        self.assertEqual(calls, [(self.g.TEXT_MODEL, 60), (self.g.FALLBACK_MODEL, 60)])

    def test_video_timeout_falls_back_with_longer_wait(self):
        from unittest import mock
        timeout = type("APITimeoutError", (Exception,), {})
        calls = []
        fake = self._fake_create(calls, lambda m: timeout("timed out") if m == self.g.TEXT_MODEL else None)
        with mock.patch.object(self.g, "client", fake):
            answer = self.g.watch("https://youtu.be/x", "요약")
        self.assertEqual(answer, f"answer from {self.g.FALLBACK_MODEL}")
        self.assertEqual([m for m, _ in calls], [self.g.TEXT_MODEL, self.g.FALLBACK_MODEL])
        self.assertTrue(all(t == self.g.VIDEO_WAIT_S > 60 for _, t in calls))

    def test_quota_error_does_not_fall_back(self):  # 429 · 400 은 다른 모델로 가도 안 풀린다 — 그대로 보여 준다
        from unittest import mock
        quota = type("RateLimitError", (Exception,), {"status_code": 429})
        calls = []
        with mock.patch.object(self.g, "client", self._fake_create(calls, lambda m: quota("limit: 0"))):
            with self.assertRaises(quota):
                self.g.ask("hi")
        self.assertEqual(len(calls), 1)

    def test_client_turns_off_silent_retries(self):  # 429를 몇 분씩 재시도하며 멈춘 것처럼 보이던 문제
        os.environ["GEMINI_API_KEY"] = "test-not-a-key"
        self.g.client.cache_clear()
        try:
            self.assertIsNone(self.g.client().interactions.sdk_configuration.retry_config)
        finally:
            self.g.client.cache_clear()
            os.environ.pop("GEMINI_API_KEY")

    def test_missing_key_stops_with_hint(self):
        os.environ.pop("GEMINI_API_KEY", None)
        (self.tmp / "cfg" / "gemini.env").write_text("GEMINI_API_KEY=\n", encoding="utf-8")
        with self.assertRaises(SystemExit) as cm:
            self.g.client()
        self.assertIn("gemini.env", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
