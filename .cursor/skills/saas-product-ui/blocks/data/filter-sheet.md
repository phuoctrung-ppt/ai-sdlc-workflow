---
name: filter-sheet
category: data
dial_compatibility:
  variance: [2, 5]
  motion: [2, 4]
  density: [6, 8]
when_to_use: "Secondary filters that do not fit the table toolbar; mobile filter entry."
not_for: "Primary search (keep search in toolbar). Full page filter dashboards."
stack: [react, next, tailwind]
---

# Filter Sheet

## Visual sketch

```
Desktop: right drawer 320px     Mobile: bottom sheet
┌──────────────────┐
│ Filters      [✕] │
│ Status           │
│ ☑ Paid  ☑ Trial  │
│ Date range       │
│ [from] — [to]    │
│                  │
│ [Reset] [Apply]  │
└──────────────────┘
```

## Props API

```ts
type FilterSheetProps = {
  open: boolean;
  onOpenChange: (v: boolean) => void;
  title?: string;
  children: React.ReactNode; // filter fields
  onApply: () => void;
  onReset: () => void;
  activeCount?: number;
};
```

## Code sketch

```tsx
"use client";

export function FilterSheet({
  open,
  onOpenChange,
  title = "Filters",
  children,
  onApply,
  onReset,
  activeCount = 0,
}: FilterSheetProps) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/40" role="dialog" aria-modal="true">
      <div className="flex h-full w-full max-w-sm flex-col bg-white shadow-xl dark:bg-zinc-950 sm:border-l sm:border-zinc-200 dark:sm:border-zinc-800">
        <div className="flex h-12 items-center justify-between border-b border-zinc-200 px-4 dark:border-zinc-800">
          <h2 className="text-[14px] font-medium">
            {title}
            {activeCount > 0 && (
              <span className="ml-2 font-mono text-[12px] text-zinc-500">{activeCount}</span>
            )}
          </h2>
          <button type="button" className="text-zinc-500" onClick={() => onOpenChange(false)} aria-label="Close">
            ✕
          </button>
        </div>
        <div className="flex-1 space-y-4 overflow-y-auto p-4">{children}</div>
        <div className="flex gap-2 border-t border-zinc-200 p-4 dark:border-zinc-800">
          <button type="button" className="h-9 flex-1 rounded-md border border-zinc-200 text-[13px] dark:border-zinc-700" onClick={onReset}>
            Reset
          </button>
          <button
            type="button"
            className="h-9 flex-1 rounded-md bg-zinc-900 text-[13px] text-white dark:bg-zinc-100 dark:text-zinc-900"
            onClick={() => {
              onApply();
              onOpenChange(false);
            }}
          >
            Apply
          </button>
        </div>
      </div>
    </div>
  );
}
```

## Mobile fallback

Prefer bottom sheet (`items-end` + `max-h-[85vh] rounded-t-xl`) under `sm`.

## Motion variants

Band 4–7: slide-in 200ms. Band 1–3: instant.

## Dark-mode notes

Solid panel; dim backdrop only.

## Anti-patterns

- Applying filters on every checkbox change without Apply (unless product is Linear-instant and documented)
- More than ~8 filter controls without grouping

## References

- Table toolbar secondary filters pattern
