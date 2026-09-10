---
name: wf-fix
description: Day-path code-loop. Use when user says fix, bug, regression, hotfix, or wants /fix behavior. Reproduce → minimal patch → verify.
---

# Workflow: fix (day path)

This encodes `.cursor/commands/fix.md` for Codex.

## Steps

1. Read AGENTS.md §0 layers and relevant stack.
2. Activate error-recovery: read `.cursor/skills/error-recovery/SKILL.md`.
3. Reproduce or state reproduction steps; identify root cause.
4. Minimal patch only; no drive-by refactors.
5. Run available tests/lint for touched areas.
6. If protected paths involved, recommend judge review and `docs/reviews/` note.
7. Optional: read `.cursor/commands/fix.md` for full command checklist if present.

## Anti-patterns

- Full feature redesign under a "fix" request
- Ignoring off layers
- Skipping verification
