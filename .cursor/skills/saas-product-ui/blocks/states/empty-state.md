---
name: empty-state
category: states
dial_compatibility:
  variance: [2, 5]
  motion: [1, 3]
  density: [5, 7]
when_to_use: "No data to show: first-use, filtered empty, cleared content, or soft error."
not_for: "Loading (use skeleton). Hard permission errors (use dedicated error/forbidden)."
stack: [react, next, tailwind]
---

# Empty State

## Variants

| Variant | When | CTA |
|---------|------|-----|
| `first-use` | User has never created objects | Create / Import |
| `no-results` | Filters/search active, zero rows | Clear filters |
| `cleared` | User deleted all items | Create again |
| `error-soft` | Failed load but recoverable | Retry |

## Visual sketch

```
┌─────────────────────────────────────┐
│                                     │
│         (optional icon 32–48)       │
│         Title                       │
│         Short explanation           │
│         [ Primary CTA ]  [Secondary]│
│                                     │
└─────────────────────────────────────┘
  centered in table body or page region
```

## Props API

```ts
type EmptyStateProps = {
  variant: "first-use" | "no-results" | "cleared" | "error-soft";
  title: string;
  description?: string;
  icon?: React.ReactNode;
  primaryAction?: { label: string; onClick: () => void };
  secondaryAction?: { label: string; onClick: () => void };
  size?: "sm" | "md"; // sm = in-table; md = page
};
```

## Code sketch

```tsx
const defaults: Record<EmptyStateProps["variant"], { title: string; description: string }> = {
  "first-use": {
    title: "No items yet",
    description: "Create your first item to get started.",
  },
  "no-results": {
    title: "No results",
    description: "Try adjusting filters or search.",
  },
  cleared: {
    title: "All clear",
    description: "There is nothing here right now.",
  },
  "error-soft": {
    title: "Could not load",
    description: "Something went wrong. You can try again.",
  },
};

export function EmptyState({
  variant,
  title,
  description,
  icon,
  primaryAction,
  secondaryAction,
  size = "md",
}: EmptyStateProps) {
  const d = defaults[variant];
  return (
    <div
      className={
        "flex flex-col items-center justify-center text-center " +
        (size === "sm" ? "px-4 py-10" : "px-6 py-16")
      }
    >
      {icon && <div className="mb-3 text-zinc-400">{icon}</div>}
      <h3 className="text-[15px] font-medium text-zinc-900 dark:text-zinc-50">
        {title || d.title}
      </h3>
      <p className="mt-1 max-w-sm text-[13px] text-zinc-500">
        {description || d.description}
      </p>
      <div className="mt-4 flex flex-wrap items-center justify-center gap-2">
        {primaryAction && (
          <button
            type="button"
            onClick={primaryAction.onClick}
            className="h-8 rounded-md bg-zinc-900 px-3 text-[13px] text-white dark:bg-zinc-100 dark:text-zinc-900"
          >
            {primaryAction.label}
          </button>
        )}
        {secondaryAction && (
          <button
            type="button"
            onClick={secondaryAction.onClick}
            className="h-8 rounded-md border border-zinc-200 px-3 text-[13px] dark:border-zinc-700"
          >
            {secondaryAction.label}
          </button>
        )}
      </div>
    </div>
  );
}
```

## Mobile fallback

Same structure; full-width buttons stacked if needed.

## Motion variants

None. Optional 150ms fade when data resolves to empty.

## Dark-mode notes

Icon muted (`text-zinc-500`); do not use large illustrative gradients.

## Anti-patterns

- Toolbar/filters on full-page first-use empty (nothing to filter) — PatternFly guidance
- Blameful copy ("You failed to…")
- Same message for `first-use` and `no-results`
- Huge illustrations crowding small table empties (use `size="sm"`)

## References

- Carbon empty states pattern; PatternFly empty state sizes
- Dual empty states: first-use vs filtered (data table guides 2026)
