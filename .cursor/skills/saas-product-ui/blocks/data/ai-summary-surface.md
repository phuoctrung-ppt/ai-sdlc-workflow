---
name: ai-summary-surface
category: data
dial_compatibility:
  variance: [3, 5]
  motion: [1, 3]
  density: [5, 7]
when_to_use: "Record/home surfaces where AI enrichment is a first-class panel (Attio-style), not a floating chatbot."
not_for: "Marketing AI claims; replacing the primary work list with only generated prose."
stack: [react, next, tailwind]
---

# AI Summary Surface

AI output sits **in the record layout** — same type scale as product UI, no gradient orbs, no “magic” purple.

## Visual sketch

```
┌─ Summary ─────────────────────────────────────────┐
│ Acme is evaluating competitors; next step: demo   │
│ on Thu. Risks: no budget owner tagged.            │
│                                    [Refresh] [ⓘ]  │
└───────────────────────────────────────────────────┘
```

## Props API

```ts
type AiSummarySurfaceProps = {
  title?: string;
  body: string;
  status?: "ready" | "loading" | "stale" | "error";
  onRefresh?: () => void;
  sourcesLabel?: string; // optional provenance
};
```

## Code sketch

```tsx
export function AiSummarySurface({
  title = "Summary",
  body,
  status = "ready",
  onRefresh,
  sourcesLabel,
}: AiSummarySurfaceProps) {
  return (
    <section className="rounded-lg border border-zinc-200 bg-zinc-50/80 p-4 dark:border-zinc-800 dark:bg-zinc-900/50">
      <div className="flex items-center justify-between gap-2">
        <h2 className="text-[12px] font-medium uppercase tracking-wide text-zinc-500">
          {title}
        </h2>
        <div className="flex items-center gap-2">
          {status === "loading" && (
            <span className="text-[11px] text-zinc-400">Updating…</span>
          )}
          {status === "stale" && (
            <span className="text-[11px] text-amber-600">Stale</span>
          )}
          {status === "error" && (
            <span className="text-[11px] text-red-600">Unavailable</span>
          )}
          {onRefresh && (
            <button
              type="button"
              onClick={onRefresh}
              className="text-[12px] text-zinc-600 underline dark:text-zinc-400"
            >
              Refresh
            </button>
          )}
        </div>
      </div>
      <p className="mt-2 text-[13px] leading-relaxed text-zinc-800 dark:text-zinc-200">
        {status === "loading" && !body ? "…" : body}
      </p>
      {sourcesLabel && (
        <p className="mt-2 text-[11px] text-zinc-400">{sourcesLabel}</p>
      )}
    </section>
  );
}
```

## Mobile fallback

Full width above record fields.

## Motion variants

No typewriter theatrics by default. Optional subtle fade when body replaces.

## Dark-mode notes

Muted panel, not neon border.

## Anti-patterns

- Purple glow, sparkle icons, “✨ AI” badges as decoration
- Summary that cannot be refreshed or shown as stale/error
- Blocking the entire page on summary load (shell + list should render)

## References

- Attio AI-native CRM surfaces; benchmarks-2026 “AI as surface”
