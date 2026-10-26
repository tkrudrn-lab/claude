"""텔레그램 알림 — 모든 잡의 마지막 단계. 실패해도 로그 줄은 남는다.

    python notify.py --job <잡> "<한 줄>" [--file 첨부]
    python notify.py --setup          # 봇에 메시지 보낸 뒤 chat_id 찾기
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


def send(text: str, file: "Path | str | None" = None, job: str = "manual") -> bool:
    log_line(job, text.splitlines()[0] if text else "")
    try:
        tg = load_env("telegram")
        token, chat_id = tg["TELEGRAM_BOT_TOKEN"], tg["TELEGRAM_CHAT_ID"]
    except (FileNotFoundError, KeyError) as e:
        print(f"notify: 설정 없음 — {e}", file=sys.stderr)
        return False

    path = Path(file) if file else None
    if path and path.stat().st_size > MAX_FILE_BYTES:
        text, path = f"{text}\n파일: {path}", None

    if path is None:
        method, field = "sendMessage", None
        data = urllib.parse.urlencode({"chat_id": chat_id, "text": text[:MAX_TEXT]}).encode()
        ctype = "application/x-www-form-urlencoded"
    else:
        ext = path.suffix.lower()
        if ext in PHOTO_EXT and path.stat().st_size <= MAX_PHOTO_BYTES:
            method, field = "sendPhoto", "photo"
        elif ext in VIDEO_EXT:
            method, field = "sendVideo", "video"
        else:
            method, field = "sendDocument", "document"
        data, ctype = _multipart({"chat_id": chat_id, "caption": text[:MAX_CAPTION]}, field, path)

    try:
        res = _call(token, method, data, ctype)
    except urllib.error.URLError as e:  # HTTPError 포함
        print(f"notify: {method} 실패 — {e}", file=sys.stderr)
        return False
    if not res.get("ok"):
        print(f"notify: {method} 실패 — {res.get('description')}", file=sys.stderr)
        return False
    return True


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
    sys.exit(main(sys.argv[1:]))
