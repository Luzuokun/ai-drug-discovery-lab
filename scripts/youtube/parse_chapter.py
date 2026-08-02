"""Parse MkDocs chapter markdown into a compact brief for video generation."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REINVENT4_DIR = ROOT / "docs" / "molecular-generation" / "reinvent4"

COMING_SOON_MARKERS = (
    '!!! note "Coming Soon',
    "**Coming Soon.**",
    "即将推出",
)

# Short names → chapter files under reinvent4/
SLUG_ALIASES = {
    "01": "01-installation-first-molecule",
    "02": "02-priors-in-practice",
    "03": "03-scoring-function",
    "04": "04-reinforcement-learning",
    "05": "05-diversity-filter",
    "06": "06-curriculum-learning",
    "07": "07-transfer-learning",
    "08": "08-docking-guided-design",
    "09": "09-scaling-and-monitoring",
    "10": "10-ablations-and-hyperparameters",
    "11": "11-case-study-braf",
    "12": "12-troubleshooting-appendix",
}


@dataclass
class ChapterBrief:
    path: str
    slug: str
    title: str
    is_outline: bool
    abstract: str
    learning_objectives: list[str] = field(default_factory=list)
    sections: list[dict[str, str]] = field(default_factory=list)
    tips_warnings: list[str] = field(default_factory=list)
    acceptance_bullets: list[str] = field(default_factory=list)
    enrichment: str = ""
    word_count: int = 0
    site_path_en: str = ""
    site_path_zh: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_chapter_path(arg: str) -> Path:
    """Resolve CLI arg to an absolute chapter .md path."""
    raw = Path(arg)
    if raw.is_file():
        return raw.resolve()

    key = arg.strip().removesuffix(".md")
    if key in SLUG_ALIASES:
        key = SLUG_ALIASES[key]
    candidate = REINVENT4_DIR / f"{key}.md"
    if candidate.is_file():
        return candidate.resolve()

    # Allow bare slug with reinvent4 prefix
    candidate = REINVENT4_DIR / Path(key).name
    if candidate.suffix != ".md":
        candidate = candidate.with_suffix(".md")
    if candidate.is_file():
        return candidate.resolve()

    raise FileNotFoundError(
        f"Cannot resolve chapter '{arg}'. Tried: {raw}, {REINVENT4_DIR / key}.md"
    )


def _strip_admonition_body(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.startswith("    "):
            lines.append(line[4:])
        elif line.startswith("\t"):
            lines.append(line[1:])
        else:
            lines.append(line)
    return "\n".join(lines).strip()


def _extract_admonition(md: str, kind: str) -> str:
    pattern = rf'!!!\s+{kind}\s+"[^"]*"\s*\n((?:    .*\n|\n)*)'
    m = re.search(pattern, md)
    if not m:
        return ""
    return _strip_admonition_body(m.group(1))


def _extract_section(md: str, heading: str) -> str:
    pattern = rf"(?m)^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s+|\Z)"
    m = re.search(pattern, md, flags=re.DOTALL)
    return m.group(1).strip() if m else ""


def _bullet_lines(block: str) -> list[str]:
    bullets: list[str] = []
    for line in block.splitlines():
        m = re.match(r"^\s*[-*]\s+\[\s*[xX ]?\s*\]\s+(.*)$", line)
        if m:
            bullets.append(re.sub(r"\*\*", "", m.group(1)).strip())
            continue
        m = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if m:
            bullets.append(re.sub(r"\*\*", "", m.group(1)).strip())
            continue
        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if m:
            bullets.append(re.sub(r"\*\*", "", m.group(1)).strip())
    return bullets


def _is_outline(md: str) -> bool:
    return any(marker in md for marker in COMING_SOON_MARKERS)


def _prior_enrichment() -> str:
    """Pull prior-related facts from Available Tutorial 01 for outline chapters."""
    path = REINVENT4_DIR / "01-installation-first-molecule.md"
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8")
    chunks: list[str] = []
    for heading in (
        "Step 4: Download a prior model",
        # admonition title varies; grab via regex below
    ):
        sec = _extract_section(text, heading)
        if sec:
            chunks.append(f"### From Tutorial 01 — {heading}\n{sec[:2500]}")

    info = re.search(
        r'!!!\s+info\s+"Prior vs Agent vs Vocabulary[^\"]*"\s*\n((?:    .*\n|\n)*)',
        text,
    )
    if info:
        chunks.append(
            "### From Tutorial 01 — Prior vs Agent vs Vocabulary\n"
            + _strip_admonition_body(info.group(1))
        )

    index = REINVENT4_DIR / "index.md"
    if index.is_file():
        idx = index.read_text(encoding="utf-8")
        chunks.append(
            "### Course syllabus context\n"
            + "Tutorial 02 role: Choose and validate a generative prior for your chemotype.\n"
            + "Reading path notes from index:\n"
            + "\n".join(
                line
                for line in idx.splitlines()
                if "02" in line or "prior" in line.lower() or "Skip" in line
            )[:2000]
        )
    return "\n\n".join(chunks)


def parse_chapter(path: Path) -> ChapterBrief:
    md = path.read_text(encoding="utf-8")
    title_m = re.search(r"^#\s+(.+)$", md, flags=re.MULTILINE)
    title = title_m.group(1).strip() if title_m else path.stem
    slug = path.stem
    is_outline = _is_outline(md)

    abstract = _extract_admonition(md, "abstract")
    lo_block = _extract_section(md, "Learning Objectives")
    learning_objectives = _bullet_lines(lo_block)

    acceptance = _extract_section(md, "What this chapter must deliver")
    acceptance_bullets = _bullet_lines(acceptance)

    sections: list[dict[str, str]] = []
    for m in re.finditer(r"(?m)^##\s+(.+?)\s*$", md):
        name = m.group(1).strip()
        body = _extract_section(md, name)
        # Keep a bounded digest for the LLM
        digest = re.sub(r"```.*?```", "[code block omitted]", body, flags=re.DOTALL)
        digest = re.sub(r"\n{3,}", "\n\n", digest).strip()
        if len(digest) > 1800:
            digest = digest[:1800] + "\n…[truncated]"
        sections.append({"heading": name, "digest": digest})

    tips_warnings: list[str] = []
    for m in re.finditer(
        r'!!!\s+(tip|warning|note|info)\s+"([^"]*)"\s*\n((?:    .*\n|\n)*)',
        md,
    ):
        kind, label, body = m.group(1), m.group(2), _strip_admonition_body(m.group(3))
        snippet = f"[{kind}] {label}: {body[:400]}"
        tips_warnings.append(snippet)

    words = len(re.findall(r"\S+", md))
    enrichment = _prior_enrichment() if is_outline and "prior" in slug else ""
    if is_outline and not enrichment:
        enrichment = _prior_enrichment()

    return ChapterBrief(
        path=str(path),
        slug=slug,
        title=title,
        is_outline=is_outline,
        abstract=abstract,
        learning_objectives=learning_objectives,
        sections=sections,
        tips_warnings=tips_warnings[:12],
        acceptance_bullets=acceptance_bullets,
        enrichment=enrichment,
        word_count=words,
        site_path_en=f"molecular-generation/reinvent4/{slug}/",
        site_path_zh=f"zh/molecular-generation/reinvent4/{slug}/",
    )
