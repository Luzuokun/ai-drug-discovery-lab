# REINVENT4 教程 02 — 别信任你没压测过的 Prior

目标时长：约 8:00

## [0:00–0:15 开场]
你下载了 reinvent_pubchem.prior。恭喜——这不等于你已经为你的化学型选对了 prior。

## [0:15–1:10 隐藏假设]
教程 01 给了你可用环境和真正的 sampled.csv。那个 prior 学的是宽分布化学语法。你的项目不是 PubChem。稀有化学型上，模型仍会吐出“有效”SMILES——有效 ≠ 相关。

## [1:10–2:20 Prior / Agent / Vocabulary]
Prior：冻结的预训练大脑。Agent：可训练副本。Vocabulary：prior 内的字母表。本章不训练，只决定从哪颗大脑起步。

## [2:20–3:50 公平对比]
固定 seed、n、device；至少两个 prior（或 prior vs TL checkpoint）。[VERIFY] 配置沿用教程 01，只换 model_file。

## [3:50–5:20 度量]
有效率、独特骨架、性质直方图。要覆盖目标区域，避免骨架塌缩。

## [5:20–6:30 何时别用 PubChem]
分布偏移 / 稀有化学型 / 远离类药均值 → 域内 prior 或教程 07 热启动。

## [6:30–8:00 CTA]
对比→度量→证据决策→再上 RL。网站完整教程 + GitHub 代码。
