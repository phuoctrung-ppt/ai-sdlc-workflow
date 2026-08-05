---
name: saas-product-ui
description: In-app SaaS product UI — app shell, tables, ranked lists, settings, AI summary. Knowledge-hub / VN SME domain packs included. Not marketing (use taste-design). Requires Design Contract.
---

# SaaS Product UI

Portable skill for **authenticated product surfaces**. Complements `taste-design` (marketing only).

**Hard rules (always):** `references/hard-rules-product.md` — paste into every product Design Contract.

**Design Contract template:** `docs/design/_templates/design-contract.v1.md`  
Benchmarks: `references/benchmarks-2026.md`  
Visual pipeline: `../taste-design/ui-visual-pipeline.md`  
Phase: `../planning/references/design-specification-phase.md`

## When to use

| Surface | This skill |
|---------|------------|
| App shell, sidebar, ⌘K | Yes |
| Lists, tables, ranked queues, filters | Yes |
| Knowledge hub / upload / sync confirm | Yes — `references/knowledge-hub-saas.md` |
| Home / overview | Yes |
| Settings, billing, onboarding | Yes |
| Marketing landing / pricing | **No → taste-design** (+ `references/sme-marketing-vn.md` for VN SME copy) |

## Step 0 — Surface, domain, tokens, benchmark, contract

1. Surface = `product`.
2. Domain pack:
   - Knowledge / multi-module business AI → **`knowledge-hub-saas.md`**
   - Else: `fintech` | `ai-devtools` | `marketplace` | `health-care` | `b2b-ops` | generic
3. Lock `references/tokens.md` → `docs/design/tokens.md`.
4. Declare home pattern (calm list-first default for knowledge products).
5. Author **Design Contract** (numeric) from template; paste **hard-rules-product**.
6. Sketches under `docs/design/sketches/{feature}/`.

## Product dials

| Dial | Product | Marketing |
|------|---------|-----------|
| VARIANCE | **3–5** | 7–9 |
| MOTION | **2–4** | 6–8 |
| DENSITY | **6–8** | 3–5 |

## Hall-of-fame patterns

| Pattern | Source | Block |
|---------|--------|-------|
| Calm default — work list first | Linear | `data-table` / `ranked-list` |
| Single-metric focus | Stripe, Vercel | `single-metric-focus` |
| Ranked attention | Attio | `ranked-list` |
| AI as surface | Attio | `ai-summary-surface` |

## Block library

`blocks/README.md` — prefer compositions `dashboard-home`, `customers-page`.  
When listing `blocks_used` in the contract, prefer ids that exist under `blocks/`.

## Anti-patterns

- Chart wallpaper / 12 equal KPIs
- Marketing bento inside app
- AI-purple gradients, sparkle spam
- Skipping Design Contract / sketch (violates DESIGN-GATE)
- Soft guideline-only specs without layout/type numbers

## Design Contract must include

1. Track product + domain pack id  
2. Hard-rules checklist (copied)  
3. Benchmark pattern  
4. Tokens pointer  
5. Blocks + composition ids  
6. Numeric layout + typography + component enums  
7. States: loading, empty×2, error  
8. Sketch path under `docs/design/sketches/{feature}/`

## Handoff keywords

```
saas,product-ui,app-shell,knowledge-hub,sidebar,dashboard,data-table,ranked-list,ai-summary,settings,empty-state,command-palette,design-contract
```
