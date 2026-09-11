---
name: agentic-workflow
description: Planner-Worker-Judge orchestration, phases, handoffs, protected changes, code-loop and shape-lite principles.
---

# agentic-workflow (Codex adapter)

1. Read and follow `.cursor/skills/agentic-workflow/SKILL.md`.
2. On Codex: main thread acts as orchestrator; spawn named subagents from `.codex/config.toml` roles only when the user asks for parallel specialists or the task is clearly multi-track.
3. Day path: fix and shape-lite first; full plan secondary.
