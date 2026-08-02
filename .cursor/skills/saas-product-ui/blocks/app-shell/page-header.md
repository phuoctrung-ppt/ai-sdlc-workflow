---
name: page-header
category: app-shell
dial_compatibility:
  variance: [2, 5]
  motion: [1, 3]
  density: [6, 8]
when_to_use: "Title row under top bar: page name, optional description, primary + secondary actions."
not_for: "Marketing heroes, full-bleed banners inside the app."
stack: [react, next, tailwind]
---

# Page Header

## Visual sketch

```
┌────────────────────────────────────────────────────┐
│ Customers                    [Export]  [+ Add]     │
│ Manage workspace customers                         │
└────────────────────────────────────────────────────┘
```

## Props API

```ts
type PageHeaderProps = {
  title: string;
  description?: string;
  actions?: React.ReactNode;
  meta?: React.ReactNode; // e.g. last synced
};
```

## Code sketch

```tsx
export function PageHeader({ title, description, actions, meta }: PageHeaderProps) {
  return (
    <div className="flex flex-col gap-3 border-b border-zinc-200 pb-4 dark:border-zinc-800 sm:flex-row sm:items-start sm:justify-between">
      <div className="min-w-0">
        <h1 className="truncate text-[18px] font-semibold tracking-tight text-zinc-900 dark:text-zinc-50">
          {title}
        </h1>
        {description && (
          <p className="mt-1 max-w-2xl text-[13px] text-zinc-500">{description}</p>
        )}
        {meta && <div className="mt-1 text-[12px] text-zinc-400">{meta}</div>}
      </div>
      {actions && <div className="flex shrink-0 flex-wrap items-center gap-2">{actions}</div>}
    </div>
  );
}
```

## Mobile fallback

Actions full-width row under title; primary button first.

## Motion variants

None.

## Dark-mode notes

Border uses `--border`; title uses `--text`.

## Anti-patterns

- Title > 24px (marketing scale)
- Gradient underlines, badge walls next to title
- Hiding the only primary CTA in a kebab menu on desktop

## References

- Linear / Vercel page headers: quiet type, actions right
