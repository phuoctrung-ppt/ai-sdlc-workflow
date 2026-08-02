---
name: dev-module
description: Full per-module development loop — brainstorm → plan → execute → test → verify → fix → loop → done + Memory/Learning distillation. Use for any new feature module from scratch. Automatically loops through fix cycles until judge approves or loop cap is reached.
---

# Module Development Loop

Act as **Orchestrator**. Run the full development loop for module: **{feature_name}**

State file: `.cursor/state/module-{feature_name}-loop.json` (created/updated at each phase transition)

> **Upstream:** `/dev-module` is the **execution** loop. If planning was already done by
> `/architecture-plan` (a `PLAN_APPROVED` breakdown for this module exists under `docs/plans/`),
> **skip Phase 1–2** — confirm the existing plan and jump to Phase 1.5 (scaffold) / Phase 3
> (execute). Only run Phase 1–2 when no approved plan/breakdown exists for this module.

---

## Phase 0 — Restore State (if resuming)

Check if `.cursor/state/module-{feature_name}-loop.json` exists. If it does, read it and resume from `state.phase`. If not:
- If `docs/plans/.active-plan` (or a `docs/plans/*-{feature_name}.md`) holds a `PLAN_APPROVED` breakdown covering this module → set `state.phase = execute` (or `scaffold` if shells are missing) and start there.
- Otherwise start fresh at Phase 1.

Also load Memory layer early:
```bash
# Always consider these before planning/executing
cat docs/memory/decisions.md docs/memory/gotchas.md docs/memory/shortcuts.md 2>/dev/null || true
cat docs/module-deps.md 2>/dev/null || true
```

---

## Phase 1 — BRAINSTORM

**Agent:** `@architect-planner`

```bash
python3 .cursor/context/context-builder.py \
  --phase brainstorm --task "{feature_name}" --agent architect-planner
```

Explore:
- Similar existing modules in the codebase
- Relevant patterns in `AGENTS.md §2` (stack) and `§3` (structure)
- Prior art in `docs/plans/` and `docs/adr/`
- **Memory layer**: decisions / gotchas / shortcuts
- 2–3 viable design approaches with tradeoffs

Output a short **Brainstorm Summary** (not a full plan yet) — options, constraints, recommendation.

Save state: `{ "feature": "{feature_name}", "phase": "plan", "loopCount": 0 }`

---

## Phase 2 — PLAN ⏸️ (requires approval)

**Agent:** `@architect-planner`

```bash
python3 .cursor/context/context-builder.py \
  --phase plan --task "{feature_name}" --agent architect-planner \
  --handoff docs/plans/.active-plan
```

### Anti-laziness contract (mandatory)

Paste this contract at the top of every Phase 2 planning prompt (verbatim — not a link-only reference):

```
You are writing an EXECUTABLE plan, not a summary.
- Every "Files" entry MUST be a real, full path (e.g. apps/api/src/modules/x/x.service.ts).
- Every acceptance criterion MUST be testable (not "API works").
- FORBIDDEN: "etc.", "and so on", "similar to above", "// TODO", "[continue]".
- If you approach the output limit, stop at a section boundary and write
  [PAUSED - section N of 6]. On "continue", resume with no recap.
- A worker with no memory of this chat must be able to execute the plan from the file alone.
```

### Section-by-section planning (Rule 2 — mandatory)

Do **NOT** ask `@architect-planner` for the whole plan in one shot. Invoke it **six times** (or six sequential turns), one section each, filling the architect-planner Plan Template field-by-field (do not restructure it). Fixed order:

1. Goal + Source Evidence (grounded facts) → then write `SECTION 1 COMPLETE`
2. Acceptance Criteria (concrete, testable) → then write `SECTION 2 COMPLETE`
3. Database / API contract → then write `SECTION 3 COMPLETE`
4. Files to Create/Modify table → then write `SECTION 4 COMPLETE`
5. Task Breakdown (one task block at a time) → then write `SECTION 5 COMPLETE`
6. Domain Config Sync + Risks → then write `SECTION 6 COMPLETE`

Rules:
- After each section, the model MUST literally write `SECTION N COMPLETE` before starting the next.
- If output limit is near: stop at a section boundary and write `[PAUSED - section N of 6]`; on continue, resume with no recap.
- **FORBIDDEN** to accept a plan that lacks every `SECTION N COMPLETE` marker (N=1..6), or that ends mid-section without a `[PAUSED - section N of 6]` marker.
- Write the accumulating plan to `docs/plans/YYYY-MM-DD-{feature_name}.md`.

### Self-verify (Rule 5 — mandatory)

Before leaving Phase 2, `@architect-planner` MUST answer every item against the plan. Any "no" ⇒ fix that section; do **not** hand off:

- [ ] Every task has real file paths and a testable acceptance line?
- [ ] Every task names its owner agent + skill (from `skills-manifest.v2.json`)?
- [ ] Contracts (DB columns, API shapes, shared types) are concrete, not "TBD"?
- [ ] Multi-tenancy respected where required (`workspace_id` / tenant filter)?
- [ ] No placeholder tokens anywhere?
- [ ] Domain Config Sync items each resolved (done or `N/A — reason`)?
- [ ] Memory layer consulted (no conflict with decisions.md / gotchas.md)?

Report pass/fail per item in chat or in the plan file. The orchestrator MUST NOT set `state.phase = execute` until all boxes are reported as pass.

### Phase 2b — SYNC DOMAIN CONFIG (before execute)

After the plan is drafted **and** Rule 5 self-verify passed, `@architect-planner` must complete Phase 1.5 from `.cursor/agents/architect-planner.md`:
- ADR in `docs/adr/` when architecture decisions changed (or N/A in plan)
- Create/update `docs/architecture.md`
- Update affected `AGENTS.md` sections (§2–§15 as applicable)
- Update `.cursor/config/*` if worker scopes / protected paths changed
- Set `docs/plans/.active-plan` to this plan
- **Register module in `docs/module-deps.md`** (status: planned, depends_on: [...])

**⏸️ STOP — wait for orchestrator approval of plan + sync diffs before Phase 1.5 scaffold / Phase 3.**

Save state: `{ "phase": "execute", "planPath": "docs/plans/..." }`

---

## Phase 1.5 — SCAFFOLD (optional, for new modules)

**Agent:** `@scaffold-agent`

If the feature requires new modules/pages that don't exist yet:
```bash
python3 .cursor/context/context-builder.py \
  --phase scaffold --task "{feature_name}" --agent scaffold-agent \
  --keywords "module,scaffold,entity,migration,stub"
```

Scaffold creates empty shells → workers fill them with logic.
Save state: `{ "phase": "execute", "scaffoldComplete": true }`

---

## Phase 3 — EXECUTE

> **Hard-gate — Module Dependencies**
> Before any worker dispatch, read `docs/module-deps.md`.
> If any entry in `depends_on` is not `status: done` (or lacks an approved contract), **STOP** and report the missing upstream module.

> **Design-first for UI:** For any task that creates/changes UI, a design artifact MUST exist before `@frontend-worker` runs — a spec `docs/design/YYYY-MM-DD-{feature}.md` **and** sketches under `docs/design/sketches/{feature}/`.
>
> **Branding / visual UI also needs an asset pack** — not sketches alone. When the UI ships logos, icons, or backgrounds (landing, hero, branded marketing, identity), `@designer-worker` MUST also produce:
> 1. **UI section sketches** → `docs/design/sketches/{feature}/`
> 2. **Background assets** (raster PNG/JPG/WebP) → `docs/design/assets/{feature}/backgrounds/`
> 3. **Logo / icon SVG assets** → `docs/design/assets/{feature}/logos/` and `.../icons/`
> 4. An **Asset Mapping** table in the design spec (which file → which section/component)
>
> If any of the above is missing for a branding UI task, dispatch `@designer-worker` (phase `design`) FIRST with keywords including `asset,background,logo,svg,icon,brandkit,imagegen`, then dispatch `@frontend-worker` to implement from the mapping (copy/import mapped files — do not invent placeholders). Skip the design step only for non-visual frontend work (note "no new UI"). This mirrors the `<DESIGN-GATE>` in `frontend-worker`.

### Contract gate (mandatory when plan lists a contract / API surface)

Before `@backend-worker` or `@frontend-worker` start:
1. Dispatch `@contract-agent` if the plan requires a contract (HTTP/API or shared schema).
2. Wait until `docs/contracts/YYYY-MM-DD-{feature}-contract.md` Status is **approved**.
3. Only then dispatch backend/frontend. Do **not** start them in parallel with an unapproved contract.

### Task dependency dispatch

Honor the plan's **Task Dependencies** table:
- Do **not** dispatch a task whose **Depends On** entries are incomplete.
- Tasks with empty Depends On **may** be dispatched in parallel.
- `[UNCERTAIN]` tasks: run `@spike-agent` first; fold the spike report into planning before worker dispatch.

**Dispatch workers** based on the task table in the plan (parallel only when dependencies allow):

| Task type | Agent | Phase |
|---|---|---|
| Uncertainty spike | `@spike-agent` | `brainstorm` |
| API/schema contract | `@contract-agent` | `plan` |
| New module/feature scaffold | `@scaffold-agent` | `scaffold` |
| Backend / API | `@backend-worker` | `implement-backend` |
| UI design (spec + sketches + **asset pack** + Asset Mapping) — before any new UI | `@designer-worker` | `design` |
| Frontend / UI | `@frontend-worker` | `implement-frontend` |
| Database / schema | `@database-worker` | `database` |
| AI/LLM integration | `@ai-worker` | `implement-backend` |
| Auth / security | `@security-worker` | `implement-backend` |
| DevOps / infra | `@devops-worker` | `devops` |

Each worker runs `context-builder.py` with its agent id before starting (see agent files). Frontend tasks receive design spec, sketch paths, **asset pack path**, and Asset Mapping in their handoff packet. Contract path goes in backend/frontend handoffs when applicable.

Save state: `{ "phase": "test" }`

---

## Phase 4 — TEST

**Agent:** `@qa-worker`

```bash
python3 .cursor/context/context-builder.py \
  --phase test --task "{feature_name}" --agent qa-worker \
  --keywords "test,jest,playwright,e2e,mock,coverage"
```

- Run unit tests for new service layer
- Run integration tests if API routes changed
- Run E2E for critical paths from `AGENTS.md §6` if affected
- Report: test results, coverage %, any failures

Save state: `{ "phase": "verify" }`

---

## Phase 5 — VERIFY (Judge Gate)

**Agent:** `@judge-agent`

```bash
python3 .cursor/context/context-builder.py \
  --phase review --task "{feature_name}" --agent judge-agent \
  --keywords "workflow,judge,security,test" --budget 5000
```

Run `/workflow-eval` against the plan + diff + test results.
Write review to `docs/reviews/YYYY-MM-DD-{feature_name}-review.md`.

Judge status uses severity tiers (see `.cursor/agents/judge-agent.md`):
- `*_APPROVED`
- `*_CHANGES_REQUESTED(Critical)`
- `*_CHANGES_REQUESTED(Minor)`
- Bare `*_CHANGES_REQUESTED` (no severity suffix) ≡ **Critical** (fail closed)

### Decision tree:

```
*_APPROVED  ────────────────────────────────────────────▶ Phase 6 (DONE ✅)
*_CHANGES_REQUESTED(Minor) only  ───────────────────────▶ Phase 6 (DONE ✅)
  (record Minor under Suggestions in the review; do NOT block approve;
   do NOT increment loopCount)
*_CHANGES_REQUESTED(Critical) + loopCount < 3 ──────────▶ Phase 5a (FIX)
*_CHANGES_REQUESTED(Critical) + loopCount >= 3 ─────────▶ Phase 5b (ESCALATE)
```

Only **Critical** findings trigger the fix loop and count toward `loopCount`. Minor ⇒ Phase 6 (record only).

Save state: `{ "phase": "fix" or "done", "reviewPath": "docs/reviews/..." }`

---

## Phase 5a — FIX (loop back)

Increment `loopCount` in state file (**Critical only** — never for Minor-only reviews).

Dispatch a focused **fix handoff** to the worker responsible for each **Critical** CHANGES_REQUESTED item (ignore Minor in loop dispatch):

```
Objective: Fix [Critical issue from judge review]
Plan: [planPath from state]
Judge review: [reviewPath from state]
In-scope: [only the files flagged by judge as Critical]
Acceptance: [specific Critical criterion from judge review]
```

After fixes are applied → return to **Phase 4 (TEST)**.

---

## Phase 5b — ESCALATE (loop cap reached)

Write escalation artifact to `docs/reviews/YYYY-MM-DD-{feature_name}-escalation.md`:

```markdown
# Escalation Required — {feature_name}

Loop cap (3) reached. Human review needed.

## Remaining Issues
[list from last judge review]

## Fix Attempts
[summary of what was tried]

## Recommendation
[what the orchestrator thinks the blocker is]
```

**⏸️ STOP — do not continue until human resolves.**

---

## Phase 6 — DONE ✅ + Memory Distillation

Save final state: `{ "phase": "done", "loopCount": N }`

### Distillation (Memory + Learning Layer) — mandatory

1. **Retrospective entry** — append to `docs/retrospective.md`:

```markdown
### YYYY-MM-DD — {feature_name}
- **Estimate vs Actual**: ...
- **Fix loops**: N (Critical only)
- **Root cause** (if loops > 0): ...
- **Pattern candidate**: ...
- **Action**: ...
```

2. **Extract facts** (1–5 max) into the Memory layer:
   - Locked decision → `docs/memory/decisions.md`
   - Failed pattern → `docs/memory/gotchas.md`
   - Proven shortcut → `docs/memory/shortcuts.md`

3. **Update dependency graph** — set the module status to `done` in `docs/module-deps.md`.

4. **Skill-updater trigger** — if 5 modules completed since last review (count entries in retrospective.md), surface a skill-update proposal.

Output summary:
```
✅ Module {feature_name} complete
Plan: docs/plans/...
Review: docs/reviews/...
Fix loops: N
Files changed: [list]
Memory updated: decisions/gotchas/shortcuts (yes/no)
Retrospective: appended
```

Clean up: optionally archive `.cursor/state/module-{feature_name}-loop.json` to `docs/plans/` for traceability.
