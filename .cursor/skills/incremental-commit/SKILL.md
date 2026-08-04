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

**Good (English)**

```
feat(auth): add refresh token rotation
fix(api): apply tenant filter on list query
chore(skills): register saas-product-ui in manifest
docs(v2): summarize memory and product-ui rollout
```

**Ví dụ tốt (tiếng Việt)**

```
feat(auth): thêm xoay vòng refresh token
fix(api): áp dụng bộ lọc tenant trên truy vấn danh sách
chore(skills): đăng ký saas-product-ui vào manifest
docs(v2): tóm tắt memory và rollout product-ui
```

> `type` + `scope` luôn tiếng Anh/ASCII. Subject/body có thể Việt nếu team thống nhất một ngôn ngữ trong repo.

**Bad / Tránh**

```
feat: updates
Fixed bug.
sửa lỗi
feat(auth): Added Refresh Token Rotation And Also Refactored Middleware.
feat(auth): Đã thêm xoay vòng token và refactor middleware luôn
```

### Types

| Type | Use when | Gợi ý (VI) |
|------|----------|------------|
| `feat` | User-visible or workflow capability | Tính năng mới |
| `fix` | Corrects incorrect behavior | Sửa lỗi |
| `refactor` | Behavior-preserving restructure | Đổi cấu trúc, không đổi hành vi |
| `docs` | Docs / comments only | Chỉ tài liệu |
| `test` | Tests only | Chỉ test |
| `chore` | Tooling, manifest, deps, non-product config | Việc lặt vặt / cấu hình |
| `perf` | Performance only | Hiệu năng |
| `style` | Formatting only (no logic) | Format, không logic |
| `ci` | CI config only | CI |

### Scope

Short kebab-case area: module, package, or workflow area.

Examples: `auth`, `billing`, `web`, `api`, `db`, `skills`, `agents`, `workflow`, `v2`.

Omit scope only when the change is truly repo-wide and no single area fits: `chore: bump node to 22`.

### Body (optional → required if non-obvious)

- Blank line after subject
- Wrap ~72 chars
- Bullets OK; explain **why** / tradeoffs / migration notes
- Do not repeat the subject

**English**

```
feat(billing): show invoice download in settings

Stripe portal already manages plan changes; this only exposes
historical invoices in-product for support load.
```

**Tiếng Việt**

```
feat(billing): hiển thị tải hóa đơn trong cài đặt

Cổng Stripe vẫn quản lý đổi gói; commit này chỉ đưa
lịch sử hóa đơn vào trong sản phẩm để giảm tải support.
```

### Footer (optional)

```
BREAKING CHANGE: <description>
Refs: <ticket-or-plan>
Closes: #123
```

`BREAKING CHANGE:` must be exact prefix when API/contract/behavior breaks.

Ví dụ footer:

```
BREAKING CHANGE: đổi tên field tenantId thành workspaceId trên API public
Refs: docs/plans/2026-08-02-v2-implementation-summary.md
Closes: #42
```

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
- ❌ Trộn Anh/Việt lung tung trong cùng một dòng subject không thống nhất team
