# Event-Driven Architecture (Advanced)

Use `@nestjs/event-emitter` to decouple modules without circular imports.

```typescript
// Emit after domain action
this.eventEmitter.emit('order.created', { orderId, userId });

// Listen in separate module
@OnEvent('order.created')
handleOrderCreated(payload: OrderCreatedEvent) {
  this.notificationsService.sendConfirmation(payload.userId);
}
```

- Events for side effects (email, analytics) — not critical path
- Keep handlers idempotent
- For cross-process: use queues instead of in-process events
