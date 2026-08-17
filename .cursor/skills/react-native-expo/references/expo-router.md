# Expo Router notes

## Defaults

- File-based routes under `app/` — a file becomes a route
- Shared navigation tree across iOS / Android / web
- Deep links / shareable URLs work per route when configured
- Prefer **typed routes** so invalid hrefs fail at typecheck
- Prefer Expo Router for new Expo apps; React Navigation remains valid underneath

## Patterns

| Need | Approach |
|------|----------|
| Layout shells | `_layout` files; groups `(name)` for organization without URL segments |
| Auth gates | Protected layouts / redirects — validate session server-side when possible |
| Platform files | `.ios.tsx` / `.android.tsx` / `.web.tsx` when APIs truly diverge |
| Lazy routes | Async routes / deferred bundling for large apps |

## Hard rules

1. Deep-link params are **untrusted** — validate before use.
2. Do not put tokens in URLs.
3. Keep product mobile UX (safe areas, tabs) via navigators + `mobile-app-ui-ux` — Router is structure, not visual system.

## Sources

- https://docs.expo.dev/router/introduction/
