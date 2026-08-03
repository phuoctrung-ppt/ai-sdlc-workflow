# AI SDLC Workflow (Cursor)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/phuoctrung-ppt/ai-sdlc-workflow)](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/commits)
[![Repo Stars](https://img.shields.io/github/stars/phuoctrung-ppt/ai-sdlc-workflow?style=social)](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/stargazers)

> **Production-oriented AI Software Development Lifecycle for [Cursor](https://cursor.com).**  
> Structured engineering (plan → implement → review → learn) instead of giant one-shot prompts.

**Branch note:** Workflow design on [`v2`](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/tree/v2). CLI + office UI on [`v2-cli-migrate-with-ui-workflow`](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/tree/v2-cli-migrate-with-ui-workflow).

> ⚠️ **Status:** v2 wiring is in place; E2E product pilot is not claimed complete. CLI office UI is a **live board** for agent events (demo + hooks), not a full remote agent runtime.

---

## CLI + office UI (`cli/`)

Initialize a work folder for **Cursor** or **Claude**, then watch the agent team on **http://localhost:9669**.

```bash
git checkout v2-cli-migrate-with-ui-workflow
cd cli && pip install -e .

# from repo root (or any app folder)
ai-sdlc --init cursor          # or: ai-sdlc --init claude
ai-sdlc ui                     # http://127.0.0.1:9669

# other terminal — animate desks
ai-sdlc demo
```

| Command | Purpose |
|---------|---------|
| `ai-sdlc --init cursor\|claude` | Copy `.cursor/`, `AGENTS.md`, `docs/memory/*`, create `.aisdlc/` |
| `ai-sdlc ui` | Office floor UI (SSE event stream) |
| `ai-sdlc event --agent … --status working --task …` | Push a desk update |
| `ai-sdlc demo` | Sample multi-agent session into the feed |
| `ai-sdlc status` | JSON snapshot |

Details: [`cli/README.md`](./cli/README.md).

---

## Walkthrough video

**[`docs/media/ai-sdlc-workflow-explained.mp4`](./docs/media/ai-sdlc-workflow-explained.mp4)** — layers, files, token hotspots (add binary if missing on checkout).

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

## Quick start — how to run (Cursor commands)

```bash
git clone https://github.com/phuoctrung-ppt/ai-sdlc-workflow.git
cd ai-sdlc-workflow
git checkout v2   # or v2-cli-migrate-with-ui-workflow for CLI

python3 .cursor/context/memory-loader.py --sync   # after filling AGENTS.md
```

```text
/architecture-plan brainstorming <idea>
/architecture-plan
/dev-module <module_name>
```

Context CLI (hyphen entry only): `python3 .cursor/context/context-builder.py --task "…" --agent <id>`

More: [HOW_TO_USE.md](./HOW_TO_USE.md) · [v2 summary](./docs/plans/2026-08-02-v2-implementation-summary.md)

---

## Token optimization

v2 is typically **~25–40% more tokens per full module** than a thin execute-only path. Learning layer alone is ~3–5%.

| Path | Approx. tokens |
|------|----------------|
| Brainstorm → breakdown | ~50–120k |
| Module lite | ~100–130k |
| Module typical | ~250–320k |
| Heavy / fat skills | ~450k–1M+ |

**Do:** context-builder only · product blocks not full taste-skill · skip plan if approved · Critical-only fix loops · memory ≤10 facts.  
**Don’t:** mega-turns · chat as memory · `.memory/*` as peer to `docs/memory/*`.

---

## Documentation map

| Doc | Purpose |
|-----|---------|
| [cli/README.md](./cli/README.md) | CLI + office UI |
| [HOW_TO_USE.md](./HOW_TO_USE.md) | Operator detail |
| [AGENTS.md](./AGENTS.md) | Domain template |
| [.cursor/context/README.md](./.cursor/context/README.md) | context-builder CLI vs library |
| [.cursor/rules/007-memory-learning.mdc](./.cursor/rules/007-memory-learning.mdc) | Memory + learning |

---

## License

MIT — see [LICENSE](./LICENSE).
