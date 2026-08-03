"""Scaffold work folder for cursor | claude hosts."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from ai_sdlc_cli.events import CONFIG_FILE, ensure_aisdlc

PROVIDERS = ("cursor", "claude")

# Paths copied from the workflow repo into the work root
COPY_PATHS = [
    ".cursor",
    "AGENTS.md",
    "docs/memory",
    "docs/retrospective.md",
    "docs/module-deps.md",
]

OPTIONAL_COPY = [
    "HOW_TO_USE.md",
    "docs/plans",
]


def find_repo_root(start: Path | None = None) -> Path | None:
    """Walk up from start (or this package) looking for .cursor/agents."""
    candidates: list[Path] = []
    if start:
        candidates.append(start.resolve())
    # package: cli/ai_sdlc_cli -> repo root is parents[2] when installed from source
    here = Path(__file__).resolve()
    candidates.extend([here.parent, here.parent.parent, here.parent.parent.parent])
    cwd = Path.cwd().resolve()
    candidates.append(cwd)
    for base in candidates:
        for p in [base, *base.parents]:
            if (p / ".cursor" / "agents").is_dir() and (p / "AGENTS.md").exists():
                return p
    return None


def _copytree(src: Path, dst: Path) -> None:
    if src.is_dir():
        if dst.exists():
            # merge: copy missing children
            for child in src.iterdir():
                _copytree(child, dst / child.name)
        else:
            shutil.copytree(src, dst)
    elif src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(src, dst)


def _ensure_memory_stubs(work_root: Path) -> None:
    mem = work_root / "docs" / "memory"
    mem.mkdir(parents=True, exist_ok=True)
    stubs = {
        "decisions.md": "# Decisions\n\n<!-- locked decisions — append dated bullets -->\n",
        "gotchas.md": "# Gotchas\n\n<!-- patterns that failed — append dated bullets -->\n",
        "shortcuts.md": "# Shortcuts\n\n<!-- patterns that worked — append dated bullets -->\n",
    }
    for name, body in stubs.items():
        path = mem / name
        if not path.exists():
            path.write_text(body, encoding="utf-8")
    retro = work_root / "docs" / "retrospective.md"
    if not retro.exists():
        retro.parent.mkdir(parents=True, exist_ok=True)
        retro.write_text("# Retrospective\n\n", encoding="utf-8")
    deps = work_root / "docs" / "module-deps.md"
    if not deps.exists():
        deps.parent.mkdir(parents=True, exist_ok=True)
        deps.write_text("# Module dependencies\n\n| Module | depends_on | status |\n|--------|------------|--------|\n", encoding="utf-8")


def _write_claude_adapter(work_root: Path) -> None:
    claude = work_root / ".claude"
    claude.mkdir(parents=True, exist_ok=True)
    claude_md = claude / "CLAUDE.md"
    if not claude_md.exists():
        claude_md.write_text(
            """# Claude adapter for ai-sdlc-workflow

This workspace was initialized with `ai-sdlc --init claude`.

## Source of truth

- Domain config: `AGENTS.md`
- Agents: `.cursor/agents/*.md`
- Skills: `.cursor/skills/`
- Durable memory: `docs/memory/`
- Runtime events (office UI): `.aisdlc/events.jsonl`

## How to work

1. Read `AGENTS.md` and `docs/memory/*` before planning.
2. Prefer the same phases as Cursor commands:
   - Plan: architect-planner flow in `.cursor/agents/architect-planner.md`
   - Implement: matching `*-worker.md`
   - Review: `judge-agent.md`
3. When finishing a module, append `docs/retrospective.md` and memory facts.
4. Optional: run `ai-sdlc ui` and `ai-sdlc event --agent <id> --status working --task "..."` so the office board stays live.

## Commands (host)

Use your Claude Code / CLI session against this folder. The workflow files under `.cursor/` are shared with Cursor-initialized projects.
""",
            encoding="utf-8",
        )


def init_workspace(
    work_root: Path,
    provider: str,
    *,
    repo_root: Path | None = None,
    force: bool = False,
) -> dict:
    provider = provider.lower().strip()
    if provider not in PROVIDERS:
        raise ValueError(f"provider must be one of {PROVIDERS}, got {provider!r}")

    work_root = work_root.resolve()
    work_root.mkdir(parents=True, exist_ok=True)

    repo = repo_root or find_repo_root(work_root)
    if repo is None:
        raise FileNotFoundError(
            "Could not locate ai-sdlc-workflow repo (need .cursor/agents + AGENTS.md). "
            "Run from a checkout or pass --repo /path/to/ai-sdlc-workflow."
        )

    copied: list[str] = []
    for rel in COPY_PATHS + OPTIONAL_COPY:
        src = repo / rel
        if not src.exists():
            continue
        dst = work_root / rel
        if dst.exists() and not force:
            copied.append(f"{rel} (exists, skipped)")
            continue
        if dst.exists() and force and dst.is_dir():
            shutil.rmtree(dst)
        elif dst.exists() and force and dst.is_file():
            dst.unlink()
        _copytree(src, dst)
        copied.append(rel)

    _ensure_memory_stubs(work_root)
    ensure_aisdlc(work_root)

    if provider == "claude":
        _write_claude_adapter(work_root)

    config = {
        "provider": provider,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repo_source": str(repo),
        "ui_port": 9669,
        "version": "0.1.0",
    }
    cfg_path = work_root / ".aisdlc" / CONFIG_FILE
    cfg_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    # marker for cursor vs claude
    host_file = work_root / ".aisdlc" / f"host-{provider}.json"
    host_file.write_text(
        json.dumps({"host": provider, "ready": True}, indent=2) + "\n",
        encoding="utf-8",
    )

    return {
        "work_root": str(work_root),
        "provider": provider,
        "repo_source": str(repo),
        "copied": copied,
        "ui": f"http://127.0.0.1:{config['ui_port']}",
        "next": [
            f"cd {work_root}",
            "ai-sdlc ui",
            "# open browser at http://127.0.0.1:9669",
            "ai-sdlc demo   # optional: animate agents",
        ],
    }
