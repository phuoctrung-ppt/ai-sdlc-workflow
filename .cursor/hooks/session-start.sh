#!/bin/bash
# Session start — inject Workflow V2 operating context for the agent.

cat <<'EOF'
{
  "additional_context": "Workflow V2 active. Context CLI (hyphen only): python3 .cursor/context/context-builder.py --task \"<task>\" --agent <agent> [--paths ...] [--keywords ...]. Obey Context Packet tiers. Memory SoT: docs/memory/{decisions,gotchas,shortcuts}.md. .memory/* is AGENTS cache only (memory-loader.py --sync). Do NOT read or edit .cursor/state/** or .aisdlc/*.json into context (tooling/UI only). Learning: retrospective + docs/memory; full skill pass via /skill-update. OFFICE UI: if .aisdlc/ exists, emit with python3 .cursor/scripts/office-event.py --agent <id> --status working|done|idle|waiting|error --task \"...\" --phase <phase> (write-only; rule 008). UI: ai-sdlc ui → http://127.0.0.1:9669. Plans: docs/plans/. Reviews: docs/reviews/."
}
EOF
