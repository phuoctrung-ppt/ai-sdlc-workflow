---
name: skill-updater
description: Read retrospective + memory, identify repeating patterns, propose concrete patches to SKILL.md or new patterns. True self-learning — never silent rewrite.
---

# Skill Updater — Learning Best Practices

Portable skill for the Learning layer (Tầng 3). Used by `@learning-agent` after modules complete.

## Goal

Turn retrospective signals into **durable skill improvements** so the next session is smarter without relying on chat memory.

## Inputs (always read)

1. `docs/retrospective.md` — newest entries first; look for repeating root causes / pattern candidates
2. `docs/memory/decisions.md`, `gotchas.md`, `shortcuts.md` — existing compressed truth
3. Target skill(s) under `.cursor/skills/**/SKILL.md` or patterns under `.cursor/patterns/**`
4. Optional: related `docs/reviews/*` and plan for the modules that produced the signal

## When to run

- After every module Done (lightweight scan — may conclude "no pattern yet")
- **Mandatory full pass** when ≥5 new retrospective entries since last skill-update proposal
- When orchestrator / human runs `/skill-update` or dispatches `@learning-agent` explicitly

## Pattern identification rules

A **pattern** is actionable only if ≥2 of:

| Signal | Example |
|--------|---------|
| Same root cause in ≥2 modules | "missing tenant filter" twice |
| Same Critical judge finding class | "no test for acceptance X" |
| Explicit `Pattern candidate` repeated | two entries name the same candidate |
| Estimate vs Actual gap with same cause | plans always under-estimate DB migrations |
| Gotcha that would have prevented a loop | shortcut missing from skill checklist |

**Non-patterns** (do not propose skill changes):
- One-off bugs, typos, environment issues
- Domain-specific product decisions (those go to `docs/memory/decisions.md` only)
- Style nits already covered by existing rules

## Output contract (mandatory)

Write a **proposal** file — never edit SKILL.md in place without approval:

`docs/reviews/YYYY-MM-DD-skill-update-proposal.md`

```markdown
# Skill Update Proposal — YYYY-MM-DD

Status: PENDING_APPROVAL

## Trigger
- Retrospective entries: [list dates/modules]
- Pattern id: `kebab-case-id`
- Confidence: high | medium | low

## Evidence
- Quote 2+ retrospective bullets / root causes
- Related gotcha/shortcut if any

## Proposed change
### Target
- Path: `.cursor/skills/<id>/SKILL.md`  OR  `.cursor/patterns/<area>/<name>.md`
- Change type: amend checklist | add forbidden | add reference | new pattern file

### Patch (unified diff or exact section to insert)
```diff
@@ ...
+ - [ ] New checklist item from pattern
```

### Why this belongs in the skill
One sentence: how the next agent will avoid the same failure.

## Non-goals
- What we deliberately did NOT change

## Approval
- [ ] Orchestrator / human approved
- [ ] Applied (date + commit)
```

## Best practices

1. **Propose, don't apply** — default is PENDING_APPROVAL. Only apply after explicit approval (or a documented auto-apply policy for pure gotcha locks).
2. **Minimal patch** — one pattern → one focused change. Prefer a checklist bullet or a short "Avoid" block over rewriting the whole skill.
3. **Prefer patterns folder** for reusable anti-patterns that are not skill-specific (`.cursor/patterns/<domain>/`).
4. **Update memory in parallel** — if the pattern is a durable gotcha/shortcut/decision, also append to the matching `docs/memory/*` file (1–3 lines, dated).
5. **Never** bulk-load or rewrite `skills-manifest.v2.json` unless registering a brand-new skill.
6. **Idempotent** — if the same proposal already exists as PENDING or APPLIED, do not duplicate; refresh evidence only.
7. **Token discipline** — proposal body ≤ ~800 tokens; patch itself should be the smallest correct change.

## Anti-patterns (skill-updater must not)

- Silent rewrite of any `SKILL.md`
- Inventing patterns without retrospective evidence
- Turning product domain rules into portable skills
- Expanding scope to "improve all skills while we're here"
- Writing implementation code for product features

## After approval

1. Apply the patch to the target file.
2. Set proposal Status to `APPLIED` with date.
3. Optionally add a one-line note under the latest retrospective entry: `Skill updated: <path>`.
4. If a new pattern file was created, ensure it is discoverable (pattern-matcher keywords / index if the repo maintains one).
