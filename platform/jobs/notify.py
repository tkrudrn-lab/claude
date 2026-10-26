"""텔레그램 알림 — 모든 잡의 마지막 단계. 실패해도 로그 줄은 남고, 어떤 예외도 밖으로 나가지 않는다.

    python notify.py --job <잡> "<한 줄>" [--file 첨부]
    python notify.py --setup          # 봇에 메시지 보낸 뒤 chat_id 찾기

첨부가 없거나·크거나·텔레그램이 거절하면 텍스트 + 경로로라도 보낸다 (하트비트 우선).
"""
import json
import mimetypes
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

from common import load_env, log_line

MAX_FILE_BYTES = 50 * 1024**2
MAX_PHOTO_BYTES = 10 * 1024**2
MAX_CAPTION = 1024
MAX_TEXT = 4096
PHOTO_EXT = {".jpg", ".jpeg", ".png"}
VIDEO_EXT = {".mp4", ".mov"}

urlopen = urllib.request.urlopen  # 테스트가 바꿔 끼운다


def _multipart(fields: dict[str, str], file_field: str, path: Path) -> tuple[bytes, str]:
    boundary = uuid.uuid4().hex
    ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    parts = []
    for k, v in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    parts.append(
        f'--{boundary}\r\nContent-Disposition: form-data; name="{file_field}"; filename="{path.name}"\r\n'
        f"Content-Type: {ctype}\r\n\r\n".encode() + path.read_bytes() + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def _call(token: str, method: str, data: bytes, content_type: str) -> dict:
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/{method}", data=data,
                                 headers={"Content-Type": content_type})
    with urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def _ok(token: str, method: str, data: bytes, content_type: str) -> bool:
    try:
        res = _call(token, method, data, content_type)
    except OSError as e:  # URLError·HTTPError·TimeoutError·ConnectionResetError 전부
        print(f"notify: {method} 실패 — {e}", file=sys.stderr)
        return False
    if not res.get("ok"):
        print(f"notify: {method} 실패 — {res.get('description')}", file=sys.stderr)
        return False
    return True


def _text_with_path(text: str, path: Path) -> str:
    tail = f"\n파일: {path}"
    return text[:MAX_TEXT - len(tail)] + tail


def _send(text: str, file: "Path | str | None") -> bool:
    tg = load_env("telegram")
    token, chat_id = tg["TELEGRAM_BOT_TOKEN"], tg["TELEGRAM_CHAT_ID"]
    path = Path(file) if file else None
    if path is not None:
        if path.is_file() and path.stat().st_size <= MAX_FILE_BYTES:
            ext = path.suffix.lower()
            if ext in PHOTO_EXT and path.stat().st_size <= MAX_PHOTO_BYTES:
                method, field = "sendPhoto", "photo"
            elif ext in VIDEO_EXT:
                method, field = "sendVideo", "video"
            else:
                method, field = "sendDocument", "document"
            data, ctype = _multipart({"chat_id": chat_id, "caption": text[:MAX_CAPTION]}, field, path)
            if _ok(token, method, data, ctype):
                return True
        text = _text_with_path(text, path)  # 없거나·크거나·거절 → 텍스트라도 간다
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text[:MAX_TEXT]}).encode()
    return _ok(token, "sendMessage", data, "application/x-www-form-urlencoded")


def send(text: str, file: "Path | str | None" = None, job: str = "manual") -> bool:
    try:
        log_line(job, text.splitlines()[0] if text else "")
    except Exception as e:
        print(f"notify: 로그 실패 — {e}", file=sys.stderr)
    try:
        return _send(text, file)
    except Exception as e:  # 설정 없음·인코딩·그 외 무엇이든 — 호출자를 죽이지 않는다
        print(f"notify: 실패 — {e!r}", file=sys.stderr)
        return False


def setup() -> int:
    try:
        token = load_env("telegram")["TELEGRAM_BOT_TOKEN"]
    except (FileNotFoundError, KeyError) as e:
        print(e, file=sys.stderr)
        return 1
    if not token:
        print("TELEGRAM_BOT_TOKEN 이 비어 있다 — @BotFather 토큰을 telegram.env 에 넣고 다시", file=sys.stderr)
        return 1
    res = _call(token, "getUpdates", b"", "application/x-www-form-urlencoded")
    msgs = [u["message"] for u in res.get("result", []) if "message" in u]
    if not msgs:
        print("봇에 먼저 아무 메시지나 보내고 다시 실행", file=sys.stderr)
        return 1
    print(msgs[-1]["chat"]["id"])
    return 0


def main(argv: list[str]) -> int:
    if argv == ["--setup"]:
        return setup()
    job, file, rest = "manual", None, []
    it = iter(argv)
    for a in it:
        if a == "--job":
            job = next(it, job)
        elif a == "--file":
            file = next(it, None)
        else:
            rest.append(a)
    if not rest:
        print(__doc__, file=sys.stderr)
        return 1
    return 0 if send(" ".join(rest), file=file, job=job) else 1


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):  # 윈도우 파이프는 cp949 — '−'·'—' 에서 죽지 않게
        s.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
