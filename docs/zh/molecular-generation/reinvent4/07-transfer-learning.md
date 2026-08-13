# REINVENT4 教程（07）：迁移学习

!!! note "英文正文已发布"
    完整可复现实操见英文版
    [Tutorial 07 — Transfer Learning](../../../molecular-generation/reinvent4/07-transfer-learning.md)。
    中文翻译将随后跟进。本章验收大纲保留如下。

!!! abstract "REINVENT4 课程第 7 章"
    在长 RL 之前（或并行）把 prior 适配到项目化学空间。

## 本章必须交付

1. 在有文档的小 SMILES 集上微调；报告样本 NLL / 有效率（前后对比）。
1. 在相同评分与 seed 预算下对比 TL→RL vs 纯 RL。
1. 点名过拟合症状（多样性塌缩、背出训练集 SMILES）。

## 不在范围内（API 文档陷阱）

只列 epoch/batch 开关、没有前后对比图，输给官方 TL 示例。

## 状态

**已发布（英文）。** 前置：见[课程大纲](index.md)。遵循贡献指南：科研实践，不是 API 文档；
Every tutorial is reproducible.

---

**下一章：** [教程 08 — 对接引导设计](08-docking-guided-design.md)
