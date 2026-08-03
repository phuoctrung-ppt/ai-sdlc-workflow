#!/usr/bin/env python3
"""Emit an agent event for the ai-sdlc office UI (.aisdlc/events.jsonl).

Works without installing the ai-sdlc package. Safe no-op if write fails.

Usage:
  python3 .cursor/scripts/office-event.py --agent architect-planner --status working --task "Plan X" --phase plan
  python3 .cursor/scripts/office-event.py --agent backend-worker --status idle
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def find_work_root(start: Path | None = None) -> Path:
    p = (start or Path.cwd()).resolve()
    for candidate in [p, *p.parents]:
        if (candidate / ".aisdlc").is_dir() or (candidate / ".cursor" / "agents").is_dir():
            return candidate
    return p


def emit(
    work_root: Path,
    *,
    agent: str,
    status: str,
    task: str = "",
    detail: str = "",
    phase: str = "",
) -> dict:
    root = work_root / ".aisdlc"
    root.mkdir(parents=True, exist_ok=True)
    events_path = root / "events.jsonl"
    state_path = root / "state.json"

    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "agent": agent,
        "status": status,
        "task": task,
        "detail": detail,
        "phase": phase,
    }
    with events_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    try:
        state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {"agents": {}}
    except json.JSONDecodeError:
        state = {"agents": {}}
    state.setdefault("agents", {})[agent] = {
        "status": status,
        "task": task,
        "detail": detail,
        "phase": phase,
        "updated_at": event["ts"],
    }
    state["updated_at"] = event["ts"]
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return event


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Emit office UI agent event")
    p.add_argument("--agent", required=True)
    p.add_argument(
        "--status",
        required=True,
        choices=("idle", "working", "waiting", "done", "error"),
    )
    p.add_argument("--task", default="")
    p.add_argument("--detail", default="")
    p.add_argument("--phase", default="")
    p.add_argument("--path", default=None, help="Work root (default: cwd / find .aisdlc)")
    args = p.parse_args(argv)

    work = Path(args.path).resolve() if args.path else find_work_root()
    try:
        event = emit(
            work,
            agent=args.agent,
            status=args.status,
            task=args.task,
            detail=args.detail,
            phase=args.phase,
        )
    except OSError as e:
        print(f"office-event: write failed: {e}", file=sys.stderr)
        return 1
    print(json.dumps(event, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
