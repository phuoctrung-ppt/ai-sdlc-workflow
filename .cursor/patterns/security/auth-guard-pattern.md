# Auth Guard Pattern

**When:** Adding or reviewing API routes.

**Do:** Default protected; mark public routes explicitly; guards enforce RBAC at route level.

**Don't:** Assume unmarked routes are public; don't check roles only in service layer.

**Verify:** Every route classified public or protected in code review.
