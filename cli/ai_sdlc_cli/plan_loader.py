"""Load active plan + rough task list for the office warehouse."""

from __future__ import annotations

import re
from pathlib import Path


def _read_active_pointer(work_root: Path) -> Path | None:
    pointer = work_root / "docs" / "plans" / ".active-plan"
    if pointer.is_file():
        text = pointer.read_text(encoding="utf-8", errors="replace").strip()
        if text:
            # may be relative path or absolute
            p = Path(text)
            if not p.is_file():
                p = work_root / text
            if p.is_file():
                return p
    plans = work_root / "docs" / "plans"
    if not plans.is_dir():
        return None
    md = sorted(plans.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    return md[0] if md else None


def _parse_tasks(text: str) -> list[dict]:
    """Extract task-ish lines from plan markdown."""
    tasks: list[dict] = []
    # ### Task N — title  or - **Owner:** agent
    task_blocks = re.split(r"\n(?=###\s+Task\b)", text, flags=re.I)
    for block in task_blocks:
        m = re.match(r"###\s+Task\s*(\d+)?\s*[—\-:]?\s*(.+)", block.strip(), re.I)
        if not m:
            continue
        title_line = m.group(2).strip()
        title = re.sub(r"\[CERTAIN\]|\[UNCERTAIN\]", "", title_line, flags=re.I).strip()
        owner_m = re.search(r"\*\*Owner:\*\*\s*`?([\w\-]+)`?", block, re.I)
        owner = owner_m.group(1) if owner_m else ""
        status = "pending"
        if re.search(r"done|complete|✅", block, re.I):
            status = "done"
        tasks.append(
            {
                "id": m.group(1) or str(len(tasks) + 1),
                "title": title[:120],
                "owner": owner,
                "status": status,
            }
        )

    if tasks:
        return tasks

    # fallback: bullet lines under Execution / Task
    for line in text.splitlines():
        if re.match(r"^\s*[-*]\s+\*\*Task", line, re.I) or re.match(
            r"^\s*[-*]\s+Task\s+\d+", line, re.I
        ):
            tasks.append(
                {
                    "id": str(len(tasks) + 1),
                    "title": re.sub(r"^\s*[-*]\s+", "", line).strip()[:120],
                    "owner": "",
                    "status": "pending",
                }
            )
    return tasks[:40]


def load_active_plan(work_root: Path) -> dict:
    path = _read_active_pointer(work_root)
    if not path:
        return {
            "path": None,
            "name": None,
            "goal": None,
            "tasks": [],
            "raw_excerpt": "",
        }
    text = path.read_text(encoding="utf-8", errors="replace")
    goal_m = re.search(r"\*\*Goal:\*\*\s*(.+)", text)
    title_m = re.search(r"^#\s+(.+)$", text, re.M)
    tasks = _parse_tasks(text)
    return {
        "path": str(path.relative_to(work_root)) if path.is_relative_to(work_root) else str(path),
        "name": (title_m.group(1).strip() if title_m else path.stem)[:80],
        "goal": (goal_m.group(1).strip() if goal_m else "")[:200],
        "tasks": tasks,
        "raw_excerpt": text[:1500],
    }
