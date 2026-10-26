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
    """urlopen 대역. calls 에 (method, body_bytes) 누적."""
    def __init__(self, ok=True, raise_url_error=False):
        self.ok, self.raise_url_error, self.calls = ok, raise_url_error, []

    def __call__(self, req, timeout=None):
        if self.raise_url_error:
            raise urllib.error.URLError("no network")
        self.calls.append((req.full_url.rsplit("/", 1)[1], req.data or b""))
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


if __name__ == "__main__":
    unittest.main()
