---
name: mobile-app-ui-ux
description: Product mobile UI/UX — safe areas, touch targets, tabs/stacks/sheets, gestures. Not marketing (taste-design); not RN mechanics (react-native-expo); not web DOM a11y alone (web-app-ui-ux).
---

# Mobile App UI/UX

Portable rules for **native / Expo product surfaces**. Complements `react-native-expo` (implement) and `web-app-ui-ux` (web).

## When to use

| Surface | This skill |
|---------|------------|
| Phone/tablet product screens, tabs, stacks, sheets | Yes |
| Safe areas, system bars, touch targets, gestures | Yes |
| Marketing landing / web-only chrome | **No → taste-design / web-app-ui-ux** |
| FlatList perf, SecureStore, Expo Router files | **No → react-native-expo** |
| Design Contract compositions / SaaS blocks | Pair with **saas-product-ui** |

## Hard rules

1. **Safe areas first** — content never under notch, status bar, home indicator, or Android system bars; use SafeAreaProvider + insets (or platform equivalent).
2. **Touch targets** — interactive controls ≥ **44×44** CSS px (WCAG 2.5.8 minimum); pad with hitSlop when icon is smaller; space adjacent targets.
3. **Primary navigation** — bottom tabs / top-level destinations ≤5; stacks for hierarchy; sheets/modals for focused tasks — no third competing global nav.
4. **Thumb zone** — primary CTAs and destructive confirms reachable one-handed; avoid critical actions only in far top corners on tall phones.
5. **System chrome** — status/nav bar style matches screen luminance; do not hide system bars for ordinary product flows.
6. **Gestures** — back/dismiss must not fight OS edge gestures; always offer a visible control alternative to swipe-only actions.
7. **Async states** — every async region: loading + error + empty×2 (first-use vs filtered); empty explains *why* and next action.
8. **Forms** — visible labels; large fields; correct keyboard types; avoid nested scroll traps.
9. **Motion** — honor reduced-motion; short transitions; no scroll-jacking.
10. **Density** — product scan over marketing whitespace; one primary CTA per screen.

## Anti-patterns

- Web hamburger-only IA on phone when destinations are peer-level (prefer bottom tabs)
- Controls under home indicator / cutout
- 24px icons with no expanded hit area
- Swipe-only destructive actions
- Desktop tables with no mobile list/card alternative
- Marketing bento / hero inside authenticated app shell

## References (lazy)

| File | When |
|------|------|
| `references/touch-and-a11y.md` | WCAG 2.5.8 + external keyboard notes |
| `references/navigation-ia.md` | tabs vs stack vs sheet |
| `references/safe-areas-system-bars.md` | insets, edge-to-edge |
| `references/sources.md` | URLs + SPDX |

## Attribution

Distilled from WCAG 2.2 (W3C Document License), Expo safe-area / system-bar docs (MIT). Platform HIG/M3 as convention notes only — see `references/sources.md`.
