"""Append-only event log + state + benchmarks for the office UI."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

AISDLC_DIR = ".aisdlc"
EVENTS_FILE = "events.jsonl"
STATE_FILE = "state.json"
CONFIG_FILE = "config.json"
BENCH_FILE = "benchmarks.json"


def aisdlc_path(work_root: Path) -> Path:
    return work_root / AISDLC_DIR


def ensure_aisdlc(work_root: Path) -> Path:
    root = aisdlc_path(work_root)
    root.mkdir(parents=True, exist_ok=True)
    events = root / EVENTS_FILE
    if not events.exists():
        events.write_text("", encoding="utf-8")
    state = root / STATE_FILE
    if not state.exists():
        state.write_text(json.dumps({"agents": {}}, indent=2) + "\n", encoding="utf-8")
    return root


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def emit_event(
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
) -> dict[str, Any]:
    ensure_aisdlc(work_root)
    t_in = int(tokens_in or 0)
    t_out = int(tokens_out or 0)
    t_total = int(tokens) if tokens is not None else (t_in + t_out if (tokens_in or tokens_out) else 0)

    event = {
        "ts": _now(),
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
    events_path = aisdlc_path(work_root) / EVENTS_FILE
    with events_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    state_path = aisdlc_path(work_root) / STATE_FILE
    state = _load(state_path, {"agents": {}})
    prev = state.setdefault("agents", {}).get(agent, {})
    shown_task = task if task else (prev.get("task") if status in ("done", "error") else "")
    if status == "idle":
        shown_task = ""
    state["agents"][agent] = {
        "status": status,
        "task": shown_task,
        "detail": detail or prev.get("detail") or "",
        "phase": phase or prev.get("phase") or "",
        "workflow": workflow or prev.get("workflow") or "",
        "updated_at": event["ts"],
        "tokens_total": int(prev.get("tokens_total") or 0) + t_total,
        "tokens_in_total": int(prev.get("tokens_in_total") or 0) + t_in,
        "tokens_out_total": int(prev.get("tokens_out_total") or 0) + t_out,
        "last_tokens": t_total,
    }
    state["updated_at"] = event["ts"]
    if workflow:
        state["active_workflow"] = workflow
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if t_total or workflow:
        bench_path = aisdlc_path(work_root) / BENCH_FILE
        bench = _load(bench_path, {"workflows": {}, "agents": {}})
        wf_key = workflow or "_default"
        wf = bench.setdefault("workflows", {}).setdefault(
            wf_key,
            {"tokens_total": 0, "tokens_in": 0, "tokens_out": 0, "events": 0, "agents": {}},
        )
        wf["tokens_total"] = int(wf.get("tokens_total") or 0) + t_total
        wf["tokens_in"] = int(wf.get("tokens_in") or 0) + t_in
        wf["tokens_out"] = int(wf.get("tokens_out") or 0) + t_out
        wf["events"] = int(wf.get("events") or 0) + 1
        wa = wf.setdefault("agents", {}).setdefault(
            agent, {"tokens_total": 0, "tokens_in": 0, "tokens_out": 0, "tasks_done": 0}
        )
        wa["tokens_total"] = int(wa.get("tokens_total") or 0) + t_total
        wa["tokens_in"] = int(wa.get("tokens_in") or 0) + t_in
        wa["tokens_out"] = int(wa.get("tokens_out") or 0) + t_out
        if status == "done":
            wa["tasks_done"] = int(wa.get("tasks_done") or 0) + 1
        ag = bench.setdefault("agents", {}).setdefault(
            agent, {"tokens_total": 0, "tokens_in": 0, "tokens_out": 0, "workflows": {}}
        )
        ag["tokens_total"] = int(ag.get("tokens_total") or 0) + t_total
        ag["tokens_in"] = int(ag.get("tokens_in") or 0) + t_in
        ag["tokens_out"] = int(ag.get("tokens_out") or 0) + t_out
        if workflow:
            ag.setdefault("workflows", {})[workflow] = int(ag.get("workflows", {}).get(workflow) or 0) + t_total
        bench["updated_at"] = event["ts"]
        bench_path.write_text(json.dumps(bench, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return event


def read_events(work_root: Path, *, after_line: int = 0, limit: int = 200) -> tuple[list[dict], int]:
    path = aisdlc_path(work_root) / EVENTS_FILE
    if not path.exists():
        return [], 0
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    slice_ = lines[after_line : after_line + limit]
    out: list[dict] = []
    for line in slice_:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out, after_line + len(slice_)


def read_state(work_root: Path) -> dict:
    return _load(aisdlc_path(work_root) / STATE_FILE, {"agents": {}})


def read_config(work_root: Path) -> dict:
    return _load(aisdlc_path(work_root) / CONFIG_FILE, {})


def read_benchmarks(work_root: Path) -> dict:
    return _load(aisdlc_path(work_root) / BENCH_FILE, {"workflows": {}, "agents": {}})
