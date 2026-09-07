# UI work in plans — DESIGN-GATE + Design Specification

When the feature includes **visible UI**:

## Ordering (mandatory)

1. **Planning Overview** — stories, coverage, architecture.
2. **Design Specification** — `@designer-worker` authors Design Contract + sketches  
   Template: `docs/design/_templates/design-contract.v1.md`  
   Output: `docs/design/YYYY-MM-DD-{feature}.spec.md`  
   Sketches: `docs/design/sketches/{feature}/`
3. **Design Judge** — `@judge-agent` mode design-contract → `DESIGN_APPROVED`.
4. **Breakdown** — only after design approved; frontend tasks reference contract paths.
5. **Execute** — frontend implements contract numbers; no inventing layout/type.

## Plan task requirements

1. Add **Task — Design Specification** owned by `designer-worker` **before** any `frontend-worker` UI task.
2. Acceptance criteria must name real paths, e.g.:
   - `docs/design/YYYY-MM-DD-{feature}.spec.md` exists and passes specificity (numbers/enums)
   - `docs/design/sketches/{feature}/` has ≥1 reference (imagegen or wire)
   - Track + domain pack + dials + hard-rules section present
3. Frontend task acceptance: “matches Design Contract layout/type/states; DESIGN-GATE satisfied”.
4. Domain hints:
   - Knowledge hub / workspace app → `knowledge-hub-saas`
   - VN SME marketing landing → `sme-marketing-vn` + taste-design
5. Visual pipeline: `.cursor/skills/taste-design/ui-visual-pipeline.md`
6. Phase doc: `.cursor/skills/planning/references/design-specification-phase.md`

## Judge

- Plan review: missing designer-before-frontend ordering → **Critical** for UI-scoped plans.
- Design Contract review: soft-only fields, missing layout numbers, missing sketches → **Critical**.
- Task/branch review: UI shipped without contract match → **Critical**.
