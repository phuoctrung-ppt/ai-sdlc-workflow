# Workflow Agents & Skills Expansion
**Goal:** Add spike-agent, contract-agent, three portable skills (error-recovery, api-contract-first, incremental-commit), plan-template dependency graph + certainty labels, and AGENTS.md §12 maintainability/test-data forbidden patterns — without redoing P1 weak-model gates.
**Protected:** yes | **Agents:** architect-planner, spike-agent, contract-agent, judge-agent

## Constraints
- Documentation/workflow-config only; no app business logic; no secrets.
- Manifest path is `.cursor/skills/skills-manifest.v2.json` (there is no `skills-manifest.json` on disk).
- Out of scope: hooks, `workflow-guard.py`, `skill-loader.py`, `protected-paths.json`, app `docs/` product plans, existing `*-worker.md` agents except edits listed in Files.
- P1 already shipped (`docs/reviews/2026-08-01-weak-model-workflow-quality-review.md` TASK_APPROVED) — do not re-edit judge severity / Phase −1 / Phase 2 section-by-section unless a regression is found.

## Source Evidence
- `Gate skipped: workflow-meta` — Goal is workflow-infra; Files are `.cursor/**` + `AGENTS.md` §5/§12 only.
- P1 present: `.cursor/agents/architect-planner.md` has `## Phase −1 — AGENTS.md Completeness Gate`; `.cursor/commands/dev-module.md` embeds Rule 4 + section-by-section + Rule 5; `.cursor/agents/judge-agent.md` has `CHANGES_REQUESTED(Critical|Minor)`.
- Missing: no `.cursor/agents/spike-agent.md`, no `.cursor/agents/contract-agent.md`, no `error-recovery` / `api-contract-first` / `incremental-commit` skill dirs, no `Task Dependencies` / `[CERTAIN]|[UNCERTAIN]` in Plan Template, no Maintainability/Test Data under `AGENTS.md` §12, no `spike-agent`/`contract-agent` in `worker-scopes.json` or manifest `agents[]`.
- Active plan replaced from `docs/plans/2026-08-01-portable-core-trim.md` per orchestrator approval.

SECTION 1 COMPLETE

## Acceptance Criteria
1. `.cursor/agents/spike-agent.md` exists; role is PoC before formal plan; write scope only `docs/spikes/YYYY-MM-DD-{topic}.md`; report includes feasibility (yes/no/partial), approach options, rough effort, blockers, recommendation; read-only elsewhere.
2. `.cursor/agents/contract-agent.md` exists; drafts/locks contracts at `docs/contracts/YYYY-MM-DD-{feature}-contract.md` with endpoints, request/response shapes, shared types, breaking-change policy; architect-planner dispatches it after plan / before backend+frontend; breaking edits add `[BREAKING]` in the contract file.
3. `spike-agent` and `contract-agent` appear in `.cursor/skills/skills-manifest.v2.json` `agents[]`, in `.cursor/config/worker-scopes.json` `agents` (spike: `docs/spikes/**` only; contract: `docs/contracts/**` + `packages/**`), and as rows in `AGENTS.md` §5 Agent Roster table.
4. `.cursor/skills/error-recovery/SKILL.md` covers error classes (build/type/test/runtime/integration), 4-question root-cause checklist, read-error→file:line→±10 lines→minimal fix→verify pattern, and bans try-catch-to-hide / `as any` / comment-out-failing-test; registered in manifest with phases `[fix, implement-backend, implement-frontend]` and keywords `[error, fix, debug, fail, broken, crash]`.
5. `.cursor/skills/api-contract-first/SKILL.md` requires approve-before-implement, OpenAPI **or** Zod per `AGENTS.md` §2, lock via contract-agent, breaking vs non-breaking definitions matching the task brief; manifest phases `[plan, implement-backend, implement-frontend, design]`.
6. `.cursor/skills/incremental-commit/SKILL.md` requires commit-per-breakdown-task, Conventional Commits per `AGENTS.md` §11, build+relevant tests pass, ≤200 lines diff guideline, bans console.log / commented code / `.env` / secrets; manifest phases `[implement-backend, implement-frontend, database, devops]`.
7. `AGENTS.md` §12 gains `### Maintainability` (no magic numbers/hardcoded strings; async/LLM/external/queue must have explicit timeout; AI features need feature flags) and `### Test Data` (no production-like fixture IDs/emails; never seed test data into production DB).
8. `.cursor/agents/architect-planner.md` Plan Template includes `## Task Dependencies` table (`Task | Depends On | Can Parallelize With`) after Task Breakdown; rule: do not dispatch a task whose Depends On is incomplete; tasks with empty Depends On may parallelize in Phase 3.
9. Every Task Breakdown entry in the Plan Template instructions requires label `[CERTAIN]` or `[UNCERTAIN]`; `[UNCERTAIN]` criteria documented (unused tech, untested external integration, no performance baseline); `[UNCERTAIN]` → dispatch `spike-agent` before detailing that task.
10. `.cursor/commands/dev-module.md` Phase 3 states: (a) do not start `@backend-worker` / `@frontend-worker` until contract-agent output is approved when the plan lists a contract; (b) dispatch order must honor the plan's Task Dependencies table.
11. Post-execution finish checklist all pass: every new skill `entry` path in manifest exists on disk; both agents in `worker-scopes.json`; Phase −1 HARD STOP still present; judge Critical+Minor still present; dependency graph in Plan Template; CERTAIN/UNCERTAIN in Task Breakdown format.
12. No edits to hooks, `workflow-guard.py`, `skill-loader.py`, or `protected-paths.json`.

SECTION 2 COMPLETE

## Database / API Contract
N/A for product DB/HTTP — workflow docs only.

**Workflow contract artifacts (normative for workers):**
- Spike report path: `docs/spikes/YYYY-MM-DD-{topic}.md`
- API contract path: `docs/contracts/YYYY-MM-DD-{feature}-contract.md`
- Shared types live under the package path named in `AGENTS.md` §3 when filled; until then contract-agent may edit `packages/**` only when that tree exists; otherwise contract shapes stay in the markdown contract file.

SECTION 3 COMPLETE

## Files
| Path | Action | Owner |
|---|---|---|
| `.cursor/agents/spike-agent.md` | Create | architect-planner |
| `.cursor/agents/contract-agent.md` | Create | architect-planner |
| `.cursor/skills/error-recovery/SKILL.md` | Create | architect-planner |
| `.cursor/skills/api-contract-first/SKILL.md` | Create | architect-planner |
| `.cursor/skills/incremental-commit/SKILL.md` | Create | architect-planner |
| `.cursor/skills/skills-manifest.v2.json` | Modify — add agents + three skill entries | architect-planner |
| `.cursor/config/worker-scopes.json` | Modify — add spike-agent, contract-agent scopes | architect-planner |
| `.cursor/agents/architect-planner.md` | Modify — Task Dependencies + CERTAIN/UNCERTAIN + spike/contract dispatch | architect-planner |
| `.cursor/commands/dev-module.md` | Modify — Phase 3 contract gate + dependency-aware dispatch | architect-planner |
| `AGENTS.md` | Modify — §5 roster rows; §12 Maintainability + Test Data | architect-planner |
| `docs/plans/2026-08-01-workflow-agents-skills-expansion.md` | Create — this plan | architect-planner |
| `docs/plans/.active-plan` | Modify — point here | architect-planner |
| `.cursor/context/handoffs/workflow-agents-skills-expansion.json` | Create | architect-planner |
| `.cursor/agents/judge-agent.md` | N/A — P1 already complete; no change unless regression | — |
| `.cursor/commands/dev-module.md` Phase 2 / Phase 5 severity | N/A — P1 already complete | — |

SECTION 4 COMPLETE

## Execution / Task Breakdown

### Task 1 — Create spike-agent [CERTAIN]
- **Owner:** architect-planner
- **Skill:** `agentic-workflow` (`.cursor/skills/agentic-workflow/SKILL.md`)
- **Create:** `.cursor/agents/spike-agent.md`
- **Do:** Define role (PoC for high uncertainty before formal plan), output template for `docs/spikes/YYYY-MM-DD-{topic}.md` (feasibility, options, effort, blockers, recommendation), read-only codebase + write only `docs/spikes/`, trigger text: architect-planner dispatches when brainstorm/task labeled `[UNCERTAIN]`.
- **Depends On:** (none)
- **Can Parallelize With:** Task 2, Task 3, Task 4, Task 5
- **Acceptance:** File exists; grep finds `docs/spikes/`, `feasibility`, `[UNCERTAIN]`; no write scopes outside spikes.

### Task 2 — Create contract-agent [CERTAIN]
- **Owner:** architect-planner
- **Skill:** `agentic-workflow`
- **Create:** `.cursor/agents/contract-agent.md`
- **Do:** Role draft/lock/enforce; contract file schema (endpoints, req/res, shared types, breaking policy); workflow after plan / before backend+frontend; on backend-driven shape change update contract + `[BREAKING]` tag for frontend-worker.
- **Depends On:** (none)
- **Can Parallelize With:** Task 1, Task 3–5
- **Acceptance:** File exists; grep finds `docs/contracts/`, `[BREAKING]`, approve-before-workers language.

### Task 3 — Create error-recovery skill [CERTAIN]
- **Owner:** architect-planner
- **Skill:** `planning` (skill-authoring pattern by analogy to existing `SKILL.md` files)
- **Create:** `.cursor/skills/error-recovery/SKILL.md`
- **Do:** Cover all content bullets in Acceptance #4.
- **Depends On:** (none)
- **Can Parallelize With:** Task 1, 2, 4, 5
- **Acceptance:** File exists; sections name build/type/test/runtime/integration; contains anti-pattern bans for try-catch hide, `as any`, comment-out test.

### Task 4 — Create api-contract-first skill [CERTAIN]
- **Owner:** architect-planner
- **Skill:** `planning`
- **Create:** `.cursor/skills/api-contract-first/SKILL.md`
- **Do:** Cover Acceptance #5 content.
- **Depends On:** (none)
- **Can Parallelize With:** Task 1–3, 5
- **Acceptance:** File exists; states approve-before-implement; OpenAPI or Zod; breaking = rename/remove field, type change, HTTP method change; non-breaking = optional field / new endpoint.

### Task 5 — Create incremental-commit skill [CERTAIN]
- **Owner:** architect-planner
- **Skill:** `planning`
- **Create:** `.cursor/skills/incremental-commit/SKILL.md`
- **Do:** Cover Acceptance #6 content.
- **Depends On:** (none)
- **Can Parallelize With:** Task 1–4
- **Acceptance:** File exists; mentions Conventional Commits, ≤200 lines, per-task commit, ban list includes `.env` and secrets.

### Task 6 — Register agents + skills in manifest and scopes [CERTAIN]
- **Owner:** architect-planner
- **Skill:** `agentic-workflow`
- **Modify:** `.cursor/skills/skills-manifest.v2.json`, `.cursor/config/worker-scopes.json`
- **Do:** Append `spike-agent`, `contract-agent` to manifest `agents[]`. Add three portable skill objects with ids/entry/phases/keywords per AC 4–6 (and agents lists as appropriate). Add `worker-scopes.json` entries: `spike-agent: ["docs/spikes/**"]`, `contract-agent: ["docs/contracts/**", "packages/**"]`.
- **Depends On:** Task 1, Task 2, Task 3, Task 4, Task 5 complete (files must exist before manifest entries point at them)
- **Can Parallelize With:** (none until deps done)
- **Acceptance:** `python3 -c` or manual check: every new skill `entry` resolves under `.cursor/skills/`; both agent keys exist in scopes; `jq`/grep shows agents in manifest `agents[]`.

### Task 7 — Plan template: dependencies + uncertainty + dispatch [CERTAIN]
- **Owner:** architect-planner
- **Skill:** `planning` + ref `.cursor/skills/planning/references/planning-with-lower-models.md`
- **Modify:** `.cursor/agents/architect-planner.md`
- **Do:** After Task Breakdown in Plan Template (expand compact template as needed for these fields), add `## Task Dependencies` table; document no-dispatch-until-deps-complete + parallel note; require `[CERTAIN]|[UNCERTAIN]` on each task with UNCERTAIN criteria; document spike-agent dispatch on UNCERTAIN and contract-agent dispatch after plan before workers.
- **Depends On:** Task 1, Task 2 (agents must be named accurately)
- **Can Parallelize With:** Task 8 (after Task 1–2)
- **Acceptance:** Grep shows `Task Dependencies`, `Can Parallelize With`, `[CERTAIN]`, `[UNCERTAIN]`, `spike-agent`, `contract-agent` in architect-planner.md; Phase −1 gate still present (no regression).

### Task 8 — dev-module Phase 3 gates [CERTAIN]
- **Owner:** architect-planner
- **Skill:** `agentic-workflow`
- **Modify:** `.cursor/commands/dev-module.md` (Phase 3 only for this task)
- **Do:** Add contract-approved gate before backend/frontend; add instruction to honor Task Dependencies / parallelize only independent tasks.
- **Depends On:** Task 2, Task 7
- **Can Parallelize With:** Task 9
- **Acceptance:** Phase 3 contains contract-agent / contract approve language and Task Dependencies; Phase 2 Rule 4/5 and Phase 5 Critical-only loop unchanged.

### Task 9 — AGENTS.md §5 + §12 [CERTAIN]
- **Owner:** architect-planner
- **Skill:** `agentic-workflow`
- **Modify:** `AGENTS.md`
- **Do:** Add `spike-agent` and `contract-agent` rows to §5 table; add §12 `### Maintainability` and `### Test Data` with the five forbidden bullets from the task brief.
- **Depends On:** Task 1, Task 2
- **Can Parallelize With:** Task 7, Task 8
- **Acceptance:** §5 lists both agents; §12 contains Maintainability and Test Data headings with magic-numbers, timeout, feature-flag, production-like IDs, and production-seed bans.

### Task 10 — Finish checklist verification [CERTAIN]
- **Owner:** architect-planner (orchestrator verifies)
- **Skill:** `agentic-workflow`
- **Do:** Run the six finish-checklist items from the user brief; fix any fail before declaring done; then `/workflow-eval` / judge-agent task review.
- **Depends On:** Task 6, Task 7, Task 8, Task 9
- **Can Parallelize With:** (none)
- **Acceptance:** All six checklist items reported pass in chat or review artifact; judge `TASK_APPROVED` or only-Minor.

## Task Dependencies
| Task | Depends On | Can Parallelize With |
|------|------------|----------------------|
| Task 1 | — | Tasks 2–5 |
| Task 2 | — | Tasks 1, 3–5 |
| Task 3 | — | Tasks 1–2, 4–5 |
| Task 4 | — | Tasks 1–3, 5 |
| Task 5 | — | Tasks 1–4 |
| Task 6 | Tasks 1–5 | — |
| Task 7 | Tasks 1–2 | Task 8 (after 1–2), Task 9 |
| Task 8 | Tasks 2, 7 | Task 9 |
| Task 9 | Tasks 1–2 | Tasks 7–8 |
| Task 10 | Tasks 6–9 | — |

**Dispatch rule:** Do not start a task until every entry in its Depends On column is complete. Tasks with empty Depends On may run in parallel in Phase 3.

SECTION 5 COMPLETE

## Domain Config Sync
- [x] Plan written — this file
- [x] `docs/plans/.active-plan` → this plan (replace portable-core-trim)
- [x] Handoff — `.cursor/context/handoffs/workflow-agents-skills-expansion.json`
- [ ] ADR — N/A — no product stack/tenancy/auth change; workflow-agent addition only
- [ ] `docs/architecture.md` — N/A — no runtime container change
- [ ] `AGENTS.md` §5 + §12 — update during Task 9 (not speculative)
- [ ] `.cursor/config/worker-scopes.json` — Task 6
- [ ] `.cursor/skills/skills-manifest.v2.json` — Task 6
- [ ] `protected-paths.json` — N/A — out of scope; no new protected globs required for docs/spikes|contracts markdown

## Risks
- Manifest consumers still referencing deleted `skills-manifest.json` — mitigate by documenting v2 path only in this plan and agent text.
- `packages/**` scope for contract-agent is broad if monorepo grows — tighten when `AGENTS.md` §3 is filled.
- Operators may skip spike/contract steps if language is soft — keep MUST / HARD-GATE wording in agent + dev-module Phase 3.
- Parallel Tasks 1–5 can race before Task 6 — Task 6 explicitly waits for files on disk.

## Handoffs
→ `.cursor/context/handoffs/workflow-agents-skills-expansion.json`

SECTION 6 COMPLETE

## Rule 5 Self-Verify
- [x] Every task has real file paths and a testable acceptance line?
- [x] Every task names its owner agent + skill (from `skills-manifest.v2.json`)?
- [x] Contracts (workflow artifact paths) are concrete, not "TBD"?
- [x] Multi-tenancy — N/A for workflow-meta docs
- [x] No placeholder tokens in executable fields?
- [x] Domain Config Sync items each resolved (done or `N/A — reason`)?
