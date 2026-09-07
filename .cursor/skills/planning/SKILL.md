---
name: planning
description: Use when you need to plan technical solutions that are scalable, secure, and maintainable. Respects AGENTS.md §0 project profile layers.
license: MIT
---

# Planning

Create detailed technical implementation plans through research, codebase analysis, solution design, and comprehensive documentation.

## When to Use

Use this skill when:
- Planning new feature implementations
- Architecting system designs
- Evaluating technical approaches
- Creating implementation roadmaps
- Breaking down complex requirements
- Assessing technical trade-offs

## Core Responsibilities & Rules

Always honoring **YAGNI**, **KISS**, and **DRY** principles.
**Be honest, be brutal, straight to the point, and be concise.**

**Project profile:** Read `AGENTS.md §0` and/or `.cursor/config/active-layers.json`. Layer **off** ⇒ do not plan that layer (no migrations if database off, no tenancy if multi-tenancy off, no UI design gate if frontend off).

### 1. Codebase Understanding
Load: `references/codebase-understanding.md`
**Skip if:** Provided with codebase or architecture existing

### 2. Planning on a lower-capability model
Load: `references/planning-with-lower-models.md`
**Load when:** running on a small/cheap model, or when plans come out vague,
truncated, or full of placeholders. It grounds the model in real facts, forces
one-section-at-a-time output, and adds a self-verify gate.

## Workflow Process

1. **Profile** → Resolve active layers from §0 / active-layers.json
2. **Initial Analysis** → Read `docs/architecture.md` + rules; do not invent off-layer stack
3. **Research Phase** → Investigate approaches yourself
4. **Synthesis** → Optimal solution within active layers
5. **Design Phase** → Architecture for on-layer surfaces only
6. **Plan Documentation** → architect-planner template; N/A one-liners for off layers
7. **Review & Refine** → Self-verify gate before handoff

## Output Requirements

- DO NOT implement code - only create plans (and sync domain config docs)
- Respond with plan file path and summary
- Ensure self-contained plans with necessary context
- Include code snippets/pseudocode when clarifying
- Provide multiple options with trade-offs when appropriate
- Fully respect the `./docs/development-rules.md` file when present

**Plan Directory Structure**
```
    - ADR: `docs/adr/NNNN-short-title.md`
    - Plan: `docs/plans/YYYY-MM-DD-feature-name.md`
    - Architecture overview: `docs/architecture.md`
    - Domain hub: `AGENTS.md` (update on-layer sections the plan changes)
```

## Domain Config Sync (required before workers)

After the plan is drafted and the approach is approved:

1. Fill the plan's **Domain Config Sync** checklist (`N/A — layer off` or `N/A — unchanged` allowed).
2. Write/update ADR(s) only for decisions that apply to **active** layers.
3. Create or update `docs/architecture.md` for active surfaces only.
4. Update `AGENTS.md` only for approved on-layer changes (§4 only if multi-tenancy on, §9 if database on, §14 if queue on).
5. If §0 or §3 changed: `python3 .cursor/context/profile-sync.py --from-agents`
6. Update scopes/protected paths when needed (orchestrator approval for expansion).
7. Point `docs/plans/.active-plan` at the new plan.

Module file scaffolds remain `@scaffold-agent`'s job.

## Active Plan State

**Canonical path:** `docs/plans/.active-plan`

1. **Check first** before creating plan
2. **Validate path** under `docs/plans/`
3. **Prompt user** continue [Y/n]
4. **Set on create**
5. **Reset** via `rm docs/plans/.active-plan`

## Quality Standards

- Be thorough and specific within active layers
- Do not pad plans with full-stack sections the project does not have
- Consider long-term maintainability
- Address security when auth layer is on
- Make plans detailed enough for junior developers
- Validate against existing codebase patterns

**Remember:** Plan quality determines implementation success. Profile-aware plans port cleanly across FE-only, BE-only, and fullstack repos.
