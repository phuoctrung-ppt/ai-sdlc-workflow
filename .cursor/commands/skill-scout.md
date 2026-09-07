---
name: skill-scout
description: Research trusted external best practices; shortlist via repo-trust rubric; write PENDING_APPROVAL proposal only (no skill/manifest write).
---

# Skill Scout

Act as **Orchestrator**. Optional path — **not** day-path (`/fix`, `/shape-lite`).

## Goal

Find trustworthy sources → score with rubric → proposal for human approve. **Do not apply.**

## Steps

1. Read task brief (stack, scope). Prefer project profile in `AGENTS.md` when present.

2. Build context:

```bash
python3 .cursor/context/context-builder.py \
  --phase skill-authoring \
  --task "skill scout external best practices" \
  --agent learning-agent \
  --keywords "skill-scout,best-practices,research,repo-trust,rubric" \
  --budget 5000
```

3. Follow skill `skill-scout` + `docs/vision/repo-trust-rubric.md`:
   - Hard gates → score → shortlist ≤3
   - Proposal → `docs/reviews/YYYY-MM-DD-skill-scout-proposal.md`
   - Status **`PENDING_APPROVAL`**
   - Draft manifest fields for the future skill (`phases`, `agents`, `keywords`, `priority` default 6–10)

4. Present shortlist + proposal path to human. Explicitly say: approve then run `/skill-scout-apply`.

## Forbidden

- Writing `.cursor/skills/{new}/SKILL.md`
- Editing `skills-manifest.v2.json`
- Treating scout as product implementation
