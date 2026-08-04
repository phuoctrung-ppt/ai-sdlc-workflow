# UI work in plans — DESIGN-GATE

When the feature includes visible UI:

1. Add **Task N — Design** owned by `designer-worker` **before** any `frontend-worker` UI task.
2. Acceptance criteria must name real paths, e.g.:
   - `docs/design/YYYY-MM-DD-{feature}.md` exists
   - `docs/design/sketches/{feature}/` has ≥1 reference (imagegen or wire)
   - Track + domain pack + hard-rules section present
3. Frontend task acceptance: “matches sketch hierarchy; DESIGN-GATE satisfied”.
4. Domain hints:
   - Knowledge hub / workspace app → `knowledge-hub-saas`
   - VN SME marketing landing → `sme-marketing-vn` + taste-design
5. Visual pipeline: `.cursor/skills/taste-design/ui-visual-pipeline.md`

Judge plan review treats missing designer-before-frontend ordering as **Critical** for UI-scoped plans.
