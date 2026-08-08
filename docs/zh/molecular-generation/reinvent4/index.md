# REINVENT4

!!! abstract "科研实践课程 —— 不是 API 导览"
    本系列教的是一条**可复现的 REINVENT4 实验链**：采样 → 评分 → 优化 →
    控制失败模式 → 适配数据/oracle → 扩规模 → 在真实靶点上验证。官方文档仍是
    参数手册；本 Lab 回答的是 *跑什么、为什么、如何判断结果*。

**原则：** Every tutorial is reproducible.（固定随机种子、报告资源占用、可下载产物。）

| # | 章节 | 在实验链中的角色 | 状态 |
|---|------|------------------|------|
| 01 | [安装与首个分子](01-installation-first-molecule.md) | 可用环境 + 真实 `sampled.csv` | 已发布（英文） |
| 02 | [Prior 实践](02-priors-in-practice.md) | 为你的化学型选择并验证生成 prior | 已发布（英文） |
| 03 | [评分函数](03-scoring-function.md) | 在烧 RL 步数之前先调通 reward | 已发布（英文） |
| 04 | [强化学习](04-reinforcement-learning.md) | 训练 agent，使高分分子更易被采样 | 已发布（英文） |
| 05 | [多样性过滤器](05-diversity-filter.md) | RL 一旦生效就防止骨架塌缩 | 已发布（英文） |
| 06 | [课程学习](06-curriculum-learning.md) | 分阶段 / checkpoint 升级目标 | 已发布（英文） |
| 07 | [迁移学习](07-transfer-learning.md) | 把 prior 适配到项目化学空间 | 即将推出 |
| 08 | [对接引导设计](08-docking-guided-design.md) | 把基于结构的 oracle 接入生成循环 | 即将推出 |
| 09 | [扩规模与监控](09-scaling-and-monitoring.md) | GPU、日志与 TensorBoard | 即将推出 |
| 10 | [消融与超参数](10-ablations-and-hyperparameters.md) | 单变量实验 + 你们自己的对照表 | 即将推出 |
| 11 | [案例：BRAF](11-case-study-braf.md) | 端到端、论文风格靶点战役 | 即将推出 |
| 12 | [故障排查附录](12-troubleshooting-appendix.md) | 跨章错误、降级边缘话题、FAQ | 即将推出 |

## 阅读路径

```text
01 安装 → 02 Prior（可选深挖） → 03 评分 → 04 RL
    → 05 多样性 → 06 课程学习 → 07 迁移学习
    → 08 对接 oracle → 09 扩规模/监控 → 10 消融 → 11 BRAF 案例
```

若 Tutorial 01 的 prior 已够用，可先跳过 **02**；需要在多个 prior 间选择或诊断
化学域偏移时再回来。

## 刻意不单独成章的内容

属于官方 `PARAMS.md`、站内其他栏目，或短注写在
[教程 12](12-troubleshooting-appendix.md) 的主题：

- 自定义词表、并行采样开关、RDKit 产品式导览
- 单独的 Logging / TensorBoard（并入扩规模与监控）
- 重复的 FAQ / Common Errors（各实操章已有 Common Errors）

## 延伸阅读

- [REINVENT4 仓库](https://github.com/MolecularAI/REINVENT4)
- [贡献指南](https://github.com/Luzuokun/ai-drug-discovery-lab/blob/main/CONTRIBUTING.md) — 科研实践，不是 API 文档
