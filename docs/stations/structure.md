# Structure station

**Job:** docking and pocket boxes you can audit and reuse.

| | |
|-|-|
| **tool_id** | `docking` |
| **Gate** | `--approve-dock` |
| **Engines in main path** | AutoDock Vina, GNINA |
| **Appendix** | [Smina](../docking/smina.md) (not a product column) |

## What you approve

- Receptor file and docking box (center / size)
- First GPU docking job on a new target
- Any claim that a pose is “the binding mode” for wet lab

## Pages

- [AutoDock Vina](../docking/autodock-vina.md) — classic score
- [Gnina](../docking/gnina.md) — CNN-enhanced docking
- Course bridge: [REINVENT4 · 08 Docking-Guided Design](../molecular-generation/reinvent4/08-docking-guided-design.md)

Handbook chapter bodies for Vina/GNINA are still thin; the **wired** path today is reinvent-agent `tools.docking`. Pocket auto-invention is out of scope — boxes stay human.
