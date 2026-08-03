# UI visual pipeline — Grok / imagegen / optional MCP

Goal: stop “code first, hope it looks good.” Visual lock **before** frontend.

## Pipeline

```
Brief → Track+domain → Design Read + dials + hard-rules
     → Visual reference (sketch OR imagegen)
     → Design spec + tokens + Asset Mapping
     → frontend-worker implements
     → judge UI rubric (Critical if slop)
     → optional visual QA (browser MCP / human)
```

## Grok built-in image generation (preferred for sketches)

When the agent runtime supports **Grok Imagine / image generation**:

1. Designer writes a **precise prompt** from the design read (layout, type mood, palette, device frame).
2. Generate 1–2 references: hero (marketing) or app-shell frame (product).
3. Save under `docs/design/sketches/{feature}/` (export or documented prompt + result path).
4. Spec must link those files. Frontend matches structure, not “vibes only.”

Prompt skeleton (marketing):

```
8k UI mock, desktop SaaS marketing landing, Vietnamese headline area,
editorial layout, one accent color {hex}, no purple gradients, no 3 equal cards,
whitespace, premium type, product name "{name}", clean hero + single CTA
```

Prompt skeleton (product):

```
Desktop SaaS app shell mock, 256px sidebar, knowledge list main panel,
zinc neutrals, one accent, dense but calm, Linear-like, no marketing hero,
empty state visible, light mode
```

Use existing skills when present:
- `taste-design/imagegen-frontend-web` — marketing references only
- `taste-design/imagegen-frontend-mobile` — mobile flows
- `taste-design/brandkit` — logo/palette boards

## MCP (optional, when connected in Cursor)

| MCP / tool | Use |
|------------|-----|
| Browser / Playwright MCP | Open local preview; screenshot; compare to sketch |
| Figma MCP (if any) | Pull frame specs — still write `docs/design/*` |
| Filesystem | Ensure sketch paths exist before DESIGN-GATE pass |

Agents must **not** claim MCP ran if the tool is not in the session.

## Fail closed

- No sketch/reference path in spec → frontend **STOP** (DESIGN-GATE)
- Implementation ignores sketch hierarchy → judge **Critical**
- Marketing dials used inside app shell → judge **Critical**
