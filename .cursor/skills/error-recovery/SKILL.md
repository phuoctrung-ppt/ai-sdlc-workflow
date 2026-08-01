---
name: error-recovery
description: Classify and fix build, type, test, runtime, and integration failures by root cause — not symptoms. Use when debugging failures during implement or fix phases.
---

# Error Recovery

Fix the **root cause**. Do not hide failures.

## Classify first

| Class | Typical signals | Approach |
|---|---|---|
| **Build error** | bundler/compiler exit ≠ 0, missing module, bad config | Fix import/path/config; re-run the same build command |
| **Type error** | `tsc` / typechecker diagnostics | Narrow types with guards; never `as any` to silence |
| **Test fail** | assertion mismatch, timeout, mock drift | Fix code or update test to match intended contract; never comment out the test |
| **Runtime error** | stack trace in logs, unhandled rejection | Reproduce → null/edge path → minimal guard or correct invariant |
| **Integration error** | HTTP 4xx/5xx to dependency, queue/DB connection | Check env, contract, mocks; fix call site or test double |

## Root-cause checklist (answer all four before editing)

1. What is the **exact** error message (full text, not a paraphrase)?
2. Which **file:line** does it point to (or nearest caller if in deps)?
3. Is this a **symptom** of an earlier failure (wrong assumption, stale mock, missing migrate)?
4. What is the **smallest** change that restores the invariant without masking the error?

If you cannot answer 1–2, gather more evidence before changing code.

## Fix pattern

1. Read the **full** error message (and preceding context in the log).
2. Identify **file:line**.
3. Read **~10 lines** of surrounding context (and callers if needed).
4. Propose a **minimal** fix that addresses the root cause.
5. Verify: re-run the failing command; confirm adjacent behavior still passes (related tests / typecheck).

## Anti-patterns (forbidden)

- ❌ Add `try/catch` (or swallow) only to hide an error without fixing the cause
- ❌ Cast `as any` / disable the typechecker to bypass a type error
- ❌ Comment out or skip a failing test to go green
- ❌ Change unrelated files “while here” without evidence they cause the failure

## Agent

Use during phases `fix`, `implement-backend`, `implement-frontend` with workers that own the failing files.
