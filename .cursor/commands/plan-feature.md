---
name: plan-feature
description: Architect planning — ADR, conditional layer sections, task breakdown. Respects AGENTS.md §0 project profile (no forced DB/tenancy on FE-only or BE-only).
---

Act as **Architect Planner** (`.cursor/agents/architect-planner.md`).

Feature: {feature_description}

1. Run context-builder:
   `python3 .cursor/context/context-builder.py --phase plan --task "{feature_description}" --agent architect-planner --handoff docs/plans/.active-plan`
2. **Resolve profile** — read `AGENTS.md §0` and/or `.cursor/config/active-layers.json`.
   - If §0 missing: ask user to fill profile + layers, or run `python3 .cursor/context/profile-sync.py --detect` then confirm.
   - **Layer off = absent** — do not plan migrations, tenancy, queues, or assign workers for that layer.
3. **Phase 0 BRAINSTORM** (HARD-GATE): explore codebase, propose 2–3 options, wait for approval — do not write the plan file yet.
4. Read `.memory/architecture.md` and `AGENTS.md §0`–§3 for profile, stack, structure.
5. Explore codebase for related modules (only paths that exist for active layers).
6. Write plan to `docs/plans/YYYY-MM-DD-{slug}.md` using the architect-planner template (include **Domain Config Sync**).
7. **Conditional plan body** (include only if layer is **on**):

| Layer on | May include |
|----------|-------------|
| database | Migration needs, entities |
| backend | API / service tasks, shared contracts |
| frontend | UI tasks, Design Contract gate if new visible UI |
| multi-tenancy | Tenant isolation notes |
| queue | Job/queue notes |
| auth | Auth/RBAC notes |
| devops | Deploy/CI notes |
| ai-llm | LLM cost/safety notes |

Always include: Goal, acceptance criteria, file list with **owner agents ⊆ active agents**, task table, risks, scope boundaries.

For every **off** layer relevant to the feature, one line only:
`N/A — layer <name> off (AGENTS.md §0)`.

**Forbidden:** unconditional "Database migration needs" or tenancy sections when those layers are off.

8. **Phase 1.5 SYNC DOMAIN CONFIG** (before workers):
   - ADR → `docs/adr/` when architecture/stack/pattern decisions changed
   - Create/update `docs/architecture.md` only for active-layer surfaces
   - Update `AGENTS.md` only sections that changed **and** whose layer is on (§4 only if multi-tenancy on, §9 only if database on, §14 only if queue on)
   - Update `worker-scopes.json` / `protected-paths.json` if scopes changed (orchestrator approval for expansion)
   - Re-run `python3 .cursor/context/profile-sync.py --from-agents` if §0 or §3 changed
   - Point `docs/plans/.active-plan` at this plan
   - Record N/A + reason for skipped sync items
9. Wait for orchestrator approval of plan + sync diffs before dispatching workers (use `@scaffold-agent` first if new module shells are required).
