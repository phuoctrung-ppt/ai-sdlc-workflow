---
name: agentic-workflow
description: Generic Planner-Worker-Judge workflow for scoped agentic execution. Use when planning work, coordinating workers, evaluating protected changes, or porting this workflow to another repo.
---

# Agentic Workflow

This skill is **repo/domain agnostic**. Project-specific context (name, tech stack, paths, compliance) lives in `AGENTS.md` and `.cursor/config/*.json`. This skill explains the workflow mechanics only.

## Core Loop (V2 + Design Contract)

1. **Classify** — `.cursor/config/protected-paths.json`
2. **Context** — `python3 .cursor/context/context-builder.py --task "..." --agent <agent>`
3. **Plan** — protected/multi-module → `docs/plans/YYYY-MM-DD-topic.md` (compact)
4. **Design Specification** (UI only) — Design Contract + sketches → Design Judge
5. **Execute** — narrowest worker; obey Context Packet tiers **and** in-scope file reads
6. **Verify** — checks proportional to risk
7. **Review** — protected → `docs/reviews/`; extract reusable patterns to `.cursor/patterns/`

## Indie continuous ship (prefer these paths day-to-day)

| Need | Command | Skips |
|------|---------|-------|
| Bug / failing test / small patch | `/fix` | Full plan, DESIGN-GATE, learning counter |
| New idea / MVP shape | `/shape-lite` | Full ADR, worker dispatch, DESIGN-GATE |
| New module / multi-file feature | `/plan-feature` or `/dev-module` | Nothing (full gates apply) |

**Policy:** `.cursor/config/workflow-policy.json` → `loops.codeLoop` / `loops.shapeLite`.

**High-signal portable skills to prefer** (do not load everything):

- `error-recovery` — every code-loop
- `agentic-workflow` — orchestration + handoff
- `saas-product-ui` — in-app product UI only (not marketing)
- `planning` — shape-lite / plan
- `api-contract-first` — when API surface changes
- Domain stack skills from `AGENTS.md §2` only when paths match

Taste/marketing skills (`taste-design`) stay for marketing pages; product UI uses `saas-product-ui` + hard-rules.

## Context orchestration (what we actually ship)

This repo is already a **context-prepared** workflow, not a prompt dump:

| Layer | Location |
|-------|----------|
| Intent | `.cursor/context/intent_detector.py` |
| Builder | `.cursor/context/context-builder.py` |
| Packet schema | `.cursor/context/schemas/context-packet.schema.json` |
| Budget | `.cursor/config/context-budget.json` |
| Heuristic score | `.cursor/config/context-score.json` |
| Agent routing | `.cursor/config/agent-matrix.json` |
| Skills registry | `.cursor/skills/skills-manifest.v2.json` |

**Packet is primary.** Agents still **may read repository files** inside `worker-scopes.json`. Do not interpret orchestration as a ban on `Read`/`grep` of application code.

**Not P0:** vendor-neutral runtime for Claude Code / Codex / Gemini, ML context rankers, analytics product, non-SDLC modules. See `docs/vision/v4-critique-and-v3-direction.md`.

## Context Builder

```bash
python3 .cursor/context/context-builder.py \
  --task "<description>" \
  --agent <agent-id> \
  [--paths path1,path2] \
  [--keywords kw1,kw2] \
  [--handoff docs/plans/.active-plan] \
  [--budget 8000]
```

Lazy reference expansion:

```bash
python3 .cursor/context/context-builder.py --expand-ref "<path>" --reason "<why>"
```

Sync project memory after AGENTS.md changes:

```bash
python3 .cursor/context/memory-loader.py --sync
```

Legacy: `--use-legacy-loader` delegates to `skill-loader.py`.

## Design Contract (UI modules)

Template: `docs/design/_templates/design-contract.v1.md`  
Phase: `.cursor/skills/planning/references/design-specification-phase.md`  
Gate: `.cursor/rules/009-design-gate.mdc`

UI flow: Planning Overview → Design Specification → Design Judge → Breakdown → Execute.

Code-loop does **not** re-run Design Gate for pure code fixes on existing UI.

## Handoff Packet

Every worker task starts from a handoff packet. Fill this before dispatching:

```markdown
Objective:
In-scope paths:
Out-of-scope paths:
Plan/ADR:
Design Contract (if UI):
Required skills:
Acceptance criteria:
Required verification:
Risk notes:
Scope expansion path:
```

For code-loop, Plan/ADR may be `N/A (code-loop)`.

## Agent Roster

See `AGENTS.md §4` for the full agent table for this project. Standard agents available in `.cursor/agents/`:

| Agent | Role |
|---|---|
| `architect-planner` | Plans, shape-lite, ADRs, dispatches handoff packets |
| `scaffold-agent` | Bootstraps module/page shells before workers implement |
| `designer-worker` | Design Contract (numeric), sketches, tokens |
| `backend-worker` | API features, services, DTOs |
| `frontend-worker` | UI from Design Contract numbers only |
| `database-worker` | Migrations, schema design, query optimization |
| `ai-worker` | LLM integration, embeddings, cost tracking |
| `devops-worker` | Docker, CI/CD, infra |
| `security-worker` | Auth, RBAC, encryption, compliance |
| `qa-worker` | Tests: unit, integration, E2E |
| `judge-agent` | Read-only review gate (incl. Design Contract Review) |
| `admin-worker` | Admin/control-plane (elevated privilege) |

Thin I/O schema (optional): `.cursor/context/schemas/agent-contract.schema.json`.

## Porting to Another Repo

Copy the workflow files, then update only configuration — do not modify hook code or skill-loader:

### Files to Copy (unchanged)
- `.cursor/hooks/` (all files)
- `.cursor/context/` (context orchestration — V2 entry point)
- `.cursor/config/` (all files — update content, not structure)
- `.cursor/skills/agentic-workflow/`
- `.cursor/skills/scripts/skill-loader.py` (legacy fallback only)
- `.cursor/rules/000-core.mdc`, `001-workflow-v2.mdc`, `006-agentic-workflow.mdc`, `009-design-gate.mdc`

### Files to Update for Your Project
1. **`AGENTS.md`** (project root) — fill in project name, tech stack, structure, agent scopes, compliance
2. **`.cursor/config/workflow-policy.json`** — no structural changes needed
3. **`.cursor/config/protected-paths.json`** — update `projectProtectedGlobs`
4. **`.cursor/config/worker-scopes.json`** — concrete folder paths
5. **`.cursor/skills/skills-manifest.v2.json`** — domain skills for your stack

After porting, run `python3 .cursor/context/memory-loader.py --sync`.
Agents use **context-builder.py** — not skill-loader.py directly.

## References

- [workflow-phases.md](references/workflow-phases.md)
- `docs/vision/v4-critique-and-v3-direction.md`
- Commands: `/fix`, `/shape-lite`, `/dev-module`, `/plan-feature`
