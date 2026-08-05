# V4 Vision — Critique & Pragmatic Direction (from Design-Gate branch)

**Base:** `enhance/design-frontend-gate-workflow`  
**This branch:** `enhance/context-orchestration-harden`  
**Date:** 2026-08-05

## 1. Guiding principle (keep)

> Configuration tells AI how to behave.  
> Context orchestration decides what AI should know before it starts thinking.

This is already the V2 product thesis. V4 restates it; it does not invent it.

## 2. Map V4 claims → what already ships in this repo

| V4 slogan | Already in tree | Gap (real) |
|-----------|-----------------|------------|
| Intent Detection | `.cursor/context/intent_detector.py` | Tune hints for Design Contract phase |
| Context Builder | `context-builder.py` + tiers | Enforce budgets harder; log packet |
| Context Packet | `schemas/context-packet.schema.json` v2.0 | Include designContract path when UI |
| Context Budget | `config/context-budget.json` | Rarely validated in CI |
| Dynamic Agent Routing | `config/agent-matrix.json` | Add design-specification sequence |
| Skill Registry | `skills-manifest.v2.json` + `estimatedTokens` | Builder must hard-cap by complexity |
| Pattern Library | `.cursor/patterns/**` | More patterns from retrospectives |
| Project Memory | `docs/memory/*` + `.memory/*` cache | Keep concise; no second memory product |
| Multi-agent roster | `.cursor/agents/*` + scopes | Contracts are prose today |
| Learning | learning-counter + skill-updater | Keep module-triggered, not platform |
| Design as first-class | Design Contract (prior branch) | Wire into intent + packet |

**Conclusion:** Building an “AI Context Orchestration Platform” from scratch would **duplicate** 70%+ of V2. Correct move = **harden and wire**, not rebrand.

## 3. Ideas that are unreasonable (do not change workflow for these)

### 3.1 “Universal” across Cursor / Claude Code / Codex / Gemini / Grok (P0)

Unreasonable as near-term workflow change.

- Hooks, `.mdc` rules, agent files, and session-start are **Cursor-native**.
- Each tool has a different config surface (CLAUDE.md, AGENTS in Codex, etc.).
- A true universal layer is an **adapter product**, not a doc rewrite inside `.cursor/`.

**Decision:** Remain Cursor-first. Porting guide already exists. Multi-tool adapters = separate initiative after Cursor path is boringly reliable.

### 3.2 “AI should never receive every document” / agents must not search the repo

Unreasonable as a hard rule for coding agents.

- Implementation **requires** reading real files under `apps/`, diffs, stack traces.
- Context Packet is a **priority pack**, not a sandbox jail.
- Forbidding repo read forces incomplete fixes and more tokens on guesswork.

**Decision:** Packet is **primary context**. Repo read is **allowed and expected** within `worker-scopes.json`. `doNotLoad` stays advisory for bulk dumps (full `node_modules`, lockfiles, raw state).

### 3.3 “Context Score” as a scored knowledge graph for every source

Unreasonable if it implies ML ranking or continuous scoring infra.

- No labeled dataset; no online feedback loop in MVP.
- Keyword + path + phase scoring already approximates relevance cheaply.

**Decision:** Ship **heuristic score config** (this branch). Defer learned ranking until analytics exist from real runs.

### 3.4 “Knowledge Compiler” as a separate compilation product

Unreasonable rename of Context Builder.

- Builder already assembles tier1–4 from memory, skills, patterns, paths.
- Markdown remains the authoring format; “compile” is the builder step.

**Decision:** Do not add a second compiler. Improve builder acceptance tests.

### 3.5 Configurable runtime Agent Graph as a product surface

Unreasonable vs current rule matrix.

- `agent-matrix.json` already encodes when/sequence/reviewer.
- A visual graph editor does not improve fix quality for SMEs.

**Decision:** Extend matrix rules (e.g. design-spec sequence). No graph runtime.

### 3.6 Full Analytics platform (token, skill, pattern, memory hits…)

Premature without volume.

- Retrospective + learning-counter already capture module-level signal.
- Building dashboards before 50+ real module runs is ceremony.

**Decision:** Optional append-only packet usage line under `.aisdlc/` later. Not a V4 blocker.

### 3.7 Expand modules to PM / Marketing / Support / CS

Scope creep away from **software delivery**.

- Strength is SDLC (plan → design contract → implement → judge → learn).
- Adjacent domains need different evaluation loops.

**Decision:** Out of scope until SDLC path is proven on multiple product repos.

### 3.8 “Model-driven → context-driven” as if the model stops reasoning

Category error.

- Orchestration **prepares** context; the model still reasons and writes code.
- Over-selling “platform decides everything” creates false confidence and under-invests in gates (Design Contract, judge rubrics).

**Decision:** Language: **context-prepared execution**, not “context replaces intelligence.”

## 4. Ideas that are reasonable (implement incrementally)

| Item | Why | This branch |
|------|-----|-------------|
| Context-first packet before agents | Already core; must include Design Contract on UI tasks | Wire phase + matrix |
| Token efficiency = cut waste, not starve reasoning | Budget ceilings exist | Document + enforce in policy |
| Multi-agent by design | Keep specialized workers | design-spec sequence |
| Skill registry with cost hints | `estimatedTokens` present | Manifest phase list |
| Thin agent contracts (I/O, scope) | Reduces handoff ambiguity | JSON schema |
| Heuristic context score | Cheap relevance ordering | `context-score.json` |
| Design Specification in orchestration | Prior branch artifact | Intent + matrix + policy |

## 5. V3.1 direction (name intentionally not “V4 platform”)

1. **Keep** Cursor-native orchestration (builder, intent, budget, matrix, packet).
2. **Keep** Design Contract gate from previous branch; treat it as tier-1 context for UI.
3. **Harden** routing for `design-specification` → designer → design-judge → breakdown.
4. **Reject** universal multi-tool, repo-read ban, ML scores, analytics product, non-SDLC modules as P0.
5. **Measure** later via retrospectives and optional packet logs — data before platform.

## 6. Success criteria for this branch

- [ ] Critique doc merged (this file)
- [ ] Intent recognizes design-contract / design-specification
- [ ] Agent matrix has explicit design-spec rule with judge
- [ ] Heuristic context-score config committed
- [ ] Thin agent-contract schema committed
- [ ] Policy + skill docs state: packet primary, scoped repo read allowed
- [ ] No claim of multi-vendor runtime

## 7. Non-goals

- Rewrite `.cursor/` into a vendor-neutral SDK
- Block `Read`/`grep` on application code
- Train a ranker
- Ship analytics UI
- Rename V2 → V4 in marketing without capability delta
