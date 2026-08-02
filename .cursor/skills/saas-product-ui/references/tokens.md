# Product design tokens (starter)

Copy into `docs/design/tokens.md` and lock one neutral family per product.
Do **not** invent a second accent mid-project.

## Surfaces (zinc example)

| Token | Light | Dark | Use |
|-------|-------|------|-----|
| `--bg-app` | `#fafafa` (zinc-50) | `#09090b` (zinc-950) | App canvas |
| `--bg-elevated` | `#ffffff` | `#18181b` (zinc-900) | Cards, panels |
| `--bg-muted` | `#f4f4f5` (zinc-100) | `#27272a` (zinc-800) | Hover, skeleton |
| `--border` | `#e4e4e7` (zinc-200) | `#27272a` | Dividers |
| `--border-strong` | `#d4d4d8` (zinc-300) | `#3f3f46` | Active cards |

## Text

| Token | Light | Dark |
|-------|-------|------|
| `--text` | `#18181b` | `#fafafa` |
| `--text-secondary` | `#71717a` | `#a1a1aa` |
| `--text-muted` | `#a1a1aa` | `#71717a` |

## Accent (pick ONE)

Examples (not all at once):
- Neutral power-tool: near-black button on light / near-white on dark (Linear-like)
- Brand: single hue e.g. `oklch(0.55 0.18 250)` for primary CTA only

Never use accent for success/warning/error.

## Semantic status

| Tone | Light text/bg chip | Meaning |
|------|--------------------|---------|
| success | emerald-700 / emerald-50 | Paid, active, healthy |
| warning | amber-700 / amber-50 | Trial, pending |
| danger | red-700 / red-50 | Failed, overdue |
| info | sky-700 / sky-50 | Processing, info |
| neutral | zinc-600 / zinc-100 | Draft, archived |

## Radius & spacing

- Radius scale: `6px` controls, `8px` cards, `12px` modals — pick and lock
- Spacing: 4, 8, 12, 16, 24, 32, 48 only

## Type

| Role | Size / weight |
|------|----------------|
| Page title | 18–20px / 600 |
| Section | 14–15px / 600 |
| Body / table | 13–14px / 400 |
| Label / meta | 12px / 500 |
| Mono meta | 12px tabular-nums |

## Tailwind map (example)

```css
:root {
  --bg-app: theme(colors.zinc.50);
  --bg-elevated: theme(colors.white);
  --border: theme(colors.zinc.200);
  --text: theme(colors.zinc.900);
  --text-secondary: theme(colors.zinc.500);
}
.dark {
  --bg-app: theme(colors.zinc.950);
  --bg-elevated: theme(colors.zinc.900);
  --border: theme(colors.zinc.800);
  --text: theme(colors.zinc.50);
  --text-secondary: theme(colors.zinc.400);
}
```
