# Migration Safety

**When:** Changing database schema.

**Do:** One migration per change; implement both `up()` and `down()`; add indexes on FK/filter columns.

**Don't:** ORM auto-sync; destructive `DROP` without rollback plan.

**Verify:** Migration runs up and down cleanly in dev.
