#!/usr/bin/env python3
"""Generate EN/ZH placeholder pages for the handbook skeleton."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TEMPLATE_LINK = "https://github.com/Luzuokun/ai-drug-discovery-lab/blob/main/docs/templates/chapter-template.md"

REINVENT4_CHAPTERS = [
    ("01-installation-first-molecule", "From Installation to Your First AI-generated Molecule", "从环境搭建到生成第一个分子"),
    ("02-scoring-function", "Scoring Function", "评分函数"),
    ("03-first-molecule", "First Molecule Deep Dive", "第一个分子深入解析"),
    ("04-prior-model", "Prior Model", "Prior 模型"),
    ("05-reinforcement-learning", "Reinforcement Learning", "强化学习"),
    ("06-curriculum-learning", "Curriculum Learning", "课程学习"),
    ("07-diversity-filter", "Diversity Filter", "多样性过滤器"),
    ("08-transfer-learning", "Transfer Learning", "迁移学习"),
    ("09-custom-vocabulary", "Custom Vocabulary", "自定义词表"),
    ("10-docking-integration", "Docking Integration", "对接集成"),
    ("11-rdkit-integration", "RDKit Integration", "RDKit 集成"),
    ("12-parallel-sampling", "Parallel Sampling", "并行采样"),
    ("13-gpu-training", "GPU Training", "GPU 训练"),
    ("14-logging", "Logging", "日志记录"),
    ("15-tensorboard", "TensorBoard", "TensorBoard 可视化"),
    ("16-hyperparameters", "Hyperparameters", "超参数调优"),
    ("17-case-study-braf", "Case Study: BRAF", "案例研究：BRAF"),
    ("18-common-errors", "Common Errors", "常见错误"),
    ("19-faq", "FAQ", "常见问题"),
    ("20-next-steps", "Next Steps", "下一步"),
]

SECTIONS = {
    "getting-started": {
        "index": ("Getting Started", "入门指南", "Environment setup for reproducible AI drug discovery workflows."),
        "pages": [
            ("linux", "Linux", "Linux 环境", "Linux workstation setup for computational chemistry."),
            ("conda", "Conda", "Conda 环境", "Conda and mamba environment management."),
            ("cuda", "CUDA", "CUDA 配置", "CUDA toolkit and GPU driver alignment."),
            ("docker", "Docker", "Docker 容器", "Containerized workflows for portability."),
        ],
    },
    "molecular-generation": {
        "index": ("Molecular Generation", "分子生成", "AI-driven de novo molecular design frameworks."),
        "pages": [
            ("drugex", "DrugEx", "DrugEx", "Deep learning-based molecule generation with DrugEx."),
            ("molgpt", "MolGPT", "MolGPT", "GPT-style molecular language models."),
            ("graphga", "GraphGA", "GraphGA", "Graph-based genetic algorithms for molecular design."),
            ("diffusion", "Diffusion Models", "扩散模型", "Diffusion models for 3D and 2D molecular generation."),
        ],
    },
    "protein-ai": {
        "index": ("Protein AI", "蛋白质 AI", "Sequence and structure models for protein engineering."),
        "pages": [
            ("esm2", "ESM2", "ESM2", "Protein language models with ESM-2."),
            ("esmfold", "ESMFold", "ESMFold", "Structure prediction with ESMFold."),
            ("proteinmpnn", "ProteinMPNN", "ProteinMPNN", "Inverse folding with ProteinMPNN."),
            ("ligandmpnn", "LigandMPNN", "LigandMPNN", "Ligand-aware sequence design."),
            ("rfdiffusion", "RFdiffusion", "RFdiffusion", "Diffusion-based protein backbone generation."),
        ],
    },
    "docking": {
        "index": ("Docking", "分子对接", "Structure-based virtual screening and pose prediction."),
        "pages": [
            ("autodock-vina", "AutoDock Vina", "AutoDock Vina", "Classic docking with AutoDock Vina."),
            ("smina", "Smina", "Smina", "Fork of AutoDock Vina with custom scoring."),
            ("gnina", "Gnina", "Gnina", "CNN-enhanced docking with Gnina."),
        ],
    },
    "molecular-dynamics": {
        "index": ("Molecular Dynamics", "分子动力学", "MD simulations for binding validation."),
        "pages": [
            ("gromacs", "GROMACS", "GROMACS", "Protein-ligand MD with GROMACS."),
            ("amber", "Amber", "Amber", "MD workflows with Amber/AmberTools."),
        ],
    },
    "rdkit": {
        "index": ("RDKit", "RDKit", "Cheminformatics utilities for medchem workflows."),
        "pages": [
            ("fingerprint", "Fingerprints", "分子指纹", "Molecular fingerprints for similarity and ML."),
            ("descriptor", "Descriptors", "分子描述符", "Physicochemical and structural descriptors."),
            ("scaffold", "Scaffolds", "骨架分析", "Scaffold analysis and Murcko frameworks."),
        ],
    },
    "python-workflow": {
        "index": ("Python Workflow", "Python 工作流", "Automation scripts for production pipelines."),
        "pages": [
            ("scripts", "Scripts", "脚本库", "Reusable Python scripts for daily lab work."),
            ("automation", "Automation", "自动化", "End-to-end pipeline automation patterns."),
        ],
    },
    "papers": {
        "index": ("Papers", "论文项目", "Reproducible workflows tied to published research."),
        "pages": [
            ("braf-project", "BRAF Project", "BRAF 项目", "BRAF kinase inhibitor design case study."),
            ("cdk1-project", "CDK1 Project", "CDK1 项目", "CDK1 inhibitor design case study."),
        ],
    },
    "cheat-sheets": {
        "index": ("Cheat Sheets", "速查表", "Quick-reference cards for common commands."),
        "pages": [],
    },
    "resources": {
        "index": ("Resources", "资源", "Datasets, papers, tools, and community links."),
        "pages": [],
    },
}


def placeholder_en(title: str, summary: str, tool: str = "") -> str:
    tool_line = f"\n**Tools:** {tool}\n" if tool else ""
    return f"""# {title}

!!! note "Coming Soon"
    This chapter is part of the *Open Handbook of AI Drug Discovery*.
    Content is under development.

{summary}
{tool_line}
Follow the [chapter template]({TEMPLATE_LINK}) when contributing.
"""


def placeholder_zh(title: str, summary: str, tool: str = "") -> str:
    tool_line = f"\n**工具：** {tool}\n" if tool else ""
    return f"""# {title}

!!! note "即将推出"
    本章属于《AI 药物发现开源教材》，内容正在编写中。

{summary}
{tool_line}
贡献请参考[章节模板]({TEMPLATE_LINK})。
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    for section, cfg in SECTIONS.items():
        en_title, zh_title, en_summary = cfg["index"]
        write(DOCS / section / "index.md", placeholder_en(en_title, en_summary))
        write(DOCS / "zh" / section / "index.md", placeholder_zh(zh_title, en_summary))

        for slug, en_page, zh_page, summary in cfg["pages"]:
            write(DOCS / section / f"{slug}.md", placeholder_en(en_page, summary, en_page))
            write(DOCS / "zh" / section / f"{slug}.md", placeholder_zh(zh_page, summary, zh_page))

    reinvent_index_en = """# REINVENT4

!!! note "Course Overview"
    A 20-chapter hands-on course covering REINVENT4 from installation to production workflows.
    Every chapter is reproducible.

| # | Chapter | Status |
|---|---------|--------|
"""
    reinvent_index_zh = """# REINVENT4

!!! note "课程概览"
    共 20 章的 REINVENT4 实战课程，从安装到生产级工作流。每章均可复现。

| # | 章节 | 状态 |
|---|------|------|
"""
    for i, (slug, en_title, zh_title) in enumerate(REINVENT4_CHAPTERS, 1):
        num = f"{i:02d}"
        write(
            DOCS / "molecular-generation" / "reinvent4" / f"{slug}.md",
            placeholder_en(
                f"REINVENT4 Tutorial {num}: {en_title}",
                f"Chapter {num} of the REINVENT4 course.",
                "REINVENT4",
            ),
        )
        write(
            DOCS / "zh" / "molecular-generation" / "reinvent4" / f"{slug}.md",
            placeholder_zh(
                f"REINVENT4 教程（{num}）：{zh_title}",
                f"REINVENT4 课程第 {num} 章。",
                "REINVENT4",
            ),
        )
        reinvent_index_en += f"| {num} | [{en_title}]({slug}.md) | Coming Soon |\n"
        reinvent_index_zh += f"| {num} | [{zh_title}]({slug}.md) | 即将推出 |\n"

    write(DOCS / "molecular-generation" / "reinvent4" / "index.md", reinvent_index_en)
    write(DOCS / "zh" / "molecular-generation" / "reinvent4" / "index.md", reinvent_index_zh)

    mg_en = placeholder_en(
        "Molecular Generation",
        "AI-driven de novo molecular design frameworks.",
    ) + "\n## Featured course\n\n- [REINVENT4](reinvent4/index.md) — 20-chapter tutorial series\n"
    mg_zh = placeholder_zh(
        "分子生成",
        "AI 驱动的从头分子设计框架。",
    ) + "\n## 特色课程\n\n- [REINVENT4](reinvent4/index.md) — 20 章教程系列\n"
    write(DOCS / "molecular-generation" / "index.md", mg_en)
    write(DOCS / "zh" / "molecular-generation" / "index.md", mg_zh)

    print(f"Scaffold complete under {DOCS}")


if __name__ == "__main__":
    main()
