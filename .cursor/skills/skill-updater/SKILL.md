---
name: skill-updater
description: Read retrospective + memory, identify repeating patterns, propose concrete patches to SKILL.md or new patterns. True self-learning — never silent rewrite.
---

# Skill Updater

## Counter gate

Read `.cursor/state/workflow-state.json` → `modulesSinceLastProposal`:
- `>= 5` or task says full pass / `/skill-update` → full retrospective + memory scan.
- `< 5` → lightweight (latest entries only) unless ≥2 strong signals justify a proposal.
- After writing a proposal, reset counter to `0` and set `lastSkillProposalPath` / `lastSkillProposalAt`.

Durable facts belong in `docs/memory/*` (primary SoT). `.memory/*` is AGENTS cache only.

Portable skill for the Learning layer (Tầng 3). Used by `@learning-agent` after modules complete.

## Goal

Turn retrospective signals into **durable skill improvements** so the next session is smarter without relying on chat memory.

## Inputs (always read)

1. `docs/retrospective.md` — newest entries first; look for repeating root causes / pattern candidates
2. `docs/memory/decisions.md`, `gotchas.md`, `shortcuts.md` — existing compressed truth
3. `.cursor/state/workflow-state.json` — module counter
4. Target skill(s) under `.cursor/skills/**/SKILL.md` or patterns under `.cursor/patterns/**`
5. Optional: related `docs/reviews/*`

## When to run

- After every module Done (lightweight scan — may conclude "no pattern yet")
- **Mandatory full pass** when `modulesSinceLastProposal >= 5`
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

## Output (mandatory)

Write a **proposal** file — never edit SKILL.md in place without approval:

`docs/reviews/YYYY-MM-DD-skill-update-proposal.md`

Status: `PENDING_APPROVAL`. Include trigger, evidence (2+), minimal patch, non-goals.

## Best practices

1. **Propose, don't apply** by default.
2. **Minimal patch** — one pattern → one focused change.
3. Prefer `.cursor/patterns/<domain>/` for reusable anti-patterns.
4. Update `docs/memory/*` in parallel when durable (1–3 lines, dated).
5. Never bulk-rewrite `skills-manifest.v2.json` unless registering a new skill.
6. Idempotent proposals.
7. Proposal body ≤ ~800 tokens.

## Anti-patterns

- Silent rewrite of any `SKILL.md`
- Inventing patterns without retrospective evidence
- Expanding scope to "improve all skills while we're here"

## After approval

1. Apply the patch.
2. Set proposal Status to `APPLIED`.
3. Optional retrospective note: `Skill updated: <path>`.
4. Register new pattern files in pattern index when required.
