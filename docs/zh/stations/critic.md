# 批判 Critic 工位

**职责：** 攻击结论。不把数字复述成发现。不发明证据。

| | |
|-|-|
| **tool_id** | `critic_review` |
| **模式** | 默认确定性；可选 LLM Critic **仅看证据** |
| **输出** | `PASS` / `WARNING` / `FAIL` + 红旗 |

## 规则

- 仅当 evidence JSON 已有带出处条目时，才可评论文献
- 拒绝编造 PMID、分数或「模型发现了药」
- `FAIL` 或会改策略的 `WARNING` → 人决定下一协议
- `PASS` → 机械步可继续；保留一页摘要

## 怎么读报告

1. 先看红旗
2. 再看 top 分子
3. 再核协议身份（`--from-run` / 预设 ID）
4. 只签你能在组会上辩护的结论

见 [怎么工作](../how-it-works.md) 与 [你（PI）](you.md)。
