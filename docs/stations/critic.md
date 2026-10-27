# Critic station

**Job:** attack conclusions. Never restate numbers as discovery. Never invent evidence.

| | |
|-|-|
| **tool_id** | `critic_review` |
| **Mode** | Deterministic default; optional LLM critic is **evidence-only** |
| **Outputs** | `PASS` / `WARNING` / `FAIL` with red flags |

## Rules

- Comment on literature only when evidence JSON already has cited entries
- Refuse fabricated PMIDs, scores, or “the model found a drug”
- `FAIL` or strategy-changing `WARNING` → human decides next protocol
- `PASS` → mechanical pipeline may continue; keep a one-page summary

## How you read a report

1. Red flags first
2. Top molecules second
3. Protocol identity (`--from-run` / preset ID) third
4. Sign only what you would defend in lab meeting

See [How it works](../how-it-works.md) and [You (PI)](you.md).
