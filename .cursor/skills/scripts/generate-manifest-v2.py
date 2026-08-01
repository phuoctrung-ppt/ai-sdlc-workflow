#!/usr/bin/env python3
"""Enrich / rewrite skills-manifest.v2.json (canonical skill manifest).

V1 skills-manifest.json is retired. This script re-estimates tokens and rebuilds
lazy `references` metadata in place on skills-manifest.v2.json.

Usage:
  python3 .cursor/skills/scripts/generate-manifest-v2.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILLS_DIR = ROOT / ".cursor" / "skills"
MANIFEST_V2 = SKILLS_DIR / "skills-manifest.v2.json"

DEFAULT_TOKENS = {
    "agentic-workflow": 600,
    "security": 800,
    "taste-design": 1200,
    "frontend-skills": 900,
    "databases": 1000,
    "databases-mongodb": 800,
    "testing-qa": 700,
    "docker-devops": 600,
    "nestjs-skills": 2500,
    "zod-shared-types": 500,
    "ai-llm-integration": 800,
    "bullmq-worker": 600,
    "planning": 700,
}

DEFAULT_PRIORITY = {
    "agentic-workflow": 20,
    "planning": 15,
    "security": 12,
    "nestjs-skills": 10,
    "frontend-skills": 10,
    "databases": 10,
    "databases-mongodb": 7,
    "testing-qa": 8,
    "taste-design": 8,
    "docker-devops": 6,
    "zod-shared-types": 7,
    "ai-llm-integration": 7,
    "bullmq-worker": 6,
}

# Fields copied through enrich unchanged when present
PASS_THROUGH = (
    "optional",
    "activateWhen",
    "note",
    "domainTag",
    "portable",
    "phases",
    "agents",
    "keywords",
    "refKeywords",
    "scripts",
    "entry",
    "referencesDir",
    "consolidation",
)


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
    enriched["references"] = {
        "lazy": True,
        "optional": [
            {"path": k, "triggers": v}
            for k, v in skill.get("refKeywords", {}).items()
        ],
    }
    if skill.get("refKeywords") and not skill.get("consolidation"):
        enriched["consolidation"] = {
            "v1ReferencesDir": skill.get("referencesDir", ""),
            "note": "Load via tier4 --expand-ref only",
        }
    return enriched


def main() -> None:
    if not MANIFEST_V2.exists():
        sys.exit(f"error: canonical manifest missing: {MANIFEST_V2}")

    manifest = json.loads(MANIFEST_V2.read_text(encoding="utf-8"))

    description = manifest.get("description", "")
    if "(V2: token budgets + lazy refs)" not in description:
        description = description.rstrip() + " (V2: token budgets + lazy refs)"

    out = {
        "manifestSchema": "2.0",
        "version": manifest.get("version", "4.0"),
        "description": description,
        "skillsRoot": manifest.get("skillsRoot", ".cursor/skills"),
        "phases": manifest.get("phases", []),
        "agents": manifest.get("agents", []),
        "defaultTokenBudget": manifest.get("defaultTokenBudget", 8000),
        "tierCeilings": manifest.get(
            "tierCeilings",
            {"tier1": 1200, "tier2": 4000, "tier3": 800, "tier4": 2000},
        ),
        "maxSkillsByComplexity": manifest.get(
            "maxSkillsByComplexity",
            {"low": 1, "medium": 2, "high": 4},
        ),
        "portableSkills": [enrich_skill(s) for s in manifest.get("portableSkills", [])],
        "skills": [enrich_skill(s) for s in manifest.get("skills", [])],
    }

    if "_commentPortableVsOptional" in manifest:
        # Keep comment near top after description
        ordered = {
            "manifestSchema": out["manifestSchema"],
            "version": out["version"],
            "description": out["description"],
            "_commentPortableVsOptional": manifest["_commentPortableVsOptional"],
        }
        for key, value in out.items():
            if key not in ordered:
                ordered[key] = value
        out = ordered

    MANIFEST_V2.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {MANIFEST_V2.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
