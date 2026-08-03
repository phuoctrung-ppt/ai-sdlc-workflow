"""ai-sdlc CLI entrypoint."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from ai_sdlc_cli import __version__
from ai_sdlc_cli.agents import DEFAULT_AGENTS, discover_agents
from ai_sdlc_cli.events import emit_event, read_config, read_state
from ai_sdlc_cli.init_workspace import PROVIDERS, find_repo_root, init_workspace
from ai_sdlc_cli.server import serve


def _work_path(args: argparse.Namespace) -> Path:
    return Path(getattr(args, "path", None) or ".").resolve()


def cmd_init(args: argparse.Namespace) -> int:
    provider = args.provider
    work = _work_path(args)
    repo = Path(args.repo).resolve() if args.repo else find_repo_root(work)
    try:
        result = init_workspace(work, provider, repo_root=repo, force=args.force)
    except (ValueError, FileNotFoundError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    print("\nNext:")
    for line in result["next"]:
        print(f"  {line}")
    return 0


def cmd_ui(args: argparse.Namespace) -> int:
    work = _work_path(args)
    if not (work / ".aisdlc").exists() and not (work / ".cursor" / "agents").exists():
        print(
            "warning: no .aisdlc or .cursor/agents — run: ai-sdlc --init cursor",
            file=sys.stderr,
        )
    port = args.port
    cfg = read_config(work)
    if not args.port_set and cfg.get("ui_port"):
        port = int(cfg["ui_port"])
    serve(work, host=args.host, port=port)
    return 0


def cmd_event(args: argparse.Namespace) -> int:
    work = _work_path(args)
    event = emit_event(
        work,
        agent=args.agent,
        status=args.status,
        task=args.task or "",
        detail=args.detail or "",
        phase=args.phase or "",
    )
    print(json.dumps(event, indent=2))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    work = _work_path(args)
    agents = discover_agents(work)
    state = read_state(work)
    config = read_config(work)
    print(json.dumps({"work_root": str(work), "config": config, "agents": agents, "state": state}, indent=2))
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    """Animate a short office scene so the UI has something to show."""
    work = _work_path(args)
    roster = discover_agents(work) or DEFAULT_AGENTS
    script = [
        ("architect-planner", "working", "Brainstorm auth module", "brainstorm"),
        ("architect-planner", "working", "Write plan breakdown", "plan"),
        ("contract-agent", "working", "Draft API contract", "plan"),
        ("database-worker", "working", "Design tenant-scoped tables", "database"),
        ("backend-worker", "working", "Implement /auth/refresh", "implement-backend"),
        ("frontend-worker", "working", "Build login form", "implement-frontend"),
        ("designer-worker", "working", "Product track settings shell", "design"),
        ("qa-worker", "working", "Add e2e login path", "test"),
        ("security-worker", "working", "Review token storage", "review"),
        ("judge-agent", "waiting", "Awaiting Critical fixes", "review"),
        ("backend-worker", "working", "Fix tenant filter (Critical)", "fix"),
        ("judge-agent", "done", "APPROVED", "review"),
        ("learning-agent", "working", "Scan retrospective", "review"),
        ("learning-agent", "done", "NO_PATTERN", "review"),
    ]
    # only use agents that exist
    ids = {a["id"] for a in roster}
    print(f"demo → {work} (Ctrl+C to stop early)")
    print("Open http://127.0.0.1:9669 in another terminal: ai-sdlc ui")
    try:
        for agent, status, task, phase in script:
            if agent not in ids and agent not in {a["id"] for a in DEFAULT_AGENTS}:
                continue
            emit_event(work, agent=agent, status=status, task=task, phase=phase)
            print(f"  {agent:22} {status:8} {task}")
            time.sleep(args.delay)
        # settle to idle
        for a in roster:
            emit_event(work, agent=a["id"], status="idle", task="", phase="")
        print("demo complete")
    except KeyboardInterrupt:
        print("\ndemo interrupted")
        return 130
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ai-sdlc",
        description="CLI wrapper for ai-sdlc-workflow — init workspaces & office UI (port 9669)",
    )
    p.add_argument("--version", action="version", version=f"ai-sdlc {__version__}")
    p.add_argument(
        "--init",
        metavar="PROVIDER",
        choices=PROVIDERS,
        help="Initialize workspace for provider: cursor | claude",
    )
    p.add_argument("--path", default=".", help="Work folder (default: cwd)")
    p.add_argument("--repo", default=None, help="Path to ai-sdlc-workflow checkout")
    p.add_argument("--force", action="store_true", help="Overwrite existing copied paths on init")

    sub = p.add_subparsers(dest="command")

    p_init = sub.add_parser("init", help="Initialize work folder")
    p_init.add_argument("provider", choices=PROVIDERS)
    p_init.add_argument("--path", default=".")
    p_init.add_argument("--repo", default=None)
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_ui = sub.add_parser("ui", help="Start office UI (default :9669)")
    p_ui.add_argument("--path", default=".")
    p_ui.add_argument("--host", default="127.0.0.1")
    p_ui.add_argument("--port", type=int, default=9669)
    p_ui.set_defaults(func=cmd_ui, port_set=False)

    p_ev = sub.add_parser("event", help="Emit agent event to the office log")
    p_ev.add_argument("--path", default=".")
    p_ev.add_argument("--agent", required=True)
    p_ev.add_argument(
        "--status",
        required=True,
        choices=("idle", "working", "waiting", "done", "error"),
    )
    p_ev.add_argument("--task", default="")
    p_ev.add_argument("--detail", default="")
    p_ev.add_argument("--phase", default="")
    p_ev.set_defaults(func=cmd_event)

    p_st = sub.add_parser("status", help="Print workspace + agent state")
    p_st.add_argument("--path", default=".")
    p_st.set_defaults(func=cmd_status)

    p_demo = sub.add_parser("demo", help="Replay a sample agent session into the event log")
    p_demo.add_argument("--path", default=".")
    p_demo.add_argument("--delay", type=float, default=1.2, help="Seconds between events")
    p_demo.set_defaults(func=cmd_demo)

    return p


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()

    # Support: ai-sdlc --init cursor
    if argv and argv[0] == "--init" and len(argv) >= 2:
        args = parser.parse_args(argv)
        args.provider = args.init
        args.force = bool(getattr(args, "force", False))
        return cmd_init(args)

    args = parser.parse_args(argv)

    if getattr(args, "init", None) and not args.command:
        args.provider = args.init
        return cmd_init(args)

    if not getattr(args, "command", None):
        parser.print_help()
        return 0

    # track whether user passed --port on ui
    if args.command == "ui":
        args.port_set = "--port" in argv

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
