---
name: fix
description: Lightweight code/fix loop for indie continuous ship. Intent → Context Packet → narrow worker → verify. Does NOT re-run full plan, DESIGN-GATE, or /dev-module.
---

# Code / Fix Loop (lightweight)

**When to use:** bug, type error, failing test, small implement, rename, style, patch, regression — anything that does **not** need a new feature plan or Design Contract.

**When NOT to use:** new module, new UI surface without existing Design Contract, protected-path architecture change, multi-module feature → use `/plan-feature` or `/dev-module` instead.

Act as **Orchestrator** for a **code-loop** only.

## Hard constraints

1. **No full plan rewrite.** Do not open or recreate `docs/plans/*` unless the user explicitly asks to escalate.
2. **No DESIGN-GATE re-run.** If the change is pure code/fix on existing UI that already has a Design Contract, implement against that contract. If there is no contract and the change is visual + non-trivial, stop and recommend `/shape-lite` or design-spec — do not invent a full marketing redesign.
3. **Context Packet first.** Always run context-builder before editing.
4. **Prefer these skills** (already high-signal in manifest):
   - `error-recovery` — root-cause fix, never mask
   - `agentic-workflow` — handoff + scope discipline
   - `saas-product-ui` — only if in-app product UI is touched
   - `frontend-skills` / domain stack skills — only if paths match
5. **Scope:** stay inside `worker-scopes.json`. Escalate if protected paths need change.

## Context hygiene

Do **not** load into context:

- `.cursor/state/workflow-state.json` (use learning-counter CLI if needed)
- `.aisdlc/*`
- full `docs/plans/` tree (read only the active plan path if relevant)

## Steps

### 0 — Office + classify

```bash
python3 .cursor/scripts/office-event.py --agent architect-planner --status working --task "Code-loop: {issue}" --phase fix --workflow code-loop
```

Detect intent (expect phase `fix`, complexity often `low`):

```bash
python3 .cursor/context/intent-detector.py --task "{issue}" --phase fix --paths "{touched_paths}"
```

### 1 — Context Packet

```bash
python3 .cursor/context/context-builder.py \
  --phase fix \
  --task "{issue}" \
  --agent <narrowest-worker> \
  --paths "{touched_paths}" \
  --keywords "fix,bug,error,patch" \
  --budget 5000
```

Pick **one** primary worker from domains (frontend-worker | backend-worker | database-worker | devops-worker | qa-worker). Optional reviewer only if protected or complexity medium+.

### 2 — Execute (worker)

Handoff packet (minimal):

```text
Objective: {issue}
In-scope paths: {paths}
Out-of-scope: everything else
Plan/ADR: N/A (code-loop)
Design Contract: {path or N/A}
Required skills: error-recovery (+ domain skill if needed)
Acceptance: failing command passes; no unrelated churn
Verification: re-run the failing test/build/typecheck
```

Worker must use **error-recovery** checklist (exact message → file:line → root cause → minimal fix).

```bash
python3 .cursor/scripts/office-event.py --agent <worker> --status working --task "{issue}" --phase fix --workflow code-loop
```

### 3 — Verify

Re-run the **same** failing command (test, tsc, build). If still red → one more root-cause pass, max 2 loops, then escalate to user.

Optional light judge when protected or medium complexity:

```bash
python3 .cursor/context/context-builder.py --phase review --task "review fix for {issue}" --agent judge-agent --budget 3000
```

### 4 — Done

```bash
python3 .cursor/scripts/office-event.py --agent <worker> --status done --task "Fixed: {issue}" --phase fix --workflow code-loop
```

- Do **not** increment learning-counter for trivial one-file fixes unless user asks.
- Append a one-line note to `docs/memory/gotchas.md` only if a durable pitfall was discovered.

## Escalate out of code-loop when

- Need new public API / schema migration affecting multiple modules
- Need new UI screen without Design Contract
- Protected architecture decision

Then: `/shape-lite` (idea) → `/plan-feature` or `/dev-module` as appropriate.
