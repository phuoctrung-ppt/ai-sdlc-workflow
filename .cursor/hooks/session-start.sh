#!/usr/bin/env bash
# Inject minimal workflow context at session start (keep short — always-on cost).
set -euo pipefail

jq -n '{
  "additional_context": "Workflow repo: read AGENTS.md for domain facts. Hotfix in chat is fine. Features: /dev-module or /plan-feature. Skills via skill-loader only — do not bulk-read .cursor/skills. Protected edits need docs/plans + docs/reviews (or logged review-override)."
}'
