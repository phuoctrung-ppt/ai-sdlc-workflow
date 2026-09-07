# Mobile navigation IA

## Patterns

| Pattern | Use when | Avoid when |
|---------|----------|------------|
| **Bottom tabs** | 2–5 peer top-level destinations | Deep hierarchy; >5 peers |
| **Stack** | Drill-down hierarchy, detail screens | Replacing all global nav |
| **Sheet / modal** | Focused create/edit, filters, confirms | Multi-step primary journeys that need deep linking as first-class routes |
| **Drawer** | Secondary/settings density (tablet-friendly) | Sole phone nav for peer destinations |

## Rules of thumb

1. One **primary** nav metaphor per app shell (tabs *or* drawer primary — not both fighting).
2. Destructive confirm lives in the flow (dialog/sheet), not hidden behind swipe-only.
3. Back must match OS expectation (edge swipe + visible back on iOS-style stacks).
4. Deep links land on the same screen as in-app navigation (no orphan routes).

## Platform convention notes (not full HIG copy)

- **iOS:** tab bar for peers; large titles optional; modal for discrete tasks.
- **Android / Material 3:** navigation bar for top-level; avoid mixing bar + permanent drawer on phone.

Re-check vendor guidelines when shipping platform-specific chrome.
