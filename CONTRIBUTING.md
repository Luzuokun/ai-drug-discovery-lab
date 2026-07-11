# AI Drug Discovery Lab — contributing guide

Thank you for helping build the **Open Handbook of AI Drug Discovery**.

## Principles

1. **Every tutorial is reproducible.** Readers must be able to rerun commands and get the same artifacts.
2. **Research practice, not API docs.** Explain *why* choices are made (Python version, CUDA, conda vs pip), not just flags.
3. **Handbook, not blog.** Each page belongs to a section in the knowledge tree.
4. **English first, Chinese follows.** Write and review EN chapters before translating to `docs/zh/`.

## Chapter structure (O'Reilly style)

Use [docs/templates/chapter-template.md](docs/templates/chapter-template.md). Every chapter should include:

| Section | Purpose |
|---------|---------|
| Learning Objectives | What the reader can do after the chapter |
| Why It Matters | Motivation and typical use cases |
| Hands-on Practice | Step-by-step, reproducible commands |
| Code Walkthrough | Config/script parameters explained |
| Expected Output | Files, metrics, screenshots |
| Think About It | Concept-check questions |
| Exercises | Optional extensions |
| Further Reading | Papers and official references |

## Environment blocks

Always specify:

- OS (e.g. Ubuntu 22.04)
- Python version
- CUDA version (if GPU)
- Conda environment name
- Package versions where they matter

## File naming

- Lowercase slugs with hyphens: `01-installation-first-molecule.md`
- Mirror paths in `docs/zh/` for translations
- Update `mkdocs.yml` nav when adding new top-level pages

## Local preview

```bash
source .venv/bin/activate
mkdocs serve
mkdocs build --strict
```

## REINVENT4 series

Chapter 01 (*From Installation to Your First AI-generated Molecule*) is the reference implementation. Later chapters should match its tone and depth.
