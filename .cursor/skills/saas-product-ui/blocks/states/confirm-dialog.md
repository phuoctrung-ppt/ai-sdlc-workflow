---
name: confirm-dialog
category: states
dial_compatibility:
  variance: [2, 4]
  motion: [2, 4]
  density: [5, 7]
when_to_use: "Destructive or irreversible actions: delete, remove member, cancel subscription."
not_for: "Informational alerts (use toast/banner). Soft navigation confirms."
stack: [react, next, tailwind]
---

# Confirm Dialog

## Visual sketch

```
┌─────────────────────────────┐
│ Delete customer?            │
│ This cannot be undone.      │
│           [Cancel] [Delete] │
└─────────────────────────────┘
```

## Props API

```ts
type ConfirmDialogProps = {
  open: boolean;
  onOpenChange: (v: boolean) => void;
  title: string;
  description?: string;
  confirmLabel?: string;
  cancelLabel?: string;
  tone?: "danger" | "default";
  onConfirm: () => void;
  loading?: boolean;
};
```

## Code sketch

```tsx
"use client";

export function ConfirmDialog({
  open,
  onOpenChange,
  title,
  description,
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
  tone = "default",
  onConfirm,
  loading,
}: ConfirmDialogProps) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" role="alertdialog" aria-modal="true">
      <div className="w-full max-w-sm rounded-lg border border-zinc-200 bg-white p-4 shadow-xl dark:border-zinc-700 dark:bg-zinc-950">
        <h2 className="text-[15px] font-semibold text-zinc-900 dark:text-zinc-50">{title}</h2>
        {description && <p className="mt-2 text-[13px] text-zinc-500">{description}</p>}
        <div className="mt-4 flex justify-end gap-2">
          <button
            type="button"
            className="h-8 rounded-md border border-zinc-200 px-3 text-[13px] dark:border-zinc-700"
            onClick={() => onOpenChange(false)}
            disabled={loading}
          >
            {cancelLabel}
          </button>
          <button
            type="button"
            className={
              "h-8 rounded-md px-3 text-[13px] text-white disabled:opacity-60 " +
              (tone === "danger" ? "bg-red-600 hover:bg-red-700" : "bg-zinc-900 dark:bg-zinc-100 dark:text-zinc-900")
            }
            onClick={onConfirm}
            disabled={loading}
          >
            {loading ? "…" : confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
```

## Mobile fallback

Full-width buttons optional; keep max-width readable.

## Motion variants

Band 4–7: 120ms opacity. Focus trap required in production.

## Dark-mode notes

Danger stays semantic red.

## Anti-patterns

- Instant delete without dialog
- Confirm button left of Cancel (western LTR: Cancel left / secondary, Confirm right)
- Vague title ("Are you sure?") without object name

## References

- Settings danger zone patterns
