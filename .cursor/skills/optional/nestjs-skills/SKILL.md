---
name: nestjs-best-practices
description: NestJS production patterns — modules, DI, security, DB, API, testing. Covers ~90% of backend tasks. Load advanced/ via context-builder --expand-ref only.
license: MIT
metadata:
  version: "2.0.0"
  consolidation: "2026-07-27"
---

# NestJS Best Practices (Consolidated)

Use this skill for modules, controllers, services, auth, migrations, and API work. **Tier 4 only:** `.cursor/skills/nestjs-skills/advanced/*.md`

## Module Structure (CRITICAL)

Organize by **feature**, not technical layer:

```
src/modules/{feature}/
├── dto/
├── entities/
├── {feature}.controller.ts
├── {feature}.service.ts
├── {feature}.repository.ts   # optional
├── {feature}.module.ts
└── index.ts
```

```typescript
@Module({
  imports: [TypeOrmModule.forFeature([User])],
  controllers: [UsersController],
  providers: [UsersService, UsersRepository],
  exports: [UsersService], // export only what others need
})
export class UsersModule {}
```

- Avoid circular imports — extract shared providers to `SharedModule`
- One service = one responsibility; no god services
- Use repository pattern when DB logic needs mocking

## Dependency Injection (CRITICAL)

- **Constructor injection only** — never service locator
- Use injection tokens for interfaces: `@Inject(USER_REPO) private repo: UserRepository`
- Default scope is singleton; use request scope only when needed

```typescript
@Injectable()
export class UsersService {
  constructor(
    private readonly usersRepo: UsersRepository,
    private readonly logger: Logger,
  ) {}
}
```

## Controllers & Services

- Controller: validate input, delegate to service, return DTO
- Service: business logic, transactions, domain rules
- Never put business logic in controllers

```typescript
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Post()
  create(@Body() dto: CreateUserDto): Promise<UserResponseDto> {
    return this.usersService.create(dto);
  }
}
```

## Input Validation & DTOs

- Validate at boundary with `ValidationPipe` globally
- Use `class-validator` + `class-transformer` on DTOs
- Separate create/update/response DTOs; never return entities directly

```typescript
export class CreateUserDto {
  @IsEmail()
  email: string;

  @MinLength(8)
  password: string;
}
```

## Error Handling

- Use `@UseFilters(HttpExceptionFilter)` or global filter
- Throw typed HTTP exceptions: `BadRequestException`, `UnauthorizedException`, etc.
- Wrap async handlers; never leave unhandled promise rejections

```typescript
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    // log structured JSON; return { data, meta, error } envelope
  }
}
```

## Security (HIGH)

### Guards — default protected, explicit public

```typescript
export const Public = () => SetMetadata('isPublic', true);
export const Roles = (...roles: Role[]) => SetMetadata('roles', roles);

@Module({
  providers: [
    { provide: APP_GUARD, useClass: JwtAuthGuard },
    { provide: APP_GUARD, useClass: RolesGuard },
  ],
})
export class AppModule {}
```

- `@Public()` on routes that skip auth
- RBAC via `@Roles()` + `RolesGuard`
- Rate-limit sensitive endpoints (auth, password reset)

### JWT Auth

- Secrets from `ConfigService` — never hardcode
- Access token: ~15m; refresh token: ~7d in HTTP-only cookie
- Minimal payload: `sub`, `roles` — no passwords or PII
- Validate user still active in `JwtStrategy.validate()`

### Output & Input

- Sanitize serialized output (prevent XSS in API responses)
- Never log tokens, passwords, or API keys

## Database & Migrations

- **`synchronize: false` in production** — migrations only
- Every migration: both `up()` and `down()`
- Index FK and filter columns
- Use transactions for multi-step writes
- Avoid N+1: eager load / joins / batch queries; explicit `select` columns

```typescript
export class AddUserAge1705312800000 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`ALTER TABLE "users" ADD "age" integer DEFAULT 0`);
    await queryRunner.query(`CREATE INDEX "IDX_users_age" ON "users" ("age")`);
  }
  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`DROP INDEX "IDX_users_age"`);
    await queryRunner.query(`ALTER TABLE "users" DROP COLUMN "age"`);
  }
}
```

## API Design

- **Pipes:** transform + validate (`ParseUUIDPipe`, custom pipes)
- **Interceptors:** logging, response mapping, timeout
- **DTO serialization:** `@Exclude()`, `@Expose()` on response DTOs
- Version via URL prefix (`/v1/`) when needed — see `advanced/api-versioning.md`

## Performance

- Cache read-heavy endpoints (Redis) with TTL
- Optimize queries: EXPLAIN, indexes, avoid SELECT *
- Lazy-load heavy modules at startup when appropriate

## Testing

```typescript
const module = await Test.createTestingModule({
  providers: [
    UsersService,
    { provide: UsersRepository, useValue: mockRepo },
  ],
}).compile();
```

- Unit test services with mocked repositories
- E2E: `supertest` + test DB or mocks
- Mock all external APIs (Stripe, SendGrid, OpenAI)

## DevOps Essentials

- `ConfigModule.forRoot({ isGlobal: true })` — env validation at boot
- Structured logging (Winston/Pino) — JSON with correlationId
- Graceful shutdown: `app.enableShutdownHooks()`

## Decision Tree

| Task | Do |
|------|-----|
| New CRUD feature | Feature module + DTOs + service + migration if schema change |
| Auth endpoint | JwtModule.registerAsync + guards + security skill |
| Background job | BullMQ skill + `advanced/microservices.md` if cross-service |
| Slow query | Index + eager load; see `db-avoid-n-plus-one` pattern |
| Circular deps | Extract shared module or interface token |

## Advanced Topics (lazy load)

Load only when task requires:

| File | When |
|------|------|
| `advanced/microservices.md` | Queues, health checks, message patterns |
| `advanced/event-driven.md` | EventEmitter, decoupling modules |
| `advanced/api-versioning.md` | URL/header versioning strategies |
| `advanced/performance-deep.md` | Caching patterns, lazy modules, async hooks |
| `advanced/di-advanced.md` | ISP, LSP, scope awareness |

Legacy detailed refs: `references/` (deprecated — do not bulk-read)
