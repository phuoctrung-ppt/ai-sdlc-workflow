---
status: PENDING_APPROVAL
kind: skill-scout
date: YYYY-MM-DD
brief: ""
# After human approve, set:
# status: APPROVED
# approved_by: <name>
# approved_at: YYYY-MM-DD
# After apply:
# status: APPLIED
# applied_at: YYYY-MM-DD
proposed_skill:
  id: kebab-case-id
  portable: true
  entry: kebab-case-id/SKILL.md
  referencesDir: kebab-case-id/references
  phases: []
  agents: []
  keywords: []
  priority: 8
  estimatedTokens: 800
  merge_into: null  # or existing skill id
sources_selected: []
---

# Skill Scout Proposal

## Brief

What the human asked to ingest and stack constraints.

## Candidates scored

### Candidate: {owner}/{repo}

- URL:
- Score: /20 (A–J: …)
- Hard gates: PASS | FAIL
- Fit / portable extract / drop / license / risk:
- Decision: shortlist | reject

## Recommended source(s)

1. …

## Distill plan (thin entry)

- **When to use**
- **Hard rules** (5–12 bullets max in entry)
- **Anti-patterns**
- **References** (filenames only; content stays lazy)
- **Attribution** (URL + SPDX)

## Manifest load map (draft)

Must be filled before APPROVE so apply is mechanical:

| Field | Value | Rationale |
|-------|--------|-----------|
| phases | | |
| agents | | |
| keywords | | Specific nouns; avoid only `test`/`code` |
| priority | 6–10 | Scout default; do not exceed 12 without ask |
| merge_into | null / id | |

## Conflicts

Overlap with existing skills (ids): …

## Human decision

- [ ] APPROVE as new skill
- [ ] APPROVE merge into existing
- [ ] REJECT

Comment:
