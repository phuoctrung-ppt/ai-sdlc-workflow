#!/usr/bin/env bash
# Inject workflow context at session start
set -euo pipefail

jq -n '{
  "additional_context": "Workflow V2 active. Before coding: python3 .cursor/context/context-builder.py --task \"<task>\" --agent <agent> [--paths ...] [--keywords ...]. Obey Context Packet tiers; read .memory/ not full AGENTS.md. Legacy: --use-legacy-loader. Handoffs: .cursor/context/handoffs/*.json. Plans: docs/plans/. Reviews: docs/reviews/ (audit only, not context)."
}'
