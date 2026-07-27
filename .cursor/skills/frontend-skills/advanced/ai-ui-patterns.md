# AI UI Patterns (Advanced)

## Architecture

- API keys on server only — Next.js route handlers or backend API
- Client uses streaming hooks; never call OpenAI directly from browser

## Streaming Chat (Vercel AI SDK pattern)

```tsx
'use client';
import { useChat } from 'ai/react';

export function Chat() {
  const { messages, input, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
  });
  return (
    <form onSubmit={handleSubmit}>
      {messages.map(m => <Message key={m.id} role={m.role} content={m.content} />)}
      <input value={input} disabled={isLoading} />
    </form>
  );
}
```

## UX Rules

- Disable input while streaming response
- Show partial tokens as they arrive
- Error boundary + retry for failed generations
- Debounce autocomplete inputs (300–500ms)
- Human-in-the-loop for destructive AI actions (confirm step)

## Components

- Decouple `ChatMessage`, `InputBox`, `StreamingText` from data layer
- Sanitize model output before rendering HTML

See also: `ai-llm-integration` skill for backend routing and cost tracking.
