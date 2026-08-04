# Agentic Planner-Worker-Judge Workflow

A **portable, domain-neutral** Cursor workflow for building software with coordinated AI agents.
It splits work into **Planner** (designs), **Workers** (implement), **Judge** (reviews) —
and sizes the loop to the job: **code-loop** and **shape-lite** for daily indie ship,
full plan → design → execute only when scope needs gates.

Everything ships stack-agnostic. You describe your project **once** in `AGENTS.md`, and every agent
reads that file to learn your tech stack, structure, and compliance rules.

---

## Table of Contents

1. [Core idea](#1-core-idea)
2. [Day-to-day: indie continuous ship](#2-day-to-day-indie-continuous-ship)
3. [Full path: new module / system](#3-full-path-new-module--system)
4. [Commands](#4-commands)
5. [Agents](#5-agents)
6. [Context builder & skills](#6-context-builder--skills-workflow-v2)
7. [Gates & guardrails](#7-gates--guardrails)
8. [Design-first frontend](#8-design-first-frontend)
9. [Directory map](#9-directory-map)
10. [Porting to another repo](#10-porting-to-another-repo)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Core idea

| Role | Who | Does | Can edit |
|---|---|---|---|
| **Planner** | `architect-planner` | Shape-lite, brainstorm, ADRs, task breakdown, syncs `AGENTS.md` | `docs/**`, `.cursor/**`, `AGENTS.md` |
| **Workers** | `backend-`, `frontend-`, `designer-`, `database-`, `ai-`, `devops-`, `security-`, `admin-`, `scaffold-`, `qa-` | Implement inside a narrow scope | only their configured paths |
| **Judge** | `judge-agent` | Read-only review of **plans** and **code** (full / protected path) | `docs/reviews/**` |

Key principles:

- **`AGENTS.md` is the single source of truth** for domain facts (stack, structure, compliance).
  The `.cursor/` machinery never needs editing to change domains.
- **Right-sized loops** — bug fixes use `/fix`; ideas use `/shape-lite`; full gates only when structural.
- **Nothing is claimed "done" from intent alone** on full path — completion requires evidence (build/tests/artifacts).
- **Protected changes** (auth, migrations, config, `AGENTS.md`, …) still require a plan + review artifact.
- **Workers ship; they don't freelance** — planning and design happen upstream when scope needs them.
- **Domain-agnostic** — no lock-in to a sample product (e.g. AI Workspace). Test repos are harnesses only.

---

## 2. Day-to-day: indie continuous ship

This is the **default** path. Do not re-run the full SDLC for every patch or small idea.

```text
Bug / test đỏ / typo / small patch
        │
        ▼
     /fix          ← code-loop (no plan rewrite, no DESIGN-GATE)

Ý tưởng mới / “nên build X?”
        │
        ▼
  /shape-lite       ← short shape note under docs/plans/shape/
        │
        └── NEXT: /fix | implement-small | /plan-feature | design-spec | drop
```

### `/fix` — code-loop

**Use when:** bug, type error, failing test, rename, style, regression, small implement on existing code.

**Do not use when:** new module, new UI screen without Design Contract, multi-module API/schema change, protected architecture decision.

In Cursor:

```text
/fix Button submit stays disabled when the form is valid
/fix TypeError in apps/web/src/... when uploading a file
```

What happens:

1. Intent → phase `fix` (often complexity `low`)
2. Context Packet via `context-builder.py` (budget ~5k; prefer `error-recovery`)
3. One narrow worker edits in-scope paths only
4. Re-run the failing command; max 2 root-cause loops
5. Done — **no** new plan file, **no** DESIGN-GATE, **no** learning-counter bump for trivial one-file fixes

Policy: `.cursor/config/workflow-policy.json` → `loops.codeLoop`  
Command: `.cursor/commands/fix.md`

### `/shape-lite` — compact idea shaping

**Use when:** new idea, small feature, quick “should we?” before coding.

**Do not use when:** pure bug (use `/fix`); large multi-module product (use `/plan-feature` or `/architecture-plan`).

```text
/shape-lite Add tag filter on the knowledge list page
```

Output: `docs/plans/shape/YYYY-MM-DD-{slug}.md` from template `docs/plans/_templates/shape-lite.md`.

Ends with exactly one line:

```text
NEXT: /fix | implement-small | /plan-feature | design-spec | drop
```

Follow `NEXT`. Shape-lite does **not** dispatch workers unless you explicitly ask to implement.

Policy: `loops.shapeLite` · Command: `.cursor/commands/shape-lite.md` · Rationale: [docs/vision/indie-ship-loops.md](./docs/vision/indie-ship-loops.md)

### Preferred skills (high-signal)

| Loop | Prefer |
|------|--------|
| `/fix` | `error-recovery`, then `agentic-workflow`, then domain skill if paths match |
| `/shape-lite` | `planning`, `agentic-workflow`, `api-contract-first` if API |
| In-app product UI | `saas-product-ui` (not marketing taste) |
| Marketing / landing | `taste-design` + hard-rules-marketing |

---

## 3. Full path: new module / system

Use when scope is structural: new module, multi-module feature, new visible UI system, protected changes.

### A. `/architecture-plan` — idea → system (planning)

**GENESIS** — `/architecture-plan brainstorming {idea}`

1. **Brainstorm** (chat-only HARD-GATE) — concept brief, MVP vs Later, 2–3 approaches. *Waits for your approval.*
2. **Standardize domain** — fills `AGENTS.md` for the approved idea.
3. **Architecture + ADRs** — `docs/architecture.md`, `docs/adr/NNNN-*.md`.
4. **System roadmap** — `docs/plans/YYYY-MM-DD-{slug}.md`, sets `docs/plans/.active-plan`.
5. **Judge Plan Review** → `PLAN_APPROVED`.

**BREAKDOWN** — `/architecture-plan` (approved roadmap exists)

1. Expands each roadmap module into executable tasks (paths, owner agent, acceptance, deps).
2. **Judge Plan Review** → ready for `/dev-module`.

### B. `/plan-feature {desc}` — single-feature planning

Lightweight subset of planning (ADR/schema/tasks) without full genesis. Still produces a plan artifact before workers on non-trivial features.

### C. `/dev-module {name}` — plan → shipped

Resumable loop (state in `.cursor/state/module-{name}-loop.json`):

```text
Phase 0  Restore state
Phase 1  Brainstorm         ─┐ skipped if approved plan exists for this module
Phase 2  Plan + sync config ─┘
Phase 1.5 Scaffold          (optional — @scaffold-agent)
Phase 3  Execute            (UI: Design Contract → designer → frontend)
Phase 4  Test               (@qa-worker)
Phase 5  Verify             (@judge-agent)
Phase 5a Fix loop           (≤ 3, then escalate)
Phase 6  Done ✅ + memory / learning counter
```

> If `PLAN_APPROVED` exists for this module → skip Phase 1–2.

---

## 4. Commands

Type these as slash-commands in Cursor. Located in `.cursor/commands/`.

### Daily (prefer these)

| Command | Purpose |
|---|---|
| **`/fix {issue}`** | Code-loop: bug/patch without full plan or DESIGN-GATE |
| **`/shape-lite {idea}`** | Compact shape note + `NEXT` recommendation |

### Full / structural

| Command | Purpose |
|---|---|
| `/architecture-plan brainstorming {idea}` | GENESIS: idea → `AGENTS.md` + architecture + roadmap |
| `/architecture-plan` | BREAKDOWN: roadmap → executable tasks |
| `/dev-module {name}` | Full per-module execution loop with judge + fix loop |
| `/plan-feature {desc}` | Single-feature planning |
| `/generate-module {name}` | Scaffold a backend feature module |
| `/generate-migration` | Create a DB migration |
| `/generate-test` | Generate unit/integration/E2E tests |
| `/workflow-eval {target}` | Judge review → `docs/reviews/` artifact |
| `/security-audit` | Security-focused review pass |
| `/skill-update` | Explicit learning / skill-updater pass |
| `/ai-cost-check` | *(AI/LLM projects only)* cost tracking check |
| `/tenant-context-check` | *(multi-tenant only)* tenant isolation audit |

---

## 5. Agents

Defined in `.cursor/agents/`. Invoke with `@agent-name`. Each runs **context-builder** first.

| Agent | Role |
|---|---|
| `architect-planner` | Shape-lite, plans, ADRs, task breakdown, syncs domain config |
| `scaffold-agent` | Empty module/page shells (no logic) |
| `designer-worker` | Design Contract (numeric) + sketches |
| `frontend-worker` | UI from Design Contract numbers only |
| `backend-worker` | API modules, services, DTOs, guards |
| `database-worker` | Migrations, entities, query optimization |
| `ai-worker` | LLM/embeddings/cost tracking (if stack has AI) |
| `security-worker` | Auth, RBAC, encryption, rate limiting |
| `devops-worker` | Docker, CI/CD, infra |
| `admin-worker` | Admin / control-plane (if any) |
| `qa-worker` | Unit / integration / E2E tests |
| `judge-agent` | Read-only quality gate (plan + code + Design Contract review) |
| `learning-agent` | Post-module skill / pattern proposals |

Each agent may only edit paths in `.cursor/config/worker-scopes.json`.

---

## 6. Context builder & skills (Workflow V2)

Skills live in `.cursor/skills/` (registered in `skills-manifest.v2.json`). Agents call **context-builder** for a tiered Context Packet:

```bash
python3 .cursor/context/context-builder.py \
  --task "<what you're doing>" \
  --agent <agent-name> \
  --phase <fix|shape-lite|brainstorm|plan|design|implement-backend|implement-frontend|database|devops|test|review|scaffold|dev-module> \
  --paths "optional/path/hints" \
  --keywords "comma,separated,hints" \
  [--handoff docs/plans/.active-plan] \
  [--budget 8000]
```

- **tier1** — core rules + `.memory/` slices
- **tier2** — matched skill `SKILL.md` (1–2 for typical /fix)
- **tier3** — patterns from `.cursor/patterns/`
- **tier4** — lazy references via `--expand-ref`

```bash
python3 .cursor/context/memory-loader.py --sync   # after AGENTS.md changes
```

Intent detection (phase `fix` / `shape-lite` preferred early for indie keywords):

```bash
python3 .cursor/context/intent-detector.py --task "…" --paths "…"
```

---

## 7. Gates & guardrails

Enforced by hooks (`.cursor/hooks.json` → `.cursor/hooks/`):

| Hook | When | What it does |
|---|---|---|
| `session-start` | session start | Loads workflow context |
| `enforce-worker-scope` | before Write/Edit | Blocks edits outside agent scope |
| `record-file-edit` | after each edit | Records touched files |
| `block-destructive-shell` | before shell | Blocks dangerous commands |
| `require-protected-review` | on stop | Protected changes need plan + review (full path) |

**Protected changes** = `.cursor/config/protected-paths.json`. Fail closed for protected; fail open for standard work.

**Code-loop exception:** `/fix` does not invent a new plan artifact; protected path edits still fail closed if the stop hook requires review — escalate to `/plan-feature` when needed.

Override (rare):

```bash
.cursor/hooks/review-override.sh --skip-review "reason"
```

---

## 8. Design-first frontend

**Full path / new UI:** cannot start without a Design Contract + sketch. DESIGN-GATE (`009-design-gate.mdc`):

1. Spec `docs/design/**/*.spec.md` (from `docs/design/_templates/design-contract.v1.md`) **and** sketch under `docs/design/sketches/`.
2. If missing → `@designer-worker` first, then Design Judge.
3. `@frontend-worker` implements **contract numbers only** — does not invent visual system.

**Code-loop exception:** pure code/fix on **existing** UI that already has a contract implements against that contract. No DESIGN-GATE re-run. If there is no contract and the change is visual + non-trivial → stop and recommend `/shape-lite` or design-spec.

Product UI skill: `saas-product-ui`. Marketing pages: `taste-design`.

---

## 9. Directory map

```text
.
├── AGENTS.md                    # domain config hub (fill once per project)
├── README.md
├── HOW_TO_USE.md                # this file
├── .memory/                     # generated cache (Workflow V2)
├── docs/
│   ├── plans/                   # full plans + .active-plan
│   │   ├── shape/               # shape-lite notes
│   │   └── _templates/shape-lite.md
│   ├── adr/
│   ├── design/                  # Design Contracts + sketches/
│   │   └── _templates/design-contract.v1.md
│   ├── reviews/
│   ├── memory/                  # durable SoT (decisions, gotchas, shortcuts)
│   └── vision/indie-ship-loops.md
└── .cursor/
    ├── agents/
    ├── commands/                # fix.md, shape-lite.md, dev-module.md, …
    ├── rules/                   # includes 009-design-gate.mdc
    ├── context/                 # context-builder, intent_detector, …
    ├── config/                  # workflow-policy.json (loops), agent-matrix.json
    ├── skills/                  # skills-manifest.v2.json
    ├── hooks/
    └── state/
```

---

## 10. Porting to another repo

1. Copy `.cursor/` and `AGENTS.md` (and optionally `docs/` scaffolding).
2. Fill `AGENTS.md` §1–§15 — or run `/architecture-plan brainstorming {idea}`.
3. Edit `.cursor/config/protected-paths.json` → `projectProtectedGlobs`.
4. Tighten `.cursor/config/worker-scopes.json` to real folders from `AGENTS.md §3`.
5. Adjust domain skills in `skills-manifest.v2.json` for your stack only.
6. `python3 .cursor/context/memory-loader.py --sync`.

**Day-to-day after port:** `/fix` and `/shape-lite` first; `/dev-module` only for new modules.

Hooks and `workflow-guard.py` stay unchanged. Agents use **context-builder.py**.

---

## 11. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| Used `/dev-module` for a one-line bug | Prefer `/fix` — cheaper, no plan rewrite |
| `/fix` wants a new screen / schema | Escalate: `/shape-lite` or `/plan-feature` |
| Edit blocked "outside scope" | Wrong agent or expand `worker-scopes.json` via orchestrator |
| Stop hook blocks completion | Protected change without plan/review — produce artifacts or logged override |
| Frontend refuses to code (full path) | DESIGN-GATE: missing contract/sketch — run `@designer-worker` |
| `context-builder` empty tier2 | Check `--agent` / `--phase` / `--keywords`; skill in `skills-manifest.v2.json` |
| Shape note has no `NEXT` line | Re-run `/shape-lite`; template requires one recommendation |

---

**In short:**  
**Daily** → `/fix` (code) · `/shape-lite` (idea).  
**Structural** → `/architecture-plan` / `/plan-feature` → `/dev-module` (Design Contract before new UI).  
Fill `AGENTS.md` once; stay domain-agnostic; do not re-enter the full loop for every patch.
