# Plan Review: Workflow Agents & Skills Expansion

Status: PLAN_APPROVED

## Scope Reviewed
- Plan/issue: `docs/plans/2026-08-01-workflow-agents-skills-expansion.md`
- Active plan: `docs/plans/.active-plan` → points at this plan (verified)
- Handoff: `.cursor/context/handoffs/workflow-agents-skills-expansion.json`
- Manifest: `.cursor/skills/skills-manifest.v2.json` exists (no `skills-manifest.json` on disk — plan path correct)
- P1 baseline spot-check (do not re-implement):
  - `.cursor/agents/architect-planner.md` — `## Phase −1 — AGENTS.md Completeness Gate` present
  - `.cursor/agents/judge-agent.md` — severity tiers + `CHANGES_REQUESTED(Critical|Minor)` present
  - `.cursor/commands/dev-module.md` — section-by-section Rule 2 + Rule 4 contract + Rule 5 self-verify present
- Commands: `python3 .cursor/context/context-builder.py --phase review --task "genesis plan workflow-agents-skills-expansion" --agent judge-agent --keywords "workflow,judge,plan" --budget 5000`
- Review mode: plan

## Critical
- None

## Suggestions
- Phase −1 workflow-meta exception text currently requires every Files path under `.cursor/`; this plan correctly documents Gate skipped with `.cursor/**` + `AGENTS.md` §5/§12 only. Consider a follow-up (out of this plan’s scope) to widen the exception wording so AGENTS.md workflow-roster/§12 edits are explicitly allowed without implying a gate violation.
- Domain Config Sync marks ADR / architecture / protected-paths as N/A with unchecked `[ ]` boxes; functionally resolved. Prefer `[x]` + `N/A — reason` for visual Rule 5 clarity.
- Task 3/4 acceptance greps are thinner than AC 4–5 (e.g. 4-question checklist, lock-via-contract-agent). Do-lines already say “cover Acceptance #N”; keep plan AC 4–5 as the execution checklist at implement time.
- Handoff `acceptanceCriteria` compresses plan AC 1–12 into eight bullets; fine for dispatch — retain plan AC 1–12 (esp. AC 11 finish checklist + AC 12 no out-of-scope edits) as the Task 10 verification source.

## Verified
- P1 (weak-model gates) marked done / N/A with no coverage hole — Phase −1, section-by-section Phase 2, judge Critical/Minor all present on disk; prior `docs/reviews/2026-08-01-weak-model-workflow-quality-review.md` TASK_APPROVED referenced.
- Concept items / plan AC 1–11 map to tasks with testable acceptance:
  - AC1 spike-agent → Task 1
  - AC2 contract-agent → Task 2
  - AC3 register agents (manifest + scopes + §5) → Tasks 6 + 9
  - AC4 error-recovery → Tasks 3 + 6
  - AC5 api-contract-first → Tasks 4 + 6
  - AC6 incremental-commit → Tasks 5 + 6
  - AC7 §12 Maintainability + Test Data → Task 9
  - AC8 Task Dependencies template → Task 7
  - AC9 CERTAIN/UNCERTAIN + spike dispatch → Task 7
  - AC10 Phase 3 contract + dependency dispatch → Task 8
  - AC11 finish checklist → Task 10
  - AC12 no hooks/guard/loader/protected-paths edits → Constraints + handoff outOfScopePaths
- Executable: real paths, owner `architect-planner`, skills `agentic-workflow` / `planning`, ordered `Task Dependencies` table, every task labeled `[CERTAIN]`.
- Handoff packet present with objective, in/out scope, skills, planPath, acceptance, verification commands, risks.
- Domain Config Sync filled with done or N/A (ADR, architecture, protected-paths N/A; AGENTS/scopes/manifest deferred to Tasks 6/9).
- Workflow-meta: Goal is workflow-infra; does not invent product domain; AGENTS.md product placeholders remain OK; uses `skills-manifest.v2.json` correctly.
- SECTION 1–6 COMPLETE markers present; Rule 5 self-verify checklist filled.

## Pattern Candidates
- [ ] propose: `workflow-meta-agents-skills-expansion` → `.cursor/patterns/` (after Task 10 ships — reusable spike/contract + CERTAIN/UNCERTAIN + Task Dependencies pattern)
