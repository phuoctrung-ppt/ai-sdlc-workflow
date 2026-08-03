---
name: dev-module
description: Full per-module development loop — brainstorm → plan → execute → test → verify → fix → loop → done + Memory distillation + learning-agent + office UI events.
---

# Module Development Loop

Act as **Orchestrator**. Run the full development loop for module: **{feature_name}**

> **Upstream:** If a `PLAN_APPROVED` breakdown for this module exists under `docs/plans/`, **skip Phase 1–2** — jump to Phase 1.5 / Phase 3.

## Context hygiene (mandatory)

**Do not read or edit** these into the agent context (noise / token waste):

- `.cursor/state/**` (including `workflow-state.json`, `module-*-loop.json`)
- `.aisdlc/state.json`, `.aisdlc/events.jsonl`, `.aisdlc/benchmarks.json`

Resume progress from **`docs/plans/`**, **`docs/module-deps.md`**, and **`docs/memory/*`** only.  
Office UI state is updated solely via `office-event.py` (write-only side effect).

## Office UI (mandatory when `.aisdlc/` exists)

Emit on every phase enter/exit (do **not** `cat` the event log afterward):

```bash
python3 .cursor/scripts/office-event.py --agent <agent-id> --status <working|waiting|done|error|idle> --task "<short>" --phase <phase> --workflow {feature_name}
```

See `.cursor/rules/008-office-ui-events.mdc`.

---

## Phase 0 — Orient (no state JSON)

Load memory + deps only:

```bash
cat docs/memory/decisions.md docs/memory/gotchas.md docs/memory/shortcuts.md 2>/dev/null || true
cat docs/module-deps.md 2>/dev/null || true
```

If an approved plan for `{feature_name}` already exists → start at Phase 1.5 / 3.  
Otherwise start at Phase 1.

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status working --task "Orient / load memory for {feature_name}" --phase restore --workflow {feature_name}
```

---

## Phase 1 — BRAINSTORM

**Agent:** `@architect-planner`

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status working --task "Brainstorm {feature_name}" --phase brainstorm --workflow {feature_name}
python3 .cursor/context/context-builder.py \
  --phase brainstorm --task "{feature_name}" --agent architect-planner
```

Explore similar modules, AGENTS.md §2–§3, prior plans/ADRs, **docs/memory/***.  
Output Brainstorm Summary.

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status done --task "Brainstorm complete: {feature_name}" --phase brainstorm --workflow {feature_name}
```

---

## Phase 2 — PLAN ⏸️ (requires approval)

**Agent:** `@architect-planner`

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status working --task "Plan {feature_name}" --phase plan --workflow {feature_name}
python3 .cursor/context/context-builder.py \
  --phase plan --task "{feature_name}" --agent architect-planner \
  --handoff docs/plans/.active-plan
```

Follow Phase −1 gate + anti-laziness. Write `docs/plans/…`.

On wait for user approval:

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status waiting --task "Await plan approval: {feature_name}" --phase plan --workflow {feature_name}
```

After approval / plan finalized:

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status done --task "Plan ready: {feature_name}" --phase plan --workflow {feature_name}
```

---

## Phase 1.5 — Scaffold (if needed)

```bash
python3 .cursor/scripts/office-event.py --agent scaffold-agent --status working --task "Scaffold shells for {feature_name}" --phase scaffold --workflow {feature_name}
```

Dispatch `@scaffold-agent` when shells are missing.

```bash
python3 .cursor/scripts/office-event.py --agent scaffold-agent --status done --task "Scaffold done" --phase scaffold --workflow {feature_name}
python3 .cursor/scripts/office-event.py --agent scaffold-agent --status idle --task "" --phase scaffold --workflow {feature_name}
```

---

## Phase 3 — EXECUTE

> **Hard-gate — Module Dependencies** — read `docs/module-deps.md`; stop if upstream not `done`.

For **each** task in the breakdown, before dispatching the worker:

```bash
python3 .cursor/scripts/office-event.py --agent <owner-agent-id> --status working --task "<task title>" --phase implement --workflow {feature_name}
```

Worker runs `context-builder.py` with its agent id, implements, then:

```bash
python3 .cursor/scripts/office-event.py --agent <owner-agent-id> --status done --task "<task title> done" --phase implement --workflow {feature_name}
python3 .cursor/scripts/office-event.py --agent <owner-agent-id> --status idle --task "" --phase implement --workflow {feature_name}
```

---

## Phase 4 — TEST

```bash
python3 .cursor/scripts/office-event.py --agent qa-worker --status working --task "Test {feature_name}" --phase test --workflow {feature_name}
python3 .cursor/context/context-builder.py \
  --phase test --task "{feature_name}" --agent qa-worker
```

```bash
python3 .cursor/scripts/office-event.py --agent qa-worker --status done --task "Tests finished" --phase test --workflow {feature_name}
python3 .cursor/scripts/office-event.py --agent qa-worker --status idle --task "" --phase test --workflow {feature_name}
```

---

## Phase 5 — JUDGE + FIX LOOP

```bash
python3 .cursor/scripts/office-event.py --agent judge-agent --status working --task "Review {feature_name}" --phase review --workflow {feature_name}
python3 .cursor/context/context-builder.py \
  --phase review --task "{feature_name}" --agent judge-agent
```

- `*_APPROVED` → Phase 6  
- Critical `*_CHANGES_REQUESTED` → fix loop  
- Minor only → Phase 6  

On Critical fix, for each assigned worker:

```bash
python3 .cursor/scripts/office-event.py --agent <worker> --status working --task "Fix Critical: …" --phase fix --workflow {feature_name}
# … after fix …
python3 .cursor/scripts/office-event.py --agent <worker> --status done --task "Fix applied" --phase fix --workflow {feature_name}
python3 .cursor/scripts/office-event.py --agent judge-agent --status working --task "Re-review {feature_name}" --phase review --workflow {feature_name}
```

When approved:

```bash
python3 .cursor/scripts/office-event.py --agent judge-agent --status done --task "APPROVED {feature_name}" --phase review --workflow {feature_name}
python3 .cursor/scripts/office-event.py --agent judge-agent --status idle --task "" --phase review --workflow {feature_name}
```

---

## Phase 6 — DONE ✅ + Memory + Learning

### A. Distillation (no state JSON)

1. Append `docs/retrospective.md`
2. Facts → **`docs/memory/*` only** (1–5)
3. `docs/module-deps.md` → module `done`

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status working --task "Distill memory for {feature_name}" --phase done --workflow {feature_name}
```

### B. Learning dispatch (lightweight default)

Do **not** read or increment any `workflow-state.json`.  
Dispatch `@learning-agent` for a **lightweight** post-module scan (full pass only via `/skill-update`):

```bash
python3 .cursor/scripts/office-event.py --agent learning-agent --status working --task "Lightweight skill scan after {feature_name}" --phase review --workflow {feature_name}
python3 .cursor/context/context-builder.py \
  --phase review \
  --task "post-module lightweight skill scan for {feature_name}" \
  --agent learning-agent \
  --keywords "retrospective,pattern,skill,learning,gotcha,shortcut" \
  --budget 5000
python3 .cursor/scripts/office-event.py --agent learning-agent --status done --task "Learning pass finished" --phase review --workflow {feature_name}
python3 .cursor/scripts/office-event.py --agent learning-agent --status idle --task "" --phase review --workflow {feature_name}
python3 .cursor/scripts/office-event.py --agent architect-planner --status idle --task "" --phase done --workflow {feature_name}
```

For a full retrospective-wide skill pass, run `/skill-update` separately.

Output summary: Plan / Review / Fix loops / Memory / Retrospective / Learning — **no state.json paths**.

---

## Orchestrator checklist

- [ ] Emit office events on phase enter/exit (write-only)
- [ ] Never `cat` / open `.cursor/state/**` or `.aisdlc/*.json` into context
- [ ] Resume from plans + module-deps + memory only
- [ ] No secrets in `--task`
