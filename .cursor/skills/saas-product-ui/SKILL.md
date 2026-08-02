---
name: saas-product-ui
description: In-app SaaS product UI — app shell, sidebar, data tables, settings, empty/loading states, onboarding. Not marketing landings (use taste-design for those).
---

# SaaS Product UI

Portable skill for **product surfaces** inside a modern SaaS app. Complements `taste-design` (marketing / landing / portfolio only).

> References: Linear (calm default, keyboard density), Stripe Dashboard (tables + metric hierarchy),
> Notion (modular views), Vercel (quiet chrome). 2025–2026 norms: collapsible sidebar, 4px grid,
> neutral + one accent + semantic status.

## When to use

| Surface | Use this skill |
|---------|----------------|
| App shell, sidebar, top bar, command palette | Yes |
| Lists, data tables, filters, bulk actions | Yes |
| Settings, billing, team/members, audit logs | Yes |
| Empty / loading / error / confirm / toast | Yes |
| Onboarding checklist | Yes |
| Marketing landing, pricing page, portfolio | **No → taste-design** |

## Step 0 — Surface + domain + tokens

1. Surface: `product` (this skill).
2. Domain pack under `references/` when known: fintech, ai-devtools, marketplace, health-care, b2b-ops.
3. Lock tokens from `references/tokens.md` into `docs/design/tokens.md` (one neutral family, one accent).

## Product dials

| Dial | Product | Marketing |
|------|---------|-----------|
| VARIANCE | **3–5** | 7–9 |
| MOTION | **2–4** | 6–8 |
| DENSITY | **6–8** | 3–5 |

Boring on purpose: scan speed > spectacle.

## Block library — prefer these

Full index: `blocks/README.md`.

| Need | Block |
|------|-------|
| Nav / top / title | `blocks/app-shell/*` |
| KPIs | `blocks/dashboard/metric-strip.md` |
| Tables / badges / filters | `blocks/data/*` |
| Empty / skeleton / confirm / toast | `blocks/states/*` |
| Settings / billing | `blocks/settings/*` |
| Onboarding | `blocks/onboarding/checklist.md` |
| ⌘K | `blocks/navigation/command-palette.md` |
| Full page recipe | `blocks/compositions/customers-page.md` |

**Rule:** compose from blocks + compositions before inventing new chrome.

## Foundations

- Sidebar 240–280px (default 256); soft active state; mobile drawer
- Spacing 4 / 8 / 12 / 16 / 24 / 32 / 48
- Type: 18–20 title, 13–14 body/table, 12 label; mono for money/IDs
- Semantic status only via `status-badge` tones
- Dual empty: first-use ≠ filtered
- Skeleton matching layout, not spinner-only pages

## Anti-patterns

- Marketing hero / bento / scroll-hijack in authenticated app
- AI-purple chrome, three equal feature cards as dashboard
- Same copy for first-use and filtered empty
- Instant destructive actions without `confirm-dialog`
- Second accent color mid-product

## Design spec must include

1. Surface `product` + domain pack + dials  
2. Tokens pointer  
3. **Blocks used** (ids)  
4. Shell widths + nav IA  
5. States: loading / empty / error / confirm  
6. Sketches: app frames under `docs/design/sketches/{feature}/`

## Pre-flight

- [ ] Tokens locked (neutral + one accent + semantic)
- [ ] Blocks from library (or justify custom)
- [ ] Composition followed when list/settings/billing
- [ ] Density 6–8; motion feedback-only
- [ ] WCAG AA; reduced-motion respected
- [ ] No marketing patterns inside shell

## Handoff keywords

```
saas,product-ui,app-shell,sidebar,dashboard,data-table,settings,billing,empty-state,onboarding,command-palette
```

## References

| File | When |
|------|------|
| `references/tokens.md` | Always for product track |
| `references/*.md` domain packs | Known industry |
| `blocks/README.md` | Implementing UI |
