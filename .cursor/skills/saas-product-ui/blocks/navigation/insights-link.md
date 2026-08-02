---
name: insights-link
category: navigation
dial_compatibility:
  variance: [2, 4]
  motion: [1, 2]
  density: [6, 8]
when_to_use: "Separate doing from analyzing — secondary entry to charts/insights (Linear pattern)."
not_for: "Primary nav replacement; stuffing charts onto the home list."
stack: [react, next, tailwind]
---

# Insights Link (progressive disclosure)

Keep the default view as **work**. Put analysis behind one obvious control.

## Visual sketch

```
PageHeader actions:  [Insights ↗]  [+ New]
```

or quiet text link under metric strip: `View insights`

## Props API

```ts
type InsightsLinkProps = {
  href: string;
  label?: string;
  variant?: "button" | "link";
};
```

## Code sketch

```tsx
export function InsightsLink({
  href,
  label = "Insights",
  variant = "button",
}: InsightsLinkProps) {
  if (variant === "link") {
    return (
      <a href={href} className="text-[13px] font-medium text-zinc-600 underline dark:text-zinc-400">
        {label}
      </a>
    );
  }
  return (
    <a
      href={href}
      className="inline-flex h-8 items-center rounded-md border border-zinc-200 px-3 text-[13px] text-zinc-700 hover:bg-zinc-50 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-900"
    >
      {label}
    </a>
  );
}
```

## Mobile fallback

Same control in page header actions wrap.

## Motion variants

None.

## Dark-mode notes

Secondary button style — never stronger than primary CTA.

## Anti-patterns

- Charts and issue list fighting on the same default screen
- Hiding insights in an unlabeled icon

## References

- Linear: list default, Insights one click away
