# SaaS Product UI — Block Library

Concrete, drop-in patterns for **in-app** surfaces. Complements `saas-product-ui/SKILL.md`.

Marketing / landing blocks live under taste-design (if any) — **do not** mix.

## Index

| Block | Path | Use when |
|-------|------|----------|
| Sidebar nav | `app-shell/sidebar-nav.md` | Primary product navigation |
| Top bar | `app-shell/top-bar.md` | Crumbs, search trigger, user menu |
| Metric strip | `dashboard/metric-strip.md` | Home / overview KPIs (4–6 max) |
| Data table + toolbar | `data/data-table.md` | Primary list/report surfaces |
| Empty state | `states/empty-state.md` | First-use, no-results, error-empty |
| Skeleton page | `states/skeleton-page.md` | Route-level loading |
| Settings section | `settings/settings-section.md` | Workspace / profile / billing forms |
| Onboarding checklist | `onboarding/checklist.md` | In-app setup progress |
| Command palette | `navigation/command-palette.md` | ⌘K navigation + actions |

## Schema (every block file)

```yaml
---
name: block-id
category: app-shell | data | states | settings | onboarding | dashboard | navigation
dial_compatibility:
  variance: [min, max]
  motion: [min, max]
  density: [min, max]
when_to_use: "..."
not_for: "..."
stack: [react, next, tailwind]
---
```

Body sections (required):
1. Visual sketch (ASCII)
2. Props API
3. Code sketch (RSC-friendly; client only when needed)
4. Mobile fallback
5. Motion variants (bands 1–3 / 4–7 — product rarely uses 8–10)
6. Dark-mode notes
7. Anti-patterns
8. References

## Discipline

- One block per file; standalone renderable sketch.
- Spacing on **4px grid** only.
- Product dials: low variance/motion, high density.
- Prefer skeleton over spinner for page loads.
- Empty first-use ≠ empty filtered results (different copy + CTA).
