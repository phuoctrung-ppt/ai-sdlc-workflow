# Avoid N+1 Queries

**When:** Loading related entities in lists.

**Do:** Eager load / join / batch queries; explicit column selects.

**Don't:** Loop with per-row queries; don't `SELECT *`.

**Verify:** Query log shows bounded query count for list endpoints.
