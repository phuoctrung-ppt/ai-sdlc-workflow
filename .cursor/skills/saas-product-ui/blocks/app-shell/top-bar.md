---
name: top-bar
category: app-shell
dial_compatibility:
  variance: [2, 4]
  motion: [1, 3]
  density: [6, 8]
when_to_use: "Thin chrome above page content: breadcrumbs, search/command trigger, user menu."
not_for: "Marketing headers, tall agency navs, logo-centered heroes."
stack: [react, next, tailwind]
---

# Top Bar

## Visual sketch

```
┌──────────────────────────────────────────────────────────┐
│ [≡]  Workspace / Projects / Acme          [⌘K Search] ☺ │
└──────────────────────────────────────────────────────────┘
  height: 48–56px
```

## Props API

```ts
type Crumb = { label: string; href?: string };

type TopBarProps = {
  crumbs?: Crumb[];
  onMenuClick?: () => void; // mobile sidebar
  onSearchClick?: () => void; // opens command palette
  searchPlaceholder?: string;
  userSlot?: React.ReactNode;
};
```

## Code sketch

```tsx
export function TopBar({
  crumbs = [],
  onMenuClick,
  onSearchClick,
  searchPlaceholder = "Search…",
  userSlot,
}: TopBarProps) {
  return (
    <header className="flex h-12 shrink-0 items-center gap-3 border-b border-zinc-200 bg-white px-3 dark:border-zinc-800 dark:bg-zinc-950 md:px-4">
      <button type="button" className="md:hidden rounded p-1.5 hover:bg-zinc-100 dark:hover:bg-zinc-900" onClick={onMenuClick} aria-label="Open menu">
        {/* menu icon */}
      </button>
      <nav aria-label="Breadcrumb" className="min-w-0 flex-1 truncate text-[13px] text-zinc-500">
        {crumbs.map((c, i) => (
          <span key={i}>
            {i > 0 && <span className="mx-1.5 text-zinc-300">/</span>}
            {c.href ? (
              <a href={c.href} className="hover:text-zinc-800 dark:hover:text-zinc-200">{c.label}</a>
            ) : (
              <span className="font-medium text-zinc-800 dark:text-zinc-100">{c.label}</span>
            )}
          </span>
        ))}
      </nav>
      <button
        type="button"
        onClick={onSearchClick}
        className="hidden items-center gap-2 rounded-md border border-zinc-200 px-2.5 py-1 text-[12px] text-zinc-500 hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-900 sm:flex"
      >
        <span>{searchPlaceholder}</span>
        <kbd className="rounded border border-zinc-200 px-1 font-mono text-[10px] dark:border-zinc-700">⌘K</kbd>
      </button>
      <div className="shrink-0">{userSlot}</div>
    </header>
  );
}
```

## Mobile fallback

- Show menu button; hide full search field → icon-only opens palette.
- Truncate breadcrumbs to last 1–2 segments.

## Motion variants

Static chrome. No scroll-hide top bar unless product explicitly requires it (rare).

## Dark-mode notes

Match sidebar surface family; 1px border only — no heavy shadow under top bar.

## Anti-patterns

- Height > 64px
- Centered logo + marketing links
- Duplicate primary nav already in sidebar

## References

- Skill: app shell diagram in `SKILL.md`
