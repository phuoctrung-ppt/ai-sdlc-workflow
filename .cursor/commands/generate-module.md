---
name: generate-module
description: Scaffold a complete feature module using the project's backend framework conventions — controller/route, service, DTOs/schemas, entity/model, and tests
---

Act as **Backend Worker**. Scaffold a complete feature module for: **{feature_name}**

1. Run context-builder first:
   ```bash
   python3 .cursor/context/context-builder.py \
     --phase implement-backend --task "scaffold {feature_name} module" --agent backend-worker \
     --keywords "module,service,controller,scaffold"
   ```
2. Obey Context Packet tiers — read tier2 backend/framework skill SKILL.md
3. Read `.memory/constraints.md` and `AGENTS.md §3` for backend app path

## Module Location

Determined by `AGENTS.md §3` — typically:
```
<backend_app_path>/src/modules/{feature_name}/
```

## Files to Generate

Scaffold these files using your framework's conventions (names and structure from `AGENTS.md §2`):

| File | Purpose |
|------|---------|
| `{feature_name}.module.*` | Module/router registration |
| `{feature_name}.controller.*` | Route handlers / endpoints |
| `{feature_name}.service.*` | Business logic |
| `dto/create-{feature_name}.*` | Create input schema/DTO |
| `dto/update-{feature_name}.*` | Update input schema/DTO |
| `entities/{feature_name}.*` | DB model / entity |
| `{feature_name}.service.spec.*` | Unit tests for service layer |
| `index.*` | Barrel export |

## Requirements

- Input validation at boundary (framework's schema/pipe system from `AGENTS.md §2`)
- Shared type contracts in the shared package (see `AGENTS.md §3`)
- Auth guard on all routes — public routes explicitly marked (auth method from `AGENTS.md §2`)
- Structured logger — no `console.log`
- Unit tests with 70%+ service layer coverage
- Compliance items from `AGENTS.md §5` applied (multi-tenancy, GDPR, RBAC, etc.)
- API docs annotations if the project uses them (check `AGENTS.md §2`)

Output complete file contents for each file.
