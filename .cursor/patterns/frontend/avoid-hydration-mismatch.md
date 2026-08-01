# Avoid Hydration Mismatch

**When:** Server-rendered HTML differs from client's first render.

**Do:** Pass serializable props from RSC; defer browser-only values to `useEffect` or dynamic import with `ssr: false`.

**Don't:** Render `Date.now()`, `window`, or random IDs in shared server/client components.

**Verify:** No hydration warnings in console; visual parity on first paint.
