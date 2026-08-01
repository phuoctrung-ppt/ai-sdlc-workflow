# DI Advanced (Advanced)

## Interface Segregation

Split large interfaces into focused contracts:

```typescript
interface UserReader { findById(id: string): Promise<User>; }
interface UserWriter { create(dto: CreateUserDto): Promise<User>; }
```

## Liskov Substitution

Implementations must honor interface contracts — no throwing where parent wouldn't.

## Scope Awareness

| Scope | Use when |
|-------|----------|
| DEFAULT (singleton) | Stateless services |
| REQUEST | Per-request context (tenant, user) |
| TRANSIENT | New instance every injection |

Request-scoped providers cannot be injected into singletons directly — use `ModuleRef` or pass context explicitly.

## Injection Tokens

```typescript
export const USER_REPO = Symbol('USER_REPO');
@Inject(USER_REPO) private repo: UserRepository
```
