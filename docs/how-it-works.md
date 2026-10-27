# How it works — HITL constitution

This Lab is the **manual** for a one-person HITL drug-discovery company. Execution lives in [reinvent-agent](https://github.com/Luzuokun/reinvent-agent). Stations are independent tool packages with human gates — not a swarm of chat agents.

## Roles

| Role | Responsibility |
|------|----------------|
| **You (PI)** | Approve protocols, sign scientific claims, pick the next cut |
| **Workbench tools** | Literature, generation, docking, MD, analysis — each with its own `--approve-*` |
| **Critic** | Attack conclusions using evidence only; never invent PMIDs or scores |
| **This handbook** | Teach the campaign path (especially REINVENT4) and document gates |

## Humans must approve

- New target, protein structure, prior, scoring function, or experiment preset
- First GPU job, docking box, production-length MD / free-energy protocol
- External claims: wet-lab advice, paper-level statements, campaign summaries sent outward
- Critic `FAIL`, or `WARNING` that changes experimental strategy
- Shortlist entering “worth synthesizing / buying”

**You approve the protocol, not every click.**

## May run automatically (once the protocol is approved)

- Repeat sampling, analysis, and reporting on an approved preset (`--from-run`)
- Batch docking on the same receptor after the box is approved
- Continue mechanical steps after Critic `PASS` (keep a one-page summary)
- Allowlisted MCP / CLI read-only checks and offline analysis

## Models must never

- Write or edit `reinvent.toml` or a full `.mdp`
- Run arbitrary shell, self-loop parameter search, or auto-write papers
- Invent citations (“literature shows…”) without provenance
- Present demo / fixture scores as scientific discovery

## Pipeline spine

```text
Research → Chemistry (REINVENT4) → Structure → Dynamics → Critic → You
```

Start on the [Workbench](stations/index.md). Campaign depth: [REINVENT4 course](molecular-generation/reinvent4/index.md). Execution repo: [reinvent-agent](https://github.com/Luzuokun/reinvent-agent).
