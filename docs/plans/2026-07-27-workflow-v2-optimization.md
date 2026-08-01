# Workflow V2 Optimization

**Goal:** Reduce context usage 40–60% while preserving multi-agent architecture via deterministic Context Packets.

**Protected:** yes | **Agents:** architect-planner (this plan), devops-worker (hooks)

## Constraints

- Do not merge agents or remove specialized roles
- Extend skill-loader internally; agents use context-builder (Phase 6 complete)
- Hooks/protected-paths structure unchanged

## Files

| Path | Action | Owner |
|------|--------|-------|
| `.cursor/context/*` | create | architect-planner |
| `.cursor/config/agent-matrix.json` | create | architect-planner |
| `.cursor/config/context-budget.json` | create | architect-planner |
| `.cursor/skills/skills-manifest.v2.json` | create | architect-planner |
| `.memory/*` | create (generated) | architect-planner |
| `.cursor/patterns/**` | create | architect-planner |
| `.cursor/rules/000-core.mdc` | create | architect-planner |
| `.cursor/rules/001-workflow-v2.mdc` | create | architect-planner |
| `.cursor/agents/*.md` | modify | architect-planner |
| `.cursor/hooks/session-start.sh` | modify | architect-planner |
| `.cursor/config/workflow-policy.json` | modify | architect-planner |

## Execution

1. **Phase 0** — context scripts, .memory/, core rules, agent-matrix ✓
2. **Phase 1** — context-builder.py, manifest v2, session-start update ✓
3. **Phase 2** — pattern library bootstrap (8 patterns) ✓
4. **Phase 2** — pattern library bootstrap (8 patterns) ✓
5. **Phase 3** — slim agent prompts (frontend, backend, architect, judge) ✓
6. **Phase 4** — skill consolidation (nestjs, frontend) ✓
7. **Phase 5** — compact planner/judge templates ✓
8. **Phase 6** — all agents/commands use context-builder ✓

## Risks

- Token estimates drift → CI measure script (future)
- `.memory/` sync drift → run after AGENTS.md updates

## Handoffs

Machine-readable: `.cursor/context/handoffs/workflow-v2-rollout.json`

## Domain Config Sync

- [ ] ADR: N/A — workflow infra, no stack change
- [ ] `docs/architecture.md`: N/A
- [ ] `AGENTS.md`: optional §3 path for `.memory/`, `.cursor/context/`
- [x] `.cursor/config/*`: agent-matrix, context-budget, workflow-policy
