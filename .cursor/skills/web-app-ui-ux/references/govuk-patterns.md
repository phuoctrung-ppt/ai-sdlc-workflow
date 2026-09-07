# Interaction & content patterns (GOV.UK-inspired)

Source: https://github.com/alphagov/govuk-design-system · https://design-system.service.gov.uk/  
License: MIT. Drop GOV.UK chrome/tokens; keep portable rules.

## Pattern chooser

| Pattern | Use when | Avoid when |
|---------|----------|------------|
| **Single question / step** | High-stakes or complex input | Simple settings that fit one screen |
| **Radios** | Mutually exclusive, ≤ ~7 options | Many options → select; multi → checkboxes |
| **Tabs** | Parallel views of same object | Sequential wizard steps (use steps instead) |
| **Accordion** | Rarely needed detail on long pages | Primary navigation or critical path content |
| **Table** | Compare like rows on shared columns | Card grid when comparison is the task |
| **Error summary** | Form submit with ≥1 field error | Inline-only errors with no page-level summary on long forms |

## Error copy (portable)

- Lead with what went wrong; end with how to fix.
- Sentence case; plain language; no blame.
- Link summary items to the field (focus moves to control).
- Example: “Enter an email address in the format name@example.com” — not “Invalid input”.

## Progressive disclosure

- One disclosure pattern per view (tabs **or** accordion **or** show-more).
- Do not hide required fields behind collapsed sections without indicating incomplete state.

## Empty states

- First-use empty ≠ filtered-empty.
- Always: short explanation + primary recovery action (create, clear filters, import).
