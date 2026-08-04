---
name: command-palette
category: navigation
dial_compatibility:
  variance: [2, 5]
  motion: [2, 4]
  density: [7, 9]
when_to_use: "Power-user jump to pages/actions (Linear/Raycast style) via ⌘K / Ctrl+K."
not_for: "Simple consumer apps with < 5 destinations and no actions."
stack: [react, next, tailwind]
---

# Command Palette

## Visual sketch

```
          ┌─────────────────────────────┐
          │ Search commands…            │
          ├─────────────────────────────┤
          │ Navigation                  │
          │  Issues                     │
          │  Projects                   │
          │ Actions                     │
          │  Create issue               │
          │  Invite member              │
          └─────────────────────────────┘
               modal centered, dim backdrop
```

## Props API

```ts
type CommandItem = {
  id: string;
  label: string;
  group: string;
  shortcut?: string;
  onSelect: () => void;
};

type CommandPaletteProps = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  items: CommandItem[];
};
```

## Code sketch

```tsx
"use client";

import { useEffect, useMemo, useState } from "react";

export function CommandPalette({ open, onOpenChange, items }: CommandPaletteProps) {
  const [q, setQ] = useState("");
  const filtered = useMemo(() => {
    const s = q.trim().toLowerCase();
    if (!s) return items;
    return items.filter((i) => i.label.toLowerCase().includes(s));
  }, [items, q]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        onOpenChange(!open);
      }
      if (e.key === "Escape") onOpenChange(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onOpenChange]);

  if (!open) return null;

  const groups = [...new Set(filtered.map((i) => i.group))];

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center bg-black/40 pt-[15vh]" role="dialog" aria-modal="true">
      <div className="w-full max-w-lg overflow-hidden rounded-lg border border-zinc-200 bg-white shadow-xl dark:border-zinc-700 dark:bg-zinc-950">
        <input
          autoFocus
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search commands…"
          className="w-full border-b border-zinc-200 bg-transparent px-3 py-3 text-[14px] outline-none dark:border-zinc-800"
        />
        <ul className="max-h-80 overflow-y-auto p-1">
          {groups.map((g) => (
            <li key={g}>
              <div className="px-2 py-1 text-[11px] font-medium uppercase tracking-wide text-zinc-400">{g}</div>
              {filtered
                .filter((i) => i.group === g)
                .map((i) => (
                  <button
                    key={i.id}
                    type="button"
                    className="flex w-full items-center rounded-md px-2 py-1.5 text-left text-[13px] hover:bg-zinc-100 dark:hover:bg-zinc-900"
                    onClick={() => {
                      i.onSelect();
                      onOpenChange(false);
                    }}
                  >
                    {i.label}
                    {i.shortcut && (
                      <kbd className="ml-auto font-mono text-[10px] text-zinc-400">{i.shortcut}</kbd>
                    )}
                  </button>
                ))}
            </li>
          ))}
          {filtered.length === 0 && (
            <li className="px-2 py-6 text-center text-[13px] text-zinc-500">No commands</li>
          )}
        </ul>
      </div>
    </div>
  );
}
```

## Mobile fallback

Full-screen sheet from bottom or full viewport; large tap targets; no reliance on ⌘K only (provide search button in top bar).

## Motion variants

| Band | Behavior |
|------|----------|
| 1–3 | Instant open/close |
| 4–7 | 150ms opacity + slight scale on panel |

## Dark-mode notes

Backdrop `bg-black/50`; panel solid surface.

## Anti-patterns

- Palette without keyboard shortcut on desktop power-tool products
- Mixing navigation and destructive actions without grouping
- Unscoped global listener without cleanup

## References

- Linear / Raycast command menu patterns; skill command palette section
