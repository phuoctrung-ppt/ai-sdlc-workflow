#!/usr/bin/env python3
"""Emit an agent event for the ai-sdlc office UI (.aisdlc/events.jsonl).

Usage:
  python3 .cursor/scripts/office-event.py --agent architect-planner --status working \\
      --task "Plan X" --phase plan --workflow billing-module
  python3 .cursor/scripts/office-event.py --agent backend-worker --status done \\
      --task "API done" --tokens 12000 --tokens-in 9000 --tokens-out 3000 --workflow billing-module
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


def _load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def emit(
    work_root: Path,
    *,
    agent: str,
    status: str,
    task: str = "",
    detail: str = "",
    phase: str = "",
    workflow: str = "",
    tokens: int | None = None,
    tokens_in: int | None = None,
    tokens_out: int | None = None,
) -> dict:
    root = work_root / ".aisdlc"
    root.mkdir(parents=True, exist_ok=True)
    events_path = root / "events.jsonl"
    state_path = root / "state.json"
    bench_path = root / "benchmarks.json"

    # derive total tokens
    t_in = int(tokens_in) if tokens_in is not None else 0
    t_out = int(tokens_out) if tokens_out is not None else 0
    t_total = int(tokens) if tokens is not None else (t_in + t_out if (tokens_in or tokens_out) else 0)

    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "agent": agent,
        "status": status,
        "task": task,
        "detail": detail,
        "phase": phase,
        "workflow": workflow or "",
        "tokens": t_total or None,
        "tokens_in": t_in or None,
        "tokens_out": t_out or None,
    }
    with events_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    state = _load_json(state_path, {"agents": {}})
    prev = state.setdefault("agents", {}).get(agent, {})
    # accumulate tokens on agent
    acc = int(prev.get("tokens_total") or 0) + (t_total or 0)
    acc_in = int(prev.get("tokens_in_total") or 0) + (t_in or 0)
    acc_out = int(prev.get("tokens_out_total") or 0) + (t_out or 0)
    # keep task text when status is done/idle if empty task passed
    shown_task = task if task else (prev.get("task") if status in ("done", "error") else "")
    state["agents"][agent] = {
        "status": status,
        "task": shown_task if status != "idle" else "",
        "detail": detail or prev.get("detail") or "",
        "phase": phase or prev.get("phase") or "",
        "workflow": workflow or prev.get("workflow") or "",
        "updated_at": event["ts"],
        "tokens_total": acc,
        "tokens_in_total": acc_in,
        "tokens_out_total": acc_out,
        "last_tokens": t_total or 0,
    }
    state["updated_at"] = event["ts"]
    if workflow:
        state["active_workflow"] = workflow
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # benchmarks rollup: per workflow → per agent
    if t_total or workflow:
        bench = _load_json(
            bench_path,
            {"workflows": {}, "agents": {}, "updated_at": None},
        )
        wf_key = workflow or "_default"
        wf = bench.setdefault("workflows", {}).setdefault(
            wf_key,
            {"tokens_total": 0, "tokens_in": 0, "tokens_out": 0, "events": 0, "agents": {}},
        )
        wf["tokens_total"] = int(wf.get("tokens_total") or 0) + (t_total or 0)
        wf["tokens_in"] = int(wf.get("tokens_in") or 0) + (t_in or 0)
        wf["tokens_out"] = int(wf.get("tokens_out") or 0) + (t_out or 0)
        wf["events"] = int(wf.get("events") or 0) + 1
        wa = wf.setdefault("agents", {}).setdefault(
            agent, {"tokens_total": 0, "tokens_in": 0, "tokens_out": 0, "tasks_done": 0}
        )
        wa["tokens_total"] = int(wa.get("tokens_total") or 0) + (t_total or 0)
        wa["tokens_in"] = int(wa.get("tokens_in") or 0) + (t_in or 0)
        wa["tokens_out"] = int(wa.get("tokens_out") or 0) + (t_out or 0)
        if status == "done":
            wa["tasks_done"] = int(wa.get("tasks_done") or 0) + 1

        ag = bench.setdefault("agents", {}).setdefault(
            agent, {"tokens_total": 0, "tokens_in": 0, "tokens_out": 0, "workflows": {}}
        )
        ag["tokens_total"] = int(ag.get("tokens_total") or 0) + (t_total or 0)
        ag["tokens_in"] = int(ag.get("tokens_in") or 0) + (t_in or 0)
        ag["tokens_out"] = int(ag.get("tokens_out") or 0) + (t_out or 0)
        if workflow:
            ag.setdefault("workflows", {})[workflow] = int(
                ag.get("workflows", {}).get(workflow) or 0
            ) + (t_total or 0)

        bench["updated_at"] = event["ts"]
        bench_path.write_text(json.dumps(bench, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

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
    p.add_argument("--workflow", default="", help="Module/workflow id for token audit")
    p.add_argument("--tokens", type=int, default=None, help="Total tokens this turn")
    p.add_argument("--tokens-in", type=int, default=None)
    p.add_argument("--tokens-out", type=int, default=None)
    p.add_argument("--path", default=None)
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
            workflow=args.workflow,
            tokens=args.tokens,
            tokens_in=getattr(args, "tokens_in", None),
            tokens_out=getattr(args, "tokens_out", None),
        )
    except OSError as e:
        print(f"office-event: write failed: {e}", file=sys.stderr)
        return 1
    print(json.dumps(event, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
