"""Shared utilities for Workflow V2 context orchestration."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

STOP_WORDS = {
    "a", "an", "and", "are", "as", "be", "by", "for", "from", "in", "into",
    "is", "it", "of", "on", "or", "the", "to", "use", "using", "when", "with",
    "build", "create", "add", "make", "new", "page", "app", "fix", "update",
}


def detect_root(explicit_root: str | None = None) -> Path:
    if explicit_root:
        return Path(explicit_root).resolve()
    try:
        git_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return Path(git_root).resolve()
    except Exception:
        return Path.cwd().resolve()


def tokenize(text: str) -> set[str]:
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9+-]*", text.lower())
    return {t.replace("_", "-") for t in tokens if t not in STOP_WORDS}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def estimate_tokens(text: str) -> int:
    """Rough token estimate (~4 chars per token for English prose)."""
    return max(1, len(text) // 4)


def read_text_if_exists(path: Path) -> str | None:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return None
