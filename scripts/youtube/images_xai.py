#!/usr/bin/env python3
"""Generate AI stills for a YouTube pack via xAI Grok Imagine.

Reads XAI_API_KEY from env or repo-root .env.
Reads prompts from youtube/packs/<slug>/assets/ai/prompts.json.

Docs: https://docs.x.ai/developers/model-capabilities/images/generation

Examples:
  python scripts/youtube/images_xai.py 03 --dry-run
  python scripts/youtube/images_xai.py 03
  python scripts/youtube/images_xai.py 03 --force
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_ROOT = _SCRIPT_DIR.parents[1]
PACKS_DIR = _ROOT / "youtube" / "packs"

DEFAULT_MODEL = "grok-imagine-image-quality"
API_URL = "https://api.x.ai/v1/images/generations"


def _load_dotenv() -> None:
    env_path = _ROOT / ".env"
    if not env_path.is_file():
        return
    try:
        from dotenv import load_dotenv
    except ImportError:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip("\"'"))
        return
    load_dotenv(env_path)


def _resolve_pack(chapter: str) -> Path:
    for child in sorted(PACKS_DIR.iterdir()) if PACKS_DIR.is_dir() else []:
        if not child.is_dir():
            continue
        if child.name == chapter or child.name.startswith(f"{chapter}-") or (
            chapter.isdigit() and child.name.startswith(chapter.zfill(2))
        ):
            return child
    raise FileNotFoundError(f"No pack for chapter '{chapter}' under {PACKS_DIR}")


def _generate_one(api_key: str, model: str, prompt: str, out_path: Path) -> None:
    body = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "n": 1,
            "aspect_ratio": "16:9",
            "response_format": "b64_json",
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {detail[:800]}") from e

    items = data.get("data") or []
    if not items:
        raise RuntimeError(f"Empty image response: {data!r}")
    item = items[0]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if item.get("b64_json"):
        out_path.write_bytes(base64.b64decode(item["b64_json"]))
    elif item.get("url"):
        with urllib.request.urlopen(item["url"], timeout=120) as img_resp:
            out_path.write_bytes(img_resp.read())
    else:
        raise RuntimeError(f"No b64_json/url in item: {item!r}")


def main(argv: list[str] | None = None) -> int:
    _load_dotenv()
    p = argparse.ArgumentParser(description="xAI image generation for a YouTube pack.")
    p.add_argument("chapter", help="Pack slug or number (e.g. 03)")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true", help="Overwrite existing PNGs")
    p.add_argument(
        "--model",
        default=os.environ.get("XAI_IMAGE_MODEL", DEFAULT_MODEL),
        help=f"Image model (default: {DEFAULT_MODEL})",
    )
    args = p.parse_args(argv)

    pack = _resolve_pack(args.chapter)
    prompts_path = pack / "assets" / "ai" / "prompts.json"
    if not prompts_path.is_file():
        print(f"ERROR: missing {prompts_path}", file=sys.stderr)
        return 2

    cfg = json.loads(prompts_path.read_text(encoding="utf-8"))
    images = cfg.get("images") or []
    model = args.model or DEFAULT_MODEL
    out_dir = pack / "assets" / "ai"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Pack: {pack}")
    print(f"Model: {model}")
    print(f"Images: {len(images)}")

    if args.dry_run:
        for item in images:
            print(f"  would write {out_dir / item['filename']}: {item['prompt'][:80]}…")
        return 0

    api_key = os.environ.get("XAI_API_KEY", "").strip()
    if not api_key:
        print("ERROR: XAI_API_KEY not set. Put it in repo-root .env.\n", file=sys.stderr)
        return 2

    failed = 0
    for item in images:
        dest = out_dir / item["filename"]
        print(f"  Generating {item['id']} → {dest.name}")
        if dest.is_file() and not args.force:
            print(f"    skip (exists; use --force)")
            continue
        try:
            _generate_one(api_key, model, item["prompt"], dest)
            print(f"    OK ({dest.stat().st_size} bytes)")
        except Exception as exc:  # noqa: BLE001
            print(f"    FAILED: {exc}", file=sys.stderr)
            failed += 1

    if failed:
        print(f"Done with {failed} failure(s).", file=sys.stderr)
        return 1
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
