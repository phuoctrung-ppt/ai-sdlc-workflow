#!/usr/bin/env python3
"""Generate and load concise .memory/ project memory files from AGENTS.md."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from _lib import detect_root, estimate_tokens, load_json, write_json

MEMORY_DIR = ".memory"
TOKEN_CAPS = {
    "architecture.md": 400,
    "constraints.md": 200,
    "coding-style.md": 150,
    "known-decisions.md": 300,
    "known-issues.md": 150,
}

DOMAIN_MEMORY_MAP: dict[str, list[str]] = {
    "frontend": ["coding-style.md", "constraints.md"],
    "backend": ["constraints.md", "coding-style.md"],
    "database": ["constraints.md"],
    "security": ["constraints.md"],
    "devops": ["constraints.md", "architecture.md"],
    "ai": ["constraints.md", "known-decisions.md"],
    "plan": ["architecture.md", "known-decisions.md", "constraints.md"],
    "review": ["constraints.md"],
    "default": ["constraints.md", "coding-style.md"],
}


def extract_section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*$"
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        return ""

    start = match.end()
    next_heading = re.search(r"^## \d+\.", text[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def truncate_to_tokens(text: str, max_tokens: int) -> str:
    lines = text.splitlines()
    result: list[str] = []
    chars = 0
    cap = max_tokens * 4
    for line in lines:
        if chars + len(line) + 1 > cap:
            result.append("… (truncated — see AGENTS.md or docs/adr/)")
            break
        result.append(line)
        chars += len(line) + 1
    return "\n".join(result)


def sync_memory(root: Path) -> dict[str, str]:
    agents_md = root / "AGENTS.md"
    dev_rules = root / "docs" / "development-rules.md"
    architecture = root / "docs" / "architecture.md"
    adr_dir = root / "docs" / "adr"

    agents_text = agents_md.read_text(encoding="utf-8") if agents_md.exists() else ""
    dev_text = dev_rules.read_text(encoding="utf-8") if dev_rules.exists() else ""

    stack = extract_section(agents_text, "2. Tech Stack (Locked — ADR required to change)")
    structure = extract_section(agents_text, "3. Repository Structure")
    tenancy = extract_section(agents_text, "4. Multi-Tenancy Rules")
    compliance = extract_section(agents_text, "6. Domain-Specific Compliance Requirements")
    forbidden = extract_section(agents_text, "12. Forbidden Patterns (Agents must NEVER do)")

    arch_doc = architecture.read_text(encoding="utf-8") if architecture.exists() else ""
    if not arch_doc.strip():
        arch_doc = f"Workflow monorepo layout:\n{structure[:800]}" if structure else (
            "See AGENTS.md §3 for repository structure."
        )

    adr_summaries: list[str] = []
    if adr_dir.exists():
        for adr in sorted(adr_dir.glob("*.md"))[:10]:
            title = adr.stem
            first_line = adr.read_text(encoding="utf-8").splitlines()[0:3]
            adr_summaries.append(f"- **{title}**: {' '.join(first_line)[:120]}")

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    files = {
        "architecture.md": truncate_to_tokens(
            f"# Architecture (auto-generated {generated_at})\n\n{arch_doc}",
            TOKEN_CAPS["architecture.md"],
        ),
        "constraints.md": truncate_to_tokens(
            f"# Constraints (auto-generated {generated_at})\n\n"
            f"## Stack\n{stack[:600]}\n\n"
            f"## Tenancy\n{tenancy[:400]}\n\n"
            f"## Compliance\n{compliance[:500]}\n\n"
            f"## Forbidden\n{forbidden[:400]}",
            TOKEN_CAPS["constraints.md"],
        ),
        "coding-style.md": truncate_to_tokens(
            f"# Coding Style (auto-generated {generated_at})\n\n"
            f"{dev_text[:400] if dev_text else 'TypeScript strict; services not controllers; migrations only; structured logging.'}",
            TOKEN_CAPS["coding-style.md"],
        ),
        "known-decisions.md": truncate_to_tokens(
            f"# Known Decisions (auto-generated {generated_at})\n\n"
            + ("\n".join(adr_summaries) if adr_summaries else "- No ADRs yet — see docs/adr/"),
            TOKEN_CAPS["known-decisions.md"],
        ),
        "known-issues.md": truncate_to_tokens(
            f"# Known Issues (auto-generated {generated_at})\n\n"
            "- AGENTS.md may contain `<PLACEHOLDER>` values until project is ported.\n"
            "- Run `memory-loader.py --sync` after AGENTS.md or ADR updates.",
            TOKEN_CAPS["known-issues.md"],
        ),
    }

    memory_root = root / MEMORY_DIR
    memory_root.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (memory_root / name).write_text(content + "\n", encoding="utf-8")

    return files


def select_memory_files(domains: list[str], phase: str) -> list[str]:
    if phase in {"plan", "brainstorm", "dev-module"}:
        keys = DOMAIN_MEMORY_MAP["plan"]
    elif phase == "review":
        keys = DOMAIN_MEMORY_MAP["review"]
    elif domains:
        keys: list[str] = []
        for domain in domains[:2]:
            keys.extend(DOMAIN_MEMORY_MAP.get(domain, []))
        if not keys:
            keys = DOMAIN_MEMORY_MAP["default"]
    else:
        keys = DOMAIN_MEMORY_MAP["default"]

    seen: set[str] = set()
    ordered: list[str] = []
    for key in keys:
        if key not in seen:
            seen.add(key)
            ordered.append(key)
    return ordered[:3]


def load_memory(root: Path, domains: list[str], phase: str) -> dict:
    memory_root = root / MEMORY_DIR
    if not memory_root.exists() or not any(memory_root.glob("*.md")):
        sync_memory(root)

    selected = select_memory_files(domains, phase)
    items = []
    total_tokens = 0
    for name in selected:
        path = memory_root / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        tokens = estimate_tokens(text)
        total_tokens += tokens
        items.append({
            "file": f"{MEMORY_DIR}/{name}",
            "path": str(path.relative_to(root)),
            "estimatedTokens": tokens,
        })

    return {"files": items, "estimatedTokens": total_tokens}


def main() -> None:
    parser = argparse.ArgumentParser(description="Project memory loader")
    parser.add_argument("--sync", action="store_true", help="Regenerate .memory/ from AGENTS.md")
    parser.add_argument("--select", action="store_true", help="Select memory for intent JSON")
    parser.add_argument("--domains", default="", help="Comma-separated domains")
    parser.add_argument("--phase", default="implement-backend")
    parser.add_argument("--root", default="")
    args = parser.parse_args()

    root = detect_root(args.root or None)

    if args.sync:
        files = sync_memory(root)
        print(json.dumps({"synced": list(files.keys()), "dir": str(root / MEMORY_DIR)}, indent=2))
        return

    if args.select:
        domains = [d.strip() for d in args.domains.split(",") if d.strip()]
        print(json.dumps(load_memory(root, domains, args.phase), indent=2))
        return

    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
