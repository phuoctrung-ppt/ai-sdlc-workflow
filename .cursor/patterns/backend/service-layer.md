# Service Layer

**When:** Implementing business logic for an API feature.

**Do:** Controller/route validates input and delegates to service; service owns transactions and domain rules.

**Don't:** Business logic in controller; don't skip input validation at boundary.

**Verify:** Controller methods are thin; service has unit tests.
