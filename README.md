# AI Drug Discovery Lab

**One-person HITL drug-discovery workbench manual** — you are the PI; [reinvent-agent](https://github.com/Luzuokun/reinvent-agent) is the gated execution OS; this site is the company handbook.

> 你是 PI。系统是带闸门的虚拟课题组。

**Live site:** [https://luzuokun.github.io/ai-drug-discovery-lab/](https://luzuokun.github.io/ai-drug-discovery-lab/)

## What this is

Not a tool encyclopedia. Navigation is by **stations** (Research / Chemistry / Structure / Dynamics / Critic / You). Depth lives in the **REINVENT4** 12-chapter research practice course. Empty Coming Soon model pages stay in the **Appendix**.

## Local development

```bash
cd ~/Projects/AI-Drug-Discovery-Lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Open [http://127.0.0.1:8000/ai-drug-discovery-lab/](http://127.0.0.1:8000/ai-drug-discovery-lab/) (English) or append `/zh/` for Chinese. The `/zh/` homepage leads with the one-person HITL company narrative.

Build for production:

```bash
mkdocs build --strict
```

## Publish to GitHub Pages

The repo includes [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml). After pushing to `main`, GitHub Actions builds and deploys the site.

Live URLs:

- English: [https://luzuokun.github.io/ai-drug-discovery-lab/](https://luzuokun.github.io/ai-drug-discovery-lab/)
- 中文: [https://luzuokun.github.io/ai-drug-discovery-lab/zh/](https://luzuokun.github.io/ai-drug-discovery-lab/zh/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the chapter template and writing standards.

## License

Content and code are open for academic and educational use. See repository for details.
