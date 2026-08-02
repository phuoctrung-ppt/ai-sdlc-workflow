---
name: saas-product-ui
description: In-app SaaS product UI — app shell, tables, ranked lists, settings, AI summary surfaces. Not marketing (use taste-design).
---

# SaaS Product UI

Portable skill for **authenticated product surfaces**. Complements `taste-design` (marketing only).

Benchmarks & patterns: `references/benchmarks-2026.md`  
(Linear, Stripe, Vercel, Attio, Notion, PostHog — 2026 consensus).

## When to use

| Surface | This skill |
|---------|------------|
| App shell, sidebar, ⌘K | Yes |
| Lists, tables, ranked queues, filters | Yes |
| Home / overview (metric or work-first) | Yes |
| Record preview, AI summary panels | Yes |
| Settings, billing, onboarding | Yes |
| Marketing landing / pricing page | **No → taste-design** |

## Step 0 — Surface, domain, tokens, benchmark pattern

1. Surface = `product`.
2. Domain pack: `references/fintech.md` | `ai-devtools.md` | `marketplace.md` | `health-care.md` | `b2b-ops.md` | generic.
3. Lock `references/tokens.md` → `docs/design/tokens.md`.
4. Declare **home pattern** (see below) when designing overview.

## Product dials

| Dial | Product | Marketing |
|------|---------|-----------|
| VARIANCE | **3–5** | 7–9 |
| MOTION | **2–4** | 6–8 |
| DENSITY | **6–8** | 3–5 |

## Hall-of-fame patterns (implement these)

| Pattern | Source | Block / composition |
|---------|--------|---------------------|
| Calm default — work list first | Linear | `data-table` / `ranked-list` + `insights-link` |
| Single-metric focus | Stripe, Vercel | `single-metric-focus` |
| Progressive disclosure | Linear, Notion | `insights-link`; depth not on first paint |
| Ranked attention | Attio | `ranked-list` |
| AI as surface | Attio | `ai-summary-surface` (no purple chrome) |
| Multi-representation record | Attio | list + `record-preview` + ⌘K + page |
| Quiet dense analytics | PostHog | table-first; personality without noise |

Full narrative: `references/benchmarks-2026.md`.

## Block library

Index: `blocks/README.md`.

**Compose first** via:
- `blocks/compositions/dashboard-home.md`
- `blocks/compositions/customers-page.md`

Core families: `app-shell/*`, `dashboard/*`, `data/*`, `states/*`, `settings/*`, `navigation/*`, `onboarding/*`.

## Foundations

- Sidebar 240–280px (256 default); soft active; mobile drawer
- 4px grid; spacing 4–48
- Type: 18–20 title, 13–14 body, 12 meta; tabular nums for money
- One accent (CTA only); semantic chips via `status-badge`
- Dual empty states; skeleton ≠ spinner-only page
- Light + dark tokens from day one

## Anti-patterns

- Chart wallpaper / 12 equal KPIs on home
- Marketing bento or scroll-hijack in-app
- AI-purple gradients, sparkle spam
- Equal-weight rows when product should prioritize
- Different field language across list vs preview vs page
- Insights and daily work fighting for the same default screen

## Design spec must include

1. Surface + domain + dials  
2. Benchmark pattern chosen (calm / single-metric / ranked / …)  
3. Tokens pointer  
4. Blocks + composition ids  
5. States: loading, empty×2, error, confirm  
6. App-frame sketches under `docs/design/sketches/{feature}/`

## Pre-flight

- [ ] Pattern matches product job (not generic pretty dashboard)
- [ ] Blocks composed; chrome not invented
- [ ] Density 6–8; motion feedback-only
- [ ] AI panels are useful surfaces, not decoration
- [ ] WCAG AA; reduced-motion OK

## Handoff keywords

```
saas,product-ui,app-shell,sidebar,dashboard,data-table,ranked-list,ai-summary,settings,billing,empty-state,command-palette,insights
```

## References

| File | When |
|------|------|
| `references/benchmarks-2026.md` | Choosing patterns |
| `references/tokens.md` | Always |
| `references/<domain>.md` | Known industry |
| `blocks/README.md` | Implementation |
