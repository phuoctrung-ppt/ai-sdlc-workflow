---
name: dev-module
description: Full per-module loop + memory distill + learning-counter inc + office events. No raw state.json in context.
---

# Module Development Loop

Act as **Orchestrator** for module: **{feature_name}**

> If `PLAN_APPROVED` exists for this module → skip Phase 1–2.

## Context hygiene

**Do not** open into context:

- `.cursor/state/workflow-state.json` (use CLI below for learning counter only)
- `.cursor/state/module-*-loop.json`
- `.aisdlc/*`

Resume from `docs/plans/`, `docs/module-deps.md`, `docs/memory/*`.

Learning counter (write-only side effect, stdout is one compact JSON line):

```bash
python3 .cursor/scripts/learning-counter.py get
python3 .cursor/scripts/learning-counter.py inc --module {feature_name}
```

Office UI (when `.aisdlc/` exists):

```bash
python3 .cursor/scripts/office-event.py --agent <id> --status working|done|idle|waiting|error --task "…" --phase <phase> --workflow {feature_name}
```

---

## Phase 0 — Orient

```bash
cat docs/memory/decisions.md docs/memory/gotchas.md docs/memory/shortcuts.md 2>/dev/null || true
cat docs/module-deps.md 2>/dev/null || true
python3 .cursor/scripts/office-event.py --agent architect-planner --status working --task "Orient {feature_name}" --phase restore --workflow {feature_name}
```

---

## Phases 1–5

Same as before: brainstorm → plan → scaffold → execute → test → judge/fix.  
Emit `office-event.py` on each phase enter/exit. Use `context-builder.py` per agent.  
Hard-gate execute on `docs/module-deps.md`.

---

## Phase 6 — Done + Memory + Learning counter

1. Append `docs/retrospective.md`
2. Facts → `docs/memory/*` (1–5)
3. `docs/module-deps.md` → module `done`
4. **Increment counter** (do not edit state JSON by hand):

```bash
python3 .cursor/scripts/learning-counter.py inc --module {feature_name}
# stdout e.g. {"modulesSinceLastProposal": 3, "fullPassRecommended": false}
```

5. Dispatch `@learning-agent`:
   - If stdout `fullPassRecommended: true` → task text includes `full pass`
   - Else → lightweight scan

```bash
python3 .cursor/scripts/office-event.py --agent learning-agent --status working --task "Skill scan after {feature_name}" --phase review --workflow {feature_name}
python3 .cursor/context/context-builder.py \
  --phase review \
  --task "post-module skill scan for {feature_name}" \
  --agent learning-agent \
  --keywords "retrospective,pattern,skill,learning,gotcha,shortcut" \
  --budget 5000
python3 .cursor/scripts/office-event.py --agent learning-agent --status done --task "Learning finished" --phase review --workflow {feature_name}
```

If learning writes a proposal, it runs `learning-counter.py reset --proposal <path>` itself.

Explicit full pass anytime: `/skill-update`.
