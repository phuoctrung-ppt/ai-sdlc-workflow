# UI visual pipeline — Design Contract + Grok / imagegen / optional MCP

Goal: stop “code first, hope it looks good.” **Numeric Design Contract + visual lock before frontend.**

## Pipeline

```
Brief → Track+domain → Design Read + dials + hard-rules
     → Design Contract (.spec.md numeric fields)
     → Visual reference (sketch OR imagegen)
     → Tokens + Asset Mapping
     → Design Judge (specificity)
     → frontend-worker implements contract numbers
     → judge UI rubric (Critical if slop / mismatch)
     → optional visual QA (browser MCP / human)
```

Template: `docs/design/_templates/design-contract.v1.md`  
Phase: `.cursor/skills/planning/references/design-specification-phase.md`

## Grok built-in image generation (preferred for sketches)

When the agent runtime supports **Grok Imagine / image generation**:

1. Designer writes a **precise prompt** from the design read (layout numbers, type mood, palette, device frame).
2. Generate 1–2 references: hero (marketing) or app-shell frame (product).
3. Save under `docs/design/sketches/{feature}/` (export or documented prompt + result path).
4. Contract must list those paths under `sketch_paths`. Frontend matches structure + contract numbers, not “vibes only.”

Prompt skeleton (marketing):

```
8k UI mock, desktop SaaS marketing landing, Vietnamese headline area,
editorial layout, one accent color {hex}, no purple gradients, no 3 equal cards,
whitespace, premium type, product name "{name}", clean hero + single CTA
```

Prompt skeleton (product):

```
Desktop SaaS app shell mock, {sidebar_width_px}px sidebar, knowledge list main panel,
zinc neutrals, one accent, dense but calm, Linear-like, no marketing hero,
empty state visible, light mode, max content width {max_width_px}px
```

Use existing skills when present:
- `taste-design/imagegen-frontend-web` — marketing references only
- `taste-design/imagegen-frontend-mobile` — mobile flows
- `taste-design/brandkit` — logo/palette boards

## MCP (optional, when connected in Cursor)

| MCP / tool | Use |
|------------|-----|
| Browser / Playwright MCP | Open local preview; screenshot; compare to sketch |
| Figma MCP (if any) | Pull frame specs — still write `docs/design/*.spec.md` |
| Filesystem | Ensure sketch paths exist before DESIGN-GATE pass |

Agents must **not** claim MCP ran if the tool is not in the session.

## Fail closed

- No `.spec.md` or missing numeric specificity → frontend **STOP** (DESIGN-GATE)
- No sketch/reference path in contract → frontend **STOP**
- Implementation ignores contract numbers / sketch hierarchy → judge **Critical**
- Marketing dials used inside app shell → judge **Critical**
