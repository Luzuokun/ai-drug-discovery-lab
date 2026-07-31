# AGENTS.md

## Cursor Cloud specific instructions

This repo is a **bilingual (EN/ZH) MkDocs Material documentation site** ("AI Drug Discovery Lab"). There is no application server or backend — the only "service" is the MkDocs dev server / static build. Standard commands live in `README.md` and `CONTRIBUTING.md`.

- **Python deps live in a venv at `.venv/`** (gitignored). The startup update script (re)installs `requirements.txt` into it. Always run tools via the venv, e.g. `. .venv/bin/activate` first, or call `.venv/bin/mkdocs ...` directly — a bare `mkdocs` is not on `PATH`.
- Creating the venv requires the system package `python3.12-venv` (installed once and retained in the VM snapshot). It is intentionally NOT in the update script (system deps are excluded there); reinstall with `sudo apt-get install -y python3.12-venv` only if venv creation ever fails.
- **Serve locally:** `.venv/bin/mkdocs serve -a 127.0.0.1:8000`. Note the site uses a base path — open `http://127.0.0.1:8000/ai-drug-discovery-lab/` (append `/zh/` for the Chinese site). The bare root `/` returns 404.
- **Strict build (matches CI):** `.venv/bin/mkdocs build --strict`. The red boxed "Warning from the Material for MkDocs team" about MkDocs 2.0 is an upstream advisory, not a build error — a successful build still exits 0.
- Content is authored EN-first under `docs/`, with Chinese mirrors under `docs/zh/` (the `mkdocs-static-i18n` plugin builds `/zh/`). When adding top-level pages, update both nav trees in `mkdocs.yml`.
- Most chapter pages are still "Coming Soon" placeholders with a **research-practice acceptance outline**. The live syllabus is **12 chapters** (see `docs/molecular-generation/reinvent4/index.md`). `scripts/scaffold_docs.py` is aligned with that list but **must not** be re-run against Available chapters (01/03/04) or the hand-authored course index — edit pages directly.
