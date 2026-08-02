# SaaS Product UI — Block Library

Concrete patterns for **in-app** surfaces. Marketing blocks → taste-design only.

## Index

### App shell
| Block | Path |
|-------|------|
| Sidebar nav | `app-shell/sidebar-nav.md` |
| Top bar | `app-shell/top-bar.md` |
| Page header | `app-shell/page-header.md` |

### Dashboard & data
| Block | Path |
|-------|------|
| Metric strip | `dashboard/metric-strip.md` |
| Data table + toolbar | `data/data-table.md` |
| Status badge | `data/status-badge.md` |
| Filter sheet | `data/filter-sheet.md` |

### States
| Block | Path |
|-------|------|
| Empty state | `states/empty-state.md` |
| Skeleton page | `states/skeleton-page.md` |
| Confirm dialog | `states/confirm-dialog.md` |
| Toast | `states/toast.md` |

### Settings & onboarding
| Block | Path |
|-------|------|
| Settings section | `settings/settings-section.md` |
| Billing panel | `settings/billing-panel.md` |
| Onboarding checklist | `onboarding/checklist.md` |

### Navigation
| Block | Path |
|-------|------|
| Command palette | `navigation/command-palette.md` |

### Compositions (assemble, don't invent)
| Recipe | Path |
|--------|------|
| Customers list page | `compositions/customers-page.md` |

## Tokens

Starter semantic tokens: `../references/tokens.md` → copy to `docs/design/tokens.md`.

## Schema

Every block file:

```yaml
---
name: block-id
category: ...
dial_compatibility: { variance, motion, density }
when_to_use / not_for / stack
---
```

Body: sketch · props · code · mobile · motion · dark · anti-patterns · references.

## Quality bar (beautiful SaaS)

1. **Quiet chrome** — hierarchy via type weight + spacing, not gradients
2. **Density for work** — 13px body, tight rows, 4px grid
3. **One accent** — primary CTA only; semantic colors for status
4. **Complete states** — loading skeleton, dual empty, error, confirm
5. **Compose blocks** — compositions/* before inventing new shells
