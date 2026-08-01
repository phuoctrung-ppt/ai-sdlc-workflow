---
name: ai-career-orchestrator
description: "[DOMAIN EXAMPLE] Orchestrator skill template for a specific project. Copy and adapt this for your project — rename it, update agent→skill mappings, and register it in skills-manifest.v2.json with domainTag matching your stack."
domainSkill: true
---

# Project Orchestrator (Domain Example)

> **This is a domain-specific skill template.** It was originally written for an AI Career Platform.
> To reuse: copy this folder, rename it, and update the agent→skill map below to match your `AGENTS.md §2` tech stack.
> Register the copy in `skills-manifest.v2.json` under `skills` with `portable: false` and your own `domainTag`.

## Workflow Phases

1. **Plan** — `@architect-planner` or `/plan-feature` → `docs/plans/`
2. **Execute** — Worker agents in parallel (see `AGENTS.md §4`)
3. **Integrate** — `@qa-worker`, `@devops-worker`
4. **Review** — `@judge-agent`

## Skill Loader (always run at task start)

```bash
python3 .cursor/skills/scripts/skill-loader.py \
  --phase <phase> --task "<description>" --agent <agent-id>
```

## Agent → Skill Map (update for your project)

| Agent | Skills |
|-------|--------|
| `backend-worker` | _(your backend framework skill, e.g. nestjs-skills)_ |
| `frontend-worker` | _(your frontend skill, e.g. frontend-skills)_ |
| `database-worker` | `databases` |
| `ai-worker` | `ai-llm-integration` _(if project uses AI)_ |
| `admin-worker` | `admin-service` _(if project has admin plane)_ |
| `devops-worker` | `docker-devops` |
| `qa-worker` | `testing-qa` |

## Context Offloading

Never keep full plans in chat. Write to `docs/plans/`, `docs/adr/`, `docs/reviews/`.

## References

- [workflow-phases.md](references/workflow-phases.md) — detailed phase diagram
- [AGENTS.md](../../../AGENTS.md) — project entry point
