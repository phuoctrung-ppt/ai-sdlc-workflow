---
name: skill-updater
description: Read retrospective + memory, identify repeating patterns, propose concrete patches to SKILL.md or new patterns. True self-learning — never silent rewrite. No state.json.
---

# Skill Updater

## Pass mode (no state file)

- Task mentions `/skill-update` or `full pass` → **full** retrospective + memory scan.
- Otherwise → **lightweight** (latest retrospective entries only) unless ≥2 strong signals justify a proposal.

**Do not** read or write `.cursor/state/workflow-state.json` (or any `.cursor/state/**`, `.aisdlc/*.json`). Those files are tooling/UI only and must stay out of the context packet.

Durable facts belong in `docs/memory/*` (primary SoT). `.memory/*` is AGENTS cache only.

Portable skill for the Learning layer (Tầng 3). Used by `@learning-agent` after modules complete.

## Goal

Turn retrospective signals into **durable skill improvements** so the next session is smarter without relying on chat memory.

## Inputs (always read)

1. `docs/retrospective.md` — newest entries first; look for repeating root causes / pattern candidates
2. `docs/memory/decisions.md`, `gotchas.md`, `shortcuts.md` — existing compressed truth
3. Target skill(s) under `.cursor/skills/**/SKILL.md` or patterns under `.cursor/patterns/**`
4. Optional: related `docs/reviews/*`

## When to run

- After every module Done (lightweight scan — may conclude "no pattern yet")
- Full pass when orchestrator / human runs `/skill-update`

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
- Opening state JSON files into the context window

## After approval

1. Apply the patch.
2. Set proposal Status to `APPLIED`.
3. Optional retrospective note: `Skill updated: <path>`.
4. Register new pattern files in pattern index when required.
