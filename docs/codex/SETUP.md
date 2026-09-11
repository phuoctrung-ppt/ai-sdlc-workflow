# Codex adapter — force design map

Branch: `adapt/codex-force-design` (from `v2`).

This branch **does not** re-implement Cursor hooks/matrix/loader in Python.
It **forces the same design principles** onto surfaces Codex actually loads.

## Design principles (unchanged)

1. **Domain-neutral AGENTS.md** — §0 layers on/off; never invent off-layer work.
2. **Planner → Worker → Judge** — plan/shape before big change; fix loop for bugs; judge on protected paths.
3. **Day path** — `/fix` and `/shape-lite` first; full plan secondary.
4. **Thin skills + lazy references** — entry rules always; deep refs on demand.
5. **Portable skills** — craft rules travel; project facts stay in AGENTS.md.
6. **No bulk context** — do not dump entire `docs/reviews/**` or skill `references/` folders.

## Surface map (Cursor → Codex)

| Design element | Cursor (canonical) | Codex (this branch) |
|----------------|--------------------|---------------------|
| Project domain config | `AGENTS.md` | Same file + Codex runtime section |
| Always-on rules | `.cursor/rules/*.mdc` | Summarized into AGENTS.md Codex section |
| Skills | `.cursor/skills/*/SKILL.md` | `.agents/skills/*/SKILL.md` adapters → read canonical |
| Multi-agent roster | `.cursor/agents/*.md` + matrix | `.codex/agents/*.toml` + `[agents]` roles |
| Commands (`/fix`, …) | `.cursor/commands/*.md` | Skills: `wf-fix`, `wf-shape-lite`, `wf-plan-feature`, … |
| Layer filter | `active-layers.json` | AGENTS §0; agents must skip off layers |
| Context builder | `context-builder.py` | **Not used** — progressive skill disclosure |
| Hooks | `.cursor/hooks*` | Policy text in AGENTS + agent instructions |

## How to run

```bash
git checkout adapt/codex-force-design
codex   # from repo root
```

Verify guidance:

```bash
codex --ask-for-approval never "Summarize active instruction sources and list discovered skills matching fix or plan."
```

Explicit skill:

```text
$wf-fix reproduce and patch the login 500
$planning break this feature into MVP tasks
```

Parallel specialists (optional):

```text
Spawn subagents: explorer for codebase map, reviewer for security risks. Wait, then summarize.
```

## Single source of truth

- **Do not fork skill bodies** under `.agents/skills` — adapters only.
- Change craft rules in `.cursor/skills/<id>/` so Cursor and Codex stay aligned.
- Change project facts only in root `AGENTS.md` §0–§15.

## Limits (honest)

- Codex does **not** auto-run the Cursor phase machine or office-event loop.
- Subagents spawn only when the user asks (or a skill explicitly instructs spawn).
- Python `profile-sync` / `context-builder` remain Cursor tooling; optional on Codex if you run them manually for JSON artifacts.
