# ai-sdlc CLI

CLI wrapper around the **v2** agentic workflow. Initialize a work folder for **Cursor** or **Claude**, then open the **office UI** to watch the agent team.

## Install (dev)

```bash
cd cli
pip install -e .
```

## Commands

```bash
# Scaffold workspace in current directory (or --path)
ai-sdlc --init cursor
ai-sdlc --init claude
ai-sdlc init cursor --path ./my-app

# Start office UI (default http://127.0.0.1:9669)
ai-sdlc ui
ai-sdlc ui --port 9669 --path ./my-app

# Emit a demo event stream (agents appear busy in the UI)
ai-sdlc demo --path ./my-app

# Log a manual agent event (for wrappers / hooks)
ai-sdlc event --agent architect-planner --status working --task "Plan auth module"

# Show workspace status
ai-sdlc status
```

## Office UI

Open **http://localhost:9669** after `ai-sdlc ui`.

- Desks for each agent defined under `.cursor/agents/`
- Live task feed from `.aisdlc/events.jsonl` (SSE)
- Status colors: idle / working / waiting / done / error

## Layout after `--init`

```text
.
├── .aisdlc/
│   ├── config.json          # provider, port, created_at
│   ├── events.jsonl         # append-only event log
│   └── state.json           # last known agent statuses
├── AGENTS.md                # domain template (from repo)
├── docs/memory/             # durable memory SoT
├── docs/retrospective.md
├── .cursor/                 # full workflow (cursor init)
│   ├── agents/
│   ├── skills/
│   ├── commands/
│   └── ...
└── .claude/                 # claude adapter notes + CLAUDE.md (claude init)
```

Claude init still copies `.cursor/` skills/agents as the source of truth and adds `.claude/CLAUDE.md` pointing at the same workflow so both hosts can share the folder.
