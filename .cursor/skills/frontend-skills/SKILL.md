---
name: frontend-skills
description: React/Next.js frontend patterns — RSC, hooks, data fetching, forms, performance. Covers ~90% of UI tasks. Load advanced/ via context-builder --expand-ref only.
license: MIT
metadata:
  version: "2.0.0"
  consolidation: "2026-07-27"
---

# Frontend Skills (Consolidated)

Use for React, Next.js App Router, components, data fetching, and forms. **Tier 4:** `.cursor/skills/frontend-skills/advanced/*.md`

## Architecture

- Feature-based: `src/features/[name]/{components,hooks,api,types}`
- Global UI: `src/components/{atoms,molecules,organisms}`
- **Presentational components** — data/orchestration in custom hooks
- Shared types from `@shared/types` or Zod schemas — never duplicate DTOs

## TypeScript

- No `any` — use `unknown` + guards or explicit interfaces
- Every component has a `Props` interface
- Align form schemas with backend validation (Zod + shared package)

## React Server Components (default in App Router)

- Server Components: **no directive** — async components, server data fetch, zero client bundle for heavy libs
- Client Components: `'use client'` only for state, effects, event handlers, browser APIs
- Server Actions: `'use server'` for mutations — not for marking server components

```tsx
// app/users/page.tsx — Server Component
export default async function UsersPage() {
  const users = await fetchUsers(); // server-only
  return <UserList initialUsers={users} />;
}

// UserList.client.tsx
'use client';
export function UserList({ initialUsers }: { initialUsers: User[] }) {
  const { data } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
    initialData: initialUsers,
  });
  return <ul>{data.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

**Don't:** use `window`, `localStorage`, or `useState` in Server Components.

## Custom Hooks

- Prefix with `use`; call only at top level of React functions
- Extract: data fetching, form logic, subscriptions, side effects
- Avoid unnecessary `useEffect` — derive state in render; use `useMemo` only for expensive work

```tsx
function useToggle(initial = false) {
  const [on, setOn] = useState(initial);
  return { on, toggle: () => setOn(v => !v), setOn };
}
```

## Data Fetching

### Server (RSC)

- Fetch in Server Components or route handlers
- Use `React.cache()` for per-request dedup (primitive args only)
- Parallelize: `Promise.all([fetchA(), fetchB()])`

### Client (TanStack Query recommended)

```tsx
const { data, isLoading, isError } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => api.getUser(userId),
  staleTime: 60_000,
});
```

- **Never** raw `useEffect` + `fetch` without caching
- Avoid waterfalls: fetch siblings in parallel, not parent→child chains
- Prefetch on hover/focus for navigation
- Optimistic updates for predictable mutations
- Pass `initialData` from RSC to client query to avoid double fetch

## Forms

- React Hook Form + `zodResolver` + shared Zod schema
- Disable submit during `isSubmitting`
- Show field errors after validation failure

## Performance

- `next/image` + WebP; lazy load below fold
- `dynamic()` / `React.lazy()` for heavy routes
- Memoize only when profiling shows benefit
- Passive listeners for scroll/touch when not calling `preventDefault()`

## Security

- No secrets in client bundle
- JWT in HTTP-only cookies or in-memory — not localStorage
- Sanitize HTML; avoid `dangerouslySetInnerHTML` unless DOMPurify
- `NEXT_PUBLIC_` only for truly public env vars

## UI/UX

- Mobile-first responsive layout
- Skeleton loaders for async sections (>200ms)
- Error boundaries around feature modules
- Loading + error state on every async boundary
- WCAG AA contrast; honor `prefers-reduced-motion`

## Testing

- Unit: hooks and utilities (Vitest/Jest)
- Integration: React Testing Library for flows
- E2E: Playwright for critical paths

## Decision Tree

| Task | Pattern |
|------|---------|
| Static marketing page | Server Component only |
| Interactive form | Client Component + RHF + Zod |
| Dashboard data | RSC fetch + client TanStack Query with initialData |
| List + detail nav | Prefetch on hover; parallel queries |
| AI chat UI | See `advanced/ai-ui-patterns.md` |
| Streaming page | See `advanced/streaming-ssr.md` |

## Advanced Topics (lazy load)

| File | When |
|------|------|
| `advanced/streaming-ssr.md` | Suspense streaming, progressive hydration |
| `advanced/composition-patterns.md` | HOC, render props, compound components |
| `advanced/ai-ui-patterns.md` | Chat, streaming LLM UI |
| `advanced/rendering-modes.md` | SSG, CSR, ISR tradeoffs |

Legacy refs: `references/` (deprecated — do not bulk-read)
