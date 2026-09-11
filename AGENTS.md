# AGENTS.md — <PROJECT_NAME>

> **TEMPLATE — DOMAIN-NEUTRAL.** This repo ships the portable Planner-Worker-Judge workflow with **no** target domain.
> Replace every `<PLACEHOLDER>` and every block tagged `> _EXAMPLE_` with your project's real values when you port this setup.
> **Agents:** if a section below is still a `<PLACEHOLDER>`, treat that fact as *unknown* — gather it from the codebase or ask the orchestrator. **Never invent stack, structure, or compliance facts from an example block.**

> **How to use this file:** This is the canonical domain-config hub for the agentic workflow.
> Every agent reads this file at task start. Generic workflow rules and skills live under `.cursor/` (Cursor) and are mirrored for Codex under `.agents/skills/` + `.codex/`.
>
> **Porting (required):**
> 1. Fill **§0 Project Profile** (profile + layers on/off).
> 2. Fill §1–§3 for layers that are on.
> 3. Cursor: `python3 .cursor/context/profile-sync.py --from-agents` then memory-loader `--sync`.
> 4. Codex: no profile-sync required; honor §0 directly. Optional JSON artifacts still generated only if you run the scripts.
> 5. Optional sections (§4, §9, §14, …): write `N/A — layer off` when the layer is off — do not invent multi-tenant/DB/queue content.

---

## Codex runtime (force design)

> **Read this section when running under OpenAI Codex CLI / IDE / app.**

### Surfaces

| Need | Path |
|------|------|
| Domain config (this file) | `AGENTS.md` |
| Skills (Codex discovery) | `.agents/skills/*/SKILL.md` → bodies in `.cursor/skills/` |
| Multi-agent roles | `.codex/config.toml` + `.codex/agents/*.toml` |
| Setup notes | `docs/codex/SETUP.md` |
| Cursor-only hooks/matrix/loader | `.cursor/**` — optional; do not assume they run inside Codex |

### Operating rules on Codex

1. **Layers first** — §0 is law. Off layer → no plan section, no code, no skill for that layer.
2. **Day path** — prefer skills `$wf-fix` and `$wf-shape-lite`; full `$wf-plan-feature` only for structural change.
3. **Single source of truth for craft** — when a skill activates, **read** the linked `.cursor/skills/.../SKILL.md` (adapters are thin).
4. **Lazy references** — never bulk-read `**/references/**` or `docs/reviews/**`.
5. **Subagents** — do not spawn unless the user asks for parallel agents or the task is clearly multi-track; use roles from `.codex/config.toml`.
6. **Protected changes** — recommend judge role + `docs/reviews/` for protected paths (see `.cursor/config/protected-paths.json` when present).
7. **Forbidden patterns** — §12 always applies.

### Suggested skill triggers

| User intent | Skill |
|-------------|--------|
| Bug / regression | `$wf-fix` + `$error-recovery` |
| Unclear idea | `$wf-shape-lite` |
| Structural feature | `$wf-plan-feature` + `$planning` |
| Product UI | `$saas-product-ui` + `$web-app-ui-ux` |
| API | `$api-contract-first` |
| Security | `$security` |

---

**IMPORTANT** : Always follow the development rules during the coding phase. See `./docs/development-rules.md` when present.

## 0. Project Profile

> **Source of truth for which layers exist.** Planners and workers must treat layer **off** as absent (no plan sections, no workers, no skills for that layer).

| Field | Value |
|---|---|
| **profile** | `<frontend \| backend \| fullstack \| library \| cli>` |
| **layout** | `<single-package \| monorepo>` |

### Layers

| Layer | Status | Notes |
|---|---|---|
| frontend | `<on \| off>` | UI / app shell / pages |
| backend | `<on \| off>` | API / services |
| database | `<on \| off>` | migrations, entities |
| multi-tenancy | `<on \| off>` | if off → §4 = N/A |
| queue | `<on \| off>` | if off → §14 = N/A |
| auth | `<on \| off>` | auth/RBAC surface |
| devops | `<on \| off>` | Docker/CI/infra |
| ai-llm | `<on \| off>` | LLM features |

> _EXAMPLE_ frontend-only: profile=`frontend`, layout=`single-package`, frontend=on, auth=on|off as needed, **all other layers off**.
> _EXAMPLE_ API-only: profile=`backend`, backend=on, database=on|off, auth=on, frontend=off, multi-tenancy=off unless real.

After editing this section (Cursor):

```bash
python3 .cursor/context/profile-sync.py --from-agents
```

---

## 1. Project Overview

| Field | Value |
|---|---|
| **Project Name** | `<name>` |
| **Domain** | `<domain / industry>` |
| **Description** | `<one-sentence description of what the product does>` |

> Layout and tenancy are declared in **§0**, not duplicated here.

---

## 2. Tech Stack (Locked — ADR required to change)

> Fill **only rows for layers that are on** in §0. Delete or mark `N/A` rows for off layers. Once filled, changing a locked choice requires an ADR in `docs/adr/`.

| Layer | Technology | Notes |
|---|---|---|
| Language | `<e.g. TypeScript (strict)>` | |
| Backend framework | `<... \| N/A>` | only if backend=on |
| Frontend framework | `<... \| N/A>` | only if frontend=on |
| Shared contracts | `<schema lib \| N/A>` | |
| Database | `<... \| N/A>` | only if database=on |
| ORM / Migrations | `<... \| N/A>` | only if database=on |
| Cache / Queue | `<... \| N/A>` | only if queue=on |
| AI / LLM | `<provider(s) \| none>` | only if ai-llm=on |
| Object storage | `<... \| N/A>` | |
| Auth | `<... \| N/A>` | only if auth=on |
| Email / Notifications | `<... \| N/A>` | |
| Payments | `<... \| none>` | |
| Infra / Deploy | `<... \| N/A>` | only if devops=on |
| Testing | `<unit / integration / e2e frameworks>` | |

---

## 3. Repository Structure

> Describe the actual layout of THIS repo. Keep in sync with `.cursor/config/worker-scopes.json` when you tighten scopes.

```
<root>/
├── <app-or-package-1>/        # <role>
├── <app-or-package-2>/        # <role>  (omit if single-package)
├── docs/                      # plans, adr, reviews, architecture
├── .cursor/                   # Cursor workflow: agents, skills, hooks, config
├── .agents/skills/            # Codex skill discovery (adapters)
└── .codex/                    # Codex multi-agent roles + config
```

---

## 4. Multi-Tenancy Rules

> **Only if §0 multi-tenancy = on.** Otherwise write exactly: `N/A — layer multi-tenancy off` and skip the rest of this section.

### Tenant Isolation Pattern

Choose and document your tenant column name (e.g. `tenant_id`, `workspace_id`, `org_id`). Every table that belongs to a tenant **MUST** carry `<TENANT_COL> NOT NULL` with an FK to the tenant table.

- **Tenant-scoped tables:** `<list here>`
- **Global / non-tenant tables:** `<list here>`

### Tenant Guard (mandatory on every tenant-scoped query)

> ❗ **NEVER write a tenant-scoped query without a tenant filter — no exceptions, not even in admin convenience methods, unless an explicit, logged override flag is used.**

---

## 5. Agent Roster & Scopes

> **Cursor:** `.cursor/agents/` + matrix + `active-layers.json`.
> **Codex:** `.codex/agents/*.toml` roles registered in `.codex/config.toml`.
> Dispatch is always filtered by §0 layers.

| Agent | Role | Cursor source | Codex role |
|---|---|---|---|
| `architect-planner` | Plan, ADR, breakdown | `.cursor/agents/architect-planner.md` | `architect_planner` |
| `spike-agent` | PoC for `[UNCERTAIN]` | spike-agent.md | `spike` |
| `contract-agent` | API contracts | contract-agent.md | `contract` |
| `scaffold-agent` | Shells only | scaffold-agent.md | `scaffold` |
| `designer-worker` | Design Contract | designer-worker.md | `designer` |
| `backend-worker` | API features | backend-worker.md | `backend` |
| `frontend-worker` | Pages/UI | frontend-worker.md | `frontend` |
| `database-worker` | Migrations | database-worker.md | `database` |
| `devops-worker` | Docker/CI | devops-worker.md | `devops` |
| `security-worker` | Auth/RBAC | security-worker.md | `security` |
| `qa-worker` | Tests | qa-worker.md | `qa` |
| `judge-agent` | Read-only review | judge-agent.md | `judge` |
| `learning-agent` | Skill authoring | learning-agent.md | `learning` |

---

## 6. Domain-Specific Compliance Requirements

> Fill subsections that apply. Delete or N/A when the related layer is off.

### Authentication & Authorization

> Only if auth=on; else `N/A — layer auth off`.

- Every endpoint is **explicitly** public or protected.
- Token strategy: `<...>`.
- RBAC roles: `<list>`. Enforcement: `<guard/middleware>`.

### Multi-Tenancy (if applicable)

> Only if multi-tenancy=on.

- Tenant filter required on every tenant-scoped query (see §4).

### Data Privacy & Compliance

- Applicable regimes: `<e.g. GDPR / none>`.
- PII handling: `<...>`.
- Never log: passwords, tokens, API keys, payment data, or PII.

### AI / LLM Rules

> Only if ai-llm=on; else `N/A — layer ai-llm off`.

- Log every LLM call; enforce cost budget where required.
- Never pass raw user input into a prompt without sanitizing/wrapping.

### Rate Limiting

| Endpoint Category | Limit | Scope |
|---|---|---|
| `<auth>` | `<n req/min>` | `<per IP>` |

---

## 7. Critical Paths (E2E flow targets)

- `<Flow 1>`
- `<Flow 2>`

---

## 8. External Services & Mocking Rules

| Service | Purpose | Mock in tests? | Mock Strategy |
|---|---|---|---|
| `<service>` | `<purpose>` | `<yes/no>` | `<how>` |

---

## 9. Database Entities Reference

> **Only if database=on.** Otherwise: `N/A — layer database off`.

| Entity | Tenant-scoped? | Notes |
|---|---|---|
| `<entity>` | `<yes/no>` | `<notes>` |

---

## 10. Workflow Artifacts

| Artifact Type | Path Pattern | Required For |
|---|---|---|
| Feature plans | `docs/plans/YYYY-MM-DD-feature-name.md` | Structural changes |
| Shape-lite notes | `docs/plans/shape/` | Idea shaping |
| ADRs | `docs/adr/NNNN-short-title.md` | Stack/architecture decisions |
| Design specs | `docs/design/YYYY-MM-DD-{feature}.md` | New/changed UI when frontend=on |
| Design sketches | `docs/design/sketches/{feature}/` | UI reference-only |
| Judge reviews | `docs/reviews/YYYY-MM-DD-description.md` | Protected-path changes |
| Active layers (Cursor) | `.cursor/config/active-layers.json` | Generated from §0 |
| Codex setup | `docs/codex/SETUP.md` | Codex adapter |

---

## 11. Git Conventions

### Commit message structure

```
<type>(<scope>): <subject>
```

| Part | Rules |
|------|--------|
| **type** | `feat` \| `fix` \| `refactor` \| `docs` \| `test` \| `chore` \| `perf` \| `style` \| `ci` |
| **scope** | module / package / workflow area |

### Branches & PRs

- **Branches:** `feature/...` \| `fix/...` \| `chore/...`
- **PR size:** target ≤ ~400 lines when practical.
- **Protected branches:** `<main / develop>`.

---

## 12. Forbidden Patterns (Agents must NEVER do)

> Apply blocks that match **on** layers. Skip database block if database=off, etc.

### Database (database=on only)
- ❌ Auto-sync schemas in staging/production — migrations only.
- ❌ Destructive migration without rollback.
- ❌ Tenant-scoped query without tenant filter (if multi-tenancy=on).
- ❌ `SELECT *` in production queries.

### Security
- ❌ Log secrets, tokens, passwords, API keys, or PII.
- ❌ Commit `.env` with real values.
- ❌ String-interpolate user input into queries.

### Code Quality
- ❌ Ad-hoc `console.log` in production code — use project logger.
- ❌ Business logic in controllers/route handlers when architecture separates services.
- ❌ Silent catches.

### AI / LLM (ai-llm=on only)
- ❌ Call LLM without try/catch and fallback.
- ❌ Skip usage logging when required by §6.

### Infrastructure (devops=on only)
- ❌ Deploy to production without passing staging when staging exists.

---

## 13. Environment Variables (Required)

> Names only — never values.

```env
# <VAR_NAME>=            # <what it is>
```

---

## 14. Queue / Background Jobs

> **Only if queue=on.** Otherwise: `N/A — layer queue off`.

| Queue Name | Processor | Concurrency | Priority | Notes |
|---|---|---|---|---|
| `<queue>` | `<processor>` | `<n>` | `<High/Normal/Low>` | `<what>` |

---

## 15. API Naming Convention

> Only if backend=on or you expose an API surface. Otherwise N/A.

- **Style:** `<REST | GraphQL | RPC | N/A>`
- **Resource paths:** `<...>`
- **Versioning:** `<...>`
- **Response envelope:** `<...>`
- **Pagination:** `<...>`
