---
name: skeleton-page
category: states
dial_compatibility:
  variance: [1, 3]
  motion: [1, 4]
  density: [6, 8]
when_to_use: "Route or section loading when final layout shape is known."
not_for: "Button-level pending (use button spinner/disabled). Infinite unknown waits without layout."
stack: [react, next, tailwind]
---

# Skeleton Page

## Visual sketch

```
Header bar ████████░░░░
Toolbar    ████  ██  ░░     ████
Table rows ████████████████████
           ████████████████████
           ████████████████████
```

Match **final layout geometry** (metric strip, table, settings form).

## Props API

```ts
type SkeletonPageProps = {
  variant: "table" | "metrics+table" | "settings-form";
};
```

## Code sketch

```tsx
function Bone({ className }: { className?: string }) {
  return (
    <div
      className={
        "animate-pulse rounded-md bg-zinc-200 dark:bg-zinc-800 " + (className ?? "")
      }
    />
  );
}

export function SkeletonPage({ variant }: SkeletonPageProps) {
  if (variant === "settings-form") {
    return (
      <div className="mx-auto max-w-xl space-y-4 p-4">
        <Bone className="h-6 w-40" />
        <Bone className="h-9 w-full" />
        <Bone className="h-9 w-full" />
        <Bone className="h-9 w-2/3" />
        <Bone className="h-9 w-24" />
      </div>
    );
  }
  return (
    <div className="space-y-4 p-4">
      {variant === "metrics+table" && (
        <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <Bone key={i} className="h-24" />
          ))}
        </div>
      )}
      <Bone className="h-8 w-full max-w-md" />
      <div className="space-y-2">
        {Array.from({ length: 6 }).map((_, i) => (
          <Bone key={i} className="h-10 w-full" />
        ))}
      </div>
    </div>
  );
}
```

## Mobile fallback

Same bones; metrics 2-col.

## Motion variants

Pulse only if `prefers-reduced-motion: no-preference`. Otherwise static gray blocks.

## Dark-mode notes

`bg-zinc-800` bones on `zinc-950` background.

## Anti-patterns

- Centered circular spinner as the only loading UI for a table page
- Skeleton shape unrelated to final layout (layout shift)

## References

- Skill empty/loading table; dashboard skeleton cards
