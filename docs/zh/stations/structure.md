# 结构 Structure 工位

**职责：** 可审计、可复用的对接与口袋盒子。

| | |
|-|-|
| **tool_id** | `docking` |
| **闸门** | `--approve-dock` |
| **主线引擎** | AutoDock Vina、GNINA |
| **附录** | [Smina](../docking/smina.md)（不占产品柱） |

## 你要批准什么

- 受体文件与对接盒子（中心 / 尺寸）
- 新靶点上的第一次 GPU 对接
- 任何把某个 pose 说成「结合模式」并进湿实验的声称

## 页面

- [AutoDock Vina](../docking/autodock-vina.md)
- [Gnina](../docking/gnina.md)
- 课程桥：[REINVENT4 · 08 对接引导设计](../molecular-generation/reinvent4/08-docking-guided-design.md)

Vina/GNINA 章节正文仍薄；**已接线**路径是 reinvent-agent `tools.docking`。禁止自动发明结合位点——盒子必须人定。
