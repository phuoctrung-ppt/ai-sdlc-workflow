#!/usr/bin/env python3
"""Workflow V2 context orchestration — deterministic context assembly.

Filters agent/skill candidates by .cursor/config/active-layers.json when present.

Usage:
  python3 .cursor/context/context-builder.py \\
      --task "Fix React button disabled state" \\
      --agent frontend-worker \\
      [--phase implement-frontend] \\
      [--paths apps/web/components/Button.tsx] \\
      [--keywords react,button] \\
      [--budget 8000] \\
      [--handoff docs/plans/.active-plan] \\
      [--use-legacy-loader] \\
      [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from _lib import detect_root, estimate_tokens, load_json
from intent_detector import detect_intent
from memory_loader import load_memory
from pattern_matcher import match_patterns
from profile_sync import filter_agents, filter_skill_ids, load_active_layers

TIER1_RULES = [
    ".cursor/rules/000-core.mdc",
    ".cursor/rules/001-workflow-v2.mdc",
]

DEFAULT_DO_NOT_LOAD = [
    "AGENTS.md",
    "docs/reviews/**",
    ".cursor/skills/**/references/**",
]

DEFAULT_SKILL_TOKENS = {
    "agentic-workflow": 600,
    "security": 800,
    "taste-design": 1200,
    "frontend-skills": 1100,
    "databases": 1000,
    "testing-qa": 700,
    "docker-devops": 600,
    "nestjs-skills": 1800,
    "zod-shared-types": 500,
    "ai-llm-integration": 800,
    "admin-service": 700,
    "bullmq-worker": 600,
    "planning": 700,
    "nestjs-scaffold": 2500,
    "web-app-ui-ux": 1200,
}


def load_config(root: Path, name: str) -> dict:
    path = root / ".cursor" / "config" / name
    if path.exists():
        return load_json(path)
    return {}


def resolve_manifest_path(root: Path, use_v2: bool = True) -> Path:
    v2 = root / ".cursor" / "skills" / "skills-manifest.v2.json"
    if not v2.exists():
        raise FileNotFoundError(
            f"canonical skill manifest missing: {v2} "
            "(skills-manifest.json v1 is retired — only skills-manifest.v2.json is supported)"
        )
    return v2


def run_skill_loader(
    root: Path,
    phase: str,
    task: str,
    agent: str,
    keywords: str,
    manifest_path: Path,
    limit: int,
    ref_limit: int,
) -> dict:
    cmd = [
        sys.executable,
        str(root / ".cursor" / "skills" / "scripts" / "skill-loader.py"),
        "--phase", phase,
        "--task", task,
        "--agent", agent,
        "--keywords", keywords,
        "--limit", str(limit),
        "--ref-limit", str(ref_limit),
        "--root", str(root),
        "--manifest-path", str(manifest_path),
    ]
    output = subprocess.check_output(cmd, text=True)
    return json.loads(output)


def activate_agents(
    matrix: dict,
    intent: dict,
    explicit_agent: str | None,
    active_layers: dict | None,
) -> dict:
    if explicit_agent:
        allowed = filter_agents([explicit_agent], active_layers)
        agent_id = allowed[0] if allowed else explicit_agent
        return {
            "agents": [{"id": agent_id, "role": "implement"}],
            "reviewer": "judge-agent" if intent.get("protected") else None,
            "reviewMode": "required" if intent.get("protected") else "optional",
            "ruleId": "explicit-agent",
            "layerFilter": bool(active_layers),
        }

    terms = set(intent.get("terms", []))
    domains = set(intent.get("domains", []))
    complexity = intent.get("complexity", "medium")
    protected = intent.get("protected", False)
    path_hints = intent.get("pathHints", [])

    best = None
    best_score = -1

    for rule in matrix.get("rules", []):
        when = rule.get("when", {})
        score = 0

        rule_domains = set(when.get("domains", []))
        if rule_domains:
            overlap = len(rule_domains & domains)
            if overlap == 0:
                continue
            score += overlap * 3

        rule_complexity = when.get("complexity", [])
        if rule_complexity and complexity not in rule_complexity:
            continue
        if rule_complexity:
            score += 2

        if "protected" in when and when["protected"] != protected:
            continue

        rule_keywords = {k.lower() for k in when.get("keywords", [])}
        if rule_keywords:
            kw_hits = len(terms & rule_keywords)
            if kw_hits == 0:
                continue
            score += kw_hits * 2

        rule_globs = when.get("pathGlobs", [])
        if rule_globs and path_hints:
            for hint in path_hints:
                hint_norm = hint.replace("\\", "/")
                for glob in rule_globs:
                    from fnmatch import fnmatch
                    if fnmatch(hint_norm, glob) or fnmatch(hint_norm.split("/")[-1], glob.lstrip("**/")):
                        score += 4
                        break

        if score > best_score:
            best_score = score
            best = rule

    if not best:
        fallback_candidates = ["frontend-worker", "backend-worker", "architect-planner"]
        filtered = filter_agents(fallback_candidates, active_layers)
        fallback_agent = filtered[0] if filtered else (explicit_agent or "architect-planner")
        return {
            "agents": [{"id": fallback_agent, "role": "implement"}],
            "reviewer": "judge-agent" if protected else None,
            "reviewMode": "required" if protected else "optional",
            "ruleId": "fallback",
            "layerFilter": bool(active_layers),
        }

    raw_agents = best.get("agents", [])
    filtered_ids = filter_agents(raw_agents, active_layers)
    if not filtered_ids:
        filtered_ids = filter_agents(["architect-planner"], active_layers) or ["architect-planner"]

    seq = best.get("sequence", raw_agents)
    filtered_seq = filter_agents(seq, active_layers) or filtered_ids

    return {
        "agents": [{"id": a, "role": "implement"} for a in filtered_ids],
        "sequence": filtered_seq,
        "reviewer": best.get("reviewer"),
        "reviewMode": best.get("reviewMode", "optional"),
        "maxSkills": best.get("maxSkills"),
        "ruleId": best.get("id"),
        "layerFilter": bool(active_layers),
        "agentsBeforeFilter": raw_agents,
    }


def enrich_skills(
    loader_result: dict,
    manifest: dict,
    max_skills: int | None,
    complexity: str,
    active_layers: dict | None,
) -> tuple[list[dict], int]:
    budget_cfg = manifest.get("maxSkillsByComplexity", {})
    if max_skills is None:
        max_skills = budget_cfg.get(complexity, budget_cfg.get("medium", 2))

    matched = loader_result.get("matchedSkills", [])
    if active_layers:
        allowed_ids = set(filter_skill_ids([s["id"] for s in matched], active_layers))
        matched = [s for s in matched if s["id"] in allowed_ids]

    skills = []
    total = 0
    for skill in matched[:max_skills]:
        meta = _find_skill_meta(manifest, skill["id"])
        est = meta.get("estimatedTokens", DEFAULT_SKILL_TOKENS.get(skill["id"], 800))
        priority = meta.get("priority", 5)
        enriched = {
            "id": skill["id"],
            "entry": skill["entry"],
            "estimatedTokens": est,
            "priority": priority,
            "loadMode": "required",
            "score": skill.get("score"),
            "matchedTerms": skill.get("matchedTerms", []),
            "scripts": skill.get("scripts", []),
        }
        skills.append(enriched)
        total += est
    return skills, total


def _find_skill_meta(manifest: dict, skill_id: str) -> dict:
    for bucket in ("portableSkills", "skills", "domainSkills"):
        for skill in manifest.get(bucket, []):
            if skill.get("id") == skill_id:
                return skill
    return {}


def pack_tier4_refs(
    loader_refs: list[dict],
    complexity: str,
    tier4_ceiling: int,
) -> tuple[list[dict], list[dict]]:
    """Paths only. Preload at most a few on high complexity; else all lazy."""
    lazy = []
    preloaded = []
    if complexity != "high":
        for ref in loader_refs:
            lazy.append({**ref, "loadMode": "lazy"})
        return preloaded, lazy

    used = 0
    for ref in loader_refs[:3]:
        est = 400
        if used + est > tier4_ceiling:
            lazy.append({**ref, "loadMode": "lazy"})
        else:
            preloaded.append({**ref, "loadMode": "preload", "estimatedTokens": est})
            used += est
    for ref in loader_refs[3:]:
        lazy.append({**ref, "loadMode": "lazy"})
    return preloaded, lazy


def build_context_packet(
    *,
    root: Path,
    task: str,
    agent: str | None,
    phase: str | None,
    path_hints: list[str],
    keywords: list[str],
    budget: int,
    handoff: str | None,
    use_legacy: bool,
) -> dict:
    intent = detect_intent(
        task,
        agent=agent,
        phase=phase,
        path_hints=path_hints,
        keywords=keywords,
        root=root,
    )

    matrix = load_config(root, "agent-matrix.json")
    budget_cfg = load_config(root, "context-budget.json")
    active_layers = load_active_layers(root)
    tier_ceilings = budget_cfg.get("tierCeilings", {
        "tier1": 1200,
        "tier2": 4000,
        "tier3": 800,
        "tier4": 2000,
    })

    activation = activate_agents(matrix, intent, agent, active_layers)
    primary_agent = agent or (activation["agents"][0]["id"] if activation["agents"] else "architect-planner")
    if active_layers and primary_agent not in set(active_layers.get("activeAgents") or []):
        # explicit agent outside profile — still allow but note
        activation["profileWarning"] = f"agent {primary_agent} not in activeAgents for profile"

    manifest_path = resolve_manifest_path(root, use_v2=not use_legacy)
    manifest = load_json(manifest_path) if manifest_path.exists() else {}

    keyword_str = ",".join(keywords)
    max_skills = activation.get("maxSkills")
    skill_limit = max_skills or budget_cfg.get("maxSkillsByComplexity", {}).get(
        intent["complexity"], 2
    )

    # Always request matched reference PATHS (lazy). Content still not inlined.
    # high → up to 8 paths; low/medium → up to 6 paths for expand-ref hints.
    ref_limit = 8 if intent["complexity"] == "high" else 6

    loader_result = run_skill_loader(
        root,
        intent["phase"],
        task,
        primary_agent,
        keyword_str,
        manifest_path,
        limit=max(skill_limit, 4),
        ref_limit=ref_limit,
    )

    memory = load_memory(root, intent["domains"], intent["phase"])
    patterns = match_patterns(task, intent["domains"], keywords, root=root, limit=2)

    tier1_tokens = sum(
        estimate_tokens((root / rule).read_text(encoding="utf-8"))
        for rule in TIER1_RULES
        if (root / rule).exists()
    ) + memory.get("estimatedTokens", 0)

    skills, tier2_tokens = enrich_skills(
        loader_result, manifest, activation.get("maxSkills"), intent["complexity"], active_layers
    )

    tier3_tokens = sum(p.get("estimatedTokens", 150) for p in patterns)
    preloaded_refs, lazy_refs = pack_tier4_refs(
        loader_result.get("referenceFiles", []),
        intent["complexity"],
        tier_ceilings.get("tier4", 2000),
    )
    tier4_tokens = sum(r.get("estimatedTokens", 400) for r in preloaded_refs)

    allocated = tier1_tokens + tier2_tokens + tier3_tokens + tier4_tokens

    handoff_data = None
    if handoff:
        handoff_path = root / handoff
        if handoff_path.exists():
            text = handoff_path.read_text(encoding="utf-8").strip()
            handoff_data = {
                "path": handoff,
                "estimatedTokens": estimate_tokens(text),
                "note": "Read plan summary only unless task requires full plan",
            }

    profile_meta = None
    if active_layers:
        profile_meta = {
            "profile": active_layers.get("profile"),
            "layout": active_layers.get("layout"),
            "layersOn": [k for k, v in (active_layers.get("layers") or {}).items() if v],
            "layersOff": [k for k, v in (active_layers.get("layers") or {}).items() if not v],
            "source": active_layers.get("source"),
        }

    return {
        "version": "2.1",
        "intent": intent,
        "projectProfile": profile_meta,
        "tokenBudget": {
            "maxTotal": budget,
            "allocated": allocated,
            "remaining": max(0, budget - allocated),
            "tierCeilings": tier_ceilings,
        },
        "activation": activation,
        "tier1": {
            "rules": [r for r in TIER1_RULES if (root / r).exists()],
            "memory": memory.get("files", []),
            "estimatedTokens": tier1_tokens,
        },
        "tier2": {
            "skills": skills,
            "estimatedTokens": tier2_tokens,
        },
        "tier3": {
            "patterns": patterns,
            "estimatedTokens": tier3_tokens,
        },
        "tier4": {
            "references": preloaded_refs,
            "lazyReferences": lazy_refs,
            "loadMode": "lazy",
            "estimatedTokens": tier4_tokens,
        },
        "handoff": handoff_data,
        "doNotLoad": DEFAULT_DO_NOT_LOAD,
        "manifestPath": str(manifest_path.relative_to(root)),
        "legacyLoader": {
            "phase": loader_result.get("phase"),
            "agent": loader_result.get("agent"),
        },
        "usage": [
            "Read tier1 rules + memory files only (not full AGENTS.md).",
            "Respect projectProfile.layersOff — do not plan those layers.",
            "Read tier2 skill entries (SKILL.md) — max 1-2 for low complexity.",
            "Read tier3 patterns when listed.",
            "tier4.lazyReferences are PATH hints only — read via --expand-ref when needed.",
            "Never bulk-read docs/reviews/ or entire references/ folders.",
        ],
    }


def expand_reference(root: Path, ref_path: str, reason: str) -> dict:
    full = root / ref_path.lstrip("/")
    if not full.exists():
        sys.exit(f"error: reference not found: {ref_path}")
    text = full.read_text(encoding="utf-8")
    return {
        "version": "2.1",
        "expandRef": {
            "path": ref_path,
            "absolutePath": str(full),
            "reason": reason,
            "estimatedTokens": estimate_tokens(text),
        },
        "usage": ["Read this reference only for the stated reason."],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Workflow V2 context builder")
    parser.add_argument("--task", default="")
    parser.add_argument("--agent", default="")
    parser.add_argument("--phase", default="")
    parser.add_argument("--paths", default="", help="Comma-separated path hints")
    parser.add_argument("--keywords", default="")
    parser.add_argument("--budget", type=int, default=8000)
    parser.add_argument("--handoff", default="")
    parser.add_argument("--use-legacy-loader", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--expand-ref", default="")
    parser.add_argument("--reason", default="")
    parser.add_argument("--root", default="")
    args = parser.parse_args()

    root = detect_root(args.root or None)

    if args.expand_ref:
        print(json.dumps(expand_reference(root, args.expand_ref, args.reason or "mid-task"), indent=2))
        return

    if not args.task:
        sys.exit("error: --task is required (unless using --expand-ref)")

    path_hints = [p.strip() for p in args.paths.split(",") if p.strip()]
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]

    packet = build_context_packet(
        root=root,
        task=args.task,
        agent=args.agent or None,
        phase=args.phase or None,
        path_hints=path_hints,
        keywords=keywords,
        budget=args.budget,
        handoff=args.handoff or None,
        use_legacy=args.use_legacy_loader,
    )

    if args.dry_run:
        packet["dryRun"] = True

    print(json.dumps(packet, indent=2))


if __name__ == "__main__":
    main()
