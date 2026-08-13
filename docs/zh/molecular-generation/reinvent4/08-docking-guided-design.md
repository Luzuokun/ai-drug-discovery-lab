# REINVENT4 教程（08）：对接引导设计

!!! note "英文正文已发布"
    完整可复现实操见英文版
    [Tutorial 08 — Docking-Guided Design](../../../molecular-generation/reinvent4/08-docking-guided-design.md)。
    中文翻译将随后跟进。本章验收大纲保留如下。

!!! abstract "REINVENT4 课程第 8 章"
    把基于结构的 oracle 接入生成循环 —— 口袋准备 → 评分组件 → 构象审查。

## 本章必须交付

1. 用有文档的协议准备一个公开口袋 / 共晶配体（交叉链接对接栏目）。
1. 把对接（或类对接组件）接入评分；跑短 RL 或 scoring 批次。
1. 检查构象 / 分数分布；列出对接分何时会误导（错误互变异构、盒子、exhaustiveness）。

## 不在范围内（API 文档陷阱）

这不是 Vina 命令行教程（见对接栏目）。本章的单元是*设计循环*。

## 状态

**已发布（英文）。** 前置：见[课程大纲](index.md)。遵循贡献指南：科研实践，不是 API 文档；
Every tutorial is reproducible.

---

**下一章：** [教程 09 — 扩规模与监控](09-scaling-and-monitoring.md)
