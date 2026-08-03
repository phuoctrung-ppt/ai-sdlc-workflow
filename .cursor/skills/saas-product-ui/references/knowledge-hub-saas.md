# Domain pack — Knowledge Hub SaaS

For products like **AI Business Workspace**: central business knowledge → marketing / sales / support modules.
ICP: VN SME, agency, startup. First module often **AI Marketing Workspace**.

## Product job (not generic dashboard)

| Job | Primary UI |
|-----|------------|
| Ingest knowledge | Upload / link sources, processing list, conflict flags |
| Single source of truth | Knowledge browser, entity pages (product, policy, FAQ) |
| Sync impact | “Affected surfaces” panel after knowledge edit |
| Module activation | Marketing / Sales / Support toggles from same hub |
| Trust | Diff / confirm before AI overwrites published content |

Home default: **work queue or knowledge list**, not 12 KPIs.

## Benchmark pattern

- **Calm list-first** (Linear): sources, entities, or “needs review” ranked first
- **AI as surface** (Attio-style): summary / conflict panel — useful text, no purple chrome
- **Single-metric** only on growth screens (e.g. leads this week) — optional secondary

## Chrome

- Sidebar: Knowledge, Marketing, Sales, Support, Settings (module-gated)
- Density 6–8; motion 2–4; variance 3–5
- One accent (CTA only); Vietnamese UI copy is first-class
- Empty states: (1) never uploaded (2) filters empty — two different CTAs

## Anti-patterns (this domain)

- Marketing landing hero inside authenticated shell
- “AI brain” illustrations as primary navigation
- Treating chatbot as the home screen of the product app
- Hiding sync/confirm behind toast-only updates

## Tokens bias

Neutral zinc/stone + one brand accent. Prefer **trust and clarity** over spectacle.
See `tokens.md`.

## Blocks to prefer

`app-shell/*`, `data-table` or `ranked-list`, `ai-summary-surface`, `empty-state`, `filter-sheet`, `page-header`, `onboarding/checklist`.
