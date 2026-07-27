#!/usr/bin/env python3
"""Match Tier-3 patterns and optionally extract from review artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _lib import detect_root, load_json, tokenize, write_json

PATTERNS_INDEX = ".cursor/patterns/index.json"


def load_index(root: Path) -> dict:
    index_path = root / PATTERNS_INDEX
    if not index_path.exists():
        return {"patterns": []}
    return load_json(index_path)


def match_patterns(
    task: str,
    domains: list[str],
    keywords: list[str] | None = None,
    *,
    root: Path | None = None,
    limit: int = 2,
) -> list[dict]:
    root = root or detect_root()
    index = load_index(root)
    terms = tokenize(task)
    if keywords:
        terms |= {k.lower().replace("_", "-") for k in keywords}

    matched: list[dict] = []
    for entry in index.get("patterns", []):
        triggers = {t.lower() for t in entry.get("triggers", [])}
        entry_domains = set(entry.get("domains", []))
        hits = terms & triggers
        domain_ok = not entry_domains or bool(entry_domains & set(domains))
        if hits and domain_ok:
            matched.append({
                "id": entry["id"],
                "path": entry["path"],
                "estimatedTokens": entry.get("estimatedTokens", 150),
                "trigger": ", ".join(sorted(hits)),
                "score": len(hits),
            })

    matched.sort(key=lambda p: p["score"], reverse=True)
    for item in matched:
        item.pop("score", None)
    return matched[:limit]


def propose_extraction(review_path: Path) -> dict | None:
    if not review_path.exists():
        return None

    text = review_path.read_text(encoding="utf-8")
    if "Status:" not in text and "## Critical" not in text:
        return None

    slug = review_path.stem.replace(" ", "-").lower()[:40]
    pattern_id = f"from-review-{slug}"

    return {
        "id": pattern_id,
        "path": f".cursor/patterns/extracted/{pattern_id}.md",
        "triggers": [],
        "domains": [],
        "estimatedTokens": 150,
        "sourceReview": str(review_path),
        "draft": (
            f"# Pattern (draft from {review_path.name})\n\n"
            "Extract reusable guidance from the review below.\n\n"
            f"---\n\n{text[:1500]}"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Pattern matcher for context builder")
    parser.add_argument("--task", default="")
    parser.add_argument("--domains", default="")
    parser.add_argument("--keywords", default="")
    parser.add_argument("--limit", type=int, default=2)
    parser.add_argument("--extract", default="", help="Review file to propose pattern from")
    parser.add_argument("--root", default="")
    args = parser.parse_args()

    root = detect_root(args.root or None)

    if args.extract:
        proposal = propose_extraction(Path(args.extract))
        if not proposal:
            sys.exit(f"error: could not extract from {args.extract}")
        print(json.dumps(proposal, indent=2))
        return

    domains = [d.strip() for d in args.domains.split(",") if d.strip()]
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    result = match_patterns(args.task, domains, keywords, root=root, limit=args.limit)
    print(json.dumps({"patterns": result}, indent=2))


if __name__ == "__main__":
    main()
