# REINVENT4 教程（10）：消融与超参数

!!! note "英文正文已发布"
    完整可复现实操见英文版
    [Tutorial 10 — Ablations & Hyperparameters](../../../molecular-generation/reinvent4/10-ablations-and-hyperparameters.md)。
    中文翻译将随后跟进。本章验收大纲保留如下。

!!! abstract "REINVENT4 课程第 10 章"
    一次只改一个变量 —— σ、batch、步数 —— 并公开*你们自己的*对照表。

## 本章必须交付

1. 以 Tutorial 04 为基线；在固定 seed 预算下对 `sigma`（或 `batch_size`）做 ≥3 档消融。
1. 列表平均 Score、有效率、独特骨架；给学习者一个默认推荐。
1. 写明下一步*不会*调什么（以及为什么）。

## 不在范围内（API 文档陷阱）

只复述 PARAMS.md 默认值、没有实测结果，不算本章。

## 状态

**已发布（英文）。** 前置：见[课程大纲](index.md)。遵循贡献指南：科研实践，不是 API 文档；
Every tutorial is reproducible.

---

**下一章：** [教程 11 — 案例：BRAF](11-case-study-braf.md)
