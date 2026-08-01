# Review: Portable Core Workflow Trim

**Date:** 2026-08-01  
**Reviewer:** judge-agent  
**Plan:** `docs/plans/2026-08-01-portable-core-trim.md`  
**Handoff:** `.cursor/context/handoffs/portable-core-trim.json`

```
Status: TASK_APPROVED
```

## Scope Reviewed
- Plan/issue: `docs/plans/2026-08-01-portable-core-trim.md`
- Handoff: `.cursor/context/handoffs/portable-core-trim.json`
- Files: `.cursor/agents/*`, `.cursor/config/worker-scopes.json`, `.cursor/skills/skills-manifest.json`, `.cursor/skills/optional/**`, `.cursor/skills/taste-design/**`, `.cursor/skills/databases/**`, `AGENTS.md` §5
- Commands: filesystem `test`/`ls`; Python JSON path verify over `portableSkills` + `skills` (entry + `skillsRoot/referencesDir/key`); `rg` on AGENTS.md / databases SKILL.md
- Review mode: task
- Out of scope (not scored as failures): `skills-manifest.v2.json`, hooks, commands, rules, skill-loader

## Acceptance Criteria (1–15)

| AC | Result | Evidence |
|---|---|---|
| 1 | PASS | `admin-worker.md`, `ai-worker.md` absent under `.cursor/agents/` |
| 2 | PASS | `worker-scopes.json` `agents` has neither `admin-worker` nor `ai-worker` |
| 3 | PASS | `skills-manifest.json` `agents[]` omits both ids |
| 4 | PASS | `.cursor/skills/threejs/`, `.cursor/skills/admin-service/` absent |
| 5 | PASS | No skill `id` in {`threejs`, `admin-service`, `nestjs-scaffold`} |
| 6 | PASS | Four skills under `optional/*/SKILL.md`; top-level trees gone |
| 7 | PASS | Four optional objects: `optional: true`, `activateWhen` starts with `AGENTS.md §2`, `entry` under `optional/` |
| 8 | PASS | Top-level `_commentPortableVsOptional` present (portable vs optional explained) |
| 9 | PASS | taste-design retains `taste-skill`, `brandkit`, `imagegen-frontend-web`, `imagegen-frontend-mobile`, `output-skill` + `llms.txt`; eight prune targets gone |
| 10 | PASS | taste-design `refKeywords` exactly five keeper `*/SKILL.md` keys |
| 11 | PASS | Four `mongodb-*.md` under `optional/databases-mongodb/references/`; absent under `databases/references/` |
| 12 | PASS | `optional/databases-mongodb/SKILL.md` + manifest `databases-mongodb` optional with MongoDB / `AGENTS.md §2` activateWhen |
| 13 | PASS | `databases/references/` = four `postgresql-*.md` only; no mongodb in keywords/refKeywords; SKILL.md does not link `references/mongodb-*.md` (only points to optional skill) |
| 14 | PASS | §5 table has no ai/admin rows; optional note at L117 only mentions those ids |
| 15 | PASS | Path verify: 56 entry/ref checks, `MISSING []`, exit 0 |

## Critical
- None.

## Suggestions
- **Known drift (out of scope):** `skills-manifest.v2.json` may still list deleted agents/skills while context-builder prefers v2 — track a follow-up so loaders do not resurrect trimmed roster entries.
- **Residual mentions (accepted risk):** `databases/scripts` and Cursor Task-tool enums may still name MongoDB / `admin-worker` / `ai-worker`; plan marked these out of scope.
- **Pointer wording:** `databases/SKILL.md` still mentions MongoDB as a redirect to the optional skill — intentional and within AC13 (no `references/mongodb-*` links).

## Verified
- Spec compliance: Tasks 1–7 acceptance met on disk and in `skills-manifest.json`.
- Scope discipline: changes match handoff in-scope paths; out-of-scope paths not required for approval.
- Workflow integrity: plan + handoff + `.active-plan` → `docs/plans/2026-08-01-portable-core-trim.md`; AGENTS.md §5 synced; Domain Config Sync N/As for ADR/architecture respected.
- Security: filesystem/JSON/markdown only — no secrets, no query/auth surface changes.
- Testing: N/A for this packaging change; AC15 path self-verify is the required verification gate and passed.

## Pattern Candidates
- [ ] propose: `portable-vs-optional-skills` → `.cursor/patterns/` (optional: document `optional: true` + `activateWhen` + `optional/` layout for future ports)

## Fix Assignment
N/A — no `*_CHANGES_REQUESTED`.
