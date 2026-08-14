---
name: skill-scout-apply
description: After human APPROVE on a skill-scout proposal — write thin skill, register manifest load map (manifest-register.py), positive+negative verify. Refuse if not approved.
---

# Skill Scout Apply

Act as **Orchestrator**. **Only** after explicit APPROVE on a scout proposal.

## Preconditions

- Proposal path provided
- Frontmatter `status: APPROVED` **or** task explicitly approves that file
- Else **refuse**

## Steps

1. Read proposal, `docs/vision/skill-scout-apply.md`, `docs/vision/skill-scout-best-practices.md`.

2. Write thin skill files under `.cursor/skills/{id}/` (entry + optional references + attribution).

3. Register load map with validation:

```bash
python3 .cursor/skills/scripts/manifest-register.py --dry-run \
  --id "{id}" \
  --entry "{id}/SKILL.md" \
  --phases "{comma phases}" \
  --agents "{comma agents}" \
  --keywords "{comma keywords}" \
  --priority {6-10} \
  --estimated-tokens {n} \
  --note "Ingested via skill-scout; source: …"
```

On OK, re-run **without** `--dry-run` (add `--replace` only when merging/updating same id).

4. Mark proposal `status: APPLIED` + `applied_at`. Optional 1–3 lines in `docs/memory/decisions.md`.

5. **Positive verify** — expect skill id in matches:

```bash
python3 .cursor/context/context-builder.py \
  --phase {phase} \
  --task "{sample task}" \
  --agent {agent} \
  --keywords "{keywords}" \
  --budget 4000
```

6. **Negative verify** — wrong phase/agent should **not** rank this skill on top (tighten keywords if it does).

7. Report paths, manifest fields, verify results.

## Forbidden

- Apply without APPROVE
- `--force-priority` unless human asked
- Day-path / matrix changes
- Upstream tree copy into skills
