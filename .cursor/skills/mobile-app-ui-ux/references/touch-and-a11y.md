# Touch targets & mobile a11y

## WCAG 2.2 — 2.5.8 Target Size (Minimum)

- **Minimum:** 24×24 CSS pixels is the SC floor for 2.5.8; **product mobile default in this skill: 44×44** so targets remain usable under fat-finger + platform HIG expectations.
- **Spacing exception:** smaller visual control OK if the *spacing* to the next target keeps an equivalent unobstructed area.
- **Other exceptions:** inline text links, user-agent controlled, essential presentation — document if used.
- Never rely on **color alone** for error/success; pair with text/icon.

## Practical RN/Expo mapping

| Control | Practice |
|---------|----------|
| Icon button | visual 20–24 + `hitSlop` / padding → ≥44 hit box |
| List row | min height ~44–56; full-row press target |
| Segmented control | equal segments, clear selected state (not color-only) |

## External keyboard / switch

When a hardware keyboard is attached: visible focus ring on focused control; no focus traps inside sheets without Escape/back.

## Sources

- https://www.w3.org/TR/WCAG22/#target-size-minimum
- Understanding docs for 2.5.8 (W3C)
