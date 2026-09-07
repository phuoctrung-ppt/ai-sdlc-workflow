# Interactive component states

Inspired by accessible component libraries (e.g. Adobe React Spectrum — Apache-2.0).  
Framework-agnostic state contract for product UI. React wiring stays in `frontend-skills`.

## Required state set

Every interactive control should define (as applicable):

| State | Meaning |
|-------|---------|
| default | Idle, enabled |
| hover | Pointer over (non-touch) |
| focus / focus-visible | Keyboard or programmatic focus |
| active / pressed | Moment of activation |
| disabled | Not operable; still visible with AA-safe styling |
| loading | Pending result of this control’s action |
| error | Invalid or failed associated input |
| selected / checked | Toggle or choice selected |

## Dialogs / menus / toasts

| Control | Rules |
|---------|--------|
| Dialog / modal | Focus trap; initial focus inside; ESC closes; restore focus to trigger; `role="dialog"` + labelled |
| Menu | Arrow-key navigation; Escape closes; typeahead when long |
| Toast / status | Prefer polite live region; do not require hover-only dismiss; queue, don’t stack aggressively |
| Combobox | Keyboard filter + listbox semantics; announce results count when practical |

## Anti-patterns

- Disabled buttons with no explanation of how to enable
- Loading that replaces the whole page for a local action
- Toasts as the only error channel for form validation
