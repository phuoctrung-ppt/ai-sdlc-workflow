---
name: skill-scout
description: Research external best-practice sources with repo-trust rubric; propose thin skills + load map. Never auto-apply.
---

# Skill Scout

Optional learning-adjacent skill. **Not** part of `/fix` or `/shape-lite`.

## When to use

- Human wants best practices ingested (Python, QA, tests, security patterns, …)
- Need ranked shortlist before any `SKILL.md` write

## Required reading

1. `docs/vision/repo-trust-rubric.md` — hard gates + score 0–20
2. `docs/vision/skill-scout-best-practices.md` — distill + keyword + priority rules
3. `docs/vision/skill-scout-apply.md` — post-approve only (do not apply here)
4. Template: `docs/reviews/_templates/skill-scout-proposal.md`

## Best practices (must follow)

1. **One craft per skill** — no kitchen-sink ids
2. **Thin entry** (~800–1500 tokens); long material → `references/` lazy
3. **Keywords** = stack + practice nouns (≥2; not only `test`/`code`)
4. **Priority** default 6–10; never ≥12 without human force
5. **Official/high-score sources first**; one strong source beats three weak
6. **Draft full load map** in proposal (`phases`, `agents`, `keywords`, `priority`) before asking APPROVE
7. **Propose, don't apply** — no manifest write in this skill

## Workflow (scout only)

1. Parse brief + stack (`AGENTS.md` profile if present)
2. Search; hard gates → score A–J → shortlist ≤3 (prefer ≥14)
3. Distill plan: when-to-use, hard rules, anti-patterns, refs, attribution
4. Write proposal from template → `docs/reviews/YYYY-MM-DD-skill-scout-proposal.md`
5. Status `PENDING_APPROVAL` + filled `proposed_skill` frontmatter
6. **Stop**

## Forbidden

- Auto-apply / silent manifest edits
- Full upstream dump into entry
- Priority competing with `error-recovery` / `agentic-workflow`
- Wiring into day-path as required step

## After human APPROVE

Orchestrator: `/skill-scout-apply` (see apply protocol + `manifest-register.py`).
