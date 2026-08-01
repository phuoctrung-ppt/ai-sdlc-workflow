# Performance Deep Dive (Advanced)

## Caching

- Redis cache for read-heavy, stale-tolerant data
- Cache keys include tenant_id when multi-tenant
- Invalidate on write; set TTL

## Lazy Module Loading

```typescript
@Module({
  imports: [
    LazyModuleLoader,
  ],
})
```

Load heavy modules on first use to speed cold start.

## Async Lifecycle

- Use `OnModuleInit` / `OnModuleDestroy` for connections
- Avoid blocking `bootstrap()` — defer non-critical init

## Query Optimization

- EXPLAIN ANALYZE slow queries
- Partial indexes for filtered columns
- Pagination: cursor for large lists
