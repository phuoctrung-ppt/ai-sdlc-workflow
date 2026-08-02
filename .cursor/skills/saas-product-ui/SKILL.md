---
name: saas-product-ui
description: In-app SaaS product UI — app shell, sidebar, data tables, settings, empty/loading states, onboarding. Not marketing landings (use taste-design for those).
---

# SaaS Product UI

Portable skill for **product surfaces** inside a modern SaaS app. Complements `taste-design` (marketing / landing / portfolio only).

> References: Linear (calm default, keyboard density), Stripe Dashboard (tables + metric hierarchy),
> Notion (modular views), Vercel (quiet chrome), Attio (AI-native density). Patterns reflect 2025–2026 SaaS norms:
> collapsible sidebar nav, 4px grid, neutral + one accent + semantic status colors.

## When to use

| Surface | Use this skill |
|---------|----------------|
| App shell, sidebar, top bar, command palette | Yes |
| Lists, data tables, filters, bulk actions | Yes |
| Settings, billing, team/members, audit logs | Yes |
| Empty / loading / error states inside the app | Yes |
| Onboarding checklist, empty workspace first-run | Yes |
| Marketing landing, pricing page, portfolio | **No → taste-design** |
| Dense enterprise analytics (Carbon/Fluent mandated) | Prefer official DS from taste-skill §2.A |

## Step 0 — Surface type + domain pack

1. Declare **Surface**: `product` (this skill) vs `marketing` (taste-design).
2. Read `AGENTS.md` domain / industry if filled; load matching pack under `references/`:
   - `fintech.md` — payments, banking, ledgers
   - `ai-devtools.md` — AI tools, IDEs, agent consoles
   - `marketplace.md` — multi-sided commerce, listings
   - `health-care.md` — clinical / wellness (calm, a11y-first)
   - `b2b-ops.md` — internal ops, admin, multi-tenant control planes
3. If domain unknown, use **defaults** in this file and note `domain-pack: generic`.

## Product dials (different from marketing)

| Dial | Product default | Marketing (taste-skill) |
|------|-----------------|-------------------------|
| `DESIGN_VARIANCE` | **3–5** | 7–9 |
| `MOTION_INTENSITY` | **2–4** | 6–8 |
| `VISUAL_DENSITY` | **6–8** | 3–5 |

**Rules:**
- Product UI is **boring on purpose** — hierarchy and scan speed beat spectacle.
- Motion only for feedback (open modal, row select, toast) — not scroll theater.
- Density serves data work; do not apply gallery spacing (`py-32`) to app content.

## Block library (implement from these first)

Prefer composition from `blocks/` instead of inventing new chrome:

| Need | Block file |
|------|------------|
| Primary nav | `blocks/app-shell/sidebar-nav.md` |
| Top chrome | `blocks/app-shell/top-bar.md` |
| Home KPIs | `blocks/dashboard/metric-strip.md` |
| Lists / reports | `blocks/data/data-table.md` |
| No data | `blocks/states/empty-state.md` |
| Loading | `blocks/states/skeleton-page.md` |
| Settings | `blocks/settings/settings-section.md` |
| First-run setup | `blocks/onboarding/checklist.md` |
| ⌘K | `blocks/navigation/command-palette.md` |

Index + schema: `blocks/README.md`.

Each block includes: ASCII sketch, props API, code sketch, mobile fallback, motion bands, dark notes, anti-patterns.

## Foundations (2026 SaaS norms)

### Navigation
- **Default:** collapsible sidebar **240–280px** (often 256px) + optional contextual sub-nav.
- One primary nav pattern per product (sidebar **or** top nav — not both competing).
- Active item: solid/soft highlight, not neon glow.
- Mobile: sidebar → drawer; preserve current route label in top bar.

### Grid & spacing
- **4px base grid.** Allowed steps: 4, 8, 12, 16, 24, 32, 48.
- Content max width for forms/settings: ~640–720px; tables: full content column.
- Page padding: 16–24px mobile, 24–32px desktop — not marketing hero padding.

### Color system
- **Neutral surfaces + text** (zinc/slate/stone family — pick one, lock it).
- **One brand accent** for primary actions only.
- **Semantic colors only for status** (success / warning / error / info) — never as decorative accents.
- Ship **light + dark** tokens from day one for product chrome.

### Typography
- UI sans (Geist, Inter *only if project already uses it*, system-ui stack) — readability > personality.
- Mono for IDs, amounts, timestamps, code-ish metadata.
- Table/body: 13–14px; labels: 12–13px; page titles: 18–20px — not marketing display scale.

### Iconography
- One family (Phosphor / Radix / Tabler). Stroke width locked.
- No emoji as navigation icons.

## Core patterns

### App shell
```
┌──────────┬─────────────────────────────┐
│ Sidebar  │ Top bar (crumbs / search /  │
│ 256px    │ user menu)                  │
│          ├─────────────────────────────┤
│          │ Page header + primary CTA   │
│          ├─────────────────────────────┤
│          │ Content (table / form /     │
│          │ canvas)                     │
└──────────┴─────────────────────────────┘
```

### Data tables
- Sticky header; row hover; selection + bulk bar when needed.
- Toolbar: search + filters left; primary action right.
- **first-use empty ≠ filtered empty** (different copy + CTA).

### Metric strip
- 4–6 KPIs; one north-star emphasized; skeleton while loading.

### Settings / onboarding / command palette
- See corresponding blocks under `blocks/`.

## Anti-patterns (product UI)

- Marketing hero, bento spectacle, or scroll-hijack **inside** the authenticated app
- Three equal feature cards as a dashboard
- AI-purple gradients on chrome
- Centered "welcome" manifesto instead of the user's work list
- Fake div screenshots of the product inside the product
- Mixing Fluent + shadcn in the same tree
- Dense charts on the home view when a simple list is the daily driver

## Design spec requirements (product track)

1. **Surface type:** `product`
2. **Domain pack** used (or `generic`)
3. **Product dials** (V/M/D)
4. **Blocks used** (list ids from `blocks/`)
5. **Shell:** sidebar width, nav IA, top bar contents
6. **Components:** table / form / empty states with all interaction states
7. **Tokens:** `docs/design/tokens.md` updates
8. **Sketches:** app frames under `docs/design/sketches/{feature}/`
9. **Asset pack:** N/A unless branded empty-state art / custom icons

## Pre-flight (product)

- [ ] Surface type `product`
- [ ] Domain pack applied or generic
- [ ] Blocks chosen from library (or justify custom)
- [ ] Sidebar/top-nav: one primary pattern; width 240–280px if sidebar
- [ ] Spacing on 4px grid only
- [ ] One accent + semantic status only
- [ ] Table/list: sticky header, toolbar, dual empty states
- [ ] No marketing layout families inside app shell
- [ ] Light + dark tokens considered
- [ ] WCAG AA; `prefers-reduced-motion` respected

## Handoff keywords

```
saas,product-ui,app-shell,sidebar,dashboard,data-table,settings,empty-state,onboarding,billing,command-palette
```

## References (lazy)

| File | When |
|------|------|
| `references/fintech.md` | Payments, banking |
| `references/ai-devtools.md` | AI / eng tools |
| `references/marketplace.md` | Listings / multi-vendor |
| `references/health-care.md` | Clinical / wellness |
| `references/b2b-ops.md` | Admin / multi-tenant |
| `blocks/README.md` | Block index + schema |
