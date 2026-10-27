# 生成 Chemistry 工位

**职责：** de novo 生成、迁移学习、描述符与过滤——全部基于人手写预设。

| | |
|-|-|
| **tool_ids** | `run_reinvent`, `smiles_prep`, `analyze_molecules` |
| **闸门** | `--approve-run`（及相关预设闸门） |
| **主轴** | [REINVENT4 十二章科研实践课](../molecular-generation/reinvent4/index.md) |
| **不是** | LLM 写 `reinvent.toml`；把 DrugEx / MolGPT / GraphGA 当产品柱 |

## 课程路径

```text
01 安装 → 03 评分 → 04 RL → 05 多样性 → 07 TL → 08 对接 oracle → 11 BRAF
```

完整大纲：[REINVENT4](../molecular-generation/reinvent4/index.md)。

## 与 Agent 的约定

- Planner **只选预设 ID**；TOML 由人离线撰写。
- SA / PAINS 与描述符过滤是确定性分析。
- 其他生成器名（DrugEx、MolGPT…）在接线前只进 [附录](../appendix/index.md)。

[:octicons-arrow-right-24: 打开 REINVENT4 课程](../molecular-generation/reinvent4/index.md){ .md-button .md-button--primary }
[:octicons-mark-github-16: reinvent-agent](https://github.com/Luzuokun/reinvent-agent){ .md-button }
