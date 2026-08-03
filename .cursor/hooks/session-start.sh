#!/bin/bash
# Session start — inject Workflow V2 operating context for the agent.

cat <<'EOF'
{
  "additional_context": "Workflow V2 active. Context CLI (hyphen only): python3 .cursor/context/context-builder.py --task \"<task>\" --agent <agent> [--paths ...] [--keywords ...]. Obey Context Packet tiers. Memory SoT: docs/memory/{decisions,gotchas,shortcuts}.md. .memory/* is AGENTS cache only (memory-loader.py --sync). Learning counter: .cursor/state/workflow-state.json modulesSinceLastProposal. OFFICE UI: if .aisdlc/ exists, emit desk events with python3 .cursor/scripts/office-event.py --agent <id> --status working|done|idle|waiting|error --task \"...\" --phase <phase> at start/end of every agent turn and every /dev-module phase (rule 008). UI: ai-sdlc ui → http://127.0.0.1:9669. Handoffs: .cursor/context/handoffs/*.json. Plans: docs/plans/. Reviews: docs/reviews/."
}
EOF
