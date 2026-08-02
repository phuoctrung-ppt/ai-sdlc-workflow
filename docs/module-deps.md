# Module Dependency Graph (Learning Layer)

> Machine-readable + human-readable dependency contracts.
> Hard-gate: do not execute a module whose dependencies are not yet `done` or `contract-approved`.
>
> Format: YAML front-matter style inside markdown for easy parsing.

```yaml
modules:
  # Example:
  # M2-auth:
  #   status: done
  #   contract: docs/contracts/2026-08-01-auth-contract.md
  #   depends_on: []
  # M3-billing:
  #   status: planned
  #   contract: null
  #   depends_on: [M2-auth]
```

## Current Graph

```yaml
modules: {}
```

## Rules

1. Before Phase 3 (Execute) of any module, the orchestrator MUST read this file.
2. If any `depends_on` entry is not `status: done` (or has an unapproved contract), block and report.
3. After a module reaches Phase 6 (Done), update its status here and write the retrospective entry.
