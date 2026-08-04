---
name: settings-section
category: settings
dial_compatibility:
  variance: [2, 4]
  motion: [1, 3]
  density: [5, 7]
when_to_use: "Workspace/profile/billing/security settings forms inside product shell."
not_for: "Marketing account teaser pages, multi-step consumer onboarding wizards with spectacle."
stack: [react, next, tailwind]
---

# Settings Section

## Visual sketch

```
┌────────────┬──────────────────────────────┐
│ Profile    │ Profile                      │
│ Workspace  │ Name     [……………]
│ Billing  ● │ Email    [……………]
│ Security   │                            │
│            │ [Save changes]             │
│            │                            │
│            │ Danger zone                │
│            │ [Delete workspace]         │
└────────────┴──────────────────────────────┘
  sub-nav ~200px     content max-w-xl
```

## Props API

```ts
type SettingsNavItem = { id: string; label: string; href: string };

type SettingsSectionProps = {
  nav: SettingsNavItem[];
  activeId: string;
  title: string;
  description?: string;
  children: React.ReactNode; // fields
  footer?: React.ReactNode; // save bar
  dangerZone?: React.ReactNode;
};
```

## Code sketch

```tsx
export function SettingsSection({
  nav,
  activeId,
  title,
  description,
  children,
  footer,
  dangerZone,
}: SettingsSectionProps) {
  return (
    <div className="flex flex-col gap-6 md:flex-row md:gap-10">
      <nav className="flex shrink-0 gap-1 overflow-x-auto md:w-48 md:flex-col md:overflow-visible">
        {nav.map((item) => (
          <a
            key={item.id}
            href={item.href}
            className={
              "rounded-md px-2 py-1.5 text-[13px] whitespace-nowrap " +
              (item.id === activeId
                ? "bg-zinc-200/80 font-medium text-zinc-900 dark:bg-zinc-800 dark:text-zinc-50"
                : "text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400")
            }
          >
            {item.label}
          </a>
        ))}
      </nav>
      <div className="min-w-0 max-w-xl flex-1 space-y-6">
        <div>
          <h1 className="text-lg font-semibold text-zinc-900 dark:text-zinc-50">{title}</h1>
          {description && <p className="mt-1 text-[13px] text-zinc-500">{description}</p>}
        </div>
        <div className="space-y-4">{children}</div>
        {footer}
        {dangerZone && (
          <div className="border-t border-red-200 pt-6 dark:border-red-900/40">
            <h2 className="text-[13px] font-medium text-red-700 dark:text-red-400">Danger zone</h2>
            <div className="mt-3">{dangerZone}</div>
          </div>
        )}
      </div>
    </div>
  );
}
```

**Field row convention:** label above input; helper muted; error below; `gap-2`.

## Mobile fallback

- Sub-nav becomes horizontal scroll chips.
- Content full width; danger zone still last.

## Motion variants

None. Instant section switches via routing.

## Dark-mode notes

Danger zone uses semantic red, not brand accent.

## Anti-patterns

- Nav labels as eng module names (`UserService`) instead of tasks (`Profile`)
- Instant delete without confirm
- Marketing hero above settings form

## References

- Skill settings section; B2B ops pack for admin density
