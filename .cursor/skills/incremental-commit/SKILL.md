---
name: incremental-commit
description: Commit after each breakdown task with structured Conventional Commits, green build+relevant tests, and small diffs. Use during implement-backend, implement-frontend, database, and devops.
---

# Incremental Commit

Canonical rules: **AGENTS.md §11**. This skill is the agent checklist.

## Rule

Commit **after each task** in the plan breakdown — not one giant commit at module end.

## Message structure (required)

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Subject line

| Rule | Detail |
|------|--------|
| Format | `type(scope): subject` |
| Length | **≤ 72 characters** total preferred; hard stop ~100 |
| Voice | Imperative, present: `add`, `fix`, `register` — not `added` / `adds` |
| Case | Lowercase after colon; **no** trailing period |
| Focus | One logical change; say *what* (and *why* only if not obvious) |

**Good**

```
feat(auth): add refresh token rotation
fix(api): apply tenant filter on list query
chore(skills): register saas-product-ui in manifest
docs(v2): summarize memory and product-ui rollout
```

**Bad**

```
feat: updates
Fixed bug.
feat(auth): Added Refresh Token Rotation And Also Refactored Middleware.
```

### Types

| Type | Use when |
|------|----------|
| `feat` | User-visible or workflow capability |
| `fix` | Correctes incorrect behavior |
| `refactor` | Behavior-preserving restructure |
| `docs` | Docs / comments only |
| `test` | Tests only |
| `chore` | Tooling, manifest, deps, non-product config |
| `perf` | Performance only |
| `style` | Formatting only (no logic) |
| `ci` | CI config only |

### Scope

Short kebab-case area: module, package, or workflow area.

Examples: `auth`, `billing`, `web`, `api`, `db`, `skills`, `agents`, `workflow`, `v2`.

Omit scope only when the change is truly repo-wide and no single area fits: `chore: bump node to 22`.

### Body (optional → required if non-obvious)

- Blank line after subject
- Wrap ~72 chars
- Bullets OK; explain **why** / tradeoffs / migration notes
- Do not repeat the subject

```
feat(billing): show invoice download in settings

Stripe portal already manages plan changes; this only exposes
historical invoices in-product for support load.
```

### Footer (optional)

```
BREAKING CHANGE: <description>
Refs: <ticket-or-plan>
Closes: #123
```

`BREAKING CHANGE:` must be exact prefix when API/contract/behavior breaks.

## Gate before each commit

1. **Build** for the touched package/app passes.
2. **Relevant tests** for the change pass.
3. Diff is reviewable and matches the subject (no drive-by files).
4. Message matches structure above.

## Size guideline

- Target **≤ 200 lines** diff per commit.
- Split by layer or task: schema → API → UI.

## Never commit

- Debug leftovers (`console.log` in prod paths)
- Commented-out dead code “for later”
- `.env` or real secrets
- Unrelated refactors mixed into a feature commit

## Workflow

1. Finish one breakdown task + acceptance checks
2. Stage **only** files for that task
3. Write message: type + scope + imperative subject [+ body if needed]
4. Commit → next task (respect Task Dependencies)

## Anti-patterns

- ❌ Mega-commit for whole module
- ❌ Red build “to save progress”
- ❌ Subject describes files (`update SKILL.md`) instead of intent
- ❌ Multiple unrelated verbs in one subject
- ❌ Ticket-only subject (`feat: JIRA-1234`) with no description
