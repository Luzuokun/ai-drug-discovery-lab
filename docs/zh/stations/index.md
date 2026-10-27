# 工作台工位

六个工位，各做一件事。已接线工具标注 reinvent-agent 稳定 `tool_id`；未接线百科页在 [附录](../appendix/index.md)。

| 工位 | 职责 | Agent 侧 |
|------|------|----------|
| [文献 Research](research.md) | 带出处的文献与公开数据 | `literature` · `--approve-literature` |
| [生成 Chemistry](chemistry.md) | 生成 / TL / 过滤 | `run_reinvent` · 预设 · REINVENT4 课 |
| [结构 Structure](structure.md) | 对接与口袋盒子 | `docking` · `--approve-dock` |
| [动力学 Dynamics](dynamics.md) | 短 MD / 协议包 | `md` / `md_carb` |
| [批判 Critic](critic.md) | 攻击结论 | `critic_review`（仅证据） |
| [你 You（PI）](you.md) | 批准、签字、选下一刀 | `--approve-*` · `--from-run` · HTML |

```text
文献 → 生成 → 结构 → 动力学 → Critic → 你签字
```

手册主轴：Chemistry 下的 [REINVENT4 十二章](../molecular-generation/reinvent4/index.md)，以及 [战役案例](../campaigns/index.md)。
