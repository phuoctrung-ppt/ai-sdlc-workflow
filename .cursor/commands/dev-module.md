---
name: dev-module
description: Full per-module development loop — brainstorm → plan → execute → test → verify → fix → loop → done + Memory distillation + dispatch learning-agent. Use for any new feature module from scratch. Automatically loops through fix cycles until judge approves or loop cap is reached.
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

Also load Memory layer early (primary SoT = `docs/memory/*`):
```bash
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

Explore similar modules, AGENTS.md §2–§3, prior plans/ADRs, and **docs/memory/***.
Output a short Brainstorm Summary — options, constraints, recommendation.
Save state: `{ "feature": "{feature_name}", "phase": "plan", "loopCount": 0 }`

---

## Phase 2 — PLAN ⏸️ (requires approval)

**Agent:** `@architect-planner`

```bash
python3 .cursor/context/context-builder.py \
  --phase plan --task "{feature_name}" --agent architect-planner \
  --handoff docs/plans/.active-plan
```

Follow architect-planner Phase −1 gate and anti-laziness contract. Write plan under `docs/plans/`.
⏸️ STOP for approval when required.

After plan drafted and Rule 5 self-verify passed, complete Phase 1.5 domain config sync from architect-planner.

---

## Phase 1.5 — Scaffold (if needed)

Dispatch `@scaffold-agent` when shells are missing. Update `.cursor/config/*` if scopes changed.

---

## Phase 3 — EXECUTE

> **Hard-gate — Module Dependencies**
> Read `docs/module-deps.md`. If any `depends_on` is not `done` → STOP.

Dispatch workers per task breakdown (respect Depends On / parallelization).
Each worker runs `context-builder.py` with its agent id before starting.

---

## Phase 4 — TEST

```bash
python3 .cursor/context/context-builder.py \
  --phase test --task "{feature_name}" --agent qa-worker
```

---

## Phase 5 — JUDGE + FIX LOOP

```bash
python3 .cursor/context/context-builder.py \
  --phase review --task "{feature_name}" --agent judge-agent
```

Judge status uses severity tiers (see `.cursor/agents/judge-agent.md`):
- `*_APPROVED` → Phase 6
- `*_CHANGES_REQUESTED` with **Critical** → fix loop (increment loopCount)
- **Minor** only → Phase 6 (record; do not burn fix loop)

Only **Critical** findings trigger the fix loop and count toward `loopCount`.

---

## Phase 6 — DONE ✅ + Memory Distillation + Learning dispatch

Save final state: `{ "phase": "done", "loopCount": N }`

### A. Lightweight distillation (orchestrator — always)

1. **Retrospective entry** — append to `docs/retrospective.md`:

```markdown
### YYYY-MM-DD — {feature_name}
- **Estimate vs Actual**: ...
- **Fix loops**: N (Critical only)
- **Root cause** (if loops > 0): ...
- **Pattern candidate**: ...
- **Action**: ...
```

2. **Extract obvious facts** (1–5 max) into **`docs/memory/*` only** (primary SoT — not `.memory/*`) when clear:
   - Locked decision → `docs/memory/decisions.md`
   - Failed pattern → `docs/memory/gotchas.md`
   - Proven shortcut → `docs/memory/shortcuts.md`

3. **Update dependency graph** — set the module status to `done` in `docs/module-deps.md`.

### B. Learning counter + agent dispatch

1. **Update** `.cursor/state/workflow-state.json` **before** dispatch:
   - `modulesSinceLastProposal` = (current or 0) + 1
   - `lastModuleCompleted` = `{feature_name}`
2. Read back `N = modulesSinceLastProposal`.
3. Dispatch `@learning-agent` (skill `skill-updater`). **Do not** rewrite any `SKILL.md` inside this phase.

```bash
python3 .cursor/context/context-builder.py \
  --phase review \
  --task "post-module skill scan for {feature_name}; modulesSinceLastProposal=N; pass=full|lightweight" \
  --agent learning-agent \
  --keywords "retrospective,pattern,skill,learning,gotcha,shortcut" \
  --budget 5000
```

- Replace `N` with the real counter. Set `pass=full` when `N >= 5`, else `pass=lightweight`.
- **Hard-gate:** learning-agent must re-read the state file; do not rely on chat memory for `N`.
- Agent writes `docs/reviews/YYYY-MM-DD-skill-update-proposal.md` when a pattern is found (`PENDING_APPROVAL`) and **resets** `modulesSinceLastProposal` to `0`.
- Apply patches only after orchestrator/human approval (or run `/skill-update` for an explicit full pass).

Output summary:
```
✅ Module {feature_name} complete
Plan: docs/plans/...
Review: docs/reviews/...
Fix loops: N
Files changed: [list]
Memory updated: decisions/gotchas/shortcuts (yes/no)
Retrospective: appended
Learning: dispatched @learning-agent → [no pattern | proposal path]
modulesSinceLastProposal: N
```

Clean up: optionally archive `.cursor/state/module-{feature_name}-loop.json` to `docs/plans/` for traceability.
