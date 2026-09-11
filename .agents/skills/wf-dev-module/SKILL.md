---
name: wf-dev-module
description: Implement a module from an existing plan. Use when plan exists and user wants implementation handoff.
---

1. Read the active plan under docs/plans/.
2. Spawn or act as the correct worker role for the layer (frontend/backend/database…).
3. Contract-first if API; Design Contract if UI.
4. Incremental commits; tests for critical paths.
5. Optional: `.cursor/commands/dev-module.md`.
