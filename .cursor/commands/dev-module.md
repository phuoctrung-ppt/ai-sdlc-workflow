---
name: dev-module
description: Full per-module development loop — brainstorm → plan → execute → test → verify → fix → loop → done + Memory distillation + learning-agent + office UI events.
---

# Module Development Loop

Act as **Orchestrator**. Run the full development loop for module: **{feature_name}**

State file: `.cursor/state/module-{feature_name}-loop.json` (created/updated at each phase transition)

> **Upstream:** If a `PLAN_APPROVED` breakdown for this module exists under `docs/plans/`, **skip Phase 1–2** — jump to Phase 1.5 / Phase 3.

## Office UI (mandatory)

When `.aisdlc/` exists, **emit an event on every phase enter/exit** so `ai-sdlc ui` (:9669) shows live desks:

```bash
python3 .cursor/scripts/office-event.py --agent <agent-id> --status <working|waiting|done|error|idle> --task "<short>" --phase <phase>
```

See `.cursor/rules/008-office-ui-events.mdc`. Prefer the script above (no global `ai-sdlc` required).

---

## Phase 0 — Restore State (if resuming)

Check `.cursor/state/module-{feature_name}-loop.json` or approved plan; set starting phase.

Load memory:
```bash
cat docs/memory/decisions.md docs/memory/gotchas.md docs/memory/shortcuts.md 2>/dev/null || true
cat docs/module-deps.md 2>/dev/null || true
```

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status working --task "Restore state / load memory for {feature_name}" --phase restore
```

---

## Phase 1 — BRAINSTORM

**Agent:** `@architect-planner`

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status working --task "Brainstorm {feature_name}" --phase brainstorm
python3 .cursor/context/context-builder.py \
  --phase brainstorm --task "{feature_name}" --agent architect-planner
```

Explore similar modules, AGENTS.md §2–§3, prior plans/ADRs, **docs/memory/***.
Output Brainstorm Summary. Save state → `phase: plan`.

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status done --task "Brainstorm complete: {feature_name}" --phase brainstorm
```

---

## Phase 2 — PLAN ⏸️ (requires approval)

**Agent:** `@architect-planner`

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status working --task "Plan {feature_name}" --phase plan
python3 .cursor/context/context-builder.py \
  --phase plan --task "{feature_name}" --agent architect-planner \
  --handoff docs/plans/.active-plan
```

Follow Phase −1 gate + anti-laziness. Write `docs/plans/…`.
On wait for user approval:

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status waiting --task "Await plan approval: {feature_name}" --phase plan
```

After approval / plan finalized:

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status done --task "Plan ready: {feature_name}" --phase plan
```

---

## Phase 1.5 — Scaffold (if needed)

```bash
python3 .cursor/scripts/office-event.py --agent scaffold-agent --status working --task "Scaffold shells for {feature_name}" --phase scaffold
```

Dispatch `@scaffold-agent` when shells are missing.

```bash
python3 .cursor/scripts/office-event.py --agent scaffold-agent --status done --task "Scaffold done" --phase scaffold
python3 .cursor/scripts/office-event.py --agent scaffold-agent --status idle --task "" --phase scaffold
```

---

## Phase 3 — EXECUTE

> **Hard-gate — Module Dependencies** — read `docs/module-deps.md`; stop if upstream not `done`.

For **each** task in the breakdown, before dispatching the worker:

```bash
python3 .cursor/scripts/office-event.py --agent <owner-agent-id> --status working --task "<task title>" --phase implement
```

Worker runs `context-builder.py` with its agent id, implements, then:

```bash
python3 .cursor/scripts/office-event.py --agent <owner-agent-id> --status done --task "<task title> done" --phase implement
python3 .cursor/scripts/office-event.py --agent <owner-agent-id> --status idle --task "" --phase implement
```

Parallel tasks → multiple agents `working` at once (emit for each).

---

## Phase 4 — TEST

```bash
python3 .cursor/scripts/office-event.py --agent qa-worker --status working --task "Test {feature_name}" --phase test
python3 .cursor/context/context-builder.py \
  --phase test --task "{feature_name}" --agent qa-worker
```

```bash
python3 .cursor/scripts/office-event.py --agent qa-worker --status done --task "Tests finished" --phase test
python3 .cursor/scripts/office-event.py --agent qa-worker --status idle --task "" --phase test
```

---

## Phase 5 — JUDGE + FIX LOOP

```bash
python3 .cursor/scripts/office-event.py --agent judge-agent --status working --task "Review {feature_name}" --phase review
python3 .cursor/context/context-builder.py \
  --phase review --task "{feature_name}" --agent judge-agent
```

- `*_APPROVED` → Phase 6  
- Critical `*_CHANGES_REQUESTED` → fix loop (`loopCount++`)  
- Minor only → Phase 6  

On Critical fix, for each assigned worker:

```bash
python3 .cursor/scripts/office-event.py --agent <worker> --status working --task "Fix Critical: …" --phase fix
# … after fix …
python3 .cursor/scripts/office-event.py --agent <worker> --status done --task "Fix applied" --phase fix
python3 .cursor/scripts/office-event.py --agent judge-agent --status working --task "Re-review {feature_name}" --phase review
```

When approved:

```bash
python3 .cursor/scripts/office-event.py --agent judge-agent --status done --task "APPROVED {feature_name}" --phase review
python3 .cursor/scripts/office-event.py --agent judge-agent --status idle --task "" --phase review
```

---

## Phase 6 — DONE ✅ + Memory + Learning

Save final state: `{ "phase": "done", "loopCount": N }`

### A. Distillation

1. Append `docs/retrospective.md`
2. Facts → **`docs/memory/*` only** (1–5)
3. `docs/module-deps.md` → module `done`

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status working --task "Distill memory for {feature_name}" --phase done
```

### B. Learning counter + dispatch

1. Increment `modulesSinceLastProposal` in `.cursor/state/workflow-state.json`
2. Dispatch `@learning-agent`:

```bash
python3 .cursor/scripts/office-event.py --agent learning-agent --status working --task "Skill scan after {feature_name}" --phase review
python3 .cursor/context/context-builder.py \
  --phase review \
  --task "post-module skill scan for {feature_name}; modulesSinceLastProposal=N; pass=full|lightweight" \
  --agent learning-agent \
  --keywords "retrospective,pattern,skill,learning,gotcha,shortcut" \
  --budget 5000
python3 .cursor/scripts/office-event.py --agent learning-agent --status done --task "Learning pass finished" --phase review
python3 .cursor/scripts/office-event.py --agent learning-agent --status idle --task "" --phase review
python3 .cursor/scripts/office-event.py --agent architect-planner --status idle --task "" --phase done
```

Output summary includes Memory / Retrospective / Learning / **office events emitted**.

---

## Orchestrator checklist

- [ ] Emit on every phase enter/exit
- [ ] Emit per worker task in Phase 3 / fix loop
- [ ] Never skip emits when `.aisdlc/` exists
- [ ] No secrets in `--task`
