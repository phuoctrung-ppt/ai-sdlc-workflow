# Task Review: Workflow Agents & Skills Expansion

Status: TASK_APPROVED

## Scope Reviewed
- Plan/issue: `docs/plans/2026-08-01-workflow-agents-skills-expansion.md`
- Handoff: `.cursor/context/handoffs/workflow-agents-skills-expansion.json`
- Prior plan review: `docs/reviews/2026-08-01-workflow-agents-skills-expansion-plan.md` (PLAN_APPROVED)
- Files (in-scope verified):
  - `.cursor/agents/spike-agent.md` (new)
  - `.cursor/agents/contract-agent.md` (new)
  - `.cursor/skills/error-recovery/SKILL.md` (new)
  - `.cursor/skills/api-contract-first/SKILL.md` (new)
  - `.cursor/skills/incremental-commit/SKILL.md` (new)
  - `.cursor/skills/skills-manifest.v2.json` (agents[] + three skill entries)
  - `.cursor/config/worker-scopes.json` (spike-agent, contract-agent)
  - `.cursor/agents/architect-planner.md` (Task Dependencies, CERTAIN/UNCERTAIN, contract/spike dispatch; Phase −1 intact)
  - `.cursor/commands/dev-module.md` (Phase 3 contract gate + dependency dispatch; Phase 2/5 P1 intact)
  - `AGENTS.md` (§5 spike/contract rows; §12 Maintainability + Test Data)
- Commands:
  - `python3 .cursor/context/context-builder.py --phase review --task "Task review workflow agents skills expansion" --agent judge-agent --budget 5000`
  - File existence checks for agents + three `SKILL.md` paths
  - Manifest entry resolve under `.cursor/skills/` for `error-recovery`, `api-contract-first`, `incremental-commit`
  - `rg` on manifest, worker-scopes, architect-planner, judge-agent, dev-module, AGENTS.md
  - `git status` on out-of-scope paths (hooks, protected-paths, workflow-guard, skill-loader, judge-agent)
- Review mode: task

## Critical
- None

## Suggestions
- `spike-agent.md` / `contract-agent.md` Start blocks call context-builder with `--agent architect-planner` (not their own ids). Works if those ids are not yet first-class in activation rules; consider `--agent spike-agent` / `contract-agent` once scopes are wired end-to-end.
- Working tree also has dirty `judge-agent.md` and `skill-loader.py` from other work (P1 severity tiers / portable-core-trim). Not required by this plan’s Files table — keep them out of this task’s PR if splitting commits.
- `AGENTS.md` §5 also demotes `ai-worker` / `admin-worker` to an optional footnote while adding spike/contract (overlaps portable-core-trim). Acceptable for a portable core; if this PR is expansion-only, split that demotion to the trim plan’s commit.

## Verified

### AC map (plan 1–12)

| AC | Result | Evidence |
|---|---|---|
| 1 spike-agent | Pass | File exists; write scope `docs/spikes/`; feasibility yes/no/partial; options/effort/blockers/recommendation; `[UNCERTAIN]` trigger; read-only elsewhere |
| 2 contract-agent | Pass | `docs/contracts/YYYY-MM-DD-{feature}-contract.md`; endpoints, req/res, shared types, breaking policy; after plan / before workers; `[BREAKING]` update path |
| 3 register agents | Pass | manifest `agents[]` has both; `worker-scopes.json`: spike=`docs/spikes/**`, contract=`docs/contracts/**`+`packages/**`; AGENTS.md §5 rows present |
| 4 error-recovery | Pass | Classes build/type/test/runtime/integration; 4-question checklist; read→file:line→±10→minimal→verify; bans try/catch-hide, `as any`, comment-out test; phases `[fix, implement-backend, implement-frontend]`; keywords match |
| 5 api-contract-first | Pass | Approve-before-implement; OpenAPI or Zod per §2; lock via contract-agent; breaking/non-breaking defs match brief; phases include plan/backend/frontend/design |
| 6 incremental-commit | Pass | Per-breakdown-task commit; Conventional Commits §11; build+relevant tests; ≤200 lines; bans console.log / commented code / `.env` / secrets; phases match |
| 7 AGENTS §12 | Pass | `### Maintainability` (magic numbers, timeout, feature flag); `### Test Data` (production-like IDs, no prod seed) |
| 8 Task Dependencies | Pass | Plan Template has `## Task Dependencies` table + no-dispatch-until-deps + parallel note |
| 9 CERTAIN/UNCERTAIN | Pass | Required on each task; UNCERTAIN criteria documented; spike-agent before detailing |
| 10 Phase 3 gates | Pass | Contract approved before backend/frontend; honor Task Dependencies; Phase 2 section-by-section + Rule 4/5 and Phase 5 Critical/Minor loop unchanged |
| 11 Finish checklist | Pass | See below |
| 12 Out of scope | Pass | hooks / `protected-paths.json` / `workflow-guard.py` clean for this task; skill-loader/judge dirty from other plans, not in this Files table |

### AC11 finish checklist
1. Every new skill `entry` resolves under `.cursor/skills/` — Pass
2. `spike-agent` and `contract-agent` in `worker-scopes.json` — Pass
3. Phase −1 Completeness Gate still present (`STOP` without plan) — Pass
4. Judge `CHANGES_REQUESTED(Critical|Minor)` still present — Pass
5. Dependency graph table in Plan Template — Pass
6. `[CERTAIN]`/`[UNCERTAIN]` in Task Breakdown format — Pass

### Workflow integrity
- Traces to plan + handoff; P1 gates not regressed
- No secrets; docs/workflow-config only
- Acceptance evidenced by file content + greps, not intent alone

## Pattern Candidates
- [x] propose: `workflow-spike-contract-certainty-deps` → `.cursor/patterns/` (spike/contract agents + CERTAIN/UNCERTAIN + Task Dependencies + Phase 3 contract gate — reusable when porting workflow)
