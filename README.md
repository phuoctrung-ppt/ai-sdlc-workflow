# AI SDLC Workflow (Cursor)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/phuoctrung-ppt/ai-sdlc-workflow)](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/commits)
[![Repo Stars](https://img.shields.io/github/stars/phuoctrung-ppt/ai-sdlc-workflow?style=social)](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/stargazers)

> **Production-oriented AI Software Development Lifecycle for [Cursor](https://cursor.com).**  
> Structured engineering (plan → implement → review → learn) instead of giant one-shot prompts.

**Branch note:** Active design lives on [`v2`](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/tree/v2) (3-layer Execute / Memory / Learning + product UI skills). `master` remains the thinner “ready to run” baseline.

> ⚠️ **Status:** Workflow design and wiring on `v2` are in place; **end-to-end pilot on a real product module is not claimed complete.** Treat the run path below as the intended operator guide.

---

## Walkthrough video

How the layers and key files fit together (slideshow explainer):

**[`docs/media/ai-sdlc-workflow-explained.mp4`](./docs/media/ai-sdlc-workflow-explained.mp4)**

Topics covered:

1. Tầng 1 Execute — Planner / Workers / Judge  
2. Tầng 2 Memory — `docs/memory/*` (source of truth)  
3. Tầng 3 Learning — retrospective → `skill-updater` → proposal  
4. Which files agents call (`context-builder.py`, rules, state)  
5. Where token cost concentrates (plan / implement / fix loop)

If the file is missing on your checkout, pull latest `v2` or open the copy under project artifacts from the design session.

---

## Why this exists

Most AI coding setups optimize **prompts**. This repo optimizes the **process**:

| Practice | What it means here |
|----------|-------------------|
| Architecture first | No implement before plan / approval gates |
| Specialized workers | Narrow scopes in `worker-scopes.json` |
| Skill-driven context | Load only relevant skills via context-builder |
| Review before “done” | Judge + severity (Critical vs Minor) |
| Durable memory | `docs/memory/*` — not chat history |
| Self-improvement | Learning agent proposes skill patches (approval required) |

---

## Three layers (v2)

```text
┌─────────────────────────────────────────────────────────┐
│  Tầng 3  LEARNING   retrospective → skill-updater       │
│                      modulesSinceLastProposal (state)   │
├─────────────────────────────────────────────────────────┤
│  Tầng 2  MEMORY     docs/memory/{decisions,gotchas,     │
│                      shortcuts}.md   ← primary SoT      │
│                     .memory/* = generated AGENTS cache  │
├─────────────────────────────────────────────────────────┤
│  Tầng 1  EXECUTE    Planner → Workers → Judge → fix     │
└─────────────────────────────────────────────────────────┘
```

| Layer | Primary paths |
|-------|----------------|
| Execute | `.cursor/agents/*`, `/dev-module`, `/architecture-plan` |
| Memory | `docs/memory/*` (SoT) · `.memory/*` (cache via `memory-loader.py --sync`) |
| Learning | `docs/retrospective.md`, `@learning-agent`, `skill-updater`, `.cursor/state/workflow-state.json` |

Canonical rule: [`.cursor/rules/007-memory-learning.mdc`](./.cursor/rules/007-memory-learning.mdc).

---

## Quick start — how to run

### Prerequisites

- [Cursor](https://cursor.com) with agent/tools enabled  
- This repo (or a port: copy `.cursor/`, `AGENTS.md`, `docs/memory/`, `.memory/`)  
- Python 3 for context tooling  

```bash
git clone https://github.com/phuoctrung-ppt/ai-sdlc-workflow.git
cd ai-sdlc-workflow
git checkout v2

# Optional: regenerate AGENTS → .memory cache after you fill AGENTS.md
python3 .cursor/context/memory-loader.py --sync
```

**Always call the hyphen CLI** (underscore modules are internal libraries):

```bash
python3 .cursor/context/context-builder.py --task "<task>" --agent <agent-id>
```

See [`.cursor/context/README.md`](./.cursor/context/README.md).

### Golden path (new product idea → modules)

```text
# 1) Genesis — brainstorm + fill AGENTS.md + architecture + roadmap
/architecture-plan brainstorming <one or two sentences about the product>

# 2) After you approve concept + judge plan review
/architecture-plan

# 3) Per module — execute → test → judge → fix → memory → learning dispatch
/dev-module <module_name>
```

| Step | Command | Outcome |
|------|---------|---------|
| 1 | `/architecture-plan brainstorming …` | Concept, filled `AGENTS.md`, ADRs, roadmap |
| 2 | `/architecture-plan` | Per-module breakdown, `PLAN_APPROVED` |
| 3 | `/dev-module <name>` | Implementation loop + Phase 6 distillation |

**Already have an approved plan for a module?** `/dev-module` should **skip** brainstorm/plan and jump to scaffold/execute.

**Single feature on an existing app:** `/dev-module <feature>` alone is enough (inline plan if none exists).

### Design tracks (UI)

| Track | Skill | Use for |
|-------|--------|---------|
| **Product** | `saas-product-ui` | App shell, tables, settings, billing |
| **Marketing** | `taste-design` | Landing, hero, pricing |

Prefer **compositions + blocks** under `saas-product-ui` for in-app UI. Do **not** load full marketing taste-skill for authenticated product screens.

### After each module (Phase 6)

1. Append `docs/retrospective.md`  
2. Update `docs/memory/*` (decisions / gotchas / shortcuts)  
3. Increment `modulesSinceLastProposal` in `.cursor/state/workflow-state.json`  
4. Dispatch `@learning-agent` (full pass when counter ≥ 5)  

Skill patches are **proposals** under `docs/reviews/*` — apply only after approval.

More detail: [HOW_TO_USE.md](./HOW_TO_USE.md) · [v2 implementation summary](./docs/plans/2026-08-02-v2-implementation-summary.md)

---

## Token optimization

v2 is typically **~25–40% more tokens per full module** than a thin execute-only path, mostly from richer planning and design context — **not** from the learning layer (~3–5%). Quality gates (Critical-only fix loops, product UI blocks) are meant to **buy fewer expensive rework turns**.

### Rough budgets (order of magnitude)

| Path | Approx. total tokens |
|------|----------------------|
| Brainstorm → breakdown only | ~50–120k |
| 1 module lite (BE, plan ready, 0 fix) | ~100–130k |
| 1 module typical (FE+BE, 1 Critical fix) | ~250–320k |
| Heavy (UI + 2–3 fix loops / fat skills) | ~450k–1M+ |

Context packet default budget: **8k** (`context-budget.json` / manifest). Per-turn agent load is often ~10–18k input when loader behaves.

### Do (high ROI)

1. **Use context-builder** — never `read` entire skill trees.  
2. **Product UI** → `saas-product-ui` + one composition / needed blocks only.  
3. **Skip plan phases** when `PLAN_APPROVED` already covers the module.  
4. **Split sessions**: long genesis plan in one chat; implement in a fresh session if history is huge.  
5. **Judge**: Critical → fix loop; Minor → backlog (no loop burn).  
6. **Cap fix loops** (e.g. 2–3).  
7. **Memory Phase 0**: only `docs/memory/*` + `module-deps`, not all of `docs/plans/`.  
8. **Learning**: lightweight until `modulesSinceLastProposal >= 5`; Phase 6 distill ≤10 facts.  
9. Prefer `.memory/constraints.md` over full `AGENTS.md` mid-implement when cache is fresh.  
10. **Never** load full `taste-design/taste-skill` (~large) for in-app product work.

### Don’t

- Mega-commit / one agent turn for entire FE+BE+DB  
- Re-brainstorm after an approved plan  
- Treat chat as durable memory  
- Treat `.memory/*` as equal to `docs/memory/*`  

### Lite vs full mode (same repo)

| Mode | Use when |
|------|----------|
| **Lite** | One-shot BE, skip long brainstorm, skip skill-updater |
| **Standard** | Normal product modules + memory write |
| **Full** | UI modules + learning full pass after ≥5 modules |

---

## Core loop (text)

```text
Requirement
    → Architecture / module plan (approve)
    → Implement (scoped workers + skills)
    → Test
    → Judge (Critical vs Minor)
    → Fix loop (Critical only)
    → Memory distill + learning dispatch
    → Done
```

---

## What this is not

- ❌ A prompt pack only  
- ❌ An LLM runtime / Cursor fork  
- ❌ Guaranteed zero-shot correctness  

Cursor executes; this repo supplies **roles, gates, memory, and skills**.

---

## Documentation map

| Doc | Purpose |
|-----|---------|
| [HOW_TO_USE.md](./HOW_TO_USE.md) | Operator detail |
| [AGENTS.md](./AGENTS.md) | Domain template (fill per project) |
| [docs/plans/2026-08-02-v2-implementation-summary.md](./docs/plans/2026-08-02-v2-implementation-summary.md) | What landed on v2 |
| [.cursor/context/README.md](./.cursor/context/README.md) | CLI vs library scripts |
| [.cursor/rules/007-memory-learning.mdc](./.cursor/rules/007-memory-learning.mdc) | Memory + learning rules |

---

## Contributing

Issues, discussions, and PRs welcome. Star the repo if the approach helps your team.

## Acknowledgements

Ideas adapted from the broader AI-engineering community, including:

- [Taste](https://github.com/Leonxlnx/taste-skill)  
- [Superpowers](https://github.com/obra/superpowers)  

This repository combines and extends patterns into a portable AI SDLC — it is not a fork of a single upstream project.

## License

MIT — see [LICENSE](./LICENSE).
