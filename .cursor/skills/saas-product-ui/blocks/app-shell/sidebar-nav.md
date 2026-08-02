---
name: sidebar-nav
category: app-shell
dial_compatibility:
  variance: [2, 5]
  motion: [1, 4]
  density: [6, 9]
when_to_use: "Primary product navigation in authenticated app shell. Default SaaS pattern 2026."
not_for: "Marketing sites, single-page landing, or products that standardize on top-only nav."
stack: [react, next, tailwind]
---

# Sidebar Nav

## Visual sketch

```
┌────────────────────┐
│ [Logo]  Product ▾  │  ← workspace / product switcher
├────────────────────┤
│ ◎ Home             │
│ ● Issues        12 │  ← active: soft fill, not neon
│ ○ Projects         │
│ ○ Inbox          3 │
├────────────────────┤
│ SECONDARY          │  ← optional section label (12px, muted)
│ ○ Views            │
│ ○ Teams            │
│                    │
│      (flex grow)   │
│                    │
├────────────────────┤
│ ○ Settings         │  ← footer cluster
│ ○ Help             │
│ [avatar] You    ▾  │
└────────────────────┘
  width: 256px expanded / 64px collapsed
```

## Props API

```ts
type NavItem = {
  id: string;
  label: string;
  href: string;
  icon: React.ReactNode;
  badge?: number | string;
  children?: NavItem[]; // optional nested
};

type SidebarNavProps = {
  items: NavItem[];
  footerItems?: NavItem[];
  activeId: string;
  collapsed?: boolean;
  onCollapsedChange?: (v: boolean) => void;
  workspace?: { name: string; onSwitch?: () => void };
  widthExpanded?: number; // default 256
  widthCollapsed?: number; // default 64
};
```

## Code sketch

```tsx
"use client";

export function SidebarNav({
  items,
  footerItems = [],
  activeId,
  collapsed = false,
  onCollapsedChange,
  workspace,
  widthExpanded = 256,
  widthCollapsed = 64,
}: SidebarNavProps) {
  const w = collapsed ? widthCollapsed : widthExpanded;
  return (
    <aside
      style={{ width: w }}
      className="flex h-full flex-col border-r border-zinc-200 bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-950"
    >
      <div className="flex h-12 items-center gap-2 border-b border-zinc-200 px-3 dark:border-zinc-800">
        {!collapsed && workspace && (
          <button type="button" onClick={workspace.onSwitch} className="truncate text-sm font-medium">
            {workspace.name}
          </button>
        )}
        <button
          type="button"
          className="ml-auto rounded p-1 text-zinc-500 hover:bg-zinc-200 dark:hover:bg-zinc-800"
          onClick={() => onCollapsedChange?.(!collapsed)}
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {/* icon: panel collapse */}
        </button>
      </div>
      <nav className="flex-1 space-y-0.5 overflow-y-auto p-2">
        {items.map((item) => {
          const active = item.id === activeId;
          return (
            <a
              key={item.id}
              href={item.href}
              className={
                "flex items-center gap-2 rounded-md px-2 py-1.5 text-[13px] " +
                (active
                  ? "bg-zinc-200/80 font-medium text-zinc-900 dark:bg-zinc-800 dark:text-zinc-50"
                  : "text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-900")
              }
            >
              <span className="size-4 shrink-0">{item.icon}</span>
              {!collapsed && <span className="truncate">{item.label}</span>}
              {!collapsed && item.badge != null && (
                <span className="ml-auto font-mono text-[11px] text-zinc-500">{item.badge}</span>
              )}
            </a>
          );
        })}
      </nav>
      <div className="space-y-0.5 border-t border-zinc-200 p-2 dark:border-zinc-800">
        {footerItems.map((item) => (
          <a key={item.id} href={item.href} className="flex items-center gap-2 rounded-md px-2 py-1.5 text-[13px] text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400">
            <span className="size-4">{item.icon}</span>
            {!collapsed && item.label}
          </a>
        ))}
      </div>
    </aside>
  );
}
```

## Mobile fallback

- `< md`: sidebar hidden; open as **drawer** from hamburger in top bar.
- Drawer width `min(100vw - 48px, 280px)`; focus trap + Esc to close.
- Show current section label in top bar when drawer closed.

## Motion variants

| Band | Behavior |
|------|----------|
| 1–3 | Instant width toggle; no animation |
| 4–7 | `transition-[width] duration-200 ease-out`; drawer slide 200ms |
| 8–10 | **Do not use** for product chrome |

Respect `prefers-reduced-motion`: force band 1–3.

## Dark-mode notes

- Surface: `bg-zinc-50` / `dark:bg-zinc-950` (or token `--sidebar`).
- Active: soft neutral fill, not accent wash on entire row (accent reserved for badges/CTA).

## Anti-patterns

- Neon / purple active glow
- Competing top mega-nav + full sidebar labels
- Width outside 240–280 expanded without product reason
- Emoji as nav icons
- Section labels on every group (max sparingly)

## References

- Linear, Notion, Vercel app shells (collapsible sidebar norm 2026)
- Skill foundations: `saas-product-ui/SKILL.md` → Navigation
