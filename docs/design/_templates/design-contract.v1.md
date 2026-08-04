---
# Design Contract v1 — copy to docs/design/YYYY-MM-DD-{feature}.spec.md
# Soft adjectives WITHOUT numbers/enums are INVALID (judge Critical).
# Frontend implements this file + sketches only. Do not invent spacing/type.
---

```yaml
meta:
  feature: ""                      # kebab-case feature id
  track: product                   # marketing | product | split
  domain_pack: generic             # knowledge-hub-saas | sme-marketing-vn | fintech | ...
  benchmark: calm-list-first       # product: calm-list-first | single-metric | ranked-attention | ai-surface
                                   # marketing: editorial-hero | bento-mixed | process-rail | ...
  dials:
    variance: 4                    # product 3–5 | marketing 7–9
    motion: 2                      # product 2–4 | marketing 5–8
    density: 7                     # product 6–8 | marketing 3–5

vision:                            # max 3 bullets, each ≤ 12 words — experience intent only
  - ""
  - ""
  - ""

layout:                            # ALL fields numeric or enum — no prose
  max_width_px: 1120
  sidebar_width_px: 256            # 0 if topbar-only
  content_padding_px: 24
  section_gap_px: 32
  grid: "12-col / 16px gutter"      # or "stack" | "bento-mixed"
  app_shell: sidebar+topbar        # topbar-only | sidebar+topbar | full-bleed

hierarchy:
  primary: ""                      # one sentence: main operator focus
  secondary: ""
  supporting: ""

typography:                        # lock sizes; map to tokens
  font_stack: "Be Vietnam Pro, system-ui, sans-serif"
  page_title: { size_px: 20, weight: 600, line_px: 28 }
  section:    { size_px: 14, weight: 600, line_px: 20 }
  body:       { size_px: 13, weight: 400, line_px: 20 }
  meta:       { size_px: 12, weight: 500, line_px: 16 }
  mono_meta:  { size_px: 12, weight: 400, tabular_nums: true }

components:
  card: elevated                   # elevated | flat | outlined
  button_primary: solid-accent
  button_secondary: outline-muted
  input_height_px: 40
  input_radius_px: 8
  table: toolbar+filters+skeleton-rows+empty-x2
  modal_max_width_px: 480
  modal_radius_px: 12
  status: semantic-chips-only      # never accent color for status

states:                            # required for every list/table surface
  loading: skeleton-matching-layout  # forbidden: spinner-only full page
  empty_never: ""                  # copy + primary CTA when zero data ever
  empty_filter: ""                 # copy + clear-filters when filters empty
  error: inline-alert+retry
  success: toast-one-line

motion:
  duration_ms: 150
  easing: ease-out
  properties: [opacity, transform] # ban transition: all
  reduced_motion: disable-all

responsive:
  desktop: ">=1024 sidebar fixed"
  tablet: "768-1023 sidebar collapse"
  mobile: "<768 drawer; stack sections"

a11y:
  focus: focus-visible ring-2
  icon_buttons: aria-label-required
  live_regions: polite-for-processing
  contrast: AA-on-cta-and-body

tokens_path: docs/design/tokens.md
sketch_paths:                      # ≥1 required; DESIGN-GATE fails if missing
  - docs/design/sketches/{feature}/desktop.png
  # - docs/design/sketches/{feature}/wire.md

hard_rules_source: product         # product | marketing
hard_rules_pasted: true            # must paste checklist body below
blocks_used: []                    # ids from saas-product-ui/blocks or taste compositions
```

## Hard-rules checklist (paste full list from skill)

<!-- product → .cursor/skills/saas-product-ui/references/hard-rules-product.md -->
<!-- marketing → .cursor/skills/taste-design/hard-rules-marketing.md -->

```
(paste here)
```

## ASCII / composition notes (optional detail under sketches)

```
┌─ shell ─────────────────────────────────────────┐
│ sidebar │ page header                           │
│         │ primary region                        │
│         │ secondary                             │
└─────────────────────────────────────────────────┘
```

## Handoff to frontend-worker

```
Objective: Implement Design Contract exactly
Contract: docs/design/YYYY-MM-DD-{feature}.spec.md
Sketches: docs/design/sketches/{feature}/
Tokens: docs/design/tokens.md
Acceptance:
  - layout numbers match contract (max_width, padding, gaps, sidebar)
  - typography sizes/weights match
  - states: loading skeleton, empty×2, error, success as specified
  - no invented palette or density outside dials
  - WCAG AA; prefers-reduced-motion honored
```
