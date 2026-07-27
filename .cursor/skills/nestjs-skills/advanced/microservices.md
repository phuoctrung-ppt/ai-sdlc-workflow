# Microservices & Queues (Advanced)

Load via `--expand-ref` when implementing background jobs or distributed patterns.

## BullMQ (NestJS)

- Never block HTTP handlers with long-running work
- Use `@nestjs/bullmq` with retry + exponential backoff
- Separate queues: email, reports, notifications
- Idempotent processors; dead-letter queue for failures

```typescript
@InjectQueue('email') private emailQueue: Queue

async enqueueWelcome(userId: string) {
  await this.emailQueue.add('welcome', { userId }, {
    attempts: 3,
    backoff: { type: 'exponential', delay: 1000 },
  });
}
```

## Health Checks

- Expose `/health` for orchestrators (DB + Redis connectivity)
- Use `@nestjs/terminus` for readiness vs liveness

## Message Patterns

- Request/response for sync RPC between services
- Events for fire-and-forget decoupling (see `event-driven.md`)

See also: `bullmq-worker` skill for processor patterns.
