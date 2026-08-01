---
name: incremental-commit
description: Commit after each breakdown task with Conventional Commits, green build+relevant tests, and small diffs. Use during implement-backend, implement-frontend, database, and devops.
---

# Incremental Commit

## Rule

Commit **after each task** in the plan breakdown — not one giant commit at module end.

## Message format

Follow Conventional Commits in `AGENTS.md` §11:

```
type(scope): description
```

Examples: `feat(auth): add refresh rotation`, `fix(api): correct tenant filter`, `chore(workflow): register spike-agent`.

## Gate before each commit

1. **Build** for the touched package/app passes (project’s build/typecheck command).
2. **Relevant tests** for the change pass (unit/integration for touched modules — full suite not required every time).
3. Diff is reviewable.

## Size guideline

- Target **≤ 200 lines** of diff per commit.
- If larger, **split** by layer or by task (e.g. schema → API → UI) into multiple commits.

## Never commit

- `console.log` / debug leftovers in production paths
- Commented-out dead code left “for later”
- `.env` files or real secret values
- Hardcoded secrets, tokens, or API keys

## Workflow

1. Finish one breakdown task + its acceptance checks
2. Stage only files for that task
3. Commit with a Conventional Commit message
4. Proceed to the next task (respect Task Dependencies)

## Anti-patterns

- ❌ One mega-commit for the whole module
- ❌ Commit red build “to save progress”
- ❌ Mixing unrelated refactors into a feature commit
