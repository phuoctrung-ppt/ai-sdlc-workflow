# Weak-Model Workflow Quality Gates
**Goal:** Raise plan/execution quality on lower-capability models by gating blank AGENTS.md, forcing section-by-section Phase 2 planning, and splitting judge severity so only Critical findings drive the fix loop.
**Protected:** yes | **Agents:** architect-planner, judge-agent

## Constraints
- Documentation-only; no app code, no secrets, no stack change.
- Stay inside three paths listed in SCOPE; do not edit hooks, skill-loader, skills-manifest, workers, or `AGENTS.md` body.
- Workflow-meta exception to the AGENTS gate applies to this change set itself when executing.

## Source Evidence
- `AGENTS.md` §1 still has raw placeholders (`<name>`, `<domain / industry>`) — proves blank-template planning risk.
- `.cursor/agents/architect-planner.md` has Phase 0 HARD-GATE and compact Plan Template, but **no** pre-plan check that §1/§2/§3 are filled.
- `.cursor/commands/dev-module.md` Phase 2 asks for one-shot full plan; does **not** embed Rule 2 / Rule 4 / mandatory Rule 5 from `.cursor/skills/planning/references/planning-with-lower-models.md`.
- `.cursor/agents/judge-agent.md` Output Format has `## Critical` + `## Suggestions`, but Status is only `*_APPROVED | *_CHANGES_REQUESTED` — no Critical vs Minor severity on the status line; `.cursor/commands/dev-module.md` Phase 5 decision tree increments `loopCount` for any `CHANGES_REQUESTED`.
- Out of scope (do not touch): hooks, `skill-loader.py`, `skills-manifest.json`, worker agents, `AGENTS.md` template body.

SECTION 1 COMPLETE

## Acceptance Criteria
1. Opening `.cursor/agents/architect-planner.md` (before Phase 0 brainstorm completes into a plan file): if `AGENTS.md` §1 **or** §2 **or** §3 still contains the literal token `<PLACEHOLDER>` **or** a table cell matching `/^<[^>]+>$/` (e.g. `<name>`, `<...>`), the agent MUST stop, print which sections are blank, and instruct the user/orchestrator to fill them (or run `/architecture-plan brainstorming`) — it MUST NOT write `docs/plans/*.md`.
2. Exception documented in the same gate: workflow-meta plans that only edit `.cursor/**` (agents/commands/rules) MAY proceed when the plan Goal is explicitly workflow-infra; product-feature plans MUST NOT use this exception.
3. `.cursor/commands/dev-module.md` Phase 2 requires the orchestrator to invoke `@architect-planner` **six times** (or six sequential turns), one section each, in order 1→6 from Rule 2, and forbids accepting a plan that lacks every `SECTION N COMPLETE` marker (N=1..6) or that ends mid-section without `[PAUSED - section N of 6]`.
4. Phase 2 body in `dev-module.md` contains the **verbatim** Rule 4 anti-laziness contract block from `planning-with-lower-models.md` §2 Rule 4 (the fenced contract starting with "You are writing an EXECUTABLE plan") — not a link-only reference.
5. Phase 2 body states Rule 5 self-verify checklist is **mandatory**; leaving Phase 2 / setting `state.phase = execute` is forbidden until all six checklist boxes are reported as pass in chat or in the plan file.
6. `.cursor/agents/judge-agent.md` Status line allows: `*_APPROVED`, `*_CHANGES_REQUESTED(Critical)`, `*_CHANGES_REQUESTED(Minor)` (for PLAN / TASK / BRANCH prefixes).
7. Severity rules in judge-agent: **Critical** = blocks ship (missing feature, security, broken build, missing tenant filter, untestable/missing acceptance evidence, blank AGENTS placeholders in genesis scope). **Minor** = style/suggestion/non-blocking doc nits; recorded under `## Suggestions` or `## Minor`; does not alone set Critical status.
8. `.cursor/commands/dev-module.md` Phase 5 decision tree: only `*_CHANGES_REQUESTED(Critical)` → Phase 5a and `loopCount++`. Status `*_APPROVED` or only-Minor → Phase 6. Minor findings are copied into the review artifact but do not block approve.
9. No files outside the three in-scope paths are modified by execution of this plan.

SECTION 2 COMPLETE

## Database / API Contract
N/A — documentation-only change to Cursor agent/command markdown. No DB migrations, no HTTP APIs, no shared Zod types.

SECTION 3 COMPLETE

## Files
| Path | Action | Owner |
|---|---|---|
| `.cursor/agents/architect-planner.md` | Modify — add **Phase −1 / AGENTS.md completeness gate** before Phase 0; list stop conditions + workflow-meta exception | architect-planner (orchestrator applies text; no app worker) |
| `.cursor/commands/dev-module.md` | Modify — rewrite Phase 2 for section-by-section calls; embed Rule 2 markers + Rule 4 contract + mandatory Rule 5; update Phase 5 decision tree for Critical-only loop | architect-planner (orchestrator applies text) |
| `.cursor/agents/judge-agent.md` | Modify — extend Status enum with Critical/Minor; define severity classification; map Minor → Suggestions, Critical → Critical section | judge-agent (doc owner; orchestrator applies text) |
| `docs/plans/2026-08-01-weak-model-workflow-quality.md` | Create — this plan | architect-planner |
| `docs/plans/.active-plan` | Modify — point to this plan | architect-planner |
| `.cursor/context/handoffs/weak-model-workflow-quality.json` | Create — handoff packet for the three-file edit | architect-planner |

SECTION 4 COMPLETE

## Execution / Task Breakdown

### Task 1 — AGENTS.md pre-plan gate
- **Owner:** architect-planner (doc edit by orchestrator)
- **Skill:** `planning` (`.cursor/skills/planning/SKILL.md`); reference already known: `planning-with-lower-models.md` Rule 1
- **Modify:** `.cursor/agents/architect-planner.md`
- **Do:** Insert a new section **immediately above** `## Phase 0 — BRAINSTORM`, titled `## Phase −1 — AGENTS.md Completeness Gate`, containing:
  1. Instruction to open `AGENTS.md` and scan §1 Overview table, §2 Tech Stack table, §3 Repository Structure fence for raw `<PLACEHOLDER>` or cells that are only `<...>` placeholders.
  2. On hit: emit `AGENTS_INCOMPLETE: §X, §Y` and **stop** — no plan file, no ADR.
  3. Explicit exception: plans whose Files table is subset of `.cursor/**` and Goal is workflow-infra MAY continue; must state `Gate skipped: workflow-meta` in the plan Source Evidence.
  4. Point Genesis callers to `/architecture-plan brainstorming` to fill domain first.
- **Acceptance:** Grep shows `Phase −1` (or `Phase -1`) heading in `.cursor/agents/architect-planner.md`; body mentions `<PLACEHOLDER>`, stop-without-plan, and workflow-meta exception; no other files changed in this task.

### Task 2 — Section-by-section Phase 2 + embedded Rule 2/4/5
- **Owner:** architect-planner (doc edit by orchestrator)
- **Skill:** `planning`; embed text from `.cursor/skills/planning/references/planning-with-lower-models.md` Rules 2, 4, 5
- **Modify:** `.cursor/commands/dev-module.md` → `## Phase 2 — PLAN`
- **Do:**
  1. Replace one-shot "Write full plan" with ordered steps: for N in 1..6, call `@architect-planner` with only section N; require literal `SECTION N COMPLETE` before N+1; on limit write `[PAUSED - section N of 6]`.
  2. Paste Rule 2 section list (Goal+Evidence → Acceptance → DB/API → Files → Tasks → Sync+Risks) inline in Phase 2.
  3. Paste Rule 4 fenced contract verbatim under a heading `### Anti-laziness contract (mandatory)`.
  4. Add `### Self-verify (Rule 5 — mandatory)` with the six checklist bullets; state orchestrator MUST NOT set `phase: execute` until all pass.
  5. Keep Phase 2b SYNC DOMAIN CONFIG and the approval STOP as-is after self-verify passes.
- **Acceptance:** `dev-module.md` Phase 2 contains strings `SECTION N COMPLETE`, `You are writing an EXECUTABLE plan`, `Self-verify (Rule 5 — mandatory)`, and does not describe Rule 4/5 as optional/"see reference".

### Task 3 — Judge severity tiers + Critical-only fix loop
- **Owner:** judge-agent (doc) + orchestrator for `dev-module.md` Phase 5
- **Skill:** `agentic-workflow` (`.cursor/skills/agentic-workflow/SKILL.md`)
- **Modify:** `.cursor/agents/judge-agent.md` and `.cursor/commands/dev-module.md` (Phase 5 + 5a only)
- **Do:**
  1. In judge-agent Review Mode / Output: Status values become `PLAN_APPROVED | PLAN_CHANGES_REQUESTED(Critical) | PLAN_CHANGES_REQUESTED(Minor)` (and same pattern for TASK_ / BRANCH_).
  2. Add severity rules: Critical vs Minor definitions matching Acceptance #7.
  3. Rule: if any Critical finding exists → status must be `*_CHANGES_REQUESTED(Critical)`. If only Minor → `*_CHANGES_REQUESTED(Minor)` **or** `*_APPROVED` with Minor listed under Suggestions — pick **one** policy and document it: **chosen policy = `*_CHANGES_REQUESTED(Minor)` when Minor-only, but Phase 5 treats Minor as non-blocking (proceed to Phase 6 without incrementing loopCount)**.
  4. Update Phase 5 decision tree and Phase 5a so only Critical triggers fix + `loopCount++`; Minor-only skips 5a.
  5. Phase 5a handoff text: "Fix [Critical issue…]" — ignore Minor in loop dispatch.
  6. Document: bare `*_CHANGES_REQUESTED` (no severity suffix) MUST be parsed as **Critical** (fail closed).
- **Acceptance:** `judge-agent.md` Status line includes `(Critical)` and `(Minor)` and states bare `CHANGES_REQUESTED` ≡ Critical; `dev-module.md` Phase 5 tree mentions Critical-only for `loopCount` and Phase 5a; Minor-only path goes to Phase 6.

### Task 4 — Handoff packet + active plan
- **Owner:** architect-planner
- **Create:** `.cursor/context/handoffs/weak-model-workflow-quality.json` with objective, in-scope paths (exactly the three markdown files), out-of-scope list from this plan, acceptance criteria 1–9, verification = grep for gate markers + status strings.
- **Modify:** `docs/plans/.active-plan` → `docs/plans/2026-08-01-weak-model-workflow-quality.md`
- **Acceptance:** handoff JSON parses; `.active-plan` content equals that path; no worker dispatch until Rule 5 pass below.

**Ordering:** Task 4 (plan bookkeeping) may run with Tasks 1–3; Tasks 1–3 are independent markdown edits and may run in parallel; no DB→API→FE chain.

SECTION 5 COMPLETE

## Risks
- Gate false-positive on workflow-meta plans if exception text is omitted → document Gate skipped explicitly.
- Operators may still one-shot Phase 2 if they ignore the command file → mitigation is imperative language ("MUST", "forbidden") not soft "should".
- Existing reviews using bare `CHANGES_REQUESTED` become ambiguous → judge-agent must say parsers treat bare `CHANGES_REQUESTED` as **Critical** (fail closed).
- Minor-only `CHANGES_REQUESTED(Minor)` naming may confuse humans into thinking approve is blocked → Phase 5 tree must say "Minor ⇒ Phase 6 (record only)".

## Handoffs
→ `.cursor/context/handoffs/weak-model-workflow-quality.json`

## Domain Config Sync
- [ ] ADR — **N/A** — no stack/tenancy/auth/storage decision; workflow prompt/gate text only
- [ ] `docs/architecture.md` — **N/A** — no container/data-flow change
- [ ] `AGENTS.md` — **N/A** — out of scope; gate *reads* placeholders but this plan does not fill the template
- [ ] `.cursor/config/worker-scopes.json` / `protected-paths.json` — **N/A** — no new agent paths or protected globs (`.cursor/agents/**` already workflow-owned)
- [x] `docs/plans/.active-plan` — set to this plan on approval/execution start
- [x] Plan Domain Config Sync section filled

SECTION 6 COMPLETE
