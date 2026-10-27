# 怎么工作 — HITL 宪法

本 Lab 是一人 HITL 药物发现「公司」的**操作手册**。执行在 [reinvent-agent](https://github.com/Luzuokun/reinvent-agent)。工位 = 独立 tool 包 + 人批闸门，不是一群互相聊天的 Agent。

## 角色

| 角色 | 职责 |
|------|------|
| **你（PI）** | 批协议、签科学声称、选下一刀 |
| **工作台工具** | 文献 / 生成 / 对接 / MD / 分析 — 各有 `--approve-*` |
| **Critic** | 只基于证据攻击结论；禁止编造 PMID 或分数 |
| **本手册** | 教战役路径（尤其 REINVENT4）并写清闸门 |

## 必须人批

- 新靶点、新蛋白结构、新 prior、新打分函数、新实验预设
- 第一次 GPU 作业、对接盒子、生产时长 MD / 自由能协议
- 对外结论：湿实验建议、论文级声称、外发战役摘要
- Critic `FAIL`；或意味着改实验策略的 `WARNING`
- shortlist 进入「值得合成 / 值得买」

**批准的是协议，不是每一次点击。**

## 协议已批后可自动

- 已批准预设上的重复采样、分析、报告（`--from-run`）
- 同一受体、盒子已批后的批量对接
- Critic `PASS` 后继续机械步（保留一页摘要）
- allowlist 上的 MCP / CLI 只读检查与离线分析

## 模型永不可做

- 写 / 改 `reinvent.toml` 或整份 `.mdp`
- 任意 shell、自循环改参、自动写论文
- 无出处「文献表明」
- 把 demo / 夹具分数说成科学发现

## 流水线主轴

```text
文献 → 生成（REINVENT4）→ 结构 → 动力学 → Critic → 你签字
```

从 [工作台](stations/index.md) 进入。课程深度：[REINVENT4](molecular-generation/reinvent4/index.md)。执行仓：[reinvent-agent](https://github.com/Luzuokun/reinvent-agent)。
