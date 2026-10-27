# Workbench stations

Six stations. One job each. Wired tools show a stable `tool_id` from [reinvent-agent](https://github.com/Luzuokun/reinvent-agent); unwired encyclopedia pages live in the [Appendix](../appendix/index.md).

| Station | Job | Agent side |
|---------|-----|------------|
| [Research](research.md) | Cited literature & public data | `literature` · `--approve-literature` |
| [Chemistry](chemistry.md) | Generate / TL / filter | `run_reinvent` · presets · REINVENT4 course |
| [Structure](structure.md) | Dock & pocket box | `docking` · `--approve-dock` |
| [Dynamics](dynamics.md) | Short MD / protocol packs | `md` / `md_carb` |
| [Critic](critic.md) | Attack conclusions | `critic_review` (evidence-only) |
| [You (PI)](you.md) | Approve, sign, choose next cut | `--approve-*` · `--from-run` · HTML reports |

```text
Research → Chemistry → Structure → Dynamics → Critic → You
```

Spine of this handbook: the [REINVENT4 12-chapter course](../molecular-generation/reinvent4/index.md) under Chemistry, plus [campaign cases](../campaigns/index.md).
