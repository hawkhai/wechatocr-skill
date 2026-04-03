#!/usr/bin/env python3
"""OCR images via the local WechatOCR HTTP service (http://127.0.0.1:8811)."""

import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.request

SERVICE_URL = "http://127.0.0.1:8811/Infai/Echo"
SUPPORTED_EXT = {".jpg", ".jpeg", ".png", ".bmp"}
MODEL_NAME = "wechatocr_1-7079.infz"
SERVER_EXE = "infserv64.exe"

SKILL_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# Server and model discovery
# ---------------------------------------------------------------------------

def find_model() -> str:
    """Locate wechatocr_1-7079.infz; checks WECHATOCR_DIR env var then skill directory."""
    for base in filter(None, [os.environ.get("WECHATOCR_DIR"), str(SKILL_DIR)]):
        candidate = os.path.join(base, "wechatocr", "serv", MODEL_NAME)
        if os.path.exists(candidate):
            return os.path.abspath(candidate)
    return ""


def find_server_exe() -> str:
    """Locate infserv64.exe; checks WECHATOCR_DIR env var then skill directory."""
    for base in filter(None, [os.environ.get("WECHATOCR_DIR"), str(SKILL_DIR)]):
        candidate = os.path.join(base, "wechatocr", "serv", "runtime", SERVER_EXE)
        if os.path.exists(candidate):
            return os.path.abspath(candidate)
    return ""


# ---------------------------------------------------------------------------
# Service management
# ---------------------------------------------------------------------------

def is_service_running() -> bool:
    try:
        payload = json.dumps({"message": "{}", "name": "ping"}).encode("utf-8")
        req = urllib.request.Request(SERVICE_URL, data=payload)
        with urllib.request.urlopen(req, timeout=2):
            return True
    except Exception:
        return False


def start_server() -> bool:
    """Start infserv64.exe if not already running. Returns True when service is available."""
    if is_service_running():
        return True
    exe = find_server_exe()
    if not exe:
        return False
    print(f"[INFO] Starting WechatOCR server: {exe}")
    subprocess.Popen(
        [exe],
        cwd=os.path.dirname(exe),
        creationflags=getattr(subprocess, "DETACHED_PROCESS", 0),
    )
    for _ in range(10):
        time.sleep(1)
        if is_service_running():
            print("[INFO] Server ready.")
            return True
    print("[WARN] Server did not respond within 10 s.", file=sys.stderr)
    return False


# ---------------------------------------------------------------------------
# OCR helpers
# ---------------------------------------------------------------------------

def ocr_image(image_path: str, force: bool = False) -> str:
    image_path = os.path.abspath(image_path)
    base, ext = os.path.splitext(image_path)
    if ext.lower() not in SUPPORTED_EXT:
        return ""

    json_path = base + "_wechatocr.json"
    if not force and os.path.exists(json_path):
        print(f"[SKIP] {os.path.basename(image_path)}")
        return json_path

    message = {"imgfile": image_path}
    model = find_model()
    if model:
        message["wechatocrfile"] = model

    try:
        payload = json.dumps({"message": json.dumps(message), "name": "wechatocr"}).encode("utf-8")
        req = urllib.request.Request(SERVICE_URL, data=payload)
        with urllib.request.urlopen(req) as resp:
            fdata = json.loads(resp.read().decode("utf-8"))
        result = json.dumps(json.loads(fdata["message"]), ensure_ascii=False, indent=2)
    except Exception as exc:
        print(f"[ERROR] {os.path.basename(image_path)}: {exc}", file=sys.stderr)
        return ""

    with open(json_path, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"[OK]   {os.path.basename(image_path)} -> {os.path.basename(json_path)}")
    return json_path


def ocr_dir(directory: str, force: bool = False) -> None:
    for entry in sorted(os.scandir(directory), key=lambda e: e.name):
        if entry.is_file():
            ocr_image(entry.path, force=force)
        elif entry.is_dir():
            ocr_dir(entry.path, force=force)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = sys.argv[1:]
    force = "--force" in args or "-f" in args
    paths = [p for p in args if not p.startswith("-")]

    if not paths:
        print("Usage: wechatocr-skill.py [--force] <image_or_dir> ...")
        sys.exit(1)

    if not start_server():
        print("[WARN] WechatOCR service may not be running; OCR calls may fail.", file=sys.stderr)

    for path in paths:
        if os.path.isdir(path):
            print(f"Directory: {path}")
            ocr_dir(path, force=force)
        elif os.path.isfile(path):
            ocr_image(path, force=force)
        else:
            print(f"Not found: {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
