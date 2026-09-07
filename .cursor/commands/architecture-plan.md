---
name: architecture-plan
description: Idea → system. GENESIS fills AGENTS.md from §0 profile (only active layers). BREAKDOWN expands roadmap. No forced full-stack sections.
---

Act as **Orchestrator** driving **`@architect-planner`** and **`@judge-agent`**. Stay inside the current `.cursor` workflow.

## Mode selection

- **GENESIS** — `/architecture-plan brainstorming {idea}`
- **BREAKDOWN** — `/architecture-plan` (active plan exists)

---

# GENESIS mode — `/architecture-plan brainstorming {idea}`

Input: **{idea}**

## Step 0 — Build context
```bash
python3 .cursor/context/context-builder.py --phase brainstorm --task "{idea}" --agent architect-planner
python3 .cursor/context/context-builder.py --phase plan --task "{idea}" --agent architect-planner
```

## Step 1 — BRAINSTORM (HARD-GATE, chat only)
<HARD-GATE>
Do NOT write or modify any file until the user approves the concept.
</HARD-GATE>

Concept brief (chat):
- **What it does** — job-to-be-done
- **Target users**
- **Core features** — MVP vs Later
- **Suggested profile** — `frontend` | `backend` | `fullstack` | `library` | `cli`
- **Suggested layers on/off** — frontend, backend, database, multi-tenancy, queue, auth, devops, ai-llm
- **Design/UX needs** — only if frontend layer likely on
- **Domain & data** — only entities/tenancy if database or multi-tenancy likely on
- **Constraints**
- **2–3 architecture approaches** + recommendation

⏸️ **STOP — wait for explicit approval of concept + profile/layers + MVP boundary.**

## Step 2 — STANDARDIZE DOMAIN (fill AGENTS.md)
After approval:
1. Write **§0 Project Profile** first (profile, layout, layers table).
2. Fill §1–§3 from the approved concept.
3. Fill **optional sections only when layer is on**:
   - multi-tenancy on → §4; else `N/A — layer multi-tenancy off`
   - database on → §9 entities; else N/A
   - queue on → §14; else N/A
   - ai-llm on → AI rules in §6; else skip
4. §5 roster: list agents that match active layers (+ always-on planner/judge/qa).
5. Align config:
```bash
python3 .cursor/context/profile-sync.py --from-agents
```
   Optionally tighten `worker-scopes.json` to §3 paths (orchestrator approval for expansion).

## Step 3 — CREATE ARCHITECTURE + ADRs
- `docs/architecture.md` — only containers/flows for **active** layers
- ADRs for foundational decisions that apply (do not invent tenancy/DB ADRs if those layers are off)

## Step 4 — SYSTEM ROADMAP PLAN
Write `docs/plans/YYYY-MM-DD-{slug}.md`:
- Goal, architecture summary, stack from §2
- MVP modules only for active layers
- Global constraints from on-layer sections only
- Domain Config Sync filled
- Risks
Set `docs/plans/.active-plan`.

## Step 5 — JUDGE PLAN REVIEW
```bash
python3 .cursor/context/context-builder.py --phase review --task "genesis plan {slug}" --agent judge-agent --keywords "workflow,judge,plan" --budget 5000
```
Judge checks: MVP coverage, §0 present, no leftover raw `<PLACEHOLDER>` in **in-scope** sections, no forced off-layer sections, consistent profile.
- `PLAN_APPROVED` → ⏸️ STOP. Next: `/architecture-plan` (BREAKDOWN).

---

# BREAKDOWN mode — `/architecture-plan`

Operates on `docs/plans/.active-plan`.

## Step 0 — Context
```bash
python3 .cursor/context/context-builder.py --phase plan --task "breakdown $(cat docs/plans/.active-plan)" --agent architect-planner --handoff docs/plans/.active-plan
```

## Step 1 — EXPAND TO EXECUTABLE TASKS
Per module: real paths, owner ∈ active agents, skills ∈ active skills, acceptance, deps.
Ordering example when layers on: DB → API → Frontend (skip missing layers).

## Step 2 — JUDGE PLAN REVIEW
Verify MVP→tasks, owners valid for profile, no off-layer tasks.

---

## Handoff
```
/dev-module {module_name}
```

## Guardrails
- Never skip HARD-GATE brainstorm in GENESIS.
- Never force database/tenancy/queue content when layer off.
- Never write app business logic in this command.
- Every gate persists an artifact under `docs/`.
