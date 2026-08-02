# REINVENT4 教程 02 — Prior 是实验选择——用数据证明

目标时长：约 8:00

## [0:00–0:15 开场]
教程 01 给了你 reinvent_pubchem.prior。下载它不是研究决策。这一期才是。

## [0:15–1:15 覆盖你的化学吗？]
实验室要问：生成起点覆盖你关心的化学吗？磺酰胺 / 大环 / 肽 / 共价 warhead 若在 prior 里极稀，RL 会浪费前期算力。

## [1:15–2:20 公平 A/B]
不同 Zenodo 文件可能是不同生成器。固定 Reinvent，只换权重：prior vs tl_sulfonamide.model（磺酰胺上 8 epoch TL）。

## [2:20–3:50 同一协议]
CPU、seed 42、约 200 SMILES、unique_molecules。只改 model_file。演示 TL ≈13 s / ~871 MiB。去重后 191 vs 196 行。

## [3:50–5:30 数字]
S(=O)(=O)N：8.4% → 64.3%。Murcko：168 vs 172。QED 0.59 → 0.65（副作用）。

## [5:30–6:45 决策表]
Prior 够用 → 教程 03；TL 有效 → 用作 RL 起点；要连接子/R 基/种子类似物 → 换生成器。

## [6:45–8:00 CTA]
对比→度量→决策→再 RL。网站完整教程 + GitHub 代码。
