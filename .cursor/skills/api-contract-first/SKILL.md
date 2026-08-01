---
name: api-contract-first
description: Require an approved API/schema contract before backend or frontend implementation. OpenAPI or Zod per AGENTS.md §2; lock changes through contract-agent.
---

# API Contract First

## Rule

The contract **MUST** be written and **approved** **before** `@backend-worker` or `@frontend-worker` implement the feature’s HTTP/API surface.

Owner of the contract artifact: `@contract-agent` → `docs/contracts/YYYY-MM-DD-{feature}-contract.md` (and shared types under `packages/**` when `AGENTS.md` §3 defines the package).

## Format

Choose **one** source of truth from `AGENTS.md` §2 (Shared contracts):

- **OpenAPI** snippet in the contract file, or
- **Zod** schema in the shared types package (preferred when §2 names Zod)

Do not maintain conflicting shapes in both without generating one from the other.

## Lock rule

After `@contract-agent` marks the contract **approved**, no worker may unilaterally change endpoint shapes. All changes go through `@contract-agent` first.

## Breaking vs non-breaking

**Breaking** (requires contract-agent update + `[BREAKING]` tag + frontend notify):
- Rename a field
- Remove a field
- Change a field’s type
- Change the HTTP method

**Non-breaking:**
- Add an optional field
- Add a new endpoint

## Workflow

1. Plan approved → dispatch `@contract-agent`
2. Contract approved → backend and frontend may start (in dependency order)
3. Need a shape change → `@contract-agent` updates file → consumers adapt

## Anti-patterns

- ❌ Implementing controllers/pages from a chat sketch with no contract file
- ❌ Frontend inventing response fields the backend never promised
- ❌ “We’ll sync types later” after both sides have shipped divergent shapes
