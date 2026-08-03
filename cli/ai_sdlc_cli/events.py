"""Append-only event log + state snapshot for the office UI."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

AISDLC_DIR = ".aisdlc"
EVENTS_FILE = "events.jsonl"
STATE_FILE = "state.json"
CONFIG_FILE = "config.json"


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


def emit_event(
    work_root: Path,
    *,
    agent: str,
    status: str,
    task: str = "",
    detail: str = "",
    phase: str = "",
) -> dict[str, Any]:
    ensure_aisdlc(work_root)
    event = {
        "ts": _now(),
        "agent": agent,
        "status": status,  # idle | working | waiting | done | error
        "task": task,
        "detail": detail,
        "phase": phase,
    }
    events_path = aisdlc_path(work_root) / EVENTS_FILE
    with events_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    state_path = aisdlc_path(work_root) / STATE_FILE
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        state = {"agents": {}}
    agents = state.setdefault("agents", {})
    agents[agent] = {
        "status": status,
        "task": task,
        "detail": detail,
        "phase": phase,
        "updated_at": event["ts"],
    }
    state["updated_at"] = event["ts"]
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
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
    path = aisdlc_path(work_root) / STATE_FILE
    if not path.exists():
        return {"agents": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"agents": {}}


def read_config(work_root: Path) -> dict:
    path = aisdlc_path(work_root) / CONFIG_FILE
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
