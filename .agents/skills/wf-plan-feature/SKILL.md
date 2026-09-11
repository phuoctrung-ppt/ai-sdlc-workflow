---
name: wf-plan-feature
description: Full feature planning for structural changes. Use when user asks plan-feature or architecture plan beyond shape-lite.
---

# Workflow: plan-feature

1. Confirm structural need (else redirect to wf-shape-lite or wf-fix).
2. Follow planning + agentic-workflow skills under `.cursor/skills/`.
3. Output `docs/plans/YYYY-MM-DD-feature-name.md`; ADR if stack decision.
4. Respect layers; list worker handoffs, not implementation dump.
5. Optional: `.cursor/commands/plan-feature.md` checklist.
