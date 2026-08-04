---
name: ranked-list
category: data
dial_compatibility:
  variance: [3, 5]
  motion: [1, 4]
  density: [7, 9]
when_to_use: "Queues where priority matters: leads, inbox, issues to triage (Attio ranked attention)."
not_for: "Alphabetical directories, pure accounting ledgers needing stable sort only."
stack: [react, next, tailwind]
---

# Ranked List

Not every row is equal. Surface **why** a row is on top (score, reason, AI rank) without turning the list into a dashboard.

## Visual sketch

```
┌────────────────────────────────────────────────────┐
│ 1  Acme Corp          High intent · +$42k   [Open] │
│ 2  Globex             Stale 14d · Owner: you       │
│ 3  Initech            Meeting tomorrow             │
└────────────────────────────────────────────────────┘
```

## Props API

```ts
type RankedItem = {
  id: string;
  title: string;
  subtitle?: string;
  reason?: string; // why ranked here
  rank?: number;
  href?: string;
  trailing?: React.ReactNode;
};

type RankedListProps = {
  items: RankedItem[];
  loading?: boolean;
  empty?: React.ReactNode;
};
```

## Code sketch

```tsx
export function RankedList({ items, loading, empty }: RankedListProps) {
  if (loading) {
    return (
      <div className="space-y-2">
        {Array.from({ length: 5 }).map((_, i) => (
          <div key={i} className="h-14 animate-pulse rounded-md bg-zinc-100 dark:bg-zinc-900" />
        ))}
      </div>
    );
  }
  if (!items.length) return <>{empty}</>;
  return (
    <ol className="divide-y divide-zinc-100 overflow-hidden rounded-lg border border-zinc-200 dark:divide-zinc-900 dark:border-zinc-800">
      {items.map((item, index) => (
        <li key={item.id}>
          <a
            href={item.href}
            className="flex items-center gap-3 px-3 py-2.5 hover:bg-zinc-50 dark:hover:bg-zinc-900/60"
          >
            <span className="w-5 shrink-0 text-center font-mono text-[12px] text-zinc-400">
              {item.rank ?? index + 1}
            </span>
            <div className="min-w-0 flex-1">
              <div className="truncate text-[13px] font-medium text-zinc-900 dark:text-zinc-50">
                {item.title}
              </div>
              {(item.subtitle || item.reason) && (
                <div className="truncate text-[12px] text-zinc-500">
                  {[item.reason, item.subtitle].filter(Boolean).join(" · ")}
                </div>
              )}
            </div>
            {item.trailing}
          </a>
        </li>
      ))}
    </ol>
  );
}
```

## Mobile fallback

Full-width rows; rank column stays narrow.

## Motion variants

None. Reorder updates should not animate wildly (confuses scan).

## Dark-mode notes

Rank index muted; title high contrast.

## Anti-patterns

- Showing rank without a readable **reason**
- Gamified trophies / podium chrome
- Equal-weight table when the product promise is prioritization

## References

- Attio “ranked attention” (2026 dashboard teardowns)
