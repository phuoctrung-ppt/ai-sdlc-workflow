---
name: data-table
category: data
dial_compatibility:
  variance: [2, 4]
  motion: [1, 3]
  density: [7, 9]
when_to_use: "Primary list/report UI: customers, payments, issues, jobs, audit logs."
not_for: "Card galleries for browsing (marketplace discovery may use cards instead)."
stack: [react, next, tailwind]
---

# Data Table + Toolbar

## Visual sketch

```
┌─ Toolbar ─────────────────────────────────────────────┐
│ [Search……]  [Status ▾] [Filter]     [Export] [+ New] │
├─ bulk bar (when selection) ───────────────────────────┤
│ 3 selected · [Archive] [Delete]              [Clear]  │
├───────────────────────────────────────────────────────┤
│ ☐  Name            Status     Amount        Updated   │  sticky header
│ ☐  Acme Corp       Paid       $1,200.00     2h ago    │
│ ☑  Globex          Pending      $480.00     1d ago    │  row hover
│ …                                                     │
└───────────────────────────────────────────────────────┘
  empty / filtered-empty / error replace body
```

## Props API

```ts
type Column<T> = {
  id: string;
  header: string;
  cell: (row: T) => React.ReactNode;
  align?: "left" | "right";
  width?: string;
};

type DataTableProps<T> = {
  columns: Column<T>[];
  rows: T[];
  getRowId: (row: T) => string;
  selectable?: boolean;
  selectedIds?: string[];
  onSelectedIdsChange?: (ids: string[]) => void;
  toolbar: React.ReactNode;
  bulkActions?: React.ReactNode;
  loading?: boolean;
  empty?: React.ReactNode; // first-use empty
  filteredEmpty?: React.ReactNode; // filters active, no rows
  error?: React.ReactNode;
};
```

## Code sketch

```tsx
export function DataTable<T>({
  columns,
  rows,
  getRowId,
  selectable,
  selectedIds = [],
  onSelectedIdsChange,
  toolbar,
  bulkActions,
  loading,
  empty,
  filteredEmpty,
  error,
}: DataTableProps<T>) {
  const allSelected = rows.length > 0 && selectedIds.length === rows.length;

  return (
    <div className="flex flex-col gap-3">
      <div className="flex flex-wrap items-center gap-2">{toolbar}</div>
      {selectedIds.length > 0 && bulkActions && (
        <div className="flex items-center gap-2 rounded-md border border-zinc-200 bg-zinc-50 px-3 py-2 text-[13px] dark:border-zinc-800 dark:bg-zinc-900">
          <span className="font-medium tabular-nums">{selectedIds.length} selected</span>
          {bulkActions}
        </div>
      )}
      <div className="overflow-auto rounded-lg border border-zinc-200 dark:border-zinc-800">
        <table className="w-full border-collapse text-left text-[13px]">
          <thead className="sticky top-0 z-10 bg-zinc-50 dark:bg-zinc-900">
            <tr className="border-b border-zinc-200 dark:border-zinc-800">
              {selectable && (
                <th className="w-10 px-3 py-2">
                  <input
                    type="checkbox"
                    checked={allSelected}
                    onChange={() =>
                      onSelectedIdsChange?.(
                        allSelected ? [] : rows.map(getRowId)
                      )
                    }
                    aria-label="Select all"
                  />
                </th>
              )}
              {columns.map((col) => (
                <th
                  key={col.id}
                  className={
                    "px-3 py-2 text-[12px] font-medium text-zinc-500 " +
                    (col.align === "right" ? "text-right" : "")
                  }
                  style={{ width: col.width }}
                >
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr>
                <td colSpan={columns.length + (selectable ? 1 : 0)} className="px-3 py-8 text-center text-zinc-500">
                  Loading…
                </td>
              </tr>
            )}
            {!loading && error && (
              <tr>
                <td colSpan={columns.length + (selectable ? 1 : 0)}>{error}</td>
              </tr>
            )}
            {!loading && !error && rows.length === 0 && (
              <tr>
                <td colSpan={columns.length + (selectable ? 1 : 0)}>
                  {filteredEmpty ?? empty}
                </td>
              </tr>
            )}
            {!loading &&
              !error &&
              rows.map((row) => {
                const id = getRowId(row);
                const checked = selectedIds.includes(id);
                return (
                  <tr
                    key={id}
                    className="border-b border-zinc-100 hover:bg-zinc-50 dark:border-zinc-900 dark:hover:bg-zinc-900/50"
                  >
                    {selectable && (
                      <td className="px-3 py-2">
                        <input
                          type="checkbox"
                          checked={checked}
                          onChange={() => {
                            const next = checked
                              ? selectedIds.filter((x) => x !== id)
                              : [...selectedIds, id];
                            onSelectedIdsChange?.(next);
                          }}
                          aria-label={`Select row ${id}`}
                        />
                      </td>
                    )}
                    {columns.map((col) => (
                      <td
                        key={col.id}
                        className={
                          "px-3 py-2 text-zinc-800 dark:text-zinc-200 " +
                          (col.align === "right" ? "text-right tabular-nums" : "")
                        }
                      >
                        {col.cell(row)}
                      </td>
                    ))}
                  </tr>
                );
              })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

**Toolbar composition (recommended):**

```tsx
<div className="flex w-full flex-wrap items-center gap-2">
  <input className="h-8 min-w-[200px] flex-1 rounded-md border border-zinc-200 px-2 text-[13px] dark:border-zinc-700" placeholder="Search…" />
  {/* filters */}
  <div className="ml-auto flex gap-2">
    <button type="button" className="h-8 rounded-md border px-3 text-[13px]">Export</button>
    <button type="button" className="h-8 rounded-md bg-zinc-900 px-3 text-[13px] text-white dark:bg-zinc-100 dark:text-zinc-900">New</button>
  </div>
</div>
```

## Mobile fallback

- Prefer **stacked list rows** (card-per-row) under `md` when > 4 columns.
- Keep toolbar search full width; collapse secondary filters into "Filters" sheet.
- Horizontal scroll table is acceptable for financial/admin density if list transform loses meaning.

## Motion variants

Row hover only (CSS). Bulk bar: simple mount/unmount; optional 100ms opacity at band 4–7.

## Dark-mode notes

Sticky header needs solid background (not translucent) to avoid row bleed-through.

## Anti-patterns

- Same copy for first-use empty and filtered empty
- Spinner-only full-page load (use skeleton rows)
- Primary CTA left-aligned in toolbar (keep right)
- Zebra stripes + heavy borders (pick one subtle separator)

## References

- Data table UI reference 2026 (toolbar, selection, dual empty states)
- Linear issue list density; Stripe payments tables
