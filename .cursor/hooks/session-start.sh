#!/bin/bash
# Session start — inject Workflow V2 operating context for the agent.

cat <<'EOF'
{
  "additional_context": "Workflow V2 active. Context CLI (hyphen only): python3 .cursor/context/context-builder.py --task \"<task>\" --agent <agent> [--paths ...] [--keywords ...]. Obey Context Packet tiers. Memory SoT: docs/memory/{decisions,gotchas,shortcuts}.md — read these for durable facts. .memory/* is a generated cache from AGENTS.md (python3 .cursor/context/memory-loader.py --sync); do not treat it as peer SoT. Learning counter: .cursor/state/workflow-state.json modulesSinceLastProposal. Legacy loader: --use-legacy-loader. Handoffs: .cursor/context/handoffs/*.json. Plans: docs/plans/. Reviews: docs/reviews/ (audit only, not context)."
}
EOF
