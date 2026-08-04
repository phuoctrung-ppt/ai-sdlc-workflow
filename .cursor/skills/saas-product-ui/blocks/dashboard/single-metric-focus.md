---
name: single-metric-focus
category: dashboard
dial_compatibility:
  variance: [2, 4]
  motion: [1, 3]
  density: [5, 7]
when_to_use: "Home/overview when one number dominates decisions (revenue, deploy health, pipeline). Stripe/Vercel pattern."
not_for: "Analytics products where the job is exploring many metrics equally (prefer dense metric grids carefully)."
stack: [react, next, tailwind]
---

# Single-Metric Focus

## Visual sketch

```
┌─────────────────────────────────────────────┐
│ Revenue                                     │
│ $128,400.12          ▲ 12.4% vs last period │
│                                             │
│ [secondary metrics as quiet row underneath] │
└─────────────────────────────────────────────┘
```

North-star is **large and alone**; secondary metrics are smaller, equal weight to each other, never competing with the hero number.

## Props API

```ts
type SecondaryMetric = { label: string; value: string; href?: string };

type SingleMetricFocusProps = {
  label: string;
  value: string;
  delta?: { text: string; tone: "up" | "down" | "neutral" };
  secondary?: SecondaryMetric[]; // max 4
  href?: string;
  loading?: boolean;
};
```

## Code sketch

```tsx
export function SingleMetricFocus({
  label,
  value,
  delta,
  secondary = [],
  href,
  loading,
}: SingleMetricFocusProps) {
  if (loading) {
    return <div className="h-32 animate-pulse rounded-lg border border-zinc-200 bg-zinc-100 dark:border-zinc-800 dark:bg-zinc-900" />;
  }
  const Inner = (
    <>
      <div className="text-[13px] font-medium text-zinc-500">{label}</div>
      <div className="mt-2 text-3xl font-semibold tracking-tight tabular-nums text-zinc-900 dark:text-zinc-50 sm:text-4xl">
        {value}
      </div>
      {delta && (
        <div
          className={
            "mt-2 text-[13px] tabular-nums " +
            (delta.tone === "up"
              ? "text-emerald-600"
              : delta.tone === "down"
                ? "text-red-600"
                : "text-zinc-500")
          }
        >
          {delta.text}
        </div>
      )}
      {secondary.length > 0 && (
        <div className="mt-6 flex flex-wrap gap-x-6 gap-y-2 border-t border-zinc-100 pt-4 dark:border-zinc-800">
          {secondary.slice(0, 4).map((s) => (
            <div key={s.label}>
              <div className="text-[11px] text-zinc-500">{s.label}</div>
              <div className="text-[14px] font-medium tabular-nums text-zinc-800 dark:text-zinc-200">{s.value}</div>
            </div>
          ))}
        </div>
      )}
    </>
  );
  const className =
    "block rounded-lg border border-zinc-200 bg-white p-5 dark:border-zinc-800 dark:bg-zinc-950";
  return href ? (
    <a href={href} className={className}>
      {Inner}
    </a>
  ) : (
    <div className={className}>{Inner}</div>
  );
}
```

## Mobile fallback

Hero number remains dominant; secondary wrap 2×2.

## Motion variants

None required. Optional number fade-in ≤ 150ms.

## Dark-mode notes

Large type must pass contrast; avoid light-gray hero numbers on dark.

## Anti-patterns

- Four equally large KPI cards (use `metric-strip` only when no true north-star)
- Chart overlapping the hero number on first paint

## References

- Stripe revenue seat; Vercel deploy status “one question”
- `references/benchmarks-2026.md`
