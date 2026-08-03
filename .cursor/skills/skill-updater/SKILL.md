---
name: skill-updater
description: Retrospective → pattern → SKILL proposal. Counter via learning-counter.py only.
---

# Skill Updater

## Counter (CLI only)

```bash
python3 .cursor/scripts/learning-counter.py get
```

- `fullPassRecommended: true` or task says full/`/skill-update` → full scan
- else → lightweight
- After proposal: `python3 .cursor/scripts/learning-counter.py reset --proposal <path>`

**Do not** open `.cursor/state/workflow-state.json` in the editor or dump it into context.

## Inputs

1. `docs/retrospective.md`
2. `docs/memory/decisions.md`, `gotchas.md`, `shortcuts.md`
3. Target `SKILL.md` / patterns
4. Optional related `docs/reviews/*`

## Pattern bar

≥2 independent signals (same root cause, repeated Critical class, repeated pattern candidate, …).

## Output

`docs/reviews/YYYY-MM-DD-skill-update-proposal.md` — `PENDING_APPROVAL` — or explicit no-pattern.

Propose, don't apply. Minimal patch. Update `docs/memory/*` when durable.
