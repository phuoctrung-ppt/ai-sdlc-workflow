# Portable Core Workflow Trim
**Goal:** Strip domain-specific agents and skills from the portable core, move stack-gated skills under `.cursor/skills/optional/`, prune taste-design to five keepers, and split MongoDB out of the databases skill.
**Protected:** yes | **Agents:** architect-planner, judge-agent

## Constraints
- Workflow-infra only; no application business logic.
- Do not touch hooks, commands, rules, `workflow-guard.py`, `skill-loader.py`, or any `docs/**` product/architecture files (this plan file + `.active-plan` + handoff are planning artifacts only).
- Do not edit `.cursor/skills/skills-manifest.v2.json` (out of scope; record drift risk).
- Gate skipped: workflow-meta — AGENTS.md §1–§3 still have `<PLACEHOLDER>`; product planning would stop; this task is roster/skill-tree cleanup with user-locked paths including AGENTS.md §5 only.

## Source Evidence
- `.cursor/agents/admin-worker.md` and `.cursor/agents/ai-worker.md` exist; listed in `AGENTS.md` §5 rows and in `.cursor/config/worker-scopes.json` `agents.admin-worker` / `agents.ai-worker`.
- `.cursor/skills/skills-manifest.json` `agents[]` includes `admin-worker`, `ai-worker`; `skills[]` includes `admin-service`, `nestjs-scaffold`, `nestjs-skills`, `bullmq-worker`, `zod-shared-types`, `ai-llm-integration`. **No** `threejs` entry in this manifest (folder still on disk).
- On disk: `.cursor/skills/threejs/`, `.cursor/skills/admin-service/`, taste-design keepers + eight prune targets, four MongoDB refs under `.cursor/skills/databases/references/mongodb-*.md`.
- `.cursor/skills/databases/SKILL.md` still documents MongoDB + PostgreSQL and links the four mongodb reference files.

SECTION 1 COMPLETE

## Acceptance Criteria
1. Files `.cursor/agents/admin-worker.md` and `.cursor/agents/ai-worker.md` do not exist.
2. `.cursor/config/worker-scopes.json` has no `agents.admin-worker` key and no `agents.ai-worker` key.
3. `.cursor/skills/skills-manifest.json` `agents` array does not contain `admin-worker` or `ai-worker`.
4. Directory `.cursor/skills/threejs/` does not exist; directory `.cursor/skills/admin-service/` does not exist.
5. `.cursor/skills/skills-manifest.json` has no skill object with `id` equal to `threejs`, `admin-service`, or `nestjs-scaffold`.
6. Paths exist: `.cursor/skills/optional/nestjs-skills/SKILL.md`, `.cursor/skills/optional/bullmq-worker/SKILL.md`, `.cursor/skills/optional/zod-shared-types/SKILL.md`, `.cursor/skills/optional/ai-llm-integration/SKILL.md`; corresponding trees are absent from `.cursor/skills/nestjs-skills`, `.cursor/skills/bullmq-worker`, `.cursor/skills/zod-shared-types`, `.cursor/skills/ai-llm-integration` (moved, not copied).
7. Each of those four optional skill objects in `skills-manifest.json` has `"optional": true`, an `activateWhen` string starting with `AGENTS.md §2`, and `entry` paths under `optional/`.
8. Manifest top-level includes a `_commentPortableVsOptional` (or equivalent `_comment*`) array/string explaining: `portableSkills` = always-shipped agnostic core; skills with `optional: true` = activate only when `activateWhen` matches `AGENTS.md §2`.
9. Taste-design directories that remain: `taste-skill/`, `brandkit/`, `imagegen-frontend-web/`, `imagegen-frontend-mobile/`, `output-skill/` (plus existing non-skill files such as `llms.txt` if present). Deleted: `brutalist-skill/`, `minimalist-skill/`, `soft-skill/`, `gpt-tasteskill/`, `stitch-skill/`, `redesign-skill/`, `taste-skill-v1/`, `image-to-code-skill/`.
10. Taste-design `refKeywords` in `skills-manifest.json` contains only keys for the five kept `*/SKILL.md` paths (no keys for deleted skills).
11. Files `.cursor/skills/databases/references/mongodb-crud.md`, `mongodb-aggregation.md`, `mongodb-indexing.md`, `mongodb-atlas.md` do not exist under `databases/references/`; they exist under `.cursor/skills/optional/databases-mongodb/references/`.
12. `.cursor/skills/optional/databases-mongodb/SKILL.md` exists and points at those four references; manifest has optional skill `id: databases-mongodb` with `optional: true` and `activateWhen` mentioning MongoDB / `AGENTS.md §2`.
13. `.cursor/skills/databases/references/` contains only the four `postgresql-*.md` files; `databases` skill `keywords` / `refKeywords` have no `mongodb` entries; `databases/SKILL.md` no longer links `references/mongodb-*.md`.
14. `AGENTS.md` §5 table has no `ai-worker` or `admin-worker` rows; a note under the table states optional domain agents/skills are re-enabled from `.cursor/skills/optional/` when the stack requires them.
15. Post-change verification: for every skill in `portableSkills` + `skills`, (a) `skillsRoot/entry` exists; (b) every `refKeywords` key resolves as `skillsRoot/referencesDir/key` when `referencesDir` is set, else `skillsRoot/key`. Do **not** join `refKeywords` keys to `skillsRoot` alone.

SECTION 2 COMPLETE

## Database / API Contract
N/A — filesystem + JSON manifest + markdown roster edits only. No HTTP API, no DB migration, no shared Zod package change.

SECTION 3 COMPLETE

## Files
| Path | Action | Owner |
|---|---|---|
| `.cursor/agents/admin-worker.md` | Delete | architect-planner |
| `.cursor/agents/ai-worker.md` | Delete | architect-planner |
| `.cursor/config/worker-scopes.json` | Modify — remove `agents.admin-worker` and `agents.ai-worker` blocks | architect-planner |
| `.cursor/skills/skills-manifest.json` | Modify — agents[], delete domain entries, move/mark optional, trim taste-design refKeywords, add databases-mongodb, add `_commentPortableVsOptional` | architect-planner |
| `.cursor/skills/threejs/` | Delete entire directory | architect-planner |
| `.cursor/skills/admin-service/` | Delete entire directory | architect-planner |
| `.cursor/skills/nestjs-skills/` | Move → `.cursor/skills/optional/nestjs-skills/` | architect-planner |
| `.cursor/skills/bullmq-worker/` | Move → `.cursor/skills/optional/bullmq-worker/` | architect-planner |
| `.cursor/skills/zod-shared-types/` | Move → `.cursor/skills/optional/zod-shared-types/` | architect-planner |
| `.cursor/skills/ai-llm-integration/` | Move → `.cursor/skills/optional/ai-llm-integration/` | architect-planner |
| `.cursor/skills/taste-design/brutalist-skill/` | Delete | architect-planner |
| `.cursor/skills/taste-design/minimalist-skill/` | Delete | architect-planner |
| `.cursor/skills/taste-design/soft-skill/` | Delete | architect-planner |
| `.cursor/skills/taste-design/gpt-tasteskill/` | Delete | architect-planner |
| `.cursor/skills/taste-design/stitch-skill/` | Delete | architect-planner |
| `.cursor/skills/taste-design/redesign-skill/` | Delete | architect-planner |
| `.cursor/skills/taste-design/taste-skill-v1/` | Delete | architect-planner |
| `.cursor/skills/taste-design/image-to-code-skill/` | Delete | architect-planner |
| `.cursor/skills/databases/references/mongodb-crud.md` | Move → `.cursor/skills/optional/databases-mongodb/references/mongodb-crud.md` | architect-planner |
| `.cursor/skills/databases/references/mongodb-aggregation.md` | Move → `.cursor/skills/optional/databases-mongodb/references/mongodb-aggregation.md` | architect-planner |
| `.cursor/skills/databases/references/mongodb-indexing.md` | Move → `.cursor/skills/optional/databases-mongodb/references/mongodb-indexing.md` | architect-planner |
| `.cursor/skills/databases/references/mongodb-atlas.md` | Move → `.cursor/skills/optional/databases-mongodb/references/mongodb-atlas.md` | architect-planner |
| `.cursor/skills/optional/databases-mongodb/SKILL.md` | Create — short MongoDB-only skill | architect-planner |
| `.cursor/skills/databases/SKILL.md` | Modify — PostgreSQL-only description and reference links | architect-planner |
| `AGENTS.md` | Modify — §5 roster only (remove two rows + optional note) | architect-planner |
| `docs/plans/2026-08-01-portable-core-trim.md` | Create — this plan | architect-planner |
| `docs/plans/.active-plan` | Modify — point to this plan | architect-planner |
| `.cursor/context/handoffs/portable-core-trim.json` | Create | architect-planner |

SECTION 4 COMPLETE

## Execution / Task Breakdown

### Task 1 — Delete domain agents + scope/manifest agent refs
- **Owner:** architect-planner
- **Skill:** `agentic-workflow` (`.cursor/skills/agentic-workflow/SKILL.md`)
- **Do:**
  1. Delete `.cursor/agents/admin-worker.md` and `.cursor/agents/ai-worker.md`.
  2. In `.cursor/config/worker-scopes.json`, remove the `admin-worker` and `ai-worker` keys under `agents` (leave `genericRoles.ai` unchanged).
  3. In `.cursor/skills/skills-manifest.json` `agents` array, remove `"admin-worker"` and `"ai-worker"`.
- **Acceptance:** Both agent files gone; `rg '"admin-worker"|"ai-worker"' .cursor/config/worker-scopes.json .cursor/skills/skills-manifest.json` shows no agent-key hits in those two files' agent registries (skill keyword strings inside optional entries may still say `admin` only if not agent id — after Task 3, optional nestjs/ai entries must drop those agent ids from their `agents` arrays).

### Task 2 — Delete threejs, admin-service, nestjs-scaffold manifest entries
- **Owner:** architect-planner
- **Skill:** `agentic-workflow`
- **Do:**
  1. `rm -rf .cursor/skills/threejs .cursor/skills/admin-service`.
  2. Remove skill objects with `id` `admin-service` and `nestjs-scaffold` from `skills-manifest.json`.
  3. Confirm no `id: threejs` object exists (already absent — no-op).
- **Acceptance:** Both directories gone; `jq` / grep finds no `"id": "admin-service"|"nestjs-scaffold"|"threejs"` in the manifest.

### Task 3 — Move four domain skills to optional/ + manifest flags
- **Owner:** architect-planner
- **Skill:** `agentic-workflow`
- **Do:**
  1. Create `.cursor/skills/optional/` if missing.
  2. `git mv` or `mv` each of: `nestjs-skills`, `bullmq-worker`, `zod-shared-types`, `ai-llm-integration` into `.cursor/skills/optional/`.
  3. Update each corresponding skill object: `entry` / `referencesDir` prefixed with `optional/`; set `"optional": true`; set `activateWhen` to:
     - nestjs-skills: `AGENTS.md §2 backend framework is NestJS`
     - bullmq-worker: `AGENTS.md §2 Cache / Queue includes BullMQ`
     - zod-shared-types: `AGENTS.md §2 Shared contracts uses Zod`
     - ai-llm-integration: `AGENTS.md §2 AI / LLM is not none`
  4. Remove `admin-worker` from nestjs-skills `agents` array; remove `ai-worker` from ai-llm-integration `agents` array (replace with `backend-worker` only if empty — keep `backend-worker`).
  5. Add top-level `_commentPortableVsOptional` explaining portableSkills vs optional skills.
- **Acceptance:** Old top-level skill dirs absent; optional paths exist; four entries have `optional: true` and `activateWhen` + valid `entry` files on disk.

### Task 4 — Prune taste-design
- **Owner:** architect-planner
- **Skill:** `taste-design` (`.cursor/skills/taste-design/taste-skill/SKILL.md`) for path awareness only
- **Do:**
  1. Delete the eight skill directories listed in Acceptance #9.
  2. Rewrite taste-design `refKeywords` to only:
     - `taste-skill/SKILL.md`
     - `brandkit/SKILL.md`
     - `imagegen-frontend-web/SKILL.md`
     - `imagegen-frontend-mobile/SKILL.md`
     - `output-skill/SKILL.md`
  3. Drop obsolete keywords that only served deleted skills if they appear solely for those (`brutalist`, `minimalist`, `stitch`, `image-to-code`, `redesign` as standalone trigger words) — keep shared words like `design`, `brand`, `imagegen`.
- **Acceptance:** Only five skill dirs remain under taste-design (plus `llms.txt`); `refKeywords` has exactly those five keys; each key file exists.

### Task 5 — Split MongoDB from databases
- **Owner:** architect-planner
- **Skill:** `databases` (`.cursor/skills/databases/SKILL.md`)
- **Do:**
  1. Create `.cursor/skills/optional/databases-mongodb/references/`.
  2. Move the four `mongodb-*.md` files into that references dir.
  3. Create `.cursor/skills/optional/databases-mongodb/SKILL.md` (~30–60 lines): when to use, link the four refs, `activateWhen` MongoDB.
  4. Add manifest skill `databases-mongodb` with `optional: true`, `activateWhen`: `AGENTS.md §2 Database includes MongoDB`, `entry`: `optional/databases-mongodb/SKILL.md`, `referencesDir`: `optional/databases-mongodb/references`, agents `database-worker` + `backend-worker`.
  5. Edit `.cursor/skills/databases/SKILL.md` to PostgreSQL-only (remove MongoDB sections and mongodb reference links).
  6. In manifest `databases` skill: remove `mongodb` from `keywords`; ensure `refKeywords` only lists the four `postgresql-*.md` files.
- **Acceptance:** AC 11–13 pass; optional SKILL.md exists.

### Task 6 — Update AGENTS.md §5
- **Owner:** architect-planner
- **Skill:** `agentic-workflow`
- **Do:**
  1. Delete the `ai-worker` and `admin-worker` table rows from §5.
  2. After the roster table, add note: `Optional domain agents (ai-worker, admin-worker) and stack-gated skills: enable by restoring agent files under .cursor/agents/ (and worker-scopes) and/or copying or activating skills from .cursor/skills/optional/ when AGENTS.md §2 requires them.`
- **Acceptance:** `rg 'admin-worker|ai-worker' AGENTS.md` finds only the optional note line(s), not table rows.

### Task 7 — Manifest path self-verify + handoff
- **Owner:** architect-planner
- **Do:**
  1. Script/check: for every skill `entry`, assert `Path(skillsRoot)/entry` exists. For every `refKeywords` key, assert `Path(skillsRoot)/referencesDir/key` exists (fallback `Path(skillsRoot)/key` only if `referencesDir` missing).
  2. Write `.cursor/context/handoffs/portable-core-trim.json`.
  3. Set `docs/plans/.active-plan` to `docs/plans/2026-08-01-portable-core-trim.md`.
- **Acceptance:** Self-verify exits 0; handoff JSON parses; `.active-plan` matches.

**Ordering:** Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6 → Task 7 (Task 4 independent of Task 5; both after Task 3).

SECTION 5 COMPLETE

## Risks
- `.cursor/skills/skills-manifest.v2.json` still lists deleted agents/skills; context-builder currently prefers v2 — out of scope here; follow-up required or loaders will drift.
- Agent markdown deleted but Cursor Task-tool enum / other docs may still name `admin-worker` / `ai-worker` — out of scope.
- `databases/scripts/*.py` may still mention MongoDB; out of scope unless a script path is listed in manifest `scripts` (leave scripts; SKILL.md PostgreSQL-focused).
- Moving skills breaks absolute paths in any unchecked docs; docs/ edits out of scope.

## Handoffs
→ `.cursor/context/handoffs/portable-core-trim.json`

## Domain Config Sync
- [ ] ADR — **N/A** — no runtime architecture decision; workflow packaging only
- [ ] `docs/architecture.md` — **N/A** — out of scope (docs/)
- [x] `AGENTS.md` — §5 roster only (Task 6)
- [x] `.cursor/config/worker-scopes.json` — remove two agent keys (Task 1)
- [x] `.cursor/skills/skills-manifest.json` — Tasks 1–5, 7
- [ ] `protected-paths.json` — **N/A** — no new protected globs
- [x] `docs/plans/.active-plan` — set on plan write

SECTION 6 COMPLETE
