#!/usr/bin/env python3
"""Resolve AGENTS.md §0 project profile → active-layers.json.

Layer off ⇒ agents/skills for that layer are not active.
Missing §0 + no --detect ⇒ keep all-layers-on defaults (backward compatible).
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from _lib import detect_root, load_json, write_json

LAYER_KEYS = [
    "frontend",
    "backend",
    "database",
    "multi-tenancy",
    "queue",
    "auth",
    "devops",
    "ai-llm",
]

LAYER_AGENTS = {
    "frontend": ["frontend-worker", "designer-worker"],
    "backend": ["backend-worker", "contract-agent"],
    "database": ["database-worker"],
    "multi-tenancy": [],
    "queue": [],
    "auth": ["security-worker"],
    "devops": ["devops-worker"],
    "ai-llm": ["ai-worker"],
}

LAYER_SKILLS = {
    "frontend": ["frontend-skills", "saas-product-ui", "taste-design"],
    "backend": ["api-contract-first"],
    "database": ["databases"],
    "multi-tenancy": [],
    "queue": [],
    "auth": ["security"],
    "devops": ["docker-devops"],
    "ai-llm": [],
}

ALWAYS_ON_AGENTS = [
    "architect-planner",
    "judge-agent",
    "qa-worker",
    "scaffold-agent",
    "spike-agent",
    "learning-agent",
]

ALWAYS_ON_SKILLS = [
    "agentic-workflow",
    "planning",
    "error-recovery",
    "incremental-commit",
    "testing-qa",
    "skill-updater",
]

PROFILE_LAYER_PRESETS = {
    "frontend": {
        "frontend": True,
        "backend": False,
        "database": False,
        "multi-tenancy": False,
        "queue": False,
        "auth": False,
        "devops": False,
        "ai-llm": False,
    },
    "backend": {
        "frontend": False,
        "backend": True,
        "database": True,
        "multi-tenancy": False,
        "queue": False,
        "auth": True,
        "devops": False,
        "ai-llm": False,
    },
    "fullstack": {
        "frontend": True,
        "backend": True,
        "database": True,
        "multi-tenancy": False,
        "queue": False,
        "auth": True,
        "devops": True,
        "ai-llm": False,
    },
    "library": {
        "frontend": False,
        "backend": False,
        "database": False,
        "multi-tenancy": False,
        "queue": False,
        "auth": False,
        "devops": False,
        "ai-llm": False,
    },
    "cli": {
        "frontend": False,
        "backend": True,
        "database": False,
        "multi-tenancy": False,
        "queue": False,
        "auth": False,
        "devops": False,
        "ai-llm": False,
    },
}


def _truthy(val: str) -> bool:
    v = val.strip().lower()
    return v in ("on", "true", "yes", "1", "enabled")


def parse_agents_profile(agents_text: str) -> dict | None:
    """Parse §0 from AGENTS.md. Returns None if section missing."""
    if not re.search(r"##\s*0\.\s*Project Profile", agents_text, re.I):
        return None

    # Slice from §0 to next ## heading
    m = re.search(
        r"##\s*0\.\s*Project Profile(.*?)(?=\n##\s+\d+\.|\Z)",
        agents_text,
        re.I | re.S,
    )
    block = m.group(1) if m else agents_text

    profile = "fullstack"
    layout = "single-package"
    pm = re.search(r"\|\s*\*\*profile\*\*\s*\|\s*`?([^|`]+)`?\s*\|", block, re.I)
    if pm:
        profile = pm.group(1).strip().lower()
    lm = re.search(r"\|\s*\*\*layout\*\*\s*\|\s*`?([^|`]+)`?\s*\|", block, re.I)
    if lm:
        layout = lm.group(1).strip().lower()

    layers = dict(PROFILE_LAYER_PRESETS.get(profile, PROFILE_LAYER_PRESETS["fullstack"]))

    # Per-row layer table: | frontend | on |
    for key in LAYER_KEYS:
        row = re.search(
            rf"\|\s*{re.escape(key)}\s*\|\s*([^|]+)\|",
            block,
            re.I,
        )
        if row:
            layers[key] = _truthy(row.group(1))

    return {"profile": profile, "layout": layout, "layers": layers, "source": "AGENTS.md#§0"}


def detect_profile(root: Path) -> dict:
    """Filesystem heuristics — suggestion only."""
    layers = {k: False for k in LAYER_KEYS}
    layout = "single-package"

    if (root / "pnpm-workspace.yaml").exists() or (root / "nx.json").exists() or (root / "turbo.json").exists():
        layout = "monorepo"

    fe_hits = any(
        (root / p).exists()
        for p in ("app", "pages", "components", "src/app", "src/components", "web", "frontend")
    )
    # crude tsx presence
    if not fe_hits:
        for p in root.rglob("*.tsx"):
            if ".cursor" in p.parts or "node_modules" in p.parts:
                continue
            fe_hits = True
            break

    be_hits = any(
        (root / p).exists()
        for p in ("api", "server", "backend", "src/server", "apps/api")
    )
    db_hits = any(
        (root / p).exists()
        for p in ("migrations", "prisma", "drizzle", "database", "db")
    ) or list(root.rglob("**/migrations/**"))[:1]

    if fe_hits:
        layers["frontend"] = True
    if be_hits:
        layers["backend"] = True
    if db_hits:
        layers["database"] = True
        layers["backend"] = True

    if layers["frontend"] and layers["backend"]:
        profile = "fullstack"
    elif layers["frontend"]:
        profile = "frontend"
    elif layers["backend"]:
        profile = "backend"
    else:
        profile = "library"

    # auth/devops soft signals
    if list(root.rglob("**/auth/**"))[:1] or list(root.rglob("**/*guard*"))[:1]:
        layers["auth"] = True
    if (root / "Dockerfile").exists() or (root / ".github" / "workflows").exists():
        layers["devops"] = True

    return {
        "profile": profile,
        "layout": layout,
        "layers": layers,
        "source": "detect",
    }


def build_active_payload(resolved: dict) -> dict:
    layers = resolved["layers"]
    agents: list[str] = list(ALWAYS_ON_AGENTS)
    skills: list[str] = list(ALWAYS_ON_SKILLS)
    plan_sections: dict[str, bool] = {}

    for key in LAYER_KEYS:
        on = bool(layers.get(key))
        plan_sections[key] = on
        if not on:
            continue
        for a in LAYER_AGENTS.get(key, []):
            if a not in agents:
                agents.append(a)
        for s in LAYER_SKILLS.get(key, []):
            if s not in skills:
                skills.append(s)

    return {
        "schemaVersion": 1,
        "description": "GENERATED by profile-sync.py — do not hand-edit.",
        "profile": resolved["profile"],
        "layout": resolved.get("layout", "single-package"),
        "layers": {k: bool(layers.get(k)) for k in LAYER_KEYS},
        "alwaysOnAgents": ALWAYS_ON_AGENTS,
        "alwaysOnSkills": ALWAYS_ON_SKILLS,
        "activeAgents": agents,
        "activeSkills": skills,
        "planSections": plan_sections,
        "source": resolved.get("source", "unknown"),
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "note": "Layer off → planners must not inject that layer into plans/sync.",
    }


def load_active_layers(root: Path) -> dict | None:
    path = root / ".cursor" / "config" / "active-layers.json"
    if not path.exists():
        return None
    try:
        return load_json(path)
    except Exception:
        return None


def filter_agents(candidates: list[str], active: dict | None) -> list[str]:
    if not active:
        return candidates
    allowed = set(active.get("activeAgents") or [])
    if not allowed:
        return candidates
    return [a for a in candidates if a in allowed]


def filter_skill_ids(skill_ids: list[str], active: dict | None) -> list[str]:
    if not active:
        return skill_ids
    allowed = set(active.get("activeSkills") or [])
    if not allowed:
        return skill_ids
    return [s for s in skill_ids if s in allowed]


def run_sync(root: Path, mode: str) -> dict:
    agents_path = root / "AGENTS.md"
    resolved = None

    if mode == "from-agents":
        if not agents_path.exists():
            raise SystemExit(f"error: AGENTS.md not found at {agents_path}")
        text = agents_path.read_text(encoding="utf-8")
        resolved = parse_agents_profile(text)
        if resolved is None:
            raise SystemExit(
                "error: AGENTS.md has no '## 0. Project Profile' section.\n"
                "Add §0 (see template) or run: python3 .cursor/context/profile-sync.py --detect"
            )
    elif mode == "detect":
        resolved = detect_profile(root)
    else:
        raise SystemExit(f"error: unknown mode {mode}")

    payload = build_active_payload(resolved)
    out = root / ".cursor" / "config" / "active-layers.json"
    write_json(out, payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync active-layers.json from AGENTS.md §0")
    parser.add_argument("--from-agents", action="store_true", help="Parse AGENTS.md §0")
    parser.add_argument("--detect", action="store_true", help="Filesystem heuristics")
    parser.add_argument("--root", default="", help="Project root")
    parser.add_argument("--print", action="store_true", help="Print JSON only")
    args = parser.parse_args()

    root = detect_root(args.root or None)

    if args.from_agents:
        mode = "from-agents"
    elif args.detect:
        mode = "detect"
    else:
        sys.exit("error: specify --from-agents or --detect")

    payload = run_sync(root, mode)
    if args.print:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Wrote .cursor/config/active-layers.json")
        print(f"  profile: {payload['profile']}")
        print(f"  layout:  {payload['layout']}")
        on = [k for k, v in payload["layers"].items() if v]
        off = [k for k, v in payload["layers"].items() if not v]
        print(f"  layers on:  {', '.join(on) or '(none)'}")
        print(f"  layers off: {', '.join(off) or '(none)'}")
        print(f"  agents: {len(payload['activeAgents'])}  skills: {len(payload['activeSkills'])}")


if __name__ == "__main__":
    main()
