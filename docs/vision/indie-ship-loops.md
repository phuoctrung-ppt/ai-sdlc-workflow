# Indie ship loops (code-loop + shape-lite)

**Branch:** `enhance/code-loop-shape-lite`  
**Builds on:** `enhance/indie-ship-loops` / context-orchestration-harden

## Problem

Indie continuous ship does not need a full plan → design-spec → breakdown → execute cycle for every bug or small idea. Forcing full workflow re-entry wastes tokens and slows delivery.

## Solution (domain-agnostic)

| Loop | Command | When | Skips |
|------|---------|------|-------|
| **Code-loop** | `/fix` | Bug, failing test, small patch | Full plan, DESIGN-GATE, learning counter |
| **Shape-lite** | `/shape-lite` | New idea / MVP scope | Full ADR, worker dispatch, DESIGN-GATE |
| **Full module** | `/dev-module` | New module / multi-module feature | (none — gates apply) |

## Preferred skills (already high-signal in this repo)

1. **error-recovery** — primary for every code-loop
2. **agentic-workflow** — orchestration + handoff discipline
3. **saas-product-ui** — in-app product UI only (not marketing)
4. **planning** — shape-lite compactness
5. **api-contract-first** — when API surface changes

Marketing / landing pages continue to use **taste-design** + hard-rules-marketing. Product track stays on saas-product-ui + hard-rules-product.

## Explicit non-goals

- Lock workflow to any product domain (e.g. AI Workspace)
- Re-run DESIGN-GATE on pure code fixes of existing screens
- Require learning-counter increment for one-file hotfixes

## Files

- `.cursor/commands/fix.md`
- `.cursor/commands/shape-lite.md`
- `docs/plans/_templates/shape-lite.md`
- `docs/plans/shape/`
- Policy: `workflow-policy.json` → `loops`
- Matrix: `code-loop-fix`, `shape-lite` rules
- Intent: early `fix` / `shape-lite` phase detection
