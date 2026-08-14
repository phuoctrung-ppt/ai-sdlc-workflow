---
name: skill-scout-apply
description: After human APPROVE on a skill-scout proposal — write thin skill files, register skills-manifest.v2.json load map, verify match. Refuse if not approved.
---

# Skill Scout Apply

Act as **Orchestrator**. Runs **only** when the user explicitly approved a scout proposal.

## Preconditions

- Proposal path given (e.g. `docs/reviews/2026-08-14-skill-scout-proposal.md`)
- Proposal contains **`APPROVED`** (or task text says `approve` / `APPROVE` for that file)
- If status is still `PENDING_APPROVAL` only → **refuse** and ask for explicit approve

## Steps

1. Read proposal + `docs/vision/skill-scout-apply.md`.

2. Write thin skill:
   - `.cursor/skills/{id}/SKILL.md` (entry only; portable rules)
   - Optional `references/` for long material
   - Attribution + license from proposal

3. Update `.cursor/skills/skills-manifest.v2.json`:
   - Append skill object with **phases**, **agents**, **keywords**, **priority**, **entry**, **estimatedTokens**
   - These four filters are what make `context-builder` / loaders auto-select the skill
   - Default priority **6–10** unless proposal says otherwise and human agreed

4. Mark proposal `APPLIED` + date. Optional 1–3 lines in `docs/memory/decisions.md`.

5. Verify:

```bash
python3 .cursor/context/context-builder.py \
  --phase <proposed-phase> \
  --task "<sample task using new keywords>" \
  --agent <proposed-agent> \
  --keywords "<keywords from manifest entry>" \
  --budget 4000
```

Confirm new `id` appears in matched skills.

6. Report: paths written, manifest fields, verify result.

## Forbidden

- Apply without APPROVE
- Always-on / matrix changes unless human asked for a new agent
- Inflating priority above planning/error-recovery without ask
- Bulk-copy upstream repo into skills tree
