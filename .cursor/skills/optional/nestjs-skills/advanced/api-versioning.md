# API Versioning (Advanced)

Prefer URL prefix versioning: `/api/v1/users`, `/api/v2/users`.

```typescript
@Controller({ path: 'users', version: '1' })
export class UsersV1Controller {}
```

- Version at controller or module level
- Maintain backward compatibility for one major version
- Document breaking changes in ADR

Alternatives: header versioning (`Accept: application/vnd.api+json;version=2`) — use only when URL versioning is impossible.
