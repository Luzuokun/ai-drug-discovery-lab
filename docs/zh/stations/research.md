# 文献 Research 工位

**职责：** 把带出处的文献与公开数据带进战役——要 provenance，不要「感觉」。

| | |
|-|-|
| **tool_id** | `literature` |
| **闸门** | `--approve-literature` |
| **输出** | `<project>/output/literature/` |
| **不是** | planner/MCP 写论文步骤；编造 PMID |

## 你要做的事

1. 自己写 PubMed 检索式。
2. 批准一次文献拉取。
3. 只保留带 URL 和/或 PMID（或 DOI）的条目。
4. 交给 Critic 的 evidence JSON 必须已带出处——Critic 不得再发明文献。

## 手册链接

- 战役阅读：[战役案例](../campaigns/index.md)
- Agent 对照表：在 [reinvent-agent](https://github.com/Luzuokun/reinvent-agent) 运行 `python -m tools.handbook_map`

!!! note "Assay / ChEMBL"
    预定义 ChEMBL 下载 + `smiles_prep` 是路线图 Phase D 的 Assay 工位。此前 assay CSV 仍由人手整理。
