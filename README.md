# AI Drug Discovery Lab

**Open Handbook of AI Drug Discovery** — practical, reproducible tutorials for AI-driven molecular design.

> Real workflows. Real code. Real papers.

**Live site:** [https://luzuokun.github.io/ai-drug-discovery-lab/](https://luzuokun.github.io/ai-drug-discovery-lab/)

## What this is

Not a blog. A continuously updated open textbook covering:

- Molecular generation (REINVENT4, DrugEx, MolGPT, …)
- Protein AI (ESM2, ProteinMPNN, RFdiffusion, …)
- Docking, molecular dynamics, RDKit, and Python workflows

Every tutorial is reproducible.

## Local development

```bash
cd ~/Projects/AI-Drug-Discovery-Lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Open [http://127.0.0.1:8000/ai-drug-discovery-lab/](http://127.0.0.1:8000/ai-drug-discovery-lab/) (English) or append `/zh/` for Chinese.

Build for production:

```bash
mkdocs build --strict
```

## Publish to GitHub Pages

The repo includes [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml). After pushing to `main`, GitHub Actions builds and deploys the site.

```bash
git push -u origin main
```

Then in GitHub: **Settings → Pages → Source: GitHub Actions**.

Live URLs:

- English: [https://luzuokun.github.io/ai-drug-discovery-lab/](https://luzuokun.github.io/ai-drug-discovery-lab/)
- 中文: [https://luzuokun.github.io/ai-drug-discovery-lab/zh/](https://luzuokun.github.io/ai-drug-discovery-lab/zh/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the chapter template and writing standards.

## License

Content and code are open for academic and educational use. See repository for details.
