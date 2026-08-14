---
name: web-app-ui-ux
description: Foundational product web UI/UX — a11y, keyboard, states, forms, feedback. Not marketing (taste-design); not React mechanics (frontend-skills); not opinionated compositions (saas-product-ui).
---

# Web App UI/UX

Portable rules for **authenticated product surfaces**. Complements `saas-product-ui` (blocks/contracts) and `frontend-skills` (React/Next).

## When to use

| Surface | This skill |
|---------|------------|
| App shell, nav, settings, tables, forms | Yes |
| Loading / empty / error feedback | Yes |
| Keyboard, focus, WCAG AA | Yes |
| Marketing landing / pricing | **No → taste-design** |
| React RSC / hooks / data fetch | **No → frontend-skills** |
| Domain blocks + Design Contract dials | Pair with **saas-product-ui** |

## Hard rules

1. **Track = product** — high density, low decorative variance; no marketing hero/bento/scroll-hijack in app chrome.
2. **WCAG 2.2 AA** — contrast AA; visible focus on every interactive control; honor `prefers-reduced-motion`.
3. **Keyboard complete** — every action reachable and operable by keyboard; no traps; tab order matches visual order.
4. **Native semantics first** — `<button>` for actions, `<a href>` for navigation; never `div`/`span` as controls. ARIA only when no native element fits.
5. **Async states required** — every async region ships loading + error + empty×2 (first-use vs filtered-empty); empty explains *why* and offers a next action.
6. **Forms** — visible label ≥ placeholder alone; validate after submit or blur; error text is associated with the field; disable submit while submitting; never color-only status.
7. **Error copy** — plain language: what failed + how to fix (sentence case).
8. **One progressive-disclosure pattern per view** — pick tabs *or* accordion *or* radio groups by task; do not stack them.
9. **One primary CTA per view** — destructive actions need confirmation; dialogs: focus trap, ESC closes, focus returns to trigger.
10. **Density over marketing whitespace** — tables/lists/dashboards optimize for scan + task completion.

## Anti-patterns

- Marketing bento / chart wallpaper / 12 equal KPIs inside the app
- Placeholder-as-only-label; gray-on-gray disabled text (AA fail)
- Keyboard-unreachable toasts or menus; alert stacking
- `div` buttons; missing focus styles; color-only errors
- Empty state with no recovery action

## References (lazy)

| File | When |
|------|------|
| `references/wcag-aa.md` | Success-criteria map for product UI |
| `references/govuk-patterns.md` | When-to-use / when-not + error copy |
| `references/component-states.md` | Interactive state enums (default→error) |
| `references/sources.md` | URLs + SPDX |

## Attribution

Distilled from WCAG 2.2 (W3C Document License), GOV.UK Design System (MIT), Adobe React Spectrum a11y patterns (Apache-2.0). See `references/sources.md`.
