# AI SDLC Workflow (Cursor)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/phuoctrung-ppt/ai-sdlc-workflow)](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/commits)
[![Repo Stars](https://img.shields.io/github/stars/phuoctrung-ppt/ai-sdlc-workflow?style=social)](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/stargazers)

> **Production-oriented AI Software Development Lifecycle for [Cursor](https://cursor.com).**  
> Structured engineering instead of giant one-shot prompts — **without forcing a full plan loop for every bug.**

**Domain-agnostic.** Built for indie developers who ship continuously from an idea. No product-domain lock-in.

**Branch note:** Indie ship loops (`/fix`, `/shape-lite`) on [`enhance/code-loop-shape-lite`](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/tree/enhance/code-loop-shape-lite). Core v2 design on [`v2`](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/tree/v2). CLI + office UI on [`v2-cli-migrate-with-ui-workflow`](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/tree/v2-cli-migrate-with-ui-workflow).

> ⚠️ **Status:** v2 wiring + indie loops are in place; E2E product pilot is not claimed complete. CLI office UI is a **live board** for agent events, not a full remote agent runtime.

---

## Day-to-day (indie continuous ship)

Most work should **not** re-enter the full plan → design → breakdown → execute cycle.

| Need | Command | Skips |
|------|---------|-------|
| Bug, failing test, small patch | **`/fix`** | Full plan, DESIGN-GATE, learning counter |
| New idea / “should we build X?” | **`/shape-lite`** | Full ADR, worker dispatch, DESIGN-GATE |
| New module / multi-module feature | `/plan-feature` or `/dev-module` | (gates apply) |
| Idea → whole system from scratch | `/architecture-plan brainstorming …` | (genesis gates apply) |

```text
Bug / test đỏ ──────────► /fix
Ý tưởng mới ────────────► /shape-lite  →  NEXT: /fix | plan | design-spec | drop
Module lớn ─────────────► /dev-module <name>
```

Details: [HOW_TO_USE.md](./HOW_TO_USE.md) · [docs/vision/indie-ship-loops.md](./docs/vision/indie-ship-loops.md)

---

## Quick start

```bash
git clone https://github.com/phuoctrung-ppt/ai-sdlc-workflow.git
cd ai-sdlc-workflow
git checkout enhance/code-loop-shape-lite   # or v2

# Optional CLI + office UI
cd cli && pip install -e . && cd ..
ai-sdlc --init cursor --path /path/to/your-app --repo .
# fill AGENTS.md in the app, then:
python3 .cursor/context/memory-loader.py --sync
```

In Cursor (inside your app):

```text
/fix <bug description>
/shape-lite <idea in one sentence>
/dev-module <module_name>          # only when scope needs full gates
```

Context CLI: `python3 .cursor/context/context-builder.py --task "…" --agent <id>`

---

## CLI + office UI (`cli/`)

```bash
ai-sdlc --init cursor|claude
ai-sdlc ui                     # http://127.0.0.1:9669
ai-sdlc demo
ai-sdlc event --agent … --status working --task …
ai-sdlc status
```

| Command | Purpose |
|---------|---------|
| `ai-sdlc --init cursor\|claude` | Copy `.cursor/`, `AGENTS.md`, `docs/memory/*`, create `.aisdlc/` |
| `ai-sdlc ui` | Office floor UI (SSE event stream) |
| `ai-sdlc event …` | Push a desk update |
| `ai-sdlc demo` | Sample multi-agent session |

Details: [`cli/README.md`](./cli/README.md).

---

## Why this exists

Most AI coding setups optimize **prompts**. This repo optimizes the **process**:

| Practice | What it means here |
|----------|-------------------|
| Right-sized loops | `/fix` / `/shape-lite` for daily work; full gates only when needed |
| Architecture first | No implement before plan **when the change is structural** |
| Specialized workers | Narrow scopes in `worker-scopes.json` |
| Skill-driven context | Load only relevant skills via context-builder |
| Design Contract for new UI | Numeric design decisions before frontend (full path) |
| Review before “done” | Judge + severity (Critical vs Minor) on protected / full modules |
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
│  Tầng 1  EXECUTE    /fix · /shape-lite · plan → workers │
│                      → judge (full path only)           │
└─────────────────────────────────────────────────────────┘
```

| Layer | Primary paths |
|-------|----------------|
| Execute | `/fix`, `/shape-lite`, `/dev-module`, `/architecture-plan`, `.cursor/agents/*` |
| Memory | `docs/memory/*` (SoT) · `.memory/*` (cache via `memory-loader.py --sync`) |
| Learning | `docs/retrospective.md`, `@learning-agent`, `skill-updater` |

Canonical rule: [`.cursor/rules/007-memory-learning.mdc`](./.cursor/rules/007-memory-learning.mdc).

---

## Token optimization

| Path | Approx. tokens | When |
|------|----------------|------|
| **`/fix` (code-loop)** | low (packet ~5k budget) | Daily bugs / patches |
| **`/shape-lite`** | low–mid | Quick idea scope |
| Brainstorm → breakdown | ~50–120k | New system / roadmap |
| Module typical | ~250–320k | Full `/dev-module` |
| Heavy / fat skills | ~450k–1M+ | Avoid |

**Do:** prefer `/fix` · context-builder only · product blocks not full taste-skill · skip full plan if already approved · memory ≤10 facts.  
**Don’t:** `/dev-module` for a typo · mega-turns · chat as memory · re-run DESIGN-GATE on pure code fixes.

Preferred portable skills: `error-recovery`, `agentic-workflow`, `saas-product-ui`, `planning`, `api-contract-first`.

---

## Documentation map

| Doc | Purpose |
|-----|---------|
| [HOW_TO_USE.md](./HOW_TO_USE.md) | Operator detail — day path + full path |
| [docs/vision/indie-ship-loops.md](./docs/vision/indie-ship-loops.md) | Code-loop + shape-lite rationale |
| [cli/README.md](./cli/README.md) | CLI + office UI |
| [AGENTS.md](./AGENTS.md) | Domain template (fill once per project) |
| [.cursor/context/README.md](./.cursor/context/README.md) | context-builder CLI |

---

## License

MIT — see [LICENSE](./LICENSE).
