---
name: agentic-workflow
description: Generic Planner-Worker-Judge workflow for scoped agentic execution. Use when planning work, coordinating workers, evaluating protected changes, or porting this workflow to another repo.
---

# Agentic Workflow

This skill is **repo/domain agnostic**. Project-specific context (name, tech stack, paths, compliance) lives in `AGENTS.md` and `.cursor/config/*.json`. This skill explains the workflow mechanics only.

## Core Loop (V2)

1. **Classify** — `.cursor/config/protected-paths.json`
2. **Context** — `python3 .cursor/context/context-builder.py --task "..." --agent <agent>`
3. **Plan** — protected/multi-module → `docs/plans/YYYY-MM-DD-topic.md` (compact)
4. **Execute** — narrowest worker; obey Context Packet tiers
5. **Verify** — checks proportional to risk
6. **Review** — protected → `docs/reviews/`; extract reusable patterns to `.cursor/patterns/`

## Context Builder (V2)

Primary entry (replaces direct skill-loader calls):

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

## Handoff Packet

Every worker task starts from a handoff packet. Fill this before dispatching:

```markdown
Objective:
In-scope paths:
Out-of-scope paths:
Plan/ADR:
Required skills:
Acceptance criteria:
Required verification:
Risk notes:
Scope expansion path:
```

## Agent Roster

See `AGENTS.md §4` for the full agent table for this project. Standard agents available in `.cursor/agents/`:

| Agent | Role |
|---|---|
| `architect-planner` | Plans, writes ADRs, dispatches handoff packets |
| `scaffold-agent` | Bootstraps module/page shells before workers implement |
| `designer-worker` | UI/UX design, component specs, design systems |
| `backend-worker` | API features, services, DTOs |
| `frontend-worker` | UI components, pages, data fetching |
| `database-worker` | Migrations, schema design, query optimization |
| `ai-worker` | LLM integration, embeddings, cost tracking |
| `devops-worker` | Docker, CI/CD, infra |
| `security-worker` | Auth, RBAC, encryption, compliance |
| `qa-worker` | Tests: unit, integration, E2E |
| `judge-agent` | Read-only review gate |
| `admin-worker` | Admin/control-plane (elevated privilege) |

## Porting to Another Repo

Copy the workflow files, then update only configuration — do not modify hook code or skill-loader:

### Files to Copy (unchanged)
- `.cursor/hooks/` (all files)
- `.cursor/context/` (context orchestration — V2 entry point)
- `.cursor/config/` (all files — update content, not structure)
- `.cursor/skills/agentic-workflow/`
- `.cursor/skills/scripts/skill-loader.py` (legacy fallback only)
- `.cursor/rules/000-core.mdc`, `001-workflow-v2.mdc`, `006-agentic-workflow.mdc`

### Files to Update for Your Project
1. **`AGENTS.md`** (project root) — fill in project name, tech stack, structure, agent scopes, compliance
2. **`.cursor/config/workflow-policy.json`** — no changes needed (already domain-agnostic)
3. **`.cursor/config/protected-paths.json`** — update `projectProtectedGlobs` with your sensitive paths
4. **`.cursor/config/worker-scopes.json`** — update `agents` section with your concrete folder paths
5. **`.cursor/skills/skills-manifest.v2.json`** — add domain skills for your tech stack

After porting, run `python3 .cursor/context/memory-loader.py --sync`.
Agents use **context-builder.py** — not skill-loader.py directly.

### Files to Copy Selectively (bring the skills your project needs)
- `.cursor/skills/databases/` — if using a SQL/NoSQL database
- `.cursor/skills/docker-devops/` — if using Docker
- `.cursor/skills/testing-qa/` — always useful
- `.cursor/skills/frontend-skills/` — if building a React/Next.js frontend
- `.cursor/skills/taste-design/` — if building any user-facing UI
- Domain skills (nestjs-skills, bullmq-worker, etc.) — only if your stack uses them

Keep hook code generic unless the hook payload format changes.

## References

- [workflow-phases.md](references/workflow-phases.md)
