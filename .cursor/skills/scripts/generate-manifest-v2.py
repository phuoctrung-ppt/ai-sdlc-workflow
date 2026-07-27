#!/usr/bin/env python3
"""Generate skills-manifest.v2.json from skills-manifest.json with token metadata."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILLS_DIR = ROOT / ".cursor" / "skills"

DEFAULT_TOKENS = {
    "agentic-workflow": 600,
    "security": 800,
    "taste-design": 1200,
    "frontend-skills": 900,
    "databases": 1000,
    "testing-qa": 700,
    "docker-devops": 600,
    "nestjs-skills": 2500,
    "zod-shared-types": 500,
    "ai-llm-integration": 800,
    "admin-service": 700,
    "bullmq-worker": 600,
    "planning": 700,
    "nestjs-scaffold": 2500,
}

DEFAULT_PRIORITY = {
    "agentic-workflow": 20,
    "planning": 15,
    "security": 12,
    "nestjs-skills": 10,
    "frontend-skills": 10,
    "databases": 10,
    "testing-qa": 8,
    "taste-design": 8,
    "docker-devops": 6,
    "zod-shared-types": 7,
    "ai-llm-integration": 7,
    "admin-service": 6,
    "bullmq-worker": 6,
    "nestjs-scaffold": 9,
}


def estimate_file_tokens(path: Path) -> int:
    if not path.exists():
        return DEFAULT_TOKENS.get(path.parent.name, 800)
    return max(100, len(path.read_text(encoding="utf-8")) // 4)


def enrich_skill(skill: dict) -> dict:
    sid = skill["id"]
    entry = SKILLS_DIR / skill["entry"]
    enriched = dict(skill)
    enriched["manifestSchema"] = "2.0"
    enriched["priority"] = skill.get("priority", DEFAULT_PRIORITY.get(sid, 5))
    enriched["estimatedTokens"] = skill.get(
        "estimatedTokens",
        estimate_file_tokens(entry) if entry.exists() else DEFAULT_TOKENS.get(sid, 800),
    )
    enriched["references"] = skill.get("references", {
        "lazy": True,
        "optional": [
            {"path": k, "triggers": v}
            for k, v in skill.get("refKeywords", {}).items()
        ],
    })
    if "refKeywords" in enriched and enriched.get("references", {}).get("lazy"):
        enriched.setdefault("consolidation", {
            "v1ReferencesDir": skill.get("referencesDir", ""),
            "note": "Load via tier4 --expand-ref only",
        })
    return enriched


def main() -> None:
    src = SKILLS_DIR / "skills-manifest.json"
    dst = SKILLS_DIR / "skills-manifest.v2.json"
    manifest = json.loads(src.read_text(encoding="utf-8"))

    out = {
        "manifestSchema": "2.0",
        "version": manifest.get("version", "4.0"),
        "description": manifest.get("description", "") + " (V2: token budgets + lazy refs)",
        "skillsRoot": manifest.get("skillsRoot", ".cursor/skills"),
        "phases": manifest.get("phases", []),
        "agents": manifest.get("agents", []),
        "defaultTokenBudget": 8000,
        "tierCeilings": {
            "tier1": 1200,
            "tier2": 4000,
            "tier3": 800,
            "tier4": 2000,
        },
        "maxSkillsByComplexity": {
            "low": 1,
            "medium": 2,
            "high": 4,
        },
        "portableSkills": [enrich_skill(s) for s in manifest.get("portableSkills", [])],
        "skills": [enrich_skill(s) for s in manifest.get("skills", [])],
    }

    dst.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {dst.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
