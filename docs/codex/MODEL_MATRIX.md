# Codex model matrix (per role)

Pinned on branch `adapt/codex-force-design`. Family: **GPT-5.6** (Codex default lineup mid/late 2026).

| Role | Model | Reasoning | Rationale |
|------|--------|-----------|-----------|
| **Main / orchestrator** (`config.toml`) | `gpt-5.6` | `high` | Coordinate, decide, merge subagent summaries |
| `architect_planner` | `gpt-5.6` | `high` | Ambiguous scope, ADR, task graphs |
| `judge` | `gpt-5.6` | `high` | Careful review; false negatives costly |
| `security` | `gpt-5.6` | `high` | Auth/threat reasoning |
| `spike` | `gpt-5.6-terra` | `medium` | Time-boxed PoC, not full design |
| `contract` | `gpt-5.6-terra` | `medium` | Schema design, everyday precision |
| `designer` | `gpt-5.6-terra` | `medium` | Design Contract quality |
| `frontend` | `gpt-5.6-terra` | `medium` | Day-to-day UI implementation |
| `backend` | `gpt-5.6-terra` | `medium` | Day-to-day API implementation |
| `database` | `gpt-5.6-terra` | `medium` | Migrations need care but bounded |
| `scaffold` | `gpt-5.6-luna` | `low` | Boilerplate shells |
| `devops` | `gpt-5.6-luna` | `low` | Compose/CI templates, high volume |
| `qa` | `gpt-5.6-luna` | `low` | Mechanical tests / reports |
| `learning` | `gpt-5.6-luna` | `low` | Draft proposals, not production code |

## Defaults

```toml
# .codex/config.toml
model = "gpt-5.6"
model_reasoning_effort = "high"

[agents]
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "medium"
```

Role TOML `model` / `model_reasoning_effort` override defaults when that role is spawned.

## Fallbacks

If an account lacks a listed id, Codex may map to the nearest available model. Prefer keeping **three tiers** (deep / everyday / fast) even if names change (`gpt-5.5`, `gpt-5.4-mini`, etc.).

## Cost note

Parallel subagents multiply spend. Prefer `luna`/`terra` workers under a single `gpt-5.6` orchestrator; reserve `high` effort for plan, judge, and security.
