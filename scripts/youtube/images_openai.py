#!/usr/bin/env python3
"""Generate AI stills for a YouTube pack via OpenAI Images API.

Reads OPENAI_API_KEY from env or repo-root .env.
Reads prompts from youtube/packs/<slug>/assets/ai/prompts.json.

Examples:
  python scripts/youtube/images_openai.py 03 --dry-run
  python scripts/youtube/images_openai.py 03
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_ROOT = _SCRIPT_DIR.parents[1]
PACKS_DIR = _ROOT / "youtube" / "packs"


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


def _generate_one(client, *, model: str, prompt: str, size: str, out: Path) -> None:
    # Prefer Responses-style images API; fall back across model/size combos.
    errors: list[str] = []
    size_fallbacks = [size, "1024x1024", "1024x1536", "1536x1024"]
    # dedupe preserving order
    seen: set[str] = set()
    sizes = [s for s in size_fallbacks if not (s in seen or seen.add(s))]

    for sz in sizes:
        try:
            result = client.images.generate(
                model=model,
                prompt=prompt,
                size=sz,
            )
            data = result.data[0]
            b64 = getattr(data, "b64_json", None)
            if b64:
                out.write_bytes(base64.b64decode(b64))
                return
            url = getattr(data, "url", None)
            if url:
                import urllib.request

                with urllib.request.urlopen(url) as resp:  # noqa: S310
                    out.write_bytes(resp.read())
                return
            errors.append(f"{model}/{sz}: empty response")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{model}/{sz}: {exc}")
    raise RuntimeError("Image generation failed:\n- " + "\n- ".join(errors))


def main(argv: list[str] | None = None) -> int:
    _load_dotenv()
    p = argparse.ArgumentParser(description="OpenAI image generation for a YouTube pack.")
    p.add_argument("chapter", help="Pack slug or number (e.g. 03)")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument(
        "--model",
        default=os.environ.get("YOUTUBE_OPENAI_IMAGE_MODEL", "gpt-image-1"),
        help="Preferred image model (falls back to dall-e-3)",
    )
    args = p.parse_args(argv)

    pack = _resolve_pack(args.chapter)
    prompts_path = pack / "assets" / "ai" / "prompts.json"
    if not prompts_path.is_file():
        print(f"ERROR: missing {prompts_path}", file=sys.stderr)
        return 2

    cfg = json.loads(prompts_path.read_text(encoding="utf-8"))
    images = cfg.get("images") or []
    size = cfg.get("size") or "1024x1024"
    models = cfg.get("model_preference") or [args.model, "dall-e-3"]
    if args.model not in models:
        models = [args.model, *models]

    out_dir = pack / "assets" / "ai"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Pack: {pack}")
    print(f"Images: {len(images)}  preferred models: {models}")

    if args.dry_run:
        for item in images:
            print(f"  would write {out_dir / item['filename']}: {item['prompt'][:80]}…")
        return 0

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        print(
            "ERROR: OPENAI_API_KEY not set. Put it in repo-root .env.\n",
            file=sys.stderr,
        )
        return 2

    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    for item in images:
        dest = out_dir / item["filename"]
        print(f"  Generating {item['id']} → {dest.name}")
        last_err: Exception | None = None
        for model in models:
            try:
                _generate_one(
                    client,
                    model=model,
                    prompt=item["prompt"],
                    size=size if model != "dall-e-3" else "1792x1024",
                    out=dest,
                )
                print(f"    OK via {model} ({dest.stat().st_size} bytes)")
                last_err = None
                break
            except Exception as exc:  # noqa: BLE001
                last_err = exc
                print(f"    fail {model}: {exc}")
        if last_err is not None and not dest.is_file():
            print(f"ERROR: could not generate {item['id']}: {last_err}", file=sys.stderr)
            return 1

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
