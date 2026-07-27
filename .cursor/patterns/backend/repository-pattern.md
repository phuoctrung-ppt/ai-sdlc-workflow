# Repository Pattern

**When:** Service needs DB access with testable boundaries.

**Do:** Inject repository interface; service calls repository methods; mock repository in unit tests.

**Don't:** Import ORM repository directly in controller; don't put queries in controllers.

**Verify:** Service tests mock repository, not database.
