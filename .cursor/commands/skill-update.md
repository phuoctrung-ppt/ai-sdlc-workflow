---
name: skill-update
description: Run the Learning layer — read retrospective, identify patterns, propose SKILL.md / pattern patches via @learning-agent. True self-learning entrypoint (full pass).
---

# Skill Update (Learning Layer)

Act as **Orchestrator**. Dispatch the learning loop (does not implement product features).

**Do not** open `.cursor/state/**` or `.aisdlc/*.json`.

## Steps

1. Ensure Memory layer files exist:
   - `docs/retrospective.md`
   - `docs/memory/decisions.md`, `gotchas.md`, `shortcuts.md`

2. Dispatch `@learning-agent` with an explicit **full pass**:

```bash
python3 .cursor/context/context-builder.py \
  --phase review \
  --task "skill update full pass from retrospective" \
  --agent learning-agent \
  --keywords "retrospective,pattern,skill,learning,gotcha,shortcut" \
  --budget 5000
```

3. Agent must follow skill `skill-updater`:
   - Identify patterns from retrospective (≥2 signals)
   - Write proposal to `docs/reviews/YYYY-MM-DD-skill-update-proposal.md` **or** report no pattern
   - Update memory files when facts are durable
   - **Do not** apply SKILL.md patches until you approve

4. Present proposal to human/orchestrator:
   - Approve → agent applies patch, marks APPLIED
   - Reject → leave PENDING or close with reason

## Notes

- This command is the explicit **full** Learning entrypoint.
- `/dev-module` Phase 6 only does lightweight distillation + a short learning-agent scan.
