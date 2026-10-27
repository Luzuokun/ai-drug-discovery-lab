# 动力学 Dynamics 工位

**职责：** 验证构象的短 MD 与协议包——与生成分离。

| | |
|-|-|
| **tool_ids** | `md`, `md_carb` |
| **主线引擎** | GROMACS |
| **附录** | [Amber](../molecular-dynamics/amber.md)（空壳已移出主导航） |
| **不是** | LLM 改整份 `.mdp`；把 2 ns 说成自由能证据 |

## 你要批准什么

- 生产时长 / 自由能协议（与短 demo MD 分开）
- 新的 mdp 标量白名单项
- 多糖 MD 协议包（`md_carb`）

## 页面

- [GROMACS](../molecular-dynamics/gromacs.md)
- Agent：[reinvent-agent](https://github.com/Luzuokun/reinvent-agent) `tools.md` / `tools.md.carb`

长时程 MD 与 MM-PBSA 属 Phase H——独立工具、另行批准。
