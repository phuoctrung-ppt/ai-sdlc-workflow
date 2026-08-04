---
name: status-badge
category: data
dial_compatibility:
  variance: [2, 4]
  motion: [1, 2]
  density: [7, 9]
when_to_use: "Row/status chips: paid, pending, failed, active, trial."
not_for: "Decorative labels, marketing tags, nav badges with brand accent wash."
stack: [react, next, tailwind]
---

# Status Badge

## Visual sketch

`[ Paid ]` soft chip — semantic color only

## Props API

```ts
type StatusTone = "success" | "warning" | "danger" | "info" | "neutral";

type StatusBadgeProps = {
  label: string;
  tone?: StatusTone;
  size?: "sm" | "md";
};
```

## Code sketch

```tsx
const toneClass: Record<StatusTone, string> = {
  success: "bg-emerald-50 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-400",
  warning: "bg-amber-50 text-amber-800 dark:bg-amber-950 dark:text-amber-400",
  danger: "bg-red-50 text-red-700 dark:bg-red-950 dark:text-red-400",
  info: "bg-sky-50 text-sky-700 dark:bg-sky-950 dark:text-sky-400",
  neutral: "bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-300",
};

export function StatusBadge({ label, tone = "neutral", size = "sm" }: StatusBadgeProps) {
  return (
    <span
      className={
        "inline-flex items-center rounded-md font-medium " +
        (size === "sm" ? "px-1.5 py-0.5 text-[11px]" : "px-2 py-0.5 text-[12px]") +
        " " +
        toneClass[tone]
      }
    >
      {label}
    </span>
  );
}
```

## Mobile fallback

Same; avoid wrapping long labels — truncate with title attribute.

## Motion variants

None.

## Dark-mode notes

Use dark-* pairs above; do not rely on opacity-only light chips on dark bg.

## Anti-patterns

- Brand purple for "active"
- Solid filled high-chroma pills competing with primary CTA
- More than one status chip system in the same product

## References

- tokens.md semantic status table
