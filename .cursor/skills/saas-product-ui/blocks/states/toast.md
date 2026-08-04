---
name: toast
category: states
dial_compatibility:
  variance: [2, 4]
  motion: [2, 4]
  density: [6, 8]
when_to_use: "Transient success/error feedback after mutations."
not_for: "Form field errors (inline). Blocking failures (dialog/banner)."
stack: [react, next, tailwind]
---

# Toast

## Visual sketch

```
                    ┌──────────────────────────┐
                    │ Saved changes            │  top-right
                    └──────────────────────────┘
```

## Props API

```ts
type ToastProps = {
  open: boolean;
  message: string;
  tone?: "success" | "danger" | "neutral";
  onClose?: () => void;
};
```

## Code sketch

```tsx
export function Toast({ open, message, tone = "neutral", onClose }: ToastProps) {
  if (!open) return null;
  const border =
    tone === "success"
      ? "border-emerald-200 dark:border-emerald-900"
      : tone === "danger"
        ? "border-red-200 dark:border-red-900"
        : "border-zinc-200 dark:border-zinc-700";
  return (
    <div
      role="status"
      className={
        "fixed bottom-4 right-4 z-50 max-w-sm rounded-lg border bg-white px-3 py-2 text-[13px] shadow-lg dark:bg-zinc-900 " +
        border
      }
    >
      <div className="flex items-start gap-2">
        <span className="text-zinc-800 dark:text-zinc-100">{message}</span>
        {onClose && (
          <button type="button" className="ml-auto text-zinc-400" onClick={onClose} aria-label="Dismiss">
            ✕
          </button>
        )}
      </div>
    </div>
  );
}
```

## Mobile fallback

Full width with side margins; bottom safe-area.

## Motion variants

Slide/fade ≤ 200ms; auto-dismiss 3–5s for success.

## Dark-mode notes

Elevated surface + subtle semantic border.

## Anti-patterns

- Stack of 5+ toasts
- Using toast for validation that must stay visible
- Accent purple success toasts

## References

- Quiet product feedback (Linear/Vercel)
