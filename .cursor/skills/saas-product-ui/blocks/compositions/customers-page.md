---
name: customers-page
category: composition
dial_compatibility:
  variance: [3, 5]
  motion: [2, 4]
  density: [7, 8]
when_to_use: "Reference composition: list page inside product shell — assemble, don't reinvent."
not_for: "Marketing customer logos section."
stack: [react, next, tailwind]
---

# Composition: Customers list page

Assembles existing blocks into one screen agents should mirror.

## Layout

```
┌ SidebarNav ─┬ TopBar ────────────────────────────┐
│             │ PageHeader (Customers + Add)       │
│             │ DataTable toolbar + rows           │
│             │   StatusBadge in status column     │
│             │ EmptyState / Skeleton as needed    │
└─────────────┴────────────────────────────────────┘
  FilterSheet from toolbar · ConfirmDialog on delete · Toast on save
```

## Block map

| Region | Block |
|--------|-------|
| Nav | `app-shell/sidebar-nav` |
| Chrome | `app-shell/top-bar` |
| Title | `app-shell/page-header` |
| List | `data/data-table` |
| Status col | `data/status-badge` |
| Filters | `data/filter-sheet` |
| Loading | `states/skeleton-page` variant `table` |
| Empty | `states/empty-state` |
| Delete | `states/confirm-dialog` tone danger |
| Feedback | `states/toast` |

## Quality bar

- Density 7–8: compact rows (`py-2`), 13px type
- One primary CTA only: **Add customer**
- Numbers/dates tabular
- No hero, no bento, no purple glow
- Light + dark tokens from `references/tokens.md`

## Acceptance checklist

- [ ] Shell consistent with rest of app
- [ ] Dual empty states wired
- [ ] Skeleton before spinner
- [ ] Destructive confirm required
- [ ] WCAG AA on text/chips
