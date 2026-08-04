# Generic Workflow Phases

## Standard Phase Chain

```text
explore → plan → execute → verify → review → loop-or-complete
```

## UI-scoped chain (Design Specification)

When the module has visible UI:

```text
brainstorm → planning-overview → design-specification ⏸️ → design-judge
                → breakdown → breakdown-judge → execute → test → verify
```

- **design-specification:** `@designer-worker` writes Design Contract + sketches  
  (`docs/design/_templates/design-contract.v1.md`)
- **design-judge:** `@judge-agent` mode design-contract → `DESIGN_APPROVED`
- Non-UI modules: `DESIGN-SPEC: N/A — no visible UI`

See `.cursor/skills/planning/references/design-specification-phase.md`.

## Per-Module Development Loop (`/dev-module`)

```text
brainstorm → plan ⏸️ → execute → test → verify
                                          │
                              APPROVED ───┘──────────────▶ done ✅
                              CHANGES_REQUESTED (loop < 3) ──▶ fix → test → verify
                              CHANGES_REQUESTED (loop ≥ 3) ───▶ escalate ⏸️
```

For UI modules, expand `plan` into: overview → design-specification → design-judge → breakdown.

## Phase Routing

| User intent | Loader phase | Typical owner |
|---|---|---|
| Explore options, prior art | `brainstorm` | architect-planner |
| Create task breakdown, ADR | `plan` | architect-planner |
| Design Contract + sketches | `design` | designer-worker |
| Define contracts / schema | `design` | planner + specialist |
| Implement backend / server | `implement-backend` | backend-worker |
| Implement frontend / UI | `implement-frontend` | frontend-worker |
| Database / storage change | `database` | database-worker |
| Infrastructure / release | `devops` | devops-worker |
| Run tests, write coverage | `test` | qa-worker |
| Fix failing tests / issues | `fix` | responsible worker |
| Quality gate / review | `review` | judge-agent / qa-worker / security-worker |
| Full module from scratch | `dev-module` | orchestrator → all workers |

## Loop State File

Per-module loop state: `.cursor/state/module-{name}-loop.json`

```json
{
  "feature": "feature-name",
  "phase": "brainstorm | plan | design-specification | execute | test | verify | fix | done | escalate",
  "loopCount": 0,
  "planPath": "docs/plans/YYYY-MM-DD-feature.md",
  "designContractPath": "docs/design/YYYY-MM-DD-feature.spec.md",
  "reviewPath": "docs/reviews/YYYY-MM-DD-feature-review.md"
}
```

## Protected Change Rule

Protected status comes from `.cursor/config/protected-paths.json`. If protected, require current plan and review artifacts unless a logged override is approved.
