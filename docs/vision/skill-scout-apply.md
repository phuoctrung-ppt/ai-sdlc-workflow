# Skill Scout — Post-approve APPLY protocol

**Status:** experiment on `experiment/repo-trust-rubric`

Human approve is the only gate between research and auto-load.

```text
/skill-scout  →  proposal PENDING_APPROVAL (+ load-map draft)
                      ↓ human APPROVE
/skill-scout-apply → SKILL.md + manifest-register.py + verify
                      ↓
context-builder matches phases + agents + keywords → worker loads entry
```

Also read: `docs/vision/skill-scout-best-practices.md`, template `docs/reviews/_templates/skill-scout-proposal.md`.

---

## Why manifest must be updated

1. `context-builder.py` reads `skills-manifest.v2.json`
2. Filter: phase ∈ skill.phases
3. Score: keywords ∩ task (+ agent boost)
4. Return `entry` path only

File on disk without manifest row ⇒ **invisible** to auto-load.

---

## APPLY checklist

### 1. Write thin skill

| Path | Rule |
|------|------|
| `.cursor/skills/{id}/SKILL.md` | ≤ ~800–1500 tokens |
| `references/*` | Lazy |
| Attribution | URL + SPDX |

### 2. Register with helper (preferred)

```bash
python3 .cursor/skills/scripts/manifest-register.py --dry-run \
  --id "{id}" --entry "{id}/SKILL.md" \
  --phases "…" --agents "…" --keywords "…" \
  --priority 8 --estimated-tokens 800 \
  --note "Ingested via skill-scout; source: owner/repo"

# then drop --dry-run
```

Helper enforces: known phases/agents, ≥2 keywords, not generic-only, priority ceiling, entry file exists, no silent id clash.

Manual JSON append remains possible but must match the same rules.

### 3. Proposal + memory

- `status: APPLIED`
- Optional `docs/memory/decisions.md` (1–3 lines)
- No raw `workflow-state.json` edits

### 4. Verify (positive + negative)

Positive: expected phase/agent/keywords → id in matched skills.

Negative: unrelated phase (e.g. marketing brainstorm) → skill must not dominate.

---

## Defaults

| Field | Scout default |
|-------|----------------|
| priority | 6–10 |
| portable | true when domain-agnostic |
| phases/agents | execution mapping only |

---

## Commands

| Command | Role |
|---------|------|
| `/skill-scout` | Proposal only |
| `/skill-scout-apply` | After APPROVE |

Refuse apply without APPROVE.
