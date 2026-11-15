"""Gemini 도우미 — Claude가 못 하는 것을 Gemini로: 그림(Nano Banana) · 영상 보기 · 음성 · 검색 근거 · URL 읽기.

키: ~/.config/hermes/gemini.env 의 GEMINI_API_KEY (저장소 밖 — OneDrive로 안 올라감). 환경변수가 있으면 먼저 쓴다.
API: google-genai 2.25+ Interactions API (client.interactions.create) — 2026-11 공식 문서(aistudio.google.com/docs) 기준.
모델 이름은 몇 달마다 바뀐다 → `python gemini.py models` 로 확인하고 아래 상수를 고친다.

  python gemini.py models
  python gemini.py text "질문" [--search] [--urls] [--file 그림.png]
  python gemini.py video <유튜브 링크|파일.mp4> "질문" [--start 2:00 --end 4:30] [--out breakdown.md]
  python gemini.py image <출력.png> --prompt "..." [--prompt "..."] [--ref style/a.png] [--aspect 9:16] [--size 2K]
  python gemini.py tts <출력.wav> "읽을 글" [--voice Kore] [--style "confident, upbeat"]
  python gemini.py podcast <대본.txt> <출력.wav> --voice Alex=Puck --voice Sam=Kore
"""
import argparse
import base64
import functools
import mimetypes
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from common import load_env

TEXT_MODEL = "gemini-4-hydrogen"  # 빠른 일상 모델(문서 예시 기본). 안정판이 필요하면 gemini-3.8-flash
IMAGE_MODEL = "gemini-nano-banana-2.1"  # 안정판 gemini-3.1-flash-image · 고품질 gemini-3-pro-image
TTS_MODEL = "gemini-3.8-flash-tts"  # 싼 판 gemini-3.8-flash-lite-tts


@functools.cache  # 한 개를 계속 붙잡아 둔다 — 임시 Client는 지워지는 순간 연결을 닫아 요청이 실패한다
def client():
    from google import genai  # 늦은 import — 테스트는 SDK·키 없이 돈다

    key = os.environ.get("GEMINI_API_KEY") or load_env("gemini").get("GEMINI_API_KEY", "")
    if not key:
        raise SystemExit("GEMINI_API_KEY 비어 있음 — ~/.config/hermes/gemini.env 에 넣어라 (aistudio.google.com/apikey)")
    c = genai.Client(api_key=key, http_options={"api_version": "v1beta"})
    # SDK는 429를 몇 분씩 조용히 재시도한다 — 무료 키 그림처럼 "하루 0회"면 기다려도 소용없으니 바로 실패시켜 이유를 보여 준다
    if hasattr(c.interactions, "sdk_configuration"):
        c.interactions.sdk_configuration.retry_config = None
    return c


def secs(t: str) -> int:
    """'150' · '2:30' · '1:02:30' → 초."""
    n = 0
    for part in t.split(":"):
        n = n * 60 + int(part)
    return n


def media_block(path: str) -> dict:
    """로컬 그림·소리 파일 → 입력 블록(base64 인라인). 영상은 video_block 으로."""
    p = Path(path)
    mime = mimetypes.guess_type(p.name)[0] or ""
    kind = mime.split("/")[0]
    if kind not in ("image", "audio"):
        raise ValueError(f"그림·소리 파일만 된다: {p.name} ({mime or '모르는 형식'})")
    return {"type": kind, "data": base64.b64encode(p.read_bytes()).decode(), "mime_type": mime}


def sources(interaction) -> list[str]:
    """검색·URL 근거 링크 — 중복 없이, 나온 순서대로."""
    seen: dict[str, str] = {}
    for step in interaction.steps or []:
        if getattr(step, "type", None) != "model_output":
            continue
        for block in step.content or []:
            for ann in getattr(block, "annotations", None) or []:
                if getattr(ann, "type", None) == "url_citation":
                    seen.setdefault(ann.url, ann.title or ann.url)
    return [f"{title} — {url}" for url, title in seen.items()]


def ask(prompt: str, files=(), search=False, urls=False, model=TEXT_MODEL) -> tuple[str, list[str]]:
    tools = [{"type": "google_search"}] * search + [{"type": "url_context"}] * urls
    blocks = [{"type": "text", "text": prompt}, *map(media_block, files)]
    it = client().interactions.create(model=model, input=blocks, **({"tools": tools} if tools else {}))
    return it.output_text, sources(it)


def video_block(src: str, start=None, end=None, c=None) -> dict:
    if src.startswith(("http://", "https://")):
        block = {"type": "video", "uri": src}  # 공개 영상만. 비공개는 받아서 파일로
    else:
        mime = mimetypes.guess_type(src)[0] or "video/mp4"
        with open(src, "rb") as fh:  # 경로로 주면 SDK가 파일 이름을 HTTP 헤더에 넣어 한글 이름에서 깨진다
            f = c.files.upload(file=fh, config={"mime_type": mime})
        while not f.state or f.state.name != "ACTIVE":
            if f.state and f.state.name == "FAILED":
                raise RuntimeError(f"영상 처리 실패: {src}")
            time.sleep(5)
            f = c.files.get(name=f.name)
        block = {"type": "video", "uri": f.uri, "mime_type": f.mime_type}
    clip = {k: f"{v}s" for k, v in (("start_offset", start), ("end_offset", end)) if v is not None}
    if clip:
        block["processing"] = {"type": "static", **clip}
    return block


def watch(src: str, prompt: str, start=None, end=None, model=TEXT_MODEL) -> str:
    c = client()
    blocks = [video_block(src, start, end, c), {"type": "text", "text": prompt}]
    return c.interactions.create(model=model, input=blocks).output_text


def image(prompt: str, out, refs=(), aspect=None, size=None, model=IMAGE_MODEL) -> Path:
    """만들기 · 고치기 겸용 — refs 에 원본 사진이나 스타일 그림(최대 14장). size 는 1K/2K/4K(대문자 K)."""
    out = Path(out).with_suffix(".jpg")  # API가 image/jpeg만 받는다(png 요청은 400, 2026-11-15 확인)
    fmt = {"type": "image", "mime_type": "image/jpeg"}
    fmt |= {k: v for k, v in (("aspect_ratio", aspect), ("image_size", size)) if v}
    blocks = [{"type": "text", "text": prompt}, *map(media_block, refs)]
    it = client().interactions.create(model=model, input=blocks, response_format=fmt)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(base64.b64decode(it.output_image.data))
    return out


def images(prompts: list[str], out, **kw) -> list[Path]:
    """프롬프트 여러 개를 한꺼번에 → out_1.png, out_2.png …"""
    out = Path(out)
    if len(prompts) == 1:
        return [image(prompts[0], out, **kw)]
    paths = [out.with_name(f"{out.stem}_{i}{out.suffix}") for i in range(1, len(prompts) + 1)]
    with ThreadPoolExecutor(len(prompts)) as ex:
        return list(ex.map(lambda pp: image(pp[0], pp[1], **kw), zip(prompts, paths)))


def speech_block(text: str, speaker=None, style=None) -> dict:
    meta = {k: v for k, v in (("speaker", speaker), ("style", style)) if v}
    block = {"type": "text", "text": text}
    return block | {"annotations": [{"type": "speech_metadata", **meta}]} if meta else block


def _speak(blocks: list[dict], speech_config, out, model: str) -> Path:
    it = client().interactions.create(
        model=model,
        input=[{"type": "user_input", "content": blocks}],
        response_format={"type": "audio"},  # 24kHz 모노 16bit WAV(헤더 포함)
        generation_config={"speech_config": speech_config},
    )
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(base64.b64decode(it.output_audio.data))
    return out


def tts(text: str, out, voice="Kore", style=None, model=TTS_MODEL) -> Path:
    return _speak([speech_block(text, style=style)], [{"voice": voice}], out, model)


def podcast(turns: list[tuple[str, str]], voices: dict[str, str], out, model=TTS_MODEL) -> Path:
    """기본 목소리로는 2명까지 한 파일."""
    blocks = [speech_block(said, speaker=who) for who, said in turns]
    cfg = {"speakers": [{"speaker": s, "voice": v} for s, v in voices.items()]}
    return _speak(blocks, cfg, out, model)


def parse_script(text: str, speakers) -> list[tuple[str, str]]:
    """'이름: 대사' 줄 → [(이름, 대사)]. 이름이 speakers 에 없으면 앞 대사에 이어 붙인다."""
    turns: list[tuple[str, str]] = []
    for line in filter(None, map(str.strip, text.splitlines())):
        who, sep, said = line.partition(":")
        if sep and who.strip() in speakers:
            turns.append((who.strip(), said.strip()))
        elif turns:
            turns[-1] = (turns[-1][0], f"{turns[-1][1]} {line}")
        else:
            raise ValueError(f"첫 줄이 '이름: 대사' 꼴이 아님: {line[:40]}")
    return turns


def models() -> list[str]:
    return sorted(m.name.removeprefix("models/") for m in client().models.list())


def main(argv=None) -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Gemini 도우미 (자세한 사용법은 파일 맨 위)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("models")
    t = sub.add_parser("text")
    t.add_argument("prompt")
    t.add_argument("--file", action="append", default=[])
    t.add_argument("--search", action="store_true", help="구글 검색 근거")
    t.add_argument("--urls", action="store_true", help="프롬프트 안 링크 읽기(최대 20개)")
    v = sub.add_parser("video")
    v.add_argument("src")
    v.add_argument("prompt")
    v.add_argument("--start", type=secs)
    v.add_argument("--end", type=secs)
    v.add_argument("--out")
    i = sub.add_parser("image")
    i.add_argument("out")
    i.add_argument("--prompt", action="append", required=True)
    i.add_argument("--ref", action="append", default=[])
    i.add_argument("--aspect")
    i.add_argument("--size")
    s = sub.add_parser("tts")
    s.add_argument("out")
    s.add_argument("text")
    s.add_argument("--voice", default="Kore")
    s.add_argument("--style")
    p = sub.add_parser("podcast")
    p.add_argument("script")
    p.add_argument("out")
    p.add_argument("--voice", action="append", required=True, help="이름=목소리")
    a = ap.parse_args(argv)

    if a.cmd == "models":
        print("\n".join(models()))
    elif a.cmd == "text":
        answer, links = ask(a.prompt, a.file, a.search, a.urls)
        print(answer + ("\n\n출처:\n" + "\n".join(links) if links else ""))
    elif a.cmd == "video":
        answer = watch(a.src, a.prompt, a.start, a.end)
        if a.out:
            Path(a.out).write_text(answer, encoding="utf-8")
        print(answer)
    elif a.cmd == "image":
        print("\n".join(map(str, images(a.prompt, a.out, refs=a.ref, aspect=a.aspect, size=a.size))))
    elif a.cmd == "tts":
        print(tts(a.text, a.out, a.voice, a.style))
    elif a.cmd == "podcast":
        voices = dict(x.split("=", 1) for x in a.voice)
        print(podcast(parse_script(Path(a.script).read_text(encoding="utf-8"), voices), voices, a.out))


if __name__ == "__main__":
    main()
