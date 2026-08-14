#!/usr/bin/env python3
"""Validate and optionally append a skill entry to skills-manifest.v2.json.

Used by /skill-scout-apply after human APPROVE. Does not write SKILL.md body.

Usage:
  # Validate only
  python3 .cursor/skills/scripts/manifest-register.py --dry-run \
    --id python-pytest --entry python-pytest/SKILL.md \
    --phases test,fix,implement-backend \
    --agents qa-worker,backend-worker \
    --keywords pytest,fixture,parametrize,unit,python \
    --priority 8 --estimated-tokens 900 \
    --note "Ingested via skill-scout"

  # Append (fails if id exists)
  python3 .cursor/skills/scripts/manifest-register.py ...   # same flags without --dry-run

  # Allow replace existing id
  python3 .cursor/skills/scripts/manifest-register.py ... --replace
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / ".cursor" / "skills" / "skills-manifest.v2.json"

CORE_PRIORITY_FLOOR = 12  # scout must not meet or exceed without --force-priority
SCOUT_PRIORITY_MAX = 10


def load_manifest() -> dict:
    if not MANIFEST.exists():
        sys.exit(f"error: missing {MANIFEST}")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def all_skill_ids(manifest: dict) -> set[str]:
    ids = {s["id"] for s in manifest.get("portableSkills", [])}
    ids |= {s["id"] for s in manifest.get("skills", [])}
    return ids


def validate(
    manifest: dict,
    *,
    skill_id: str,
    entry: str,
    phases: list[str],
    agents: list[str],
    keywords: list[str],
    priority: int,
    force_priority: bool,
    replace: bool,
) -> list[str]:
    errors: list[str] = []
    known_phases = set(manifest.get("phases", []))
    known_agents = set(manifest.get("agents", []))

    if not skill_id or skill_id != skill_id.lower() or " " in skill_id:
        errors.append("id must be non-empty kebab-case lowercase")

    if not entry.endswith("SKILL.md"):
        errors.append("entry must end with SKILL.md")

    entry_path = ROOT / ".cursor" / "skills" / entry
    if not entry_path.exists():
        errors.append(f"entry file not found: {entry_path.relative_to(ROOT)} (write SKILL.md first)")

    bad_phases = [p for p in phases if p not in known_phases]
    if bad_phases:
        errors.append(f"unknown phases: {bad_phases}; valid={sorted(known_phases)}")
    if not phases:
        errors.append("phases must be non-empty")

    bad_agents = [a for a in agents if a not in known_agents]
    if bad_agents:
        errors.append(f"unknown agents: {bad_agents}; valid={sorted(known_agents)}")
    if not agents:
        errors.append("agents must be non-empty")

    if len(keywords) < 2:
        errors.append("keywords: need ≥2 specific terms (avoid a single generic token)")
    generic_only = {"test", "code", "build", "fix", "app"}
    if keywords and set(k.lower() for k in keywords) <= generic_only:
        errors.append("keywords too generic; add stack/practice nouns")

    if priority >= CORE_PRIORITY_FLOOR and not force_priority:
        errors.append(
            f"priority {priority} ≥ {CORE_PRIORITY_FLOOR} reserved for core skills; "
            f"use ≤{SCOUT_PRIORITY_MAX} or pass --force-priority"
        )
    if priority > SCOUT_PRIORITY_MAX and not force_priority:
        errors.append(
            f"scout default ceiling is {SCOUT_PRIORITY_MAX}; pass --force-priority to override"
        )

    exists = skill_id in all_skill_ids(manifest)
    if exists and not replace:
        errors.append(f"id '{skill_id}' already in manifest; pass --replace to overwrite entry")

    return errors


def build_entry(args: argparse.Namespace) -> dict:
    entry: dict = {
        "id": args.id,
        "portable": not args.not_portable,
        "note": args.note or f"Ingested via skill-scout",
        "entry": args.entry,
        "phases": args.phases,
        "agents": args.agents,
        "keywords": args.keywords,
        "manifestSchema": "2.0",
        "priority": args.priority,
        "estimatedTokens": args.estimated_tokens,
    }
    if args.references_dir:
        entry["referencesDir"] = args.references_dir
    return entry


def upsert(manifest: dict, skill: dict, replace: bool) -> None:
    sid = skill["id"]
    for bucket in ("portableSkills", "skills"):
        arr = manifest.get(bucket, [])
        for i, existing in enumerate(arr):
            if existing.get("id") == sid:
                if not replace:
                    sys.exit(f"error: id exists in {bucket}")
                arr[i] = skill
                manifest[bucket] = arr
                return
    manifest.setdefault("skills", []).append(skill)


def main() -> None:
    p = argparse.ArgumentParser(description="Register skill in skills-manifest.v2.json")
    p.add_argument("--id", required=True)
    p.add_argument("--entry", required=True, help="Relative to .cursor/skills/")
    p.add_argument("--phases", required=True, help="Comma-separated")
    p.add_argument("--agents", required=True, help="Comma-separated")
    p.add_argument("--keywords", required=True, help="Comma-separated")
    p.add_argument("--priority", type=int, default=8)
    p.add_argument("--estimated-tokens", type=int, default=800)
    p.add_argument("--references-dir", default="")
    p.add_argument("--note", default="")
    p.add_argument("--not-portable", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--replace", action="store_true")
    p.add_argument("--force-priority", action="store_true")
    args = p.parse_args()

    args.phases = [x.strip() for x in args.phases.split(",") if x.strip()]
    args.agents = [x.strip() for x in args.agents.split(",") if x.strip()]
    args.keywords = [x.strip() for x in args.keywords.split(",") if x.strip()]

    manifest = load_manifest()
    errors = validate(
        manifest,
        skill_id=args.id,
        entry=args.entry,
        phases=args.phases,
        agents=args.agents,
        keywords=args.keywords,
        priority=args.priority,
        force_priority=args.force_priority,
        replace=args.replace,
    )
    if errors:
        print("validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    skill = build_entry(args)
    print(json.dumps({"ok": True, "dry_run": args.dry_run, "entry": skill}, indent=2))

    if args.dry_run:
        print("dry-run: manifest not written", file=sys.stderr)
        return

    upsert(manifest, skill, replace=args.replace)
    note = manifest.get("_note", "")
    if "skill-scout" not in note.lower():
        manifest["_note"] = (note + " | manifest-register used for scout ingest").strip(" |")
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
