# ai-sdlc CLI

CLI wrapper around the **v2** agentic workflow. Initialize a work folder for **Cursor** or **Claude**, then open the **office UI** to watch the agent team.

## Install (dev / global)

```bash
cd cli
pip install -e .
# or: pipx install --editable .
```

## Commands

```bash
ai-sdlc --init cursor
ai-sdlc --init claude
ai-sdlc init cursor --path ./my-app --repo /path/to/ai-sdlc-workflow

ai-sdlc ui                  # http://127.0.0.1:9669
ai-sdlc demo
ai-sdlc event --agent architect-planner --status working --task "Plan auth"
ai-sdlc status
```

## Auto events from `/dev-module` (important)

After this branch’s workflow wiring:

| Piece | Role |
|-------|------|
| `.cursor/scripts/office-event.py` | Portable emitter → `.aisdlc/events.jsonl` (no pip) |
| `.cursor/rules/008-office-ui-events.mdc` | Agents **must** emit start/end of every turn |
| `.cursor/commands/dev-module.md` | Orchestrator emits on **every phase** + each worker task |

**You still need:**

1. Workspace with `.aisdlc/` (`ai-sdlc --init …`)
2. `ai-sdlc ui` running
3. Cursor session using **updated** `.cursor/` from this branch (re-init or copy `.cursor/scripts` + rule `008` + `dev-module.md`)

If you init’d before the wiring commit, refresh:

```bash
cd /your/app
ai-sdlc --init cursor --repo /path/to/ai-sdlc-workflow --force
# or manually copy:
#   .cursor/scripts/office-event.py
#   .cursor/rules/008-office-ui-events.mdc
#   .cursor/commands/dev-module.md
```

Then run `/dev-module <name>` in Cursor — desks should move as phases progress.

## Office UI

Open **http://localhost:9669** after `ai-sdlc ui`.

- Desks from `.cursor/agents/`
- Live feed from `.aisdlc/events.jsonl` (SSE)

## Layout after `--init`

```text
.
├── .aisdlc/
│   ├── config.json
│   ├── events.jsonl
│   └── state.json
├── AGENTS.md
├── docs/memory/
├── .cursor/          # includes scripts/office-event.py + rule 008
└── .claude/          # claude init only
```
