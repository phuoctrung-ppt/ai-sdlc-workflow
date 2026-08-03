"""Discover agent roster from .cursor/agents/*.md."""

from __future__ import annotations

import re
from pathlib import Path

# Fallback roster if agents dir missing
DEFAULT_AGENTS: list[dict] = [
    {"id": "architect-planner", "role": "Planner", "emoji": "📐", "desk": "north"},
    {"id": "designer-worker", "role": "Design", "emoji": "🎨", "desk": "north"},
    {"id": "frontend-worker", "role": "Frontend", "emoji": "🖥️", "desk": "east"},
    {"id": "backend-worker", "role": "Backend", "emoji": "⚙️", "desk": "east"},
    {"id": "database-worker", "role": "Database", "emoji": "🗄️", "desk": "south"},
    {"id": "qa-worker", "role": "QA", "emoji": "🧪", "desk": "south"},
    {"id": "security-worker", "role": "Security", "emoji": "🔒", "desk": "west"},
    {"id": "devops-worker", "role": "DevOps", "emoji": "🚀", "desk": "west"},
    {"id": "judge-agent", "role": "Judge", "emoji": "⚖️", "desk": "center"},
    {"id": "learning-agent", "role": "Learning", "emoji": "🧠", "desk": "center"},
    {"id": "scaffold-agent", "role": "Scaffold", "emoji": "🏗️", "desk": "north"},
    {"id": "spike-agent", "role": "Spike", "emoji": "🔬", "desk": "south"},
    {"id": "contract-agent", "role": "Contract", "emoji": "📜", "desk": "east"},
]

ROLE_HINTS = {
    "architect": ("Planner", "📐", "north"),
    "designer": ("Design", "🎨", "north"),
    "frontend": ("Frontend", "🖥️", "east"),
    "backend": ("Backend", "⚙️", "east"),
    "database": ("Database", "🗄️", "south"),
    "qa": ("QA", "🧪", "south"),
    "security": ("Security", "🔒", "west"),
    "devops": ("DevOps", "🚀", "west"),
    "judge": ("Judge", "⚖️", "center"),
    "learning": ("Learning", "🧠", "center"),
    "scaffold": ("Scaffold", "🏗️", "north"),
    "spike": ("Spike", "🔬", "south"),
    "contract": ("Contract", "📜", "east"),
}


def _hint(agent_id: str) -> tuple[str, str, str]:
    low = agent_id.lower()
    for key, val in ROLE_HINTS.items():
        if key in low:
            return val
    return ("Agent", "🤖", "center")


def discover_agents(work_root: Path) -> list[dict]:
    agents_dir = work_root / ".cursor" / "agents"
    if not agents_dir.is_dir():
        return [dict(a) for a in DEFAULT_AGENTS]

    found: list[dict] = []
    for path in sorted(agents_dir.glob("*.md")):
        agent_id = path.stem
        text = path.read_text(encoding="utf-8", errors="replace")[:2000]
        role, emoji, desk = _hint(agent_id)
        m = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
        desc = m.group(1).strip() if m else role
        found.append(
            {
                "id": agent_id,
                "role": role,
                "emoji": emoji,
                "desk": desk,
                "description": desc[:120],
            }
        )
    return found or [dict(a) for a in DEFAULT_AGENTS]
