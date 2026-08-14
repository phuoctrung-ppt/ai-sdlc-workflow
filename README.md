# AI SDLC Workflow (Cursor)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/phuoctrung-ppt/ai-sdlc-workflow)](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/commits)
[![Repo Stars](https://img.shields.io/github/stars/phuoctrung-ppt/ai-sdlc-workflow?style=social)](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/stargazers)

> **Production-oriented AI Software Development Lifecycle for [Cursor](https://cursor.com).**  
> Structured engineering instead of giant one-shot prompts — **without forcing a full plan loop for every bug.**

**Domain-agnostic + profile-aware.** Port to FE-only, BE-only, or fullstack by filling `AGENTS.md §0` (layers) — no hand-trimming of plan commands per repo.

**Branch note:** Project profile + layers on [`enhance/project-profile-layers`](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/tree/enhance/project-profile-layers) (from `v2`). Indie ship loops on [`enhance/code-loop-shape-lite`](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/tree/enhance/code-loop-shape-lite). Core v2 on [`v2`](https://github.com/phuoctrung-ppt/ai-sdlc-workflow/tree/v2).

> ⚠️ **Status:** Profile/layer filtering is implemented on the enhance branch; validate on a real FE-only and BE-only port before treating as production-default.

---

## Day-to-day (indie continuous ship)

| Need | Command | Skips |
|------|---------|-------|
| Bug, failing test, small patch | **`/fix`** | Full plan, DESIGN-GATE |
| New idea / “should we build X?” | **`/shape-lite`** | GENESIS, full ADR |
| Structural feature | `/plan-feature` | (layer-conditional checklist) |
| Idea → whole system | `/architecture-plan brainstorming …` | (genesis; §0 first) |

---

## Quick start (portable port)

```bash
git clone https://github.com/phuoctrung-ppt/ai-sdlc-workflow.git
cd ai-sdlc-workflow
git checkout enhance/project-profile-layers

# In your app repo: copy .cursor/ + AGENTS.md, then:
# 1) Fill AGENTS.md §0 profile + layers
python3 .cursor/context/profile-sync.py --from-agents
python3 .cursor/context/memory-loader.py --sync
```

```text
/fix <bug>
/shape-lite <idea>
/plan-feature <desc>          # no forced DB/tenancy if layers off
```

Details: [HOW_TO_USE.md](./HOW_TO_USE.md) · [docs/vision/project-profile-layers.md](./docs/vision/project-profile-layers.md)

---

## Why profile + layers

v2 still injected full-stack plan sections (migrations, multi-tenant, queues) into FE-only or BE-only projects. **§0 + `profile-sync` + conditional plan commands** fix that so one workflow tree serves many repo shapes.

---

## Documentation map

| Doc | Purpose |
|-----|---------|
| [HOW_TO_USE.md](./HOW_TO_USE.md) | Operator detail |
| [docs/vision/project-profile-layers.md](./docs/vision/project-profile-layers.md) | Profile/layer design |
| [AGENTS.md](./AGENTS.md) | Template — fill §0 first |
| [.cursor/context/README.md](./.cursor/context/README.md) | context-builder + profile-sync CLI |

---

## License

MIT — see [LICENSE](./LICENSE).
