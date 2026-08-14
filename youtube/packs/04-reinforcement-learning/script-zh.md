# REINVENT4 教程 04：强化学习让高分更可能出现

## [0:00–0:12] 开场

评分只给已有分子排队。强化学习会改变生成器接下来吐出什么。这就是教程 03 到 04 的跳跃。

## [0:12–0:48] 问题

药物发现需要更多像好分子的分子，而不是一张静态表。每一步 RL 采样一批、打分、更新 agent，让高分序列更可能出现。Prior 冻结，充当化学语法锚。这就是 DAP。

## [0:48–1:35] 心智模型

即使只有一个阶段，run_type 也是 staged_learning。prior_file 和 agent_file 一开始指向同一个 PubChem prior。评分必须写在 stage.scoring 下，顶层 scoring 会校验失败。这是从教程 03 复制过来的第一陷阱。4.8.24 的 RL 模式不接受 unique_sequences。DAP 的 sigma 128、学习率 1e-4 是手册默认。

## [1:35–2:55] 证据

25 步，batch 64，CPU，种子 42。大约 27 秒，峰值内存约 1.5 GiB。平均 Score 从 0.66 到 0.79。Agent NLL 从 34.79 到 27.15。高于 0.8 的比例从 53% 到 66%。检查点约 23 MB。演示长度不是生产战役——库真要出货时再加大 max_steps。

## [2:55–3:35] 失败模式

分数贴着零？先用 run_type scoring 在固定列表上调试奖励。本章故意不加多样性过滤器，那是教程 05。要续跑，把 agent_file 指到检查点，prior_file 仍用原来的 prior。

## [3:35–4:00] 结尾

完整 TOML、CSV 和 Score 曲线在 AI Drug Discovery Lab 网站。代码在 GitHub。下一集教程 05：RL 一生效就拦住骨架塌缩。
