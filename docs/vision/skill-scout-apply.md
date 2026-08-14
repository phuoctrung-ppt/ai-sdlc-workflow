# Skill Scout — Post-approve APPLY protocol

**Status:** experiment on `experiment/repo-trust-rubric`

Human approve is the only gate between “research” and “agents can auto-load this skill”.

```text
/skill-scout  →  shortlist + proposal  PENDING_APPROVAL
                      ↓ human APPROVE
/skill-scout-apply → write files + manifest + (optional) memory
                      ↓
context-builder / skill-loader match phases+agents+keywords → worker loads skill
```

---

## Why manifest must be updated

Load path (v2):

1. `context-builder.py` (or legacy `skill-loader.py`) reads `.cursor/skills/skills-manifest.v2.json`
2. Filters by **phase** ∈ skill.phases
3. Scores by **keywords** ∩ task terms (+ boost if **agent** ∈ skill.agents)
4. Returns `entry` path only — agent reads that `SKILL.md`

If you only write `.cursor/skills/foo/SKILL.md` and **skip manifest**, the skill is invisible to auto-load.

---

## APPLY checklist (after APPROVE)

### 1. Write skill files (thin)

| Path | Rule |
|------|------|
| `.cursor/skills/{id}/SKILL.md` | Entry ≤ ~800–1500 tokens; hard rules + when-to-use |
| `.cursor/skills/{id}/references/*` | Optional; lazy — only when needed |
| Attribution | Source URL + SPDX license in SKILL footer or `NOTICE` |

**Do not** dump full upstream README into entry.

### 2. Register manifest entry

Append to `skills` (or `portableSkills` if truly domain-agnostic) in `skills-manifest.v2.json`:

```json
{
  "id": "{kebab-id}",
  "portable": true,
  "note": "Ingested via skill-scout; source: {owner/repo}",
  "entry": "{id}/SKILL.md",
  "referencesDir": "{id}/references",
  "phases": ["…"],
  "agents": ["…"],
  "keywords": ["…"],
  "manifestSchema": "2.0",
  "priority": 6,
  "estimatedTokens": 800
}
```

| Field | How to choose |
|-------|----------------|
| **phases** | Where the craft runs (e.g. pytest → `test`, `fix`, `implement-backend`) |
| **agents** | Who should see it (e.g. `qa-worker`, `backend-worker`) |
| **keywords** | Task tokens that should trigger load (stack + practice nouns) |
| **priority** | Default **6–10** for scout-ingested; raise only after proven useful |
| **estimatedTokens** | Rough size of entry only |

Bump manifest `version` note (e.g. `_note`) when batch-applying.

### 3. Optional — memory / proposal status

- Mark proposal `APPLIED` + date in `docs/reviews/…-skill-scout-proposal.md`
- 1–3 lines in `docs/memory/decisions.md` or `shortcuts.md` if durable
- Do **not** hand-edit `workflow-state.json`

### 4. Verify load map

```bash
python3 .cursor/context/context-builder.py \
  --phase test \
  --task "write pytest unit tests for service layer" \
  --agent qa-worker \
  --keywords "pytest,unit,test" \
  --budget 4000
```

Expect new skill `id` in matched skills when phase/keywords align.

Legacy check:

```bash
python3 .cursor/skills/scripts/skill-loader.py \
  --phase test \
  --task "pytest service" \
  --keywords "pytest,test" \
  --agent qa-worker
```

---

## What NOT to touch on apply

| Item | Reason |
|------|--------|
| Day-path `/fix`, `/shape-lite` | Scout stays optional |
| `agent-matrix.json` workers for product loops | Only if a **new agent** is required (rare) |
| Auto-raise priority above core skills | Avoid crowding error-recovery / planning |
| Copy entire upstream tree into skills | Bloat + license risk |

---

## Merge vs new skill

| Situation | Action |
|-----------|--------|
| New domain (e.g. `python-pytest`) | **New** id + manifest row |
| Extends existing (e.g. more Playwright patterns) | Patch existing `SKILL.md` / references + refresh keywords if needed |
| Conflicts with existing rule | Proposal must call it out; human chooses override |

---

## Commands

| Command | Role |
|---------|------|
| `/skill-scout` | Research + rubric + proposal `PENDING_APPROVAL` only |
| `/skill-scout-apply` | **Only after** explicit human APPROVE on a proposal path |

Apply without APPROVE line in the task → **refuse**.
