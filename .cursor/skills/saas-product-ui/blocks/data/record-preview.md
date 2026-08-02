---
name: record-preview
category: data
dial_compatibility:
  variance: [3, 5]
  motion: [2, 4]
  density: [6, 8]
when_to_use: "Hover/focus preview of an entity without leaving the list (Attio multi-representation)."
not_for: "Full editing surfaces (use record page). Tooltips for icon-only labels."
stack: [react, next, tailwind]
---

# Record Preview

Same object model as list row and full page — **compressed representation**.

## Visual sketch

```
┌─────────────────────────────┐
│ Acme Corp          [Open]   │
│ Customer · SF               │
│ ARR $42k · Stage Proposal   │
│ Owner Maya · Updated 2h     │
└─────────────────────────────┘
```

## Props API

```ts
type RecordField = { label: string; value: React.ReactNode };

type RecordPreviewProps = {
  title: string;
  subtitle?: string;
  fields: RecordField[]; // max 6
  href?: string;
  footer?: React.ReactNode;
};
```

## Code sketch

```tsx
export function RecordPreview({ title, subtitle, fields, href, footer }: RecordPreviewProps) {
  return (
    <div className="w-72 rounded-lg border border-zinc-200 bg-white p-3 shadow-lg dark:border-zinc-700 dark:bg-zinc-950">
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <div className="truncate text-[13px] font-semibold text-zinc-900 dark:text-zinc-50">{title}</div>
          {subtitle && <div className="truncate text-[12px] text-zinc-500">{subtitle}</div>}
        </div>
        {href && (
          <a href={href} className="shrink-0 text-[12px] font-medium text-zinc-700 underline dark:text-zinc-300">
            Open
          </a>
        )}
      </div>
      <dl className="mt-3 space-y-1.5">
        {fields.slice(0, 6).map((f) => (
          <div key={f.label} className="flex justify-between gap-3 text-[12px]">
            <dt className="text-zinc-500">{f.label}</dt>
            <dd className="truncate text-right text-zinc-800 dark:text-zinc-200">{f.value}</dd>
          </div>
        ))}
      </dl>
      {footer && <div className="mt-3 border-t border-zinc-100 pt-2 dark:border-zinc-800">{footer}</div>}
    </div>
  );
}
```

## Mobile fallback

On touch, prefer navigate to full record or bottom sheet — not hover.

## Motion variants

Band 4–7: 100–150ms opacity. No layout jump of the list underneath.

## Dark-mode notes

Elevated shadow subtle; solid panel background.

## Anti-patterns

- Preview with different field names than full page (breaks multi-representation)
- Editable forms inside hover preview

## References

- Attio: list / hover / ⌘K / page same underlying record
