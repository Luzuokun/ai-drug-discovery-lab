#!/usr/bin/env python3
"""Markdown → YouTube text-pack CLI (V1).

Examples:
  python scripts/youtube/publish.py 02
  python scripts/youtube/publish.py docs/molecular-generation/reinvent4/02-priors-in-practice.md
  python scripts/youtube/publish.py 02 --dry-run
  python scripts/youtube/publish.py 02 --from-json path/to/pack.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Allow `python scripts/youtube/publish.py` without installing a package.
_SCRIPT_DIR = Path(__file__).resolve().parent
_ROOT = _SCRIPT_DIR.parents[1]
if str(_SCRIPT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR.parent))

from youtube.openai_client import generate_pack_json, render_user_prompt, load_prompt
from youtube.parse_chapter import parse_chapter, resolve_chapter_path
from youtube.writer import write_pack

DEFAULT_SITE = "https://luzuokun.github.io/ai-drug-discovery-lab"
DEFAULT_REPO = "https://github.com/Luzuokun/ai-drug-discovery-lab"
MIN_WORDS_FULL = 200


def _load_dotenv() -> None:
    env_path = _ROOT / ".env"
    if not env_path.is_file():
        return
    try:
        from dotenv import load_dotenv
    except ImportError:
        # Minimal fallback
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip("\"'"))
        return
    load_dotenv(env_path)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Generate a YouTube text pack from a MkDocs chapter."
    )
    p.add_argument(
        "chapter",
        help="Chapter path, slug, or number (e.g. 02, 02-priors-in-practice, path.md)",
    )
    p.add_argument(
        "--model",
        default=os.environ.get("YOUTUBE_OPENAI_MODEL", "gpt-4o"),
        help="OpenAI model (default: gpt-4o or YOUTUBE_OPENAI_MODEL)",
    )
    p.add_argument(
        "--site-base-url",
        default=os.environ.get("YOUTUBE_SITE_BASE_URL", DEFAULT_SITE),
    )
    p.add_argument(
        "--github-repo-url",
        default=os.environ.get("YOUTUBE_GITHUB_REPO_URL", DEFAULT_REPO),
    )
    p.add_argument(
        "--playlist-url",
        default=os.environ.get("YOUTUBE_PLAYLIST_URL", "TODO_PLAYLIST_URL"),
    )
    p.add_argument(
        "--allow-outline",
        action="store_true",
        help="Allow Coming Soon / outline chapters (uses enrichment context).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print prompts / brief only; do not call the API or write packs.",
    )
    p.add_argument(
        "--from-json",
        type=Path,
        help="Skip OpenAI; write pack files from an existing pack.json",
    )
    p.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Override output directory (default: youtube/packs/<slug>/)",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    _load_dotenv()
    args = build_parser().parse_args(argv)

    path = resolve_chapter_path(args.chapter)
    brief = parse_chapter(path)
    brief_dict = brief.to_dict()

    rel_github = str(path.relative_to(_ROOT)).replace("\\", "/")
    print(f"Chapter: {brief.title}")
    print(f"  path: {brief.path}")
    print(f"  slug: {brief.slug}")
    print(f"  words: {brief.word_count}")
    print(f"  outline: {brief.is_outline}")

    if brief.is_outline and not args.allow_outline and not args.from_json:
        print(
            "\nERROR: Chapter looks like Coming Soon / outline-only.\n"
            "Full Available chapters produce better videos.\n"
            "Re-run with --allow-outline to generate from acceptance criteria + enrichment.\n",
            file=sys.stderr,
        )
        return 2

    if (
        not brief.is_outline
        and brief.word_count < MIN_WORDS_FULL
        and not args.allow_outline
        and not args.from_json
    ):
        print(
            f"\nERROR: Chapter is very short ({brief.word_count} words). "
            "Use --allow-outline if intentional.\n",
            file=sys.stderr,
        )
        return 2

    if args.dry_run:
        user = render_user_prompt(
            brief_dict,
            site_base_url=args.site_base_url,
            github_repo_url=args.github_repo_url,
            github_chapter_path=rel_github,
            playlist_placeholder=args.playlist_url,
        )
        print("\n===== SYSTEM =====\n")
        print(load_prompt("system.txt"))
        print("\n===== USER (truncated to 4000 chars) =====\n")
        print(user[:4000])
        if len(user) > 4000:
            print(f"\n…[{len(user) - 4000} more chars]")
        print("\nDry-run complete (no API call, no files written).")
        return 0

    if args.from_json:
        data = json.loads(args.from_json.read_text(encoding="utf-8"))
        generator = "from-json"
        model = data.get("_model") or args.model
    else:
        data = generate_pack_json(
            brief_dict,
            model=args.model,
            site_base_url=args.site_base_url,
            github_repo_url=args.github_repo_url,
            github_chapter_path=rel_github,
            playlist_placeholder=args.playlist_url,
        )
        generator = "openai"
        model = args.model

    dest = write_pack(
        data,
        brief=brief_dict,
        model=model,
        generator=generator,
        site_base_url=args.site_base_url,
        github_repo_url=args.github_repo_url,
        out_dir=args.out_dir,
    )
    print(f"\nWrote pack → {dest}")
    print(f"Review: {dest / 'REVIEW.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
