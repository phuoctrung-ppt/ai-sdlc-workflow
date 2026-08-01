# Rendering Modes (Advanced)

| Mode | When | Tradeoff |
|------|------|----------|
| **SSG** | Static content, marketing | Fast CDN; stale until rebuild |
| **SSR** | Personalized per request | Fresh; TTFB cost |
| **ISR** | Semi-static with revalidation | Balance; complexity |
| **CSR** | Heavy client interactivity, dashboards behind auth | Slow FCP; simple deploy |
| **RSC** | Default in App Router | Zero bundle for server parts |

## Next.js

- `export const dynamic = 'force-static'` for SSG
- `export const revalidate = 3600` for ISR
- Client-only: `'use client'` + dynamic import with `ssr: false` for browser-only libs

## Choose

- Public landing → SSG/RSC
- Authenticated app shell → RSC + client islands
- Real-time dashboard → CSR + TanStack Query
