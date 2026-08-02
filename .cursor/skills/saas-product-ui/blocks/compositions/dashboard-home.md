---
name: dashboard-home
category: composition
dial_compatibility:
  variance: [3, 5]
  motion: [2, 4]
  density: [6, 8]
when_to_use: "Authenticated home after login — calm, not chart wallpaper."
not_for: "Public marketing dashboard mockups."
stack: [react, next, tailwind]
---

# Composition: Dashboard home

## Layout recipes (pick one primary pattern)

### A — Operator home (Linear-like)
```
Shell → PageHeader → RankedList / DataTable (work)
                      InsightsLink secondary
                      Optional OnboardingChecklist
```

### B — Revenue home (Stripe-like)
```
Shell → PageHeader → SingleMetricFocus (north-star)
                      MetricStrip quiet secondary (≤4)
                      DataTable recent activity
```

### C — AI CRM home (Attio-like)
```
Shell → PageHeader → RankedList (attention)
                      AiSummarySurface (workspace pulse)
                      RecordPreview on hover
```

## Quality bar

- First paint answers **one job**: what should I do / what’s the number / what needs attention
- Progressive disclosure for charts
- Skeleton for metrics + list, not one spinner
- No 12-tile KPI wall

## Block map

| Piece | Block |
|-------|-------|
| Shell | sidebar-nav, top-bar, page-header |
| North-star | single-metric-focus |
| Secondary KPIs | metric-strip |
| Work queue | ranked-list or data-table |
| AI pulse | ai-summary-surface |
| Analysis exit | insights-link |
| Loading | skeleton-page metrics+table |
