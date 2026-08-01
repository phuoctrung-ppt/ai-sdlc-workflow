---
name: generate-test
description: Scaffold unit, integration, or E2E tests with mocks for external APIs — uses project's test framework from AGENTS.md
---

Act as **QA Worker**. Generate tests for: **{target}**

Type: {unit|integration|e2e}

1. Run context-builder:
   ```bash
   python3 .cursor/context/context-builder.py \
     --phase test --task "generate {type} tests for {target}" --agent qa-worker \
     --keywords "test,mock,coverage,e2e,jest,vitest,playwright"
   ```
2. Read `.memory/constraints.md` and `AGENTS.md §7` (external services to mock)

Requirements:
- Read tier2 `testing-qa` SKILL.md; tier4 refs via `--expand-ref` only if needed
- Mock all external services listed in `AGENTS.md §7` (never hit real APIs in tests)
- Multi-tenancy isolation cases if `AGENTS.md §5` declares multi-tenancy
- Follow naming convention from `AGENTS.md §2` (e.g. `*.spec.ts`, `*.test.ts`, `*.e2e-spec.ts`)
- Coverage target: 70%+ for service/business logic layers (see `AGENTS.md §6`)

Output complete test file(s).
