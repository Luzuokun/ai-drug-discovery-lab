"""Structured schema for one YouTube text pack (OpenAI JSON response)."""

from __future__ import annotations

from typing import Any

# JSON Schema describing the model response we ask OpenAI to return.
PACK_JSON_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "title_en",
        "title_zh",
        "target_duration_seconds",
        "hook_en",
        "hook_zh",
        "beats",
        "script_en",
        "script_zh",
        "voiceover_en",
        "voiceover_zh",
        "storyboard",
        "thumbnail_title",
        "thumbnail_prompt",
        "broll",
        "youtube_description_en",
        "youtube_description_zh",
        "chapters",
        "tags",
        "subtitles_en",
        "subtitles_zh",
        "verify_flags",
    ],
    "properties": {
        "title_en": {"type": "string"},
        "title_zh": {"type": "string"},
        "target_duration_seconds": {
            "type": "integer",
            "minimum": 300,
            "maximum": 480,
        },
        "hook_en": {"type": "string"},
        "hook_zh": {"type": "string"},
        "beats": {
            "type": "array",
            "minItems": 5,
            "maxItems": 12,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "id",
                    "start_sec",
                    "end_sec",
                    "label_en",
                    "label_zh",
                    "narration_en",
                    "narration_zh",
                    "visual",
                ],
                "properties": {
                    "id": {"type": "string"},
                    "start_sec": {"type": "integer", "minimum": 0},
                    "end_sec": {"type": "integer", "minimum": 1},
                    "label_en": {"type": "string"},
                    "label_zh": {"type": "string"},
                    "narration_en": {"type": "string"},
                    "narration_zh": {"type": "string"},
                    "visual": {"type": "string"},
                },
            },
        },
        "script_en": {"type": "string"},
        "script_zh": {"type": "string"},
        "voiceover_en": {"type": "string"},
        "voiceover_zh": {"type": "string"},
        "storyboard": {
            "type": "array",
            "minItems": 5,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "timecode",
                    "shot",
                    "on_screen_text",
                    "voice_beat",
                    "asset_type",
                ],
                "properties": {
                    "timecode": {"type": "string"},
                    "shot": {"type": "string"},
                    "on_screen_text": {"type": "string"},
                    "voice_beat": {"type": "string"},
                    "asset_type": {
                        "type": "string",
                        "enum": [
                            "talking_head",
                            "screencast",
                            "diagram",
                            "molecule_anim",
                            "terminal",
                            "broll",
                            "title_card",
                            "cta_card",
                        ],
                    },
                },
            },
        },
        "thumbnail_title": {"type": "string"},
        "thumbnail_prompt": {"type": "string"},
        "broll": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["item", "why", "source_hint"],
                "properties": {
                    "item": {"type": "string"},
                    "why": {"type": "string"},
                    "source_hint": {"type": "string"},
                },
            },
        },
        "youtube_description_en": {"type": "string"},
        "youtube_description_zh": {"type": "string"},
        "chapters": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["timecode", "title"],
                "properties": {
                    "timecode": {"type": "string"},
                    "title": {"type": "string"},
                },
            },
        },
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 8,
            "maxItems": 25,
        },
        "subtitles_en": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["start_sec", "end_sec", "text"],
                "properties": {
                    "start_sec": {"type": "number"},
                    "end_sec": {"type": "number"},
                    "text": {"type": "string"},
                },
            },
        },
        "subtitles_zh": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["start_sec", "end_sec", "text"],
                "properties": {
                    "start_sec": {"type": "number"},
                    "end_sec": {"type": "number"},
                    "text": {"type": "string"},
                },
            },
        },
        "verify_flags": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Claims that need human fact-check ([VERIFY] items).",
        },
    },
}

REQUIRED_PACK_KEYS = list(PACK_JSON_SCHEMA["required"])


def validate_pack(data: dict[str, Any]) -> list[str]:
    """Return a list of validation errors (empty = OK)."""
    errors: list[str] = []
    for key in REQUIRED_PACK_KEYS:
        if key not in data:
            errors.append(f"missing key: {key}")
    duration = data.get("target_duration_seconds")
    if isinstance(duration, int) and not (300 <= duration <= 480):
        errors.append(
            f"target_duration_seconds={duration} outside 300–480 (5–8 min)"
        )
    beats = data.get("beats")
    if isinstance(beats, list) and len(beats) < 5:
        errors.append(f"beats too short: {len(beats)}")
    return errors
