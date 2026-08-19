# REINVENT4 教程（09）：扩规模与监控

!!! note "英文正文已发布"
    完整可复现实操见英文版
    [Tutorial 09 — Scaling & Monitoring](../../../molecular-generation/reinvent4/09-scaling-and-monitoring.md)。
    中文翻译将随后跟进。本章验收大纲保留如下。

!!! abstract "REINVENT4 课程第 9 章"
    把同一实验搬到 GPU 并盯住它 —— 日志与 TensorBoard 是战役级仪表。

## 本章必须交付

1. 把已知的 CPU RL 配置搬到 GPU；报告墙钟，并核对同 seed 曲线是否一致。
1. 打开 TensorBoard（或等价工具），标注你用来停/续跑的曲线。
1. 并行采样仅在影响本协议吞吐时提及。

## 不在范围内（API 文档陷阱）

单独的「如何打开 TensorBoard」或 CUDA 安装见入门指南。

## 状态

**已发布（英文）。** 前置：见[课程大纲](index.md)。遵循贡献指南：科研实践，不是 API 文档；
Every tutorial is reproducible.

---

**下一章：** [教程 10 — 消融与超参数](10-ablations-and-hyperparameters.md)
