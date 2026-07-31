"""OpenAI client for generating a YouTube text pack JSON."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .schema import PACK_JSON_SCHEMA, validate_pack

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


def load_prompt(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


def render_user_prompt(
    brief: dict[str, Any],
    *,
    site_base_url: str,
    github_repo_url: str,
    github_chapter_path: str,
    playlist_placeholder: str = "TODO_PLAYLIST_URL",
) -> str:
    template = load_prompt("user_template.txt")
    return (
        template.replace("{{SITE_BASE_URL}}", site_base_url.rstrip("/"))
        .replace("{{GITHUB_REPO_URL}}", github_repo_url.rstrip("/"))
        .replace("{{GITHUB_CHAPTER_PATH}}", github_chapter_path)
        .replace("{{PLAYLIST_PLACEHOLDER}}", playlist_placeholder)
        .replace(
            "{{CHAPTER_BRIEF_JSON}}",
            json.dumps(brief, ensure_ascii=False, indent=2),
        )
    )


def generate_pack_json(
    brief: dict[str, Any],
    *,
    model: str,
    site_base_url: str,
    github_repo_url: str,
    github_chapter_path: str,
    playlist_placeholder: str = "TODO_PLAYLIST_URL",
    api_key: str | None = None,
) -> dict[str, Any]:
    try:
        from openai import OpenAI
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "Missing dependency 'openai'. Install with:\n"
            "  pip install -r requirements-youtube.txt"
        ) from exc

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise SystemExit(
            "OPENAI_API_KEY is not set. Export it or put it in a .env file."
        )

    system = load_prompt("system.txt")
    user = render_user_prompt(
        brief,
        site_base_url=site_base_url,
        github_repo_url=github_repo_url,
        github_chapter_path=github_chapter_path,
        playlist_placeholder=playlist_placeholder,
    )

    client = OpenAI(api_key=key)
    # Prefer structured outputs when the model supports json_schema;
    # fall back to json_object for broader compatibility.
    try:
        response = client.chat.completions.create(
            model=model,
            temperature=0.4,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "youtube_text_pack",
                    "strict": True,
                    "schema": PACK_JSON_SCHEMA,
                },
            },
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
    except Exception:
        response = client.chat.completions.create(
            model=model,
            temperature=0.4,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": system
                    + "\n\nRespond with a single JSON object matching this schema:\n"
                    + json.dumps(PACK_JSON_SCHEMA),
                },
                {"role": "user", "content": user},
            ],
        )

    content = response.choices[0].message.content or "{}"
    data = json.loads(content)
    errors = validate_pack(data)
    if errors:
        raise ValueError("Pack failed validation:\n- " + "\n- ".join(errors))
    return data
