"""미디어 카탈로그 — 폴더마다 _catalog.csv 하나. 새 파일만 추가, 사라진 파일 행은 삭제, note 는 보존.

    python catalog.py [폴더 ...] [--notify]     # 폴더 없으면 paths.env 의 HERMES_CATALOG_DIRS

폴더에 .nocatalog 파일을 두면 그 폴더(하위 포함)는 건너뛴다. 원본은 읽기만 한다.
"""
import csv
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from common import load_env

CATALOG_NAME = "_catalog.csv"
COLUMNS = ["rel_path", "taken", "duration_s", "width", "height", "size_mb", "note"]
MEDIA_EXT = {".jpg", ".jpeg", ".png", ".gif", ".mov", ".mp4", ".m4v", ".avi", ".mkv", ".webm"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif"}
SKIP_DIRS = {"$RECYCLE.BIN", "System Volume Information", "PremiereCache", "_esrgan_work", "_mosaic", "node_modules"}
SKIP_MARKER = ".nocatalog"
TS = "%Y-%m-%d %H:%M:%S"


def scan(folder: Path) -> list[Path]:
    found = []
    for dirpath, dirnames, filenames in os.walk(folder):
        if SKIP_MARKER in filenames:
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for name in filenames:
            if name != CATALOG_NAME and Path(name).suffix.lower() in MEDIA_EXT:
                found.append(Path(dirpath) / name)
    return found


def _probe_image(path: Path, out: dict) -> None:
    from PIL import Image
    with Image.open(path) as im:
        out["width"], out["height"] = str(im.size[0]), str(im.size[1])
        dt = im.getexif().get_ifd(0x8769).get(0x9003)
    if dt:
        d, t = str(dt).split(" ", 1)
        out["taken"] = f"{d.replace(':', '-')} {t}"


def _probe_video(path: Path, out: dict) -> None:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return
    res = subprocess.run(
        [ffprobe, "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height:stream_side_data=rotation:format=duration:format_tags=creation_time",
         "-of", "json", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    info = json.loads(res.stdout or "{}")
    stream = (info.get("streams") or [{}])[0]
    w, h = stream.get("width"), stream.get("height")
    # ponytail: 회전은 side_data rotation 만 본다, 안 잡히는 파일은 가로세로 그대로
    rot = next((sd.get("rotation") for sd in stream.get("side_data_list", []) if "rotation" in sd), 0)
    if w and h:
        if abs(int(float(rot or 0))) == 90:
            w, h = h, w
        out["width"], out["height"] = str(w), str(h)
    fmt = info.get("format", {})
    if fmt.get("duration"):
        out["duration_s"] = f"{float(fmt['duration']):.1f}"
    ct = fmt.get("tags", {}).get("creation_time")
    if ct:
        out["taken"] = ct.replace("T", " ")[:19]


def probe(path: Path) -> dict[str, str]:
    out = {"taken": "", "duration_s": "", "width": "", "height": "", "size_mb": ""}
    try:
        st = path.stat()
        out["size_mb"] = f"{st.st_size / 1024**2:.1f}"
        mtime = datetime.fromtimestamp(st.st_mtime).strftime(TS)
    except OSError:
        return out
    try:
        if path.suffix.lower() in IMAGE_EXT:
            _probe_image(path, out)
        else:
            _probe_video(path, out)
    except Exception:  # 깨진 파일 하나가 스캔 전체를 죽이면 안 된다
        pass
    out["taken"] = out["taken"] or mtime
    return out


def update_catalog(folder: Path) -> tuple[int, int]:
    folder = Path(folder)
    if not folder.is_dir():
        raise FileNotFoundError(folder)
    csv_path = folder / CATALOG_NAME
    rows: dict[str, dict] = {}
    if csv_path.is_file():
        with csv_path.open(encoding="utf-8-sig", newline="") as f:
            rows = {r["rel_path"]: r for r in csv.DictReader(f)}
    present = {p.relative_to(folder).as_posix(): p for p in scan(folder)}
    removed = [k for k in rows if k not in present]
    for k in removed:
        del rows[k]
    added = [k for k in present if k not in rows]
    for k in added:
        rows[k] = {"rel_path": k, **probe(present[k]), "note": ""}
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        for k in sorted(rows):
            w.writerow({c: rows[k].get(c, "") for c in COLUMNS})
    return len(added), len(removed)


def main(argv: list[str]) -> int:
    do_notify = "--notify" in argv
    folders = [Path(a) for a in argv if a != "--notify"]
    if not folders:
        folders = [Path(p) for p in load_env("paths").get("HERMES_CATALOG_DIRS", "").split(";") if p]
    lines, processed = [], 0
    for folder in folders:
        if not folder.is_dir():
            lines.append(f"{folder.name} 없음")
        else:
            added, removed = update_catalog(folder)
            with (folder / CATALOG_NAME).open(encoding="utf-8-sig", newline="") as f:
                total = sum(1 for _ in f) - 1
            lines.append(f"{folder.name} +{added} −{removed} ({total})")
            processed += 1
        print(lines[-1])
    if do_notify:
        import notify
        notify.send("카탈로그 · " + " · ".join(lines), job="catalog")
    return 0 if processed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
