---
name: skill-scout
description: Research external best-practice sources with repo-trust rubric; propose thin skills. Never auto-apply.
---

# Skill Scout

Optional learning-adjacent skill. **Not** part of `/fix` or `/shape-lite`.

## When to use

- Human asks to ingest best practices (Python, QA, tests, security patterns, …) from GitHub/docs
- Need ranked shortlist before writing any `SKILL.md`

## Required reading

1. `docs/vision/repo-trust-rubric.md` — hard gates + score 0–20
2. `docs/vision/skill-scout-apply.md` — what happens **after** approve (do not run apply here)

## Workflow (scout only)

1. Parse brief: stack (prefer `AGENTS.md` profile if present), scope, exclusions
2. Search web/GitHub; collect candidates
3. Apply **hard gates** → reject failures with one-line reason
4. Score A–J; shortlist **≤3** (prefer score ≥14)
5. For each shortlist: portable extract (3–7 bullets), drop list, license, risk
6. Write proposal:
   - Path: `docs/reviews/YYYY-MM-DD-skill-scout-proposal.md`
   - Status: `PENDING_APPROVAL`
   - Include proposed manifest fields draft (`id`, `phases`, `agents`, `keywords`, `priority`)
7. **Stop.** Do not write `.cursor/skills/**` or edit `skills-manifest.v2.json`

## Forbidden

- Auto-apply / silent manifest edits
- Full upstream copy into entry skill
- Priority ≥ core portable skills without human ask
- Loading this skill into product implement loops by default

## Handoff after human APPROVE

Orchestrator runs `/skill-scout-apply` with the proposal path. See apply protocol.
