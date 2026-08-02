---
name: onboarding-checklist
category: onboarding
dial_compatibility:
  variance: [3, 5]
  motion: [1, 4]
  density: [5, 7]
when_to_use: "In-app setup progress after first login; dismissible checklist in product shell."
not_for: "Full-screen marketing carousels, blocking paywalls disguised as onboarding."
stack: [react, next, tailwind]
---

# Onboarding Checklist

## Visual sketch

```
┌─────────────────────────────────────┐
│ Get started              2/4  [✕]   │
│ ████████░░░░ 50%                    │
│ ✓ Create workspace                  │
│ ✓ Invite teammate                   │
│ ○ Connect integration    [Start]    │
│ ○ Run first report       [Start]    │
└─────────────────────────────────────┘
```

## Props API

```ts
type ChecklistItem = {
  id: string;
  label: string;
  done: boolean;
  href?: string;
  onAction?: () => void;
};

type OnboardingChecklistProps = {
  title?: string;
  items: ChecklistItem[];
  onDismiss?: () => void;
};
```

## Code sketch

```tsx
export function OnboardingChecklist({
  title = "Get started",
  items,
  onDismiss,
}: OnboardingChecklistProps) {
  const done = items.filter((i) => i.done).length;
  const total = items.length || 1;
  const pct = Math.round((done / total) * 100);

  return (
    <section className="rounded-lg border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-950">
      <div className="flex items-center gap-2">
        <h2 className="text-[14px] font-medium text-zinc-900 dark:text-zinc-50">{title}</h2>
        <span className="font-mono text-[12px] text-zinc-500">
          {done}/{total}
        </span>
        {onDismiss && (
          <button type="button" className="ml-auto text-zinc-400 hover:text-zinc-600" onClick={onDismiss} aria-label="Dismiss">
            ✕
          </button>
        )}
      </div>
      <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-zinc-100 dark:bg-zinc-800">
        <div className="h-full bg-zinc-900 dark:bg-zinc-100" style={{ width: `${pct}%` }} />
      </div>
      <ul className="mt-3 space-y-1">
        {items.map((item) => (
          <li key={item.id} className="flex items-center gap-2 text-[13px]">
            <span className={item.done ? "text-emerald-600" : "text-zinc-400"}>
              {item.done ? "✓" : "○"}
            </span>
            <span className={item.done ? "text-zinc-500 line-through" : "text-zinc-800 dark:text-zinc-200"}>
              {item.label}
            </span>
            {!item.done && (item.href || item.onAction) && (
              <button
                type="button"
                className="ml-auto text-[12px] font-medium text-zinc-900 underline dark:text-zinc-100"
                onClick={item.onAction}
              >
                Start
              </button>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}
```

## Mobile fallback

Full width in content column; do not pin over primary CTA permanently.

## Motion variants

Progress bar width transition ≤ 200ms at band 4–7.

## Dark-mode notes

Progress fill uses neutral foreground, not accent purple.

## Anti-patterns

- Non-dismissible forever
- Blocking modal every session after completion
- More than ~7 checklist items (split or prioritize)

## References

- Skill onboarding: checklist in product > marketing carousel
