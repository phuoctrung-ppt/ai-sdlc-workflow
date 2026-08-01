# Architecture (auto-generated 2026-07-27T10:41:38Z)

Workflow monorepo layout:
> Describe the actual layout of THIS repo. Keep it in sync with `.cursor/config/worker-scopes.json` (agent path scopes must match real folders).

```
<root>/
├── <app-or-package-1>/        # <role>
├── <app-or-package-2>/        # <role>
├── docs/                      # plans, adr, reviews, architecture
└── .cursor/                   # workflow: agents, skills, hooks, config
```

> _EXAMPLE_ (delete when porting): a monorepo might use `apps/api`, `apps/web`, `apps/worker`, `packages/shared-types`. Whatever you choose, mirror it exactly in `worker-scopes.json`.

---
