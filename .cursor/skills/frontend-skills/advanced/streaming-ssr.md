# Streaming SSR (Advanced)

Use when TTFB/FCP matter and page has slow + fast sections.

## Next.js App Router

- Default streaming with `Suspense` boundaries
- Shell renders first; slow sections stream later

```tsx
export default function Page() {
  return (
    <>
      <Header />
      <Suspense fallback={<PostsSkeleton />}>
        <SlowPosts />
      </Suspense>
    </>
  );
}
```

## Raw React 18+

- `renderToPipeableStream` (Node) — not deprecated `renderToNodeStream`
- `onShellReady` to start piping; `onError` for failures

## Progressive Hydration

- Hydrate interactive islands first
- Defer below-fold client components
- See `.cursor/patterns/frontend/avoid-hydration-mismatch.md`

## When NOT to use

- Small static pages
- Platforms that buffer full response (some serverless)
