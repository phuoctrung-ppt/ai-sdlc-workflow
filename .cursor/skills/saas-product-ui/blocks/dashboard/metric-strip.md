---
name: metric-strip
category: dashboard
dial_compatibility:
  variance: [2, 5]
  motion: [1, 3]
  density: [6, 8]
when_to_use: "Overview / home: 4–6 KPIs with one north-star metric emphasized (Stripe-style)."
not_for: "Marketing feature grids, 12-tile walls, chart-first homes when list is the daily driver."
stack: [react, next, tailwind]
---

# Metric Strip

## Visual sketch

```
┌──────────────┬──────────┬──────────┬──────────┐
│ Revenue      │ Customers│ Churn    │ MRR      │
│ $128,400  ▲  │ 1,042    │ 2.1%     │ $42.1k   │
│ primary card │          │          │          │
└──────────────┴──────────┴──────────┴──────────┘
  north-star spans emphasis (border or larger type)
```

## Props API

```ts
type Metric = {
  id: string;
  label: string;
  value: string; // preformatted
  delta?: { value: string; tone: "up" | "down" | "neutral" };
  href?: string; // drill-down
  primary?: boolean; // north-star
};

type MetricStripProps = {
  metrics: Metric[]; // max 6
  loading?: boolean;
};
```

## Code sketch

```tsx
export function MetricStrip({ metrics, loading }: MetricStripProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="h-24 animate-pulse rounded-lg border border-zinc-200 bg-zinc-100 dark:border-zinc-800 dark:bg-zinc-900" />
        ))}
      </div>
    );
  }
  return (
    <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
      {metrics.slice(0, 6).map((m) => (
        <a
          key={m.id}
          href={m.href}
          className={
            "rounded-lg border p-4 " +
            (m.primary
              ? "border-zinc-300 bg-white dark:border-zinc-600 dark:bg-zinc-900"
              : "border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-950")
          }
        >
          <div className="text-[12px] text-zinc-500">{m.label}</div>
          <div className="mt-1 font-semibold tabular-nums tracking-tight text-zinc-900 dark:text-zinc-50 text-xl">
            {m.value}
          </div>
          {m.delta && (
            <div
              className={
                "mt-1 text-[12px] tabular-nums " +
                (m.delta.tone === "up"
                  ? "text-emerald-600"
                  : m.delta.tone === "down"
                    ? "text-red-600"
                    : "text-zinc-500")
              }
            >
              {m.delta.value}
            </div>
          )}
        </a>
      ))}
    </div>
  );
}
```

## Mobile fallback

- 2-column grid; primary metric first.
- Horizontal scroll only if > 4 metrics and product insists — prefer wrap.

## Motion variants

None required. Optional fade-in of values when loading completes (band 4–7, 150ms opacity).

## Dark-mode notes

Semantic up/down colors must pass contrast on dark surfaces; do not use accent brand color for deltas.

## Anti-patterns

- More than 6 KPIs
- Equal visual weight when one north-star exists
- Charts inside every card by default (link to Insights instead — Linear pattern)

## References

- Stripe dashboard metric hierarchy; Linear calm default
