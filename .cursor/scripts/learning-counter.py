#!/usr/bin/env python3
"""Tiny learning counter API — do NOT cat workflow-state.json into agent context.

Only these keys are touched:
  modulesSinceLastProposal, lastModuleCompleted,
  lastSkillProposalPath, lastSkillProposalAt

Guard fields (editedFiles, events, …) are preserved untouched.

Usage:
  python3 .cursor/scripts/learning-counter.py get
  python3 .cursor/scripts/learning-counter.py inc --module payments
  python3 .cursor/scripts/learning-counter.py reset --proposal docs/reviews/2026-08-03-skill-update-proposal.md
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / ".cursor" / "state" / "workflow-state.json"

LEARNING_KEYS = {
    "modulesSinceLastProposal",
    "lastModuleCompleted",
    "lastSkillProposalPath",
    "lastSkillProposalAt",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load() -> dict:
    if not STATE.exists():
        return {
            "schemaVersion": 1,
            "modulesSinceLastProposal": 0,
            "lastSkillProposalPath": None,
            "lastSkillProposalAt": None,
            "lastModuleCompleted": None,
            "editedFiles": [],
            "stopBlockCount": 0,
            "overrides": [],
            "events": [],
        }
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"modulesSinceLastProposal": 0}


def _save(data: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cmd_get(_: argparse.Namespace) -> int:
    s = _load()
    n = int(s.get("modulesSinceLastProposal") or 0)
    # One compact line for agent context — not the whole file
    out = {
        "modulesSinceLastProposal": n,
        "lastModuleCompleted": s.get("lastModuleCompleted"),
        "fullPassRecommended": n >= 5,
        "lastSkillProposalPath": s.get("lastSkillProposalPath"),
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


def cmd_inc(args: argparse.Namespace) -> int:
    s = _load()
    n = int(s.get("modulesSinceLastProposal") or 0) + 1
    s["modulesSinceLastProposal"] = n
    if args.module:
        s["lastModuleCompleted"] = args.module
    _save(s)
    print(json.dumps({"modulesSinceLastProposal": n, "fullPassRecommended": n >= 5}, ensure_ascii=False))
    return 0


def cmd_reset(args: argparse.Namespace) -> int:
    s = _load()
    s["modulesSinceLastProposal"] = 0
    if args.proposal:
        s["lastSkillProposalPath"] = args.proposal
        s["lastSkillProposalAt"] = _now()
    _save(s)
    print(json.dumps({"modulesSinceLastProposal": 0, "reset": True}, ensure_ascii=False))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Learning counter (workflow-state learning keys only)")
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("get", help="Print compact counter JSON (safe for agent context)")
    g.set_defaults(func=cmd_get)

    i = sub.add_parser("inc", help="Increment modulesSinceLastProposal after module done")
    i.add_argument("--module", default=None)
    i.set_defaults(func=cmd_inc)

    r = sub.add_parser("reset", help="Reset counter after skill proposal written")
    r.add_argument("--proposal", default=None, help="Proposal path to record")
    r.set_defaults(func=cmd_reset)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
