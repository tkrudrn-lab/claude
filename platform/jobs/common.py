"""hermes 공용 — 설정 읽기와 실행 로그 한 줄.

설정은 저장소 밖 ~/.config/hermes/<name>.env (HERMES_CONFIG_DIR 로 덮어쓸 수 있음).
로그는 HERMES_LOGS/<job>.log 에 실행당 1줄.
"""
import os
from datetime import datetime
from pathlib import Path


def config_dir() -> Path:
    override = os.environ.get("HERMES_CONFIG_DIR")
    return Path(override) if override else Path.home() / ".config" / "hermes"


def load_env(name: str) -> dict[str, str]:
    path = config_dir() / f"{name}.env"
    if not path.is_file():
        raise FileNotFoundError(f"{path} 없음 — platform/jobs/{name}.env.example 을 복사해서 채워라")
    env: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = os.path.expanduser(value.strip())
    return env


def log_line(job: str, msg: str) -> Path:
    try:
        logs = load_env("paths").get("HERMES_LOGS")
    except FileNotFoundError:
        logs = None
    log_dir = Path(logs) if logs else Path.home() / "hermes-logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / f"{job}.log"
    with path.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M} | {msg}\n")
    return path
