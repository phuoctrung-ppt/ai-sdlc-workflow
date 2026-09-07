# Design Specification phase

Insert **after** Planning Overview (feature coverage approved) and **before** Breakdown when the module has visible UI.

```
Planning Overview  (what to build)
       ↓
Design Specification  (how it should feel / look — numeric contract)
       ↓
Design Judge
       ↓
Breakdown  (tasks that reference contract paths)
       ↓
Execute
```

## Why

Planning and Breakdown gate **feature coverage**.  
They do not lock **experience intent, layout numbers, hierarchy, or component strategy**.  
Without a Design Contract, frontend models invent spacing/type → inconsistent, non-sellable UI.

## Artifact

| Item | Path |
|------|------|
| Contract | `docs/design/YYYY-MM-DD-{feature}.spec.md` |
| Template | `docs/design/_templates/design-contract.v1.md` |
| Sketches | `docs/design/sketches/{feature}/` (≥1) |
| Tokens | `docs/design/tokens.md` |

Contract fields must be **numbers or enums**. Soft-only prose (`premium`, `generous whitespace`, `Linear-like`) without numbers → Design Judge **Critical**.

## Owners

| Step | Agent |
|------|--------|
| Author contract + sketches | `@designer-worker` |
| Design Judge | `@judge-agent` (mode: design-contract) |
| Breakdown UI tasks | `@architect-planner` only after `DESIGN_APPROVED` |
| Implement | `@frontend-worker` (DESIGN-GATE + contract numbers) |

## Skip rule

No visible UI → document in plan:

```text
DESIGN-SPEC: N/A — no visible UI
```

## Plan checklist (UI modules)

1. [ ] Design Spec task before any frontend UI task
2. [ ] Acceptance names `.spec.md` + sketch dir paths
3. [ ] Design Judge required before Breakdown approval for UI scope
4. [ ] Track + domain_pack + dials declared in contract

See also: `ui-design-gate-in-plans.md`, `009-design-gate.mdc`, `ui-visual-pipeline.md`.
