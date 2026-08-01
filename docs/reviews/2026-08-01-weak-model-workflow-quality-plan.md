# Plan Review: Weak-Model Workflow Quality Gates

Status: PLAN_APPROVED

## Scope Reviewed
- Plan/issue: `docs/plans/2026-08-01-weak-model-workflow-quality.md`
- Active plan: `docs/plans/.active-plan` → points at that plan (verified)
- Handoff: `.cursor/context/handoffs/weak-model-workflow-quality.json`
- Grounding (consistency only): `.cursor/agents/architect-planner.md`, `.cursor/commands/dev-module.md`, `.cursor/agents/judge-agent.md`, `.cursor/skills/planning/references/planning-with-lower-models.md`
- Commands: `python3 .cursor/context/context-builder.py --phase review --task "genesis plan weak-model-workflow-quality" --agent judge-agent --keywords "workflow,judge,plan" --budget 5000`
- Review mode: plan

## Critical
- None

## Suggestions
- Handoff `acceptanceCriteria` compresses plan AC 1–9 into six bullets; fine for dispatch, but keep plan AC 1–9 as the execution checklist so workflow-meta exception (AC2) and “no files outside three paths” (AC9) are not dropped during Task 1–3 edits.
- Handoff `requiredVerificationCommands` grep on `dev-module.md` covers Critical / Rule 4 / Rule 5 markers but not an explicit Minor→Phase 6 / `loopCount` Critical-only string; add one `rg` for that phrase when executing Task 3 acceptance.
- When implementing Phase −1, state clearly that Genesis “Standardize the domain” (fill `AGENTS.md`) runs *before* this gate for product plans; gate only blocks writing `docs/plans/*.md`, not brainstorming/domain fill — avoids false stops during `/architecture-plan brainstorming`.

## Verified
- MVP feature 1 (AGENTS completeness gate) → Task 1 + AC 1–2; grounding shows Phase 0 HARD-GATE exists but no §1/§2/§3 placeholder stop before plan write.
- MVP feature 2 (section-by-section Phase 2 + Rule 2/4 embed + Rule 5 mandatory) → Task 2 + AC 3–5; `dev-module.md` Phase 2 is still one-shot “Write full plan”; Rule 4 contract text and Rule 5 checklist exist in `planning-with-lower-models.md` for verbatim paste.
- MVP feature 3 (Critical vs Minor; Critical-only fix loop) → Task 3 + AC 6–8; `judge-agent.md` has Critical/Suggestions sections but bare `*_CHANGES_REQUESTED` status; Phase 5 tree increments `loopCount` on any CHANGES_REQUESTED.
- Out of scope respected: hooks, skill-loader, skills-manifest, workers, AGENTS.md body — not requested.
- Executable: three in-scope paths, owners, testable acceptance, parallel-safe Tasks 1–3; Domain Config Sync correctly N/A for ADR/architecture/AGENTS/config; handoff + `.active-plan` present; plan demonstrates SECTION 1–6 COMPLETE markers.

## Pattern Candidates
- [ ] propose: `judge-severity-critical-minor` → `.cursor/patterns/` (after Task 3 ships — reusable Critical-only loop policy)
