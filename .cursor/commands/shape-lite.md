---
name: shape-lite
description: Compact idea shaping for indie continuous ship. Produce a short shape note (not a full plan). Optional path into plan-feature or direct code-loop.
---

# Shape-Lite (new idea / small feature)

**When to use:** new idea, small feature, “should we build X?”, quick scope before coding — without running the full `/plan-feature` or `/dev-module` ceremony.

**When NOT to use:** already-approved plan, pure bugfix → use `/fix`; large multi-module product → `/plan-feature`.

Act as **Architect Planner** in **shape-lite** mode only.

## Goal

Write a **single short shape note** (≤ ~80 lines) that lets an indie decide:

1. Ship now via `/fix` or implement-small, or
2. Escalate to full plan + Design Contract, or
3. Drop / defer.

## Hard constraints

1. **No full ADR stack, no task tables of 20 rows, no DESIGN-GATE** unless the idea is clearly UI-heavy and user asks to continue.
2. Prefer portable skills already rated high in this repo:
   - `planning` (compact)
   - `agentic-workflow`
   - `api-contract-first` (only if API surface changes)
   - `saas-product-ui` / `taste-design` — only mention if UI is in scope; do not generate marketing slop
3. Domain-agnostic: do not assume AI Workspace or any specific product domain.

## Steps

### 0 — Context

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status working --task "Shape-lite: {idea}" --phase plan --workflow shape-lite
python3 .cursor/context/context-builder.py \
  --phase plan \
  --task "shape-lite: {idea}" \
  --agent architect-planner \
  --keywords "shape,scope,mvp,indie" \
  --budget 4000
```

### 1 — Write shape note

Path: `docs/plans/shape/YYYY-MM-DD-{slug}.md`  
Template: `docs/plans/_templates/shape-lite.md`

Fill every section briefly. Prefer bullets over prose.

### 2 — Recommend next command

End the shape note with exactly one of:

- `NEXT: /fix` — if the work is a small patch on existing code
- `NEXT: implement-small` — if greenfield but ≤ ~3 files, no schema, no new UI system
- `NEXT: /plan-feature` — if multi-module, protected, or needs ADR
- `NEXT: design-spec` — if new visible UI needs Design Contract first
- `NEXT: drop` — if not worth building now

### 3 — Done

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status done --task "Shape-lite ready: {idea}" --phase plan --workflow shape-lite
```

Point `docs/plans/.active-plan` at the shape note **only if** user chooses to continue from it.

Do not dispatch workers from shape-lite unless user explicitly says to implement.
