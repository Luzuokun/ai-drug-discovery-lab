#!/usr/bin/env python3
"""Build Discovery packs for REINVENT4 chapters missing YouTube drafts."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_ROOT = _SCRIPT_DIR.parents[1]
if str(_SCRIPT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR.parent))

from youtube.discovery_pack_lib import PACKS, materialize, svg_to_png  # noqa: E402

AI_STYLE = (
    "Cinematic educational still, 16:9, dark teal lab atmosphere, "
    "3Blue1Brown-like graphic clarity, no logos, no watermarks, "
    "no fake numeric axes, no purple neon, high contrast, space for title text."
)


def ai(name: str, prompt: str) -> dict:
    return {"id": name, "filename": f"{name}.png", "prompt": f"{AI_STYLE} {prompt}"}


COMMON_TAGS = [
    "REINVENT4",
    "drug discovery",
    "generative chemistry",
    "AI drug design",
    "cheminformatics",
    "molecular generation",
    "open science",
    "AstraZeneca REINVENT",
    "tutorial",
    "machine learning",
]


def broll(*items: tuple[str, str, str]) -> list[dict]:
    return [{"item": a, "why": b, "source_hint": c} for a, b, c in items]


def spec_01() -> dict:
    beats = [
        {
            "id": "hook",
            "tc": "0:00–0:12",
            "start_sec": 0,
            "end_sec": 12,
            "label_en": "Hook",
            "label_zh": "开场",
            "narration_en": "You do not have a generative model until you have a real sampled.csv. This episode installs REINVENT4 and proves it with molecules — on CPU, seed 42.",
            "narration_zh": "在你拿到一份真实的 sampled.csv 之前，你还没有生成模型。这一集安装 REINVENT4，并在 CPU、随机种子 42 上用分子证明它能跑。",
            "sub_en": "No sampled.csv, no generative model.",
            "sub_zh": "没有 sampled.csv，就还没有生成模型。",
            "shot": "Title card + first molecules",
            "on_screen": "First molecules · seed 42",
            "asset_type": "title_card",
        },
        {
            "id": "problem",
            "tc": "0:12–0:50",
            "start_sec": 12,
            "end_sec": 50,
            "label_en": "Problem",
            "label_zh": "问题",
            "narration_en": "pip install reinvent will not work. REINVENT4 is cloned and installed with install.py so PyTorch matches CPU or CUDA. Python must be 3.11 or newer. The prior is not a filename trophy. It is the trained distribution that emits SMILES.",
            "narration_zh": "直接 pip install reinvent 行不通。REINVENT4 要克隆仓库，用 install.py 让 PyTorch 匹配 CPU 或 CUDA。Python 需要 3.11 及以上。Prior 不是文件名奖杯，而是会吐出 SMILES 的训练分布。",
            "sub_en": "Clone + install.py. Python 3.11+. The prior is the distribution.",
            "sub_zh": "克隆并用 install.py。Python 3.11+。Prior 才是分布。",
            "shot": "Install decision cards",
            "on_screen": "Python 3.11+ · CPU is enough",
            "asset_type": "diagram",
        },
        {
            "id": "model",
            "tc": "0:50–1:35",
            "start_sec": 50,
            "end_sec": 95,
            "label_en": "Mental model",
            "label_zh": "心智模型",
            "narration_en": "Three words. Prior: the frozen chemical brain from Zenodo — here reinvent_pubchem.prior. Agent: a trainable copy you will later fine-tune with reinforcement learning. Vocabulary: the SMILES tokens stored inside the prior file. Sampling asks the prior for molecules. It does not score them yet.",
            "narration_zh": "三个词。Prior：Zenodo 上冻结的化学大脑，这里是 reinvent_pubchem.prior。Agent：稍后用强化学习微调的可训练副本。词表：写在 prior 文件里的 SMILES 记号。采样只是向 prior 要分子，还没有打分。",
            "sub_en": "Prior frozen. Agent trainable. Vocab lives in the prior.",
            "sub_zh": "Prior 冻结。Agent 可训练。词表在 prior 里。",
            "shot": "Prior / agent / vocab diagram",
            "on_screen": "Prior · Agent · Vocabulary",
            "asset_type": "diagram",
        },
        {
            "id": "proof",
            "tc": "1:35–2:50",
            "start_sec": 95,
            "end_sec": 170,
            "label_en": "Proof",
            "label_zh": "证据",
            "narration_en": "Config: run_type sampling, device cpu, num_smiles 100, unique_molecules true, seed 42. The handbook run finished in about 3.5 seconds and peaked near 550 mebibytes. One hundred requested. Four invalid strings dropped. Ninety-six unique valid molecules written. Columns: SMILES, SMILES_state, NLL. NLL min 21.37, mean 36.44, max 76.98. Lower NLL means the model was more confident. There is no Score column — sampling has no reward.",
            "narration_zh": "配置：run_type sampling，CPU，num_smiles 100，unique_molecules 打开，种子 42。手册这次跑大约 3.5 秒，峰值内存约 550 MiB。请求 100 个，4 条无效被丢掉，写出 96 个唯一有效分子。列是 SMILES、SMILES_state、NLL。NLL 最小 21.37，均值 36.44，最大 76.98。NLL 越低，模型越自信。没有 Score 列——采样还没有奖励。",
            "sub_en": "100 requested → 96 unique. NLL 21–77. No Score column.",
            "sub_zh": "请求 100 → 唯一 96。NLL 21–77。没有 Score。",
            "shot": "first-molecules.png + metrics card",
            "on_screen": "96 molecules · ~3.5 s · ~550 MiB",
            "asset_type": "molecule_anim",
        },
        {
            "id": "failures",
            "tc": "2:50–3:35",
            "start_sec": 170,
            "end_sec": 215,
            "label_en": "Failure modes",
            "label_zh": "失败模式",
            "narration_en": "unique_molecules true is a request, not a guarantee — duplicates and invalids vanish after generation. High NLL is unusual chemistry, not a crash. If you ever see Score all zeros, that is a scoring bug in a later run_type, not a failed sample. Wrong prior file or a truncated Zenodo download is a FileNotFound or load error — check the path.",
            "narration_zh": "unique_molecules 为真只是请求，不是保证——重复和无效会在生成后消失。高 NLL 是少见化学，不是崩溃。如果 Score 全是零，那是后续评分配置的问题，不是采样失败。Prior 路径错了或 Zenodo 下到一半，才会找不到文件。",
            "sub_en": "Unique is after-the-fact. Score=0 is not sampling.",
            "sub_zh": "去重在事后。Score=0 不是采样失败。",
            "shot": "Common errors cards",
            "on_screen": "unique ≠ 100 · no Score yet",
            "asset_type": "diagram",
        },
        {
            "id": "cta",
            "tc": "3:35–4:00",
            "start_sec": 215,
            "end_sec": 240,
            "label_en": "CTA",
            "label_zh": "结尾",
            "narration_en": "Full install commands, the sampling TOML, and sampled.csv live on the AI Drug Discovery Lab site. Code is on GitHub. Next: Tutorial 02 if you must choose a prior — or Tutorial 03 to attach a reward. Links in the description.",
            "narration_zh": "完整安装命令、采样 TOML 和 sampled.csv 在 AI Drug Discovery Lab 网站。代码在 GitHub。下一集：需要选 prior 看教程 02；要接奖励看教程 03。链接在简介里。",
            "sub_en": "Site = tutorial. GitHub = reproduce. Next: 02 or 03.",
            "sub_zh": "网站看教程。GitHub 复现。下一集 02 或 03。",
            "shot": "CTA end card",
            "on_screen": "Site → GitHub",
            "asset_type": "cta_card",
        },
    ]
    return {
        "slug": "01-installation-first-molecule",
        "title_en": "REINVENT4 Tutorial 01: Your First AI Molecules in 4 Minutes",
        "title_zh": "REINVENT4 教程 01：四分钟拿到第一批 AI 分子",
        "duration": 240,
        "beats": beats,
        "chapters": [
            {"timecode": "0:00", "title": "You need sampled.csv"},
            {"timecode": "0:12", "title": "Install for real"},
            {"timecode": "0:50", "title": "Prior vs agent"},
            {"timecode": "1:35", "title": "96 molecules, seed 42"},
            {"timecode": "2:50", "title": "What NLL is not"},
            {"timecode": "3:35", "title": "Site and GitHub"},
        ],
        "blurb_en": "Install REINVENT4 the way the handbook does it, sample 96 molecules on CPU with seed 42, and learn why NLL is not a Score.",
        "blurb_zh": "按手册安装 REINVENT4，在 CPU、种子 42 上采样 96 个分子，并搞清 NLL 不是 Score。",
        "thumb_title": "First molecules · seed 42",
        "thumb_prompt": "Dark teal lab, glowing SMILES ticker becoming 2D molecules, large empty top third for title First molecules. Laptop with terminal vibe, no logos.",
        "metrics_title": "Tutorial 01 — sampling proof",
        "metrics_rows": [
            ("Requested num_smiles", "100"),
            ("Unique valid written", "96"),
            ("Invalid dropped", "4"),
            ("NLL min / mean / max", "21.37 / 36.44 / 76.98"),
            ("Wall-clock / peak RAM", "~3.5 s · ~550 MiB"),
        ],
        "pipeline_title": "Campaign start",
        "pipeline_boxes": [
            ("01 Sample", "this episode", True),
            ("03 Score", "worth making?", False),
            ("04 RL", "change the generator", False),
        ],
        "copy_images": [("01/first-molecules.png", "first-molecules.png")],
        "slideshow": [
            {"id": "hook", "start_sec": 0, "end_sec": 12, "image": "assets/ai/hook.png", "fallback": "assets/pipeline.png"},
            {"id": "problem", "start_sec": 12, "end_sec": 50, "image": "assets/pipeline.png", "fallback": "assets/pipeline.png"},
            {"id": "model", "start_sec": 50, "end_sec": 95, "image": "assets/ai/mental-model.png", "fallback": "assets/pipeline.png"},
            {"id": "proof", "start_sec": 95, "end_sec": 140, "image": "assets/metrics-callout.png", "fallback": "assets/metrics-callout.png"},
            {"id": "mols", "start_sec": 140, "end_sec": 170, "image": "assets/first-molecules.png", "fallback": "assets/metrics-callout.png"},
            {"id": "fail", "start_sec": 170, "end_sec": 215, "image": "assets/ai/failures.png", "fallback": "assets/pipeline.png"},
            {"id": "cta", "start_sec": 215, "end_sec": 240, "image": "assets/ai/cta.png", "fallback": "assets/pipeline.png"},
        ],
        "ai_images": [
            ai("hook", "A CSV file named sampled.csv materializing molecules in a dark teal lab."),
            ai("mental-model", "Three panels: a frozen brain labeled prior, a trainable copy labeled agent, token tiles for SMILES vocabulary. Abstract, no readable fake numbers."),
            ai("failures", "Warning cards about duplicates, invalid SMILES, and a missing Score column. Educational infographic."),
            ai("cta", "End-card background, molecular network, empty center for Site and GitHub text."),
            ai("thumbnail", "YouTube thumbnail, first AI molecules bursting from a terminal, empty top for title."),
        ],
        "tags": COMMON_TAGS + ["installation", "SMILES", "sampling"],
        "broll": broll(
            ("Terminal: reinvent --version", "Prove the CLI exists", "Optional 剪映 insert"),
            ("sampled.csv in a spreadsheet", "Show three columns", "assets CSV / handbook"),
            ("Molecule grid", "Visual payoff", "first-molecules.png"),
        ),
    }


def spec_04() -> dict:
    beats = [
        {
            "id": "hook",
            "tc": "0:00–0:12",
            "start_sec": 0,
            "end_sec": 12,
            "label_en": "Hook",
            "label_zh": "开场",
            "narration_en": "Scoring ranks a list you already have. Reinforcement learning changes what the generator emits next. That is the jump from Tutorial 03 to 04.",
            "narration_zh": "评分只给已有分子排队。强化学习会改变生成器接下来吐出什么。这就是教程 03 到 04 的跳跃。",
            "sub_en": "Scoring ranks. RL rewrites the generator.",
            "sub_zh": "评分是排队。RL 改写生成器。",
            "shot": "Score vs step hook",
            "on_screen": "Score up · NLL down",
            "asset_type": "title_card",
        },
        {
            "id": "problem",
            "tc": "0:12–0:48",
            "start_sec": 12,
            "end_sec": 48,
            "label_en": "Problem",
            "label_zh": "问题",
            "narration_en": "Drug discovery needs more molecules like the good ones — not a static spreadsheet. Each RL step samples a batch, scores it, and updates the agent so high-scoring sequences become more probable. The prior stays frozen as a chemical-grammar anchor. That is DAP — Direct Augmented Prior.",
            "narration_zh": "药物发现需要更多像好分子的分子，而不是一张静态表。每一步 RL 采样一批、打分、更新 agent，让高分序列更可能出现。Prior 冻结，充当化学语法锚。这就是 DAP。",
            "sub_en": "Sample, score, update. Prior stays frozen.",
            "sub_zh": "采样、打分、更新。Prior 保持冻结。",
            "shot": "RL loop diagram",
            "on_screen": "sample → score → DAP update",
            "asset_type": "diagram",
        },
        {
            "id": "model",
            "tc": "0:48–1:35",
            "start_sec": 48,
            "end_sec": 95,
            "label_en": "Mental model",
            "label_zh": "心智模型",
            "narration_en": "run_type is staged_learning even for one stage. prior_file and agent_file start as the same PubChem prior. Scoring must nest under stage.scoring — a bare scoring section fails validation. That is the number-one copy-paste trap from Tutorial 03. Unique_sequences is not accepted in REINVENT 4.8.24 RL schema. DAP sigma 128 and rate 1e-4 are the handbook defaults.",
            "narration_zh": "即使只有一个阶段，run_type 也是 staged_learning。prior_file 和 agent_file 一开始指向同一个 PubChem prior。评分必须写在 stage.scoring 下，顶层 scoring 会校验失败。这是从教程 03 复制过来的第一陷阱。4.8.24 的 RL 模式不接受 unique_sequences。DAP 的 sigma 128、学习率 1e-4 是手册默认。",
            "sub_en": "stage.scoring, not scoring. DAP sigma 128.",
            "sub_zh": "用 stage.scoring，不要用顶层 scoring。",
            "shot": "TOML nesting card",
            "on_screen": "[stage.scoring] required",
            "asset_type": "diagram",
        },
        {
            "id": "proof",
            "tc": "1:35–2:55",
            "start_sec": 95,
            "end_sec": 175,
            "label_en": "Proof",
            "label_zh": "证据",
            "narration_en": "Twenty-five steps, batch 64, CPU, seed 42. About 27 seconds, peak RAM about 1.5 gibibytes. Mean Score 0.66 to 0.79. Agent NLL 34.79 to 27.15. Fraction above 0.8 goes 53 percent to 66 percent. Checkpoint rl_agent.chkpt is about 23 megabytes. Demo length is not a production campaign — scale max_steps when the library matters.",
            "narration_zh": "25 步，batch 64，CPU，种子 42。大约 27 秒，峰值内存约 1.5 GiB。平均 Score 从 0.66 到 0.79。Agent NLL 从 34.79 到 27.15。高于 0.8 的比例从 53% 到 66%。检查点约 23 MB。演示长度不是生产战役——库真要出货时再加大 max_steps。",
            "sub_en": "Score 0.66→0.79. NLL 34.79→27.15. ~27 s CPU.",
            "sub_zh": "Score 0.66→0.79。NLL 34.79→27.15。约 27 秒。",
            "shot": "score-vs-step.png",
            "on_screen": "25 steps · batch 64",
            "asset_type": "diagram",
        },
        {
            "id": "failures",
            "tc": "2:55–3:35",
            "start_sec": 175,
            "end_sec": 215,
            "label_en": "Failure modes",
            "label_zh": "失败模式",
            "narration_en": "Scores stuck near zero? Debug the reward with run_type scoring on a fixed list first. No diversity filter here on purpose — that is Tutorial 05. To continue later, point agent_file at the checkpoint and keep prior_file as the original prior.",
            "narration_zh": "分数贴着零？先用 run_type scoring 在固定列表上调试奖励。本章故意不加多样性过滤器，那是教程 05。要续跑，把 agent_file 指到检查点，prior_file 仍用原来的 prior。",
            "sub_en": "Flat scores → fix the reward. Resume via agent_file.",
            "sub_zh": "分数太平 → 先修奖励。用 agent_file 续跑。",
            "shot": "Checkpoint reuse card",
            "on_screen": "agent_file = rl_agent.chkpt",
            "asset_type": "diagram",
        },
        {
            "id": "cta",
            "tc": "3:35–4:00",
            "start_sec": 215,
            "end_sec": 240,
            "label_en": "CTA",
            "label_zh": "结尾",
            "narration_en": "Full TOML, CSV, and the Score-versus-step figure are on the AI Drug Discovery Lab site. Code is on GitHub. Next: Tutorial 05 — stop scaffold collapse once RL starts working.",
            "narration_zh": "完整 TOML、CSV 和 Score 曲线在 AI Drug Discovery Lab 网站。代码在 GitHub。下一集教程 05：RL 一生效就拦住骨架塌缩。",
            "sub_en": "Site and GitHub. Next: diversity filter.",
            "sub_zh": "网站与 GitHub。下一集：多样性过滤器。",
            "shot": "CTA",
            "on_screen": "Site → GitHub → Tutorial 05",
            "asset_type": "cta_card",
        },
    ]
    return {
        "slug": "04-reinforcement-learning",
        "title_en": "REINVENT4 Tutorial 04: RL Makes High Scores More Probable",
        "title_zh": "REINVENT4 教程 04：强化学习让高分更可能出现",
        "duration": 240,
        "beats": beats,
        "chapters": [
            {"timecode": "0:00", "title": "Rank vs generate"},
            {"timecode": "0:12", "title": "The RL loop"},
            {"timecode": "0:48", "title": "stage.scoring trap"},
            {"timecode": "1:35", "title": "0.66 to 0.79 in 25 steps"},
            {"timecode": "2:55", "title": "When Score is flat"},
            {"timecode": "3:35", "title": "Site and GitHub"},
        ],
        "blurb_en": "Single-stage staged_learning on CPU, seed 42: Score rises, agent NLL falls, and we show the stage.scoring trap.",
        "blurb_zh": "CPU、种子 42 的单阶段 staged_learning：Score 上升、Agent NLL 下降，并讲清 stage.scoring 陷阱。",
        "thumb_title": "Score ↑  NLL ↓",
        "thumb_prompt": "Dark teal, rising score curve and falling NLL curve as two glowing lines, empty top for title.",
        "metrics_title": "Tutorial 04 — 25-step RL",
        "metrics_rows": [
            ("Mean Score step 1 → 25", "0.66 → 0.79"),
            ("Agent NLL step 1 → 25", "34.79 → 27.15"),
            ("Score > 0.8 fraction", "53% → 66%"),
            ("Wall-clock / RAM", "~27 s · ~1.5 GiB"),
        ],
        "pipeline_title": "Where RL sits",
        "pipeline_boxes": [
            ("03 Score", "debug reward", False),
            ("04 RL", "this episode", True),
            ("05 Diversity", "stop collapse", False),
        ],
        "copy_images": [
            ("04/score-vs-step.png", "score-vs-step.png"),
            ("04/top-rl-molecules.png", "top-rl-molecules.png"),
        ],
        "slideshow": [
            {"id": "hook", "start_sec": 0, "end_sec": 12, "image": "assets/ai/hook.png", "fallback": "assets/pipeline.png"},
            {"id": "problem", "start_sec": 12, "end_sec": 48, "image": "assets/pipeline.png", "fallback": "assets/pipeline.png"},
            {"id": "model", "start_sec": 48, "end_sec": 95, "image": "assets/ai/mental-model.png", "fallback": "assets/metrics-callout.png"},
            {"id": "proof", "start_sec": 95, "end_sec": 145, "image": "assets/score-vs-step.png", "fallback": "assets/metrics-callout.png"},
            {"id": "mols", "start_sec": 145, "end_sec": 175, "image": "assets/top-rl-molecules.png", "fallback": "assets/metrics-callout.png"},
            {"id": "fail", "start_sec": 175, "end_sec": 215, "image": "assets/metrics-callout.png", "fallback": "assets/pipeline.png"},
            {"id": "cta", "start_sec": 215, "end_sec": 240, "image": "assets/ai/cta.png", "fallback": "assets/pipeline.png"},
        ],
        "ai_images": [
            ai("hook", "Two arrows: a static ranked list versus a generator morphing molecules."),
            ai("mental-model", "Frozen prior lock icon beside a trainable agent network, DAP arrow labeled score-augmented target. Abstract."),
            ai("cta", "End-card molecular network, empty center for Site and GitHub."),
            ai("thumbnail", "YouTube thumbnail with rising score curve, empty top third for title Score up NLL down."),
        ],
        "tags": COMMON_TAGS + ["reinforcement learning", "DAP"],
        "broll": broll(
            ("score-vs-step.png", "Core proof", "chapter figure"),
            ("rl.toml nesting", "Show stage.scoring", "optional screencast"),
            ("top-rl-molecules.png", "Late-step chemistry", "chapter figure"),
        ),
    }


def spec_05() -> dict:
    beats = [
        {
            "id": "hook", "tc": "0:00–0:12", "start_sec": 0, "end_sec": 12,
            "label_en": "Hook", "label_zh": "开场",
            "narration_en": "A high Score can be twenty near-copies of benzene. Tutorial 04 made RL work. This episode treats diversity as the experimental control.",
            "narration_zh": "很高的 Score 可能只是二十个苯环近亲。教程 04 让 RL 生效。这一集把多样性当成实验对照。",
            "sub_en": "High Score can still be scaffold collapse.",
            "sub_zh": "高分也可能是骨架塌缩。",
            "shot": "Benzene pile vs diverse cores", "on_screen": "Score ≠ library",
            "asset_type": "title_card",
        },
        {
            "id": "problem", "tc": "0:12–0:50", "start_sec": 12, "end_sec": 50,
            "label_en": "Problem", "label_zh": "问题",
            "narration_en": "Without diversity pressure, RL rediscovers the same easy Murcko core with tiny side-chain edits. The CSV looks great. Chemistry gets duplicates. A diversity filter memorizes scaffolds that already scored well and down-weights further hits in that bucket.",
            "narration_zh": "没有多样性压力，RL 会反复发现同一个好挖的 Murcko 核心，只改一点点侧链。CSV 很好看，化学上全是重复。多样性过滤器会记住已经高分的骨架，并压低同一桶里的后续命中。",
            "sub_en": "Filter memorizes high-scoring scaffolds.",
            "sub_zh": "过滤器记住已高分的骨架。",
            "shot": "Bucket memory diagram", "on_screen": "IdenticalMurckoScaffold",
            "asset_type": "diagram",
        },
        {
            "id": "model", "tc": "0:50–1:35", "start_sec": 50, "end_sec": 95,
            "label_en": "Mental model", "label_zh": "心智模型",
            "narration_en": "We rerun the Tutorial 04 campaign twice. Same seed 42, same 25 steps, same scoring. One arm has no filter. The other adds a global IdenticalMurckoScaffold diversity filter with bucket_size 25 and minscore 0.4. One variable. Other filter types exist — pick one hypothesis per experiment.",
            "narration_zh": "教程 04 的战役跑两遍。同样种子 42、同样 25 步、同样评分。一臂无过滤器，另一臂加上全局 IdenticalMurckoScaffold，bucket_size 25，minscore 0.4。只改一个变量。其他过滤器类型也有——一次实验只验证一个假设。",
            "sub_en": "A/B at seed 42. One variable: the filter.",
            "sub_zh": "种子 42 做 A/B。只改过滤器。",
            "shot": "A/B protocol card", "on_screen": "same seed · ± DF",
            "asset_type": "diagram",
        },
        {
            "id": "proof", "tc": "1:35–2:55", "start_sec": 95, "end_sec": 175,
            "label_en": "Proof", "label_zh": "证据",
            "narration_en": "Mean Score at step 25: 0.79 without the filter, 0.74 with it. Unique Murcko scaffolds: 1165 versus 1238. Count of the top scaffold, benzene: 120 versus 101. Step 1 Scores matched at 0.66. Each leg about 27 to 28 seconds on CPU. You trade a little mean Score for a wider library.",
            "narration_zh": "第 25 步平均 Score：无过滤器 0.79，有过滤器 0.74。唯一 Murcko 骨架：1165 对 1238。第一骨架苯环计数：120 对 101。第 1 步 Score 都是 0.66。每臂大约 27 到 28 秒。你用一点平均分，换更宽的库。",
            "sub_en": "Score 0.79 vs 0.74. Scaffolds 1165 vs 1238.",
            "sub_zh": "Score 0.79 对 0.74。骨架 1165 对 1238。",
            "shot": "df-ab-compare.png", "on_screen": "Score vs scaffolds",
            "asset_type": "diagram",
        },
        {
            "id": "failures", "tc": "2:55–3:35", "start_sec": 175, "end_sec": 215,
            "label_en": "Decision", "label_zh": "决策",
            "narration_en": "If top-scaffold occupancy barely moves, the bucket is too large or minscore never fires. If Score collapses, the filter is starving the agent — loosen bucket_size. Diversity is an experimental knob, not a checkbox you forget after Tutorial 04.",
            "narration_zh": "如果第一骨架占用几乎不变，桶太大或 minscore 从未触发。如果 Score 崩了，过滤器把 agent 饿死了——放宽 bucket_size。多样性是实验旋钮，不是教程 04 之后忘掉的勾选。",
            "sub_en": "Diversity is a knob, not a checkbox.",
            "sub_zh": "多样性是旋钮，不是勾选。",
            "shot": "Trade-off card", "on_screen": "bucket_size · minscore",
            "asset_type": "diagram",
        },
        {
            "id": "cta", "tc": "3:35–4:00", "start_sec": 215, "end_sec": 240,
            "label_en": "CTA", "label_zh": "结尾",
            "narration_en": "A/B CSVs and figures are on the AI Drug Discovery Lab site. Code is on GitHub. Next: Tutorial 06 — escalate objectives across stages.",
            "narration_zh": "A/B 的 CSV 和图在 AI Drug Discovery Lab 网站。代码在 GitHub。下一集教程 06：分阶段升级目标。",
            "sub_en": "Site and GitHub. Next: curriculum.",
            "sub_zh": "网站与 GitHub。下一集：课程学习。",
            "shot": "CTA", "on_screen": "Site → GitHub → Tutorial 06",
            "asset_type": "cta_card",
        },
    ]
    return {
        "slug": "05-diversity-filter",
        "title_en": "REINVENT4 Tutorial 05: High Score Can Still Be Collapse",
        "title_zh": "REINVENT4 教程 05：高分仍可能是骨架塌缩",
        "duration": 240, "beats": beats,
        "chapters": [
            {"timecode": "0:00", "title": "Score is not a library"},
            {"timecode": "0:12", "title": "Why filters exist"},
            {"timecode": "0:50", "title": "A/B protocol"},
            {"timecode": "1:35", "title": "0.79 vs 0.74"},
            {"timecode": "2:55", "title": "Tune the knob"},
            {"timecode": "3:35", "title": "Site and GitHub"},
        ],
        "blurb_en": "Same 25-step RL with and without IdenticalMurckoScaffold: Score 0.79 vs 0.74, scaffolds 1165 vs 1238.",
        "blurb_zh": "同样 25 步 RL，有无 Murcko 多样性过滤器：Score 0.79 对 0.74，骨架 1165 对 1238。",
        "thumb_title": "Stop scaffold collapse",
        "thumb_prompt": "A collapsing stack of identical benzene rings versus a spread of different scaffolds, dark teal, empty top for title.",
        "metrics_title": "Tutorial 05 — DF A/B",
        "metrics_rows": [
            ("Score step 25  no DF / DF", "0.79 / 0.74"),
            ("Unique Murcko scaffolds", "1165 / 1238"),
            ("Top scaffold c1ccccc1 count", "120 / 101"),
            ("Wall-clock each arm", "~27–28 s"),
        ],
        "pipeline_title": "Control the failure mode",
        "pipeline_boxes": [
            ("04 RL", "Score rises", False),
            ("05 DF", "this episode", True),
            ("06 Curriculum", "escalate goals", False),
        ],
        "copy_images": [
            ("05/df-ab-compare.png", "df-ab-compare.png"),
            ("05/no-df-top-scaffold.png", "no-df-top-scaffold.png"),
            ("05/with-df-top-scaffold.png", "with-df-top-scaffold.png"),
        ],
        "slideshow": [
            {"id": "hook", "start_sec": 0, "end_sec": 12, "image": "assets/ai/hook.png", "fallback": "assets/pipeline.png"},
            {"id": "problem", "start_sec": 12, "end_sec": 50, "image": "assets/pipeline.png", "fallback": "assets/pipeline.png"},
            {"id": "model", "start_sec": 50, "end_sec": 95, "image": "assets/ai/mental-model.png", "fallback": "assets/metrics-callout.png"},
            {"id": "proof", "start_sec": 95, "end_sec": 145, "image": "assets/df-ab-compare.png", "fallback": "assets/metrics-callout.png"},
            {"id": "scaf", "start_sec": 145, "end_sec": 175, "image": "assets/no-df-top-scaffold.png", "fallback": "assets/metrics-callout.png"},
            {"id": "fail", "start_sec": 175, "end_sec": 215, "image": "assets/metrics-callout.png", "fallback": "assets/pipeline.png"},
            {"id": "cta", "start_sec": 215, "end_sec": 240, "image": "assets/ai/cta.png", "fallback": "assets/pipeline.png"},
        ],
        "ai_images": [
            ai("hook", "A tower of identical benzene rings cracking, diverse scaffolds escaping to the side."),
            ai("mental-model", "Two lab notebooks labeled no DF and Murcko DF, one variable highlighted."),
            ai("cta", "End-card molecular network, empty center for Site and GitHub."),
            ai("thumbnail", "YouTube thumbnail, collapsed vs diverse molecule clouds, empty top for title."),
        ],
        "tags": COMMON_TAGS + ["diversity filter", "Murcko scaffold"],
        "broll": broll(
            ("df-ab-compare.png", "A/B proof", "chapter figure"),
            ("TOML diversity_filter block", "Show the knob", "optional screencast"),
        ),
    }


def spec_06() -> dict:
    beats = [
        {
            "id": "hook", "tc": "0:00–0:12", "start_sec": 0, "end_sec": 12,
            "label_en": "Hook", "label_zh": "开场",
            "narration_en": "Do not demand LogP on day one. Curriculum learning in REINVENT4 is multi-stage RL with different scoring setups — not a separate algorithm.",
            "narration_zh": "不要第一天就要求 LogP。REINVENT4 的课程学习是多阶段、不同评分的 RL，不是另一种算法。",
            "sub_en": "Curriculum = staged scoring, not a new algorithm.",
            "sub_zh": "课程学习是分阶段评分，不是新算法。",
            "shot": "Easy then hard objectives", "on_screen": "Stage 1 then Stage 2",
            "asset_type": "title_card",
        },
        {
            "id": "problem", "tc": "0:12–0:55", "start_sec": 12, "end_sec": 55,
            "label_en": "Problem", "label_zh": "问题",
            "narration_en": "A single hard reward from step one is noisy. Medicinal chemistry stabilizes a series, then tightens ADMET. Stage 1 uses the Tutorial 04 stack: QED, molecular weight, alerts. Stage 2 adds SlogP with a reverse sigmoid. Auto curriculum is multiple stage blocks in one TOML. Manual curriculum hands a checkpoint to a new file.",
            "narration_zh": "从第一步就上很难的奖励，分数会很吵。药物化学先稳住系列，再收紧 ADMET。阶段 1 用教程 04 的 QED、分子量、alerts。阶段 2 加上 reverse sigmoid 的 SlogP。自动课程是一个 TOML 里多个 stage；手动课程是把检查点交给新文件。",
            "sub_en": "Easy MPO first. Then add SlogP.",
            "sub_zh": "先简单 MPO，再加 SlogP。",
            "shot": "Two-stage diagram", "on_screen": "QED+MW → +SlogP",
            "asset_type": "diagram",
        },
        {
            "id": "model", "tc": "0:55–1:40", "start_sec": 55, "end_sec": 100,
            "label_en": "The trap", "label_zh": "陷阱",
            "narration_en": "If a stage ends because max_steps was reached, REINVENT terminates all remaining stages. Auto curriculum only advances when max_score fires after min_steps. Treat stage-one max_steps as a safety ceiling, not the plan.",
            "narration_zh": "如果一个阶段因为碰到 max_steps 结束，REINVENT 会终止后面所有阶段。自动课程只有在 min_steps 之后触达 max_score 才会前进。把阶段 1 的 max_steps 当成安全天花板，而不是计划本身。",
            "sub_en": "Hitting max_steps aborts later stages.",
            "sub_zh": "碰到 max_steps 会中止后续阶段。",
            "shot": "Termination rules", "on_screen": "max_score advances · max_steps kills",
            "asset_type": "diagram",
        },
        {
            "id": "proof", "tc": "1:40–2:55", "start_sec": 100, "end_sec": 175,
            "label_en": "Proof", "label_zh": "证据",
            "narration_en": "Seed 42 auto run. Stage 1 early-stops at step 12, mean Score 0.74, above max_score 0.72. Stage 2 runs 20 steps. Score drops to 0.46 on the harder reward, then climbs to 0.59. About 29 seconds, peak RAM about 1.5 gibibytes. That cliff at the boundary is evidence the objective changed — not a crash.",
            "narration_zh": "种子 42 的自动跑。阶段 1 在第 12 步提前停止，平均 Score 0.74，高于 max_score 0.72。阶段 2 跑满 20 步。更难奖励让 Score 掉到 0.46，再爬到 0.59。大约 29 秒，峰值约 1.5 GiB。边界上的悬崖说明目标变了，不是崩溃。",
            "sub_en": "Stage 1: 12 steps. Stage 2: 0.46 → 0.59.",
            "sub_zh": "阶段 1：12 步。阶段 2：0.46 → 0.59。",
            "shot": "curriculum-score-stages.png", "on_screen": "early-stop then climb",
            "asset_type": "diagram",
        },
        {
            "id": "manual", "tc": "2:55–3:35", "start_sec": 175, "end_sec": 215,
            "label_en": "Manual CL", "label_zh": "手动课程",
            "narration_en": "Manual curriculum: agent_file is the stage-one checkpoint, prior_file stays the original prior. Use auto when stage 1 will early-stop. Use manual when you need to inspect CSV, retune transforms, or continue tomorrow.",
            "narration_zh": "手动课程：agent_file 是阶段 1 检查点，prior_file 仍是原来的 prior。阶段 1 能提前停就用自动；需要看 CSV、改变换、或明天再跑，就用手动。",
            "sub_en": "Manual: agent_file = chkpt, prior unchanged.",
            "sub_zh": "手动：agent 用检查点，prior 不变。",
            "shot": "Checkpoint hand-off", "on_screen": "auto vs manual",
            "asset_type": "diagram",
        },
        {
            "id": "cta", "tc": "3:35–4:00", "start_sec": 215, "end_sec": 240,
            "label_en": "CTA", "label_zh": "结尾",
            "narration_en": "Configs and stage CSVs are on the AI Drug Discovery Lab site. Code is on GitHub. Next: Tutorial 07 — adapt the prior with transfer learning before a long RL campaign.",
            "narration_zh": "配置和各阶段 CSV 在 AI Drug Discovery Lab 网站。代码在 GitHub。下一集教程 07：在长 RL 之前用迁移学习适配 prior。",
            "sub_en": "Site and GitHub. Next: transfer learning.",
            "sub_zh": "网站与 GitHub。下一集：迁移学习。",
            "shot": "CTA", "on_screen": "Site → GitHub → Tutorial 07",
            "asset_type": "cta_card",
        },
    ]
    return {
        "slug": "06-curriculum-learning",
        "title_en": "REINVENT4 Tutorial 06: Escalate Objectives — Don't Front-Load Hardness",
        "title_zh": "REINVENT4 教程 06：升级目标，而不是一开始就很难",
        "duration": 240, "beats": beats,
        "chapters": [
            {"timecode": "0:00", "title": "Not a new algorithm"},
            {"timecode": "0:12", "title": "Easy then hard"},
            {"timecode": "0:55", "title": "max_steps kills the rest"},
            {"timecode": "1:40", "title": "Early-stop at step 12"},
            {"timecode": "2:55", "title": "Auto vs manual"},
            {"timecode": "3:35", "title": "Site and GitHub"},
        ],
        "blurb_en": "Two-stage auto curriculum on CPU: stage 1 early-stops at step 12; stage 2 Score 0.46 to 0.59. Hitting max_steps aborts later stages.",
        "blurb_zh": "CPU 上双阶段自动课程：阶段 1 第 12 步提前停；阶段 2 Score 从 0.46 到 0.59。碰到 max_steps 会中止后续阶段。",
        "thumb_title": "max_score advances",
        "thumb_prompt": "Two-stage staircase of objectives, a trapdoor labeled max_steps, dark teal, empty top for title.",
        "metrics_title": "Tutorial 06 — auto curriculum",
        "metrics_rows": [
            ("Stage 1 length", "12 steps (early-stop)"),
            ("Stage 1 Score", "0.66 → 0.74"),
            ("Stage 2 Score", "0.46 → 0.59"),
            ("Wall-clock / RAM", "~29 s · ~1.5 GiB"),
        ],
        "pipeline_title": "Escalate, then adapt",
        "pipeline_boxes": [
            ("05 DF", "control collapse", False),
            ("06 Curriculum", "this episode", True),
            ("07 TL", "shift the prior", False),
        ],
        "copy_images": [
            ("06/curriculum-score-stages.png", "curriculum-score-stages.png"),
            ("06/stage2-top-molecules.png", "stage2-top-molecules.png"),
            ("06/manual-curriculum-scores.png", "manual-curriculum-scores.png"),
        ],
        "slideshow": [
            {"id": "hook", "start_sec": 0, "end_sec": 12, "image": "assets/ai/hook.png", "fallback": "assets/pipeline.png"},
            {"id": "problem", "start_sec": 12, "end_sec": 55, "image": "assets/pipeline.png", "fallback": "assets/pipeline.png"},
            {"id": "model", "start_sec": 55, "end_sec": 100, "image": "assets/ai/mental-model.png", "fallback": "assets/metrics-callout.png"},
            {"id": "proof", "start_sec": 100, "end_sec": 155, "image": "assets/curriculum-score-stages.png", "fallback": "assets/metrics-callout.png"},
            {"id": "mols", "start_sec": 155, "end_sec": 175, "image": "assets/stage2-top-molecules.png", "fallback": "assets/metrics-callout.png"},
            {"id": "manual", "start_sec": 175, "end_sec": 215, "image": "assets/manual-curriculum-scores.png", "fallback": "assets/metrics-callout.png"},
            {"id": "cta", "start_sec": 215, "end_sec": 240, "image": "assets/ai/cta.png", "fallback": "assets/pipeline.png"},
        ],
        "ai_images": [
            ai("hook", "A difficulty staircase: easy drug-like icons then a LogP weight dropping onto the agent."),
            ai("mental-model", "Flowchart: max_score opens stage 2, max_steps slams a gate. Educational."),
            ai("cta", "End-card molecular network, empty center for Site and GitHub."),
            ai("thumbnail", "YouTube thumbnail, two stages with a cliff then climb, empty top for title."),
        ],
        "tags": COMMON_TAGS + ["curriculum learning", "staged learning"],
        "broll": broll(
            ("curriculum-score-stages.png", "Stage boundary cliff", "chapter figure"),
            ("Log line: Terminating all stages", "Teach the trap", "optional screencast"),
        ),
    }


def spec_07() -> dict:
    beats = [
        {
            "id": "hook", "tc": "0:00–0:12", "start_sec": 0, "end_sec": 12,
            "label_en": "Hook", "label_zh": "开场",
            "narration_en": "Tutorial 02 was eight epochs of transfer learning. This episode asks when to stop — and whether TL actually changes the RL campaign.",
            "narration_zh": "教程 02 只做了 8 个 epoch 的迁移学习。这一集问：何时该停，以及 TL 会不会真的改变 RL 战役。",
            "sub_en": "Short TL was a taste. Now: stop rules.",
            "sub_zh": "短 TL 只是尝尝。现在看停训规则。",
            "shot": "Overfit curve hook", "on_screen": "When do you stop TL?",
            "asset_type": "title_card",
        },
        {
            "id": "problem", "tc": "0:12–0:50", "start_sec": 12, "end_sec": 50,
            "label_en": "Problem", "label_zh": "问题",
            "narration_en": "A tiny sulfonamide set keeps enriching if you train long enough — and then it memorizes. Official docs list flags. Lab work needs a stop rule, an overfitting checklist, and a TL-then-RL versus RL-only A/B under the same scoring function.",
            "narration_zh": "很小的磺酰胺集，训得够久命中率还会涨，然后就开始背诵。官方文档列开关。实验室需要停训规则、过拟合清单，以及同一评分下 TL 再 RL 对纯 RL 的对照。",
            "sub_en": "Enrichment without memorizing the train set.",
            "sub_zh": "要富集，但不要背训练集。",
            "shot": "Memorization vs invention", "on_screen": "val NLL · mem % · scaffolds",
            "asset_type": "diagram",
        },
        {
            "id": "proof_tl", "tc": "0:50–2:10", "start_sec": 50, "end_sec": 130,
            "label_en": "Overfit curve", "label_zh": "过拟合曲线",
            "narration_en": "Same Tutorial 02 SMILES. Forty epochs, checkpoints every eight, CPU, seed 42, about 62 seconds. Epoch 0: 8.4 percent sulfonamide, 168 scaffolds, zero exact train SMILES. Epoch 8: 64.3 percent, still zero memorized — and best validation NLL. Epoch 24: 83 percent hits but 12 percent exact train SMILES. Epoch 40: 86 percent hits, 40 percent memorized, unique rows fall from 191 to 165. Last epoch is not the winner.",
            "narration_zh": "还是教程 02 那套 SMILES。40 个 epoch，每 8 个存盘，CPU，种子 42，大约 62 秒。第 0 轮：磺酰胺 8.4%，168 个骨架，0 条背出训练集。第 8 轮：64.3%，仍未背诵——验证 NLL 也最好。第 24 轮：命中 83%，但 12% 是训练集原样。第 40 轮：命中 86%，背诵 40%，唯一行从 191 掉到 165。最后一个 epoch 不是赢家。",
            "sub_en": "Best val NLL at epoch 8. Epoch 40 memorizes 40%.",
            "sub_zh": "最佳验证 NLL 在第 8 轮。第 40 轮背出 40%。",
            "shot": "tl-overfit-curve.png", "on_screen": "ep8 vs ep40",
            "asset_type": "diagram",
        },
        {
            "id": "proof_rl", "tc": "2:10–3:10", "start_sec": 130, "end_sec": 190,
            "label_en": "TL then RL", "label_zh": "TL 再 RL",
            "narration_en": "Same QED, molecular weight, alerts as Tutorial 04. Twenty-five steps. RL-only last-five mean Score 0.775 and 4.4 percent sulfonamide. TL-then-RL from the epoch-24 checkpoint: Score 0.847 and 66.6 percent sulfonamide — even though the reward does not pay for the motif. Set both prior_file and agent_file to the TL checkpoint so DAP anchors to the adapted distribution.",
            "narration_zh": "评分仍是教程 04 的 QED、分子量、alerts。25 步。纯 RL 最后五步平均 Score 0.775，磺酰胺 4.4%。用第 24 轮检查点做 TL 再 RL：Score 0.847，磺酰胺 66.6%——尽管奖励并不给这个结构付钱。prior_file 和 agent_file 都要指向 TL 检查点，让 DAP 锚在适配后的分布上。",
            "sub_en": "TL→RL 0.847 / 66.6% vs RL-only 0.775 / 4.4%.",
            "sub_zh": "TL→RL 0.847 / 66.6%，纯 RL 0.775 / 4.4%。",
            "shot": "tl-vs-rl-compare.png", "on_screen": "same reward · different start",
            "asset_type": "diagram",
        },
        {
            "id": "decision", "tc": "3:10–3:35", "start_sec": 190, "end_sec": 215,
            "label_en": "Decision", "label_zh": "决策",
            "narration_en": "Keep the checkpoint where validation NLL bottoms and mem percent is still near zero. Need linkers or R-groups? Wrong generator — not more epochs. Curriculum changes the reward schedule. TL changes the starting distribution. They compose.",
            "narration_zh": "留在验证 NLL 最低、背诵率仍接近零的检查点。需要连接子或 R 基团？换生成器，而不是再加 epoch。课程学习改的是奖励日程，TL 改的是起始分布。两者可以组合。",
            "sub_en": "Stop on val NLL. TL ≠ curriculum.",
            "sub_zh": "按验证 NLL 停训。TL 不是课程学习。",
            "shot": "Decision table", "on_screen": "keep / stop / switch generator",
            "asset_type": "diagram",
        },
        {
            "id": "cta", "tc": "3:35–4:00", "start_sec": 215, "end_sec": 240,
            "label_en": "CTA", "label_zh": "结尾",
            "narration_en": "Curves, CSVs, and configs are on the AI Drug Discovery Lab site. Code is on GitHub. Next: Tutorial 08 — put a docking oracle in the loop.",
            "narration_zh": "曲线、CSV 和配置在 AI Drug Discovery Lab 网站。代码在 GitHub。下一集教程 08：把对接 oracle 放进循环。",
            "sub_en": "Site and GitHub. Next: docking-guided design.",
            "sub_zh": "网站与 GitHub。下一集：对接引导设计。",
            "shot": "CTA", "on_screen": "Site → GitHub → Tutorial 08",
            "asset_type": "cta_card",
        },
    ]
    return {
        "slug": "07-transfer-learning",
        "title_en": "REINVENT4 Tutorial 07: Stop TL Before It Memorizes",
        "title_zh": "REINVENT4 教程 07：在背诵训练集之前停下 TL",
        "duration": 240, "beats": beats,
        "chapters": [
            {"timecode": "0:00", "title": "Eight epochs was a taste"},
            {"timecode": "0:12", "title": "The stop rule"},
            {"timecode": "0:50", "title": "Overfitting on 145 SMILES"},
            {"timecode": "2:10", "title": "TL then RL vs RL-only"},
            {"timecode": "3:10", "title": "What to keep"},
            {"timecode": "3:35", "title": "Site and GitHub"},
        ],
        "blurb_en": "40-epoch sulfonamide TL: best val NLL at epoch 8; epoch 40 memorizes 40%. TL then RL beats RL-only under the same reward.",
        "blurb_zh": "磺酰胺 40 epoch TL：最佳验证 NLL 在第 8 轮；第 40 轮背出 40%。同一奖励下 TL 再 RL 优于纯 RL。",
        "thumb_title": "Don't pick last epoch",
        "thumb_prompt": "A training curve smiling then eating its own molecules, dark teal, empty top for title Don't pick last epoch.",
        "metrics_title": "Tutorial 07 — TL then RL",
        "metrics_rows": [
            ("Best validation NLL", "epoch 8"),
            ("Sulfonamide %  ep0 / ep8 / ep40", "8.4 / 64.3 / 86.1"),
            ("Exact train SMILES ep40", "40%"),
            ("TL→RL vs RL-only last-5 Score", "0.847 vs 0.775"),
        ],
        "pipeline_title": "Adapt the start",
        "pipeline_boxes": [
            ("02 Short TL", "enrich motif", False),
            ("07 Long TL", "this episode", True),
            ("04/08 RL", "use the checkpoint", False),
        ],
        "copy_images": [
            ("07/tl-overfit-curve.png", "tl-overfit-curve.png"),
            ("07/tl-vs-rl-compare.png", "tl-vs-rl-compare.png"),
            ("07/tl-ep24-molecules.png", "tl-ep24-molecules.png"),
        ],
        "slideshow": [
            {"id": "hook", "start_sec": 0, "end_sec": 12, "image": "assets/ai/hook.png", "fallback": "assets/pipeline.png"},
            {"id": "problem", "start_sec": 12, "end_sec": 50, "image": "assets/pipeline.png", "fallback": "assets/pipeline.png"},
            {"id": "proof_tl", "start_sec": 50, "end_sec": 130, "image": "assets/tl-overfit-curve.png", "fallback": "assets/metrics-callout.png"},
            {"id": "proof_rl", "start_sec": 130, "end_sec": 175, "image": "assets/tl-vs-rl-compare.png", "fallback": "assets/metrics-callout.png"},
            {"id": "mols", "start_sec": 175, "end_sec": 190, "image": "assets/tl-ep24-molecules.png", "fallback": "assets/metrics-callout.png"},
            {"id": "decision", "start_sec": 190, "end_sec": 215, "image": "assets/metrics-callout.png", "fallback": "assets/pipeline.png"},
            {"id": "cta", "start_sec": 215, "end_sec": 240, "image": "assets/ai/cta.png", "fallback": "assets/pipeline.png"},
        ],
        "ai_images": [
            ai("hook", "A small SMILES list being photocopied by a neural net, warning triangle."),
            ai("cta", "End-card molecular network, empty center for Site and GitHub."),
            ai("thumbnail", "YouTube thumbnail, epoch dial past a green zone into red memorize, empty top for title."),
        ],
        "tags": COMMON_TAGS + ["transfer learning", "overfitting"],
        "broll": broll(
            ("tl-overfit-curve.png", "Stop rule", "chapter figure"),
            ("tl-vs-rl-compare.png", "Campaign A/B", "chapter figure"),
        ),
    }


def spec_08() -> dict:
    beats = [
        {
            "id": "hook", "tc": "0:00–0:12", "start_sec": 0, "end_sec": 12,
            "label_en": "Hook", "label_zh": "开场",
            "narration_en": "A high QED molecule can sit nowhere near the pocket. This episode puts a structure-based oracle into the generation loop — not a Vina command-line class.",
            "narration_zh": "QED 很高的分子也可能离口袋八丈远。这一集把基于结构的 oracle 放进生成循环——不是 Vina 命令行课。",
            "sub_en": "QED is not a pose. Design loop, not a CLI.",
            "sub_zh": "QED 不是构象。这是设计循环，不是命令行。",
            "shot": "Pocket vs pretty molecule", "on_screen": "Worth docking?",
            "asset_type": "title_card",
        },
        {
            "id": "loop", "tc": "0:12–0:55", "start_sec": 12, "end_sec": 55,
            "label_en": "Design loop", "label_zh": "设计循环",
            "narration_en": "Pocket prep, then a scoring component, then a short generation, then pose sanity checks. DockStream is marked superseded. We use AutoDock Vina through REINVENT ExternalProcess so you can see every byte on the wire. Ligands via meeko. Receptor via Open Babel. Public pocket: PDB 1IEP, Abl plus imatinib.",
            "narration_zh": "先准备口袋，再接评分组件，再短生成，再审查构象。DockStream 已标过时。我们用 ExternalProcess 调 AutoDock Vina，线上每个字节都看得见。配体用 meeko，受体用 Open Babel。公开口袋：PDB 1IEP，Abl 加伊马替尼。",
            "sub_en": "Pocket → ExternalProcess Vina → poses.",
            "sub_zh": "口袋 → ExternalProcess Vina → 构象。",
            "shot": "Loop diagram", "on_screen": "1IEP · ExternalProcess",
            "asset_type": "diagram",
        },
        {
            "id": "oracle", "tc": "0:55–1:40", "start_sec": 55, "end_sec": 100,
            "label_en": "Debug the oracle", "label_zh": "先调试 oracle",
            "narration_en": "Same discipline as Tutorial 03: run_type scoring before RL. Geometric mean of QED weight 0.3 and Vina weight 1. Reverse sigmoid maps about minus 5 to minus 12 kilocalories into zero to one. Exhaustiveness 1 is a smoke test. Production uses higher exhaustiveness, diversity filters, and queues.",
            "narration_zh": "和教程 03 一样：先 run_type scoring 再 RL。几何平均：QED 权重 0.3，Vina 权重 1。reverse sigmoid 把大约 -5 到 -12 千卡映射到 0 到 1。exhaustiveness 1 只是冒烟。生产要用更高搜索、多样性过滤和队列。",
            "sub_en": "Score the oracle before RL. exh=1 is a smoke test.",
            "sub_zh": "先给 oracle 打分再 RL。exh=1 只是冒烟。",
            "shot": "Transform card", "on_screen": "reverse_sigmoid −5 to −12",
            "asset_type": "diagram",
        },
        {
            "id": "proof", "tc": "1:40–2:55", "start_sec": 100, "end_sec": 175,
            "label_en": "Proof", "label_zh": "证据",
            "narration_en": "Seed 42 prior pool: 37 unique SMILES. Vina raw from minus 12.1 to minus 4.6. About 199 seconds. Imatinib in the same box at exhaustiveness 1 is about minus 9.4. The best raw dock can have low QED — geometric mean is allowed to disagree. Short RL, five steps times batch 8, about 123 seconds, is noisy on purpose. It proves the loop runs. It does not prove a hit series.",
            "narration_zh": "种子 42 的先验池：37 个唯一 SMILES。Vina 原始分从 -12.1 到 -4.6。大约 199 秒。同一盒子里 exhaustiveness 1 的伊马替尼大约 -9.4。原始对接最好的分子 QED 可以很低——几何平均允许不同意。短 RL：5 步乘 batch 8，大约 123 秒，噪声是故意的。它证明回路通了，不证明你有苗头系列。",
            "sub_en": "Pool −12.1 to −4.6. Short RL is loop proof only.",
            "sub_zh": "池子 -12.1 到 -4.6。短 RL 只证明回路。",
            "shot": "docking-score-dist.png", "on_screen": "n=37 · exh=1",
            "asset_type": "diagram",
        },
        {
            "id": "poses", "tc": "2:55–3:35", "start_sec": 175, "end_sec": 215,
            "label_en": "When docking lies", "label_zh": "对接何时说谎",
            "narration_en": "Wrong box, low exhaustiveness, bad tautomer, wrong protein chain — affinities look great and poses are nonsense. Always open top PDBQTs on the receptor. Scoring 0.0 often means embed or Vina failed. Keep QED or alerts so you do not invent greasy bricks.",
            "narration_zh": "盒子错、exhaustiveness 太低、互变异构不对、蛋白链不对——亲和力很好看，构象是胡说。一定要把顶部 PDBQT 叠在受体上看。Score 0.0 常常是 3D 嵌入或 Vina 失败。保留 QED 或 alerts，免得发明一堆油腻砖头。",
            "sub_en": "Affinity is not a pose validator.",
            "sub_zh": "亲和力不能代替构象审查。",
            "shot": "top-docked-molecules.png", "on_screen": "Inspect poses",
            "asset_type": "molecule_anim",
        },
        {
            "id": "cta", "tc": "3:35–4:00", "start_sec": 215, "end_sec": 240,
            "label_en": "CTA", "label_zh": "结尾",
            "narration_en": "Pocket files, the ExternalProcess script, and CSVs are on the AI Drug Discovery Lab site. Code is on GitHub. Next: Tutorial 09 — scale and monitor expensive oracles.",
            "narration_zh": "口袋文件、ExternalProcess 脚本和 CSV 在 AI Drug Discovery Lab 网站。代码在 GitHub。下一集教程 09：给昂贵 oracle 扩规模和监控。",
            "sub_en": "Site and GitHub. Next: scale and monitor.",
            "sub_zh": "网站与 GitHub。下一集：扩规模与监控。",
            "shot": "CTA", "on_screen": "Site → GitHub → Tutorial 09",
            "asset_type": "cta_card",
        },
    ]
    return {
        "slug": "08-docking-guided-design",
        "title_en": "REINVENT4 Tutorial 08: Docking in the Loop — Not a Vina Class",
        "title_zh": "REINVENT4 教程 08：把对接放进循环，而不是上一堂 Vina 课",
        "duration": 240, "beats": beats,
        "chapters": [
            {"timecode": "0:00", "title": "QED is not a pose"},
            {"timecode": "0:12", "title": "The design loop"},
            {"timecode": "0:55", "title": "Debug the oracle first"},
            {"timecode": "1:40", "title": "Pool scores and honest RL"},
            {"timecode": "2:55", "title": "When docking misleads"},
            {"timecode": "3:35", "title": "Site and GitHub"},
        ],
        "blurb_en": "PDB 1IEP + ExternalProcess Vina: score a prior pool (−12.1 to −4.6), run a short docking RL smoke test, and inspect poses.",
        "blurb_zh": "PDB 1IEP + ExternalProcess Vina：给先验池打分（-12.1 到 -4.6），跑短对接 RL 冒烟，并审查构象。",
        "thumb_title": "Dock the generator",
        "thumb_prompt": "A generative molecule being lowered into a protein pocket like a key, dark teal, empty top for title Dock the generator.",
        "metrics_title": "Tutorial 08 — docking loop",
        "metrics_rows": [
            ("Pocket", "PDB 1IEP chain A"),
            ("Pool Vina raw", "−12.1 to −4.6 kcal/mol"),
            ("Imatinib demo (exh=1)", "~ −9.4 kcal/mol"),
            ("Score pool / short RL", "~199 s / ~123 s"),
        ],
        "pipeline_title": "Structure enters the loop",
        "pipeline_boxes": [
            ("03/04 Score+RL", "fast properties", False),
            ("08 Dock", "this episode", True),
            ("09 Scale", "expensive oracles", False),
        ],
        "copy_images": [
            ("08/docking-score-dist.png", "docking-score-dist.png"),
            ("08/top-docked-molecules.png", "top-docked-molecules.png"),
        ],
        "slideshow": [
            {"id": "hook", "start_sec": 0, "end_sec": 12, "image": "assets/ai/hook.png", "fallback": "assets/pipeline.png"},
            {"id": "loop", "start_sec": 12, "end_sec": 55, "image": "assets/pipeline.png", "fallback": "assets/pipeline.png"},
            {"id": "oracle", "start_sec": 55, "end_sec": 100, "image": "assets/ai/mental-model.png", "fallback": "assets/metrics-callout.png"},
            {"id": "proof", "start_sec": 100, "end_sec": 155, "image": "assets/docking-score-dist.png", "fallback": "assets/metrics-callout.png"},
            {"id": "mols", "start_sec": 155, "end_sec": 175, "image": "assets/top-docked-molecules.png", "fallback": "assets/metrics-callout.png"},
            {"id": "poses", "start_sec": 175, "end_sec": 215, "image": "assets/metrics-callout.png", "fallback": "assets/pipeline.png"},
            {"id": "cta", "start_sec": 215, "end_sec": 240, "image": "assets/ai/cta.png", "fallback": "assets/pipeline.png"},
        ],
        "ai_images": [
            ai("hook", "A beautiful drug-like molecule floating far outside a protein pocket, caution motif."),
            ai("mental-model", "Four-step loop icons: pocket, JSON scores, generator, pose inspection."),
            ai("cta", "End-card molecular network, empty center for Site and GitHub."),
            ai("thumbnail", "YouTube thumbnail, molecule docking into Abl pocket, empty top for title."),
        ],
        "tags": COMMON_TAGS + ["molecular docking", "AutoDock Vina", "structure-based design"],
        "broll": broll(
            ("docking-score-dist.png", "Oracle distribution", "chapter figure"),
            ("vina_external.py JSON", "Show the contract", "optional screencast"),
            ("PyMOL pose later", "User inserts in 剪映", "top PDBQT"),
        ),
    }


def write_pack_02_slideshow() -> None:
    """02 already has a text pack; add slideshow + Imagine prompts if missing."""
    dest = PACKS / "02-priors-in-practice"
    assets = dest / "assets"
    ai_dir = assets / "ai"
    ai_dir.mkdir(parents=True, exist_ok=True)
    if not (assets / "metrics-callout.png").is_file() and (assets / "metrics-callout.svg").is_file():
        svg_to_png(assets / "metrics-callout.svg", assets / "metrics-callout.png")
    if not (assets / "decision-table.png").is_file() and (assets / "decision-table.svg").is_file():
        svg_to_png(assets / "decision-table.svg", assets / "decision-table.png")
    prompts = {
        "model_preference": ["grok-imagine-image-quality"],
        "aspect_ratio": "16:9",
        "images": [
            ai("hook", "A download arrow labeled prior versus a scientist asking will this cover my chemistry."),
            ai("mental-model", "Same generator architecture, two weight sets: PubChem vs sulfonamide TL."),
            ai("cta", "End-card molecular network, empty center for Site and GitHub."),
            ai("thumbnail", "YouTube thumbnail, 8 percent versus 64 percent motif, empty top for title. No fake axes."),
        ],
    }
    (ai_dir / "prompts.json").write_text(json.dumps(prompts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    slideshow = {
        "slug": "02-priors-in-practice",
        "audio": "youtube/audio/02-priors-in-practice/en.mp3",
        "subtitles": "youtube/packs/02-priors-in-practice/subtitles-en.srt",
        "width": 1920,
        "height": 1080,
        "fade_sec": 0.25,
        "segments": [
            {"id": "hook", "start_sec": 0, "end_sec": 15, "image": "assets/ai/hook.png", "fallback": "assets/metrics-callout.png"},
            {"id": "problem", "start_sec": 15, "end_sec": 55, "image": "assets/ai/mental-model.png", "fallback": "assets/decision-table.png"},
            {"id": "protocol", "start_sec": 55, "end_sec": 110, "image": "assets/metrics-callout.png", "fallback": "assets/metrics-callout.png"},
            {"id": "compare", "start_sec": 110, "end_sec": 150, "image": "assets/prior-vs-tl-compare.png", "fallback": "assets/metrics-callout.png"},
            {"id": "prior_mols", "start_sec": 150, "end_sec": 175, "image": "assets/prior-sample-molecules.png", "fallback": "assets/metrics-callout.png"},
            {"id": "tl_mols", "start_sec": 175, "end_sec": 200, "image": "assets/tl-sample-molecules.png", "fallback": "assets/metrics-callout.png"},
            {"id": "decide", "start_sec": 200, "end_sec": 235, "image": "assets/decision-table.png", "fallback": "assets/metrics-callout.png"},
            {"id": "cta", "start_sec": 235, "end_sec": 270, "image": "assets/ai/cta.png", "fallback": "assets/metrics-callout.png"},
        ],
    }
    (dest / "slideshow.json").write_text(json.dumps(slideshow, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    produce = dest / "PRODUCE.md"
    extra = """
## xAI production (this run)

```bash
python scripts/youtube/images_xai.py 02
python scripts/youtube/tts_xai.py 02 --lang both
python scripts/youtube/render_slideshow.py 02
```

Target cut: 3–5 minutes. Insert live terminal later in 剪映 if desired.
"""
    if produce.is_file():
        text = produce.read_text(encoding="utf-8")
        if "images_xai.py 02" not in text:
            produce.write_text(text.rstrip() + "\n" + extra, encoding="utf-8")
    print(f"Updated slideshow for {dest.name}")


def write_pack_03_produce_note() -> None:
    dest = PACKS / "03-scoring-function"
    produce = dest / "PRODUCE.md"
    extra = """
## Re-render this environment

```bash
python scripts/youtube/images_xai.py 03
python scripts/youtube/tts_xai.py 03 --lang both
python scripts/youtube/render_slideshow.py 03
```
"""
    if produce.is_file() and "tts_xai.py 03 --lang both" not in produce.read_text(encoding="utf-8"):
        produce.write_text(produce.read_text(encoding="utf-8").rstrip() + "\n" + extra, encoding="utf-8")


def main() -> int:
    sudo = shutil.which("rsvg-convert")
    if not sudo:
        print("Note: rsvg-convert missing; SVG rasterization may use matplotlib fallback.")
    specs = [spec_01(), spec_04(), spec_05(), spec_06(), spec_07(), spec_08()]
    for spec in specs:
        dest = materialize(spec)
        print(f"Wrote pack {dest}")
    write_pack_02_slideshow()
    write_pack_03_produce_note()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
