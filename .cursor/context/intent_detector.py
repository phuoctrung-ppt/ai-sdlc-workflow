#!/usr/bin/env python3
"""Detect task intent: phase, domains, complexity, protected status."""

from __future__ import annotations

import argparse
import fnmatch
import json
import sys
from pathlib import Path

from _lib import detect_root, load_json, tokenize

DOMAIN_KEYWORDS: dict[str, set[str]] = {
    "frontend": {
        "react", "nextjs", "next", "tsx", "jsx", "component", "page", "ui", "ux",
        "frontend", "web", "css", "tailwind", "form", "dashboard", "landing",
        "rsc", "hydration", "button", "layout", "design", "sketch",
    },
    "backend": {
        "nestjs", "backend", "api", "rest", "service", "controller", "module",
        "dto", "endpoint", "server", "graphql", "rpc",
    },
    "database": {
        "database", "postgres", "postgresql", "mongodb", "sql", "schema",
        "migration", "index", "query", "typeorm", "entity", "table",
    },
    "security": {
        "auth", "authentication", "authorization", "jwt", "oauth", "guard",
        "rbac", "permission", "mfa", "totp", "security", "encrypt", "secret",
    },
    "devops": {
        "docker", "compose", "nginx", "ci", "cd", "deploy", "kubernetes",
        "terraform", "workflow", "dockerfile", "infra",
    },
    "ai": {
        "llm", "openai", "anthropic", "embedding", "prompt", "ai", "copilot",
        "vector", "pgvector", "streaming",
    },
    "qa": {
        "test", "jest", "vitest", "playwright", "e2e", "spec", "coverage", "mock",
    },
    "design": {
        "design", "mockup", "wireframe", "sketch", "brandkit", "imagegen",
        "typography", "hero", "landing", "redesign",
    },
}

PHASE_HINTS: dict[str, set[str]] = {
    "plan": {"plan", "architect", "adr", "roadmap", "breakdown", "scope"},
    "design": {"design", "mockup", "wireframe", "sketch", "brandkit", "imagegen"},
    "implement-frontend": {"react", "nextjs", "tsx", "component", "page", "ui", "frontend"},
    "implement-backend": {"nestjs", "backend", "api", "service", "controller", "module"},
    "database": {"migration", "schema", "postgres", "sql", "index", "entity"},
    "devops": {"docker", "compose", "ci", "cd", "deploy", "nginx"},
    "test": {"test", "jest", "playwright", "e2e", "coverage", "spec"},
    "fix": {"fix", "bug", "broken", "error", "regression", "patch"},
    "review": {"review", "judge", "audit", "compliance", "pr"},
    "scaffold": {"scaffold", "bootstrap", "stub", "skeleton", "shell"},
}

LOW_COMPLEXITY_HINTS = {"fix", "typo", "button", "label", "style", "css", "rename", "patch"}
HIGH_COMPLEXITY_HINTS = {
    "architect", "migration", "auth", "multi-tenant", "refactor", "redesign",
    "genesis", "roadmap", "integration", "microservice",
}


def detect_domains(terms: set[str]) -> list[str]:
    scores: dict[str, int] = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        hits = len(terms & keywords)
        if hits:
            scores[domain] = hits
    return [d for d, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)]


def detect_phase(
    terms: set[str],
    domains: list[str],
    explicit_phase: str | None,
    agent: str | None,
) -> str:
    if explicit_phase:
        return explicit_phase

    if agent == "architect-planner":
        return "plan"
    if agent == "judge-agent":
        return "review"
    if agent == "designer-worker":
        return "design"
    if agent == "database-worker":
        return "database"
    if agent == "devops-worker":
        return "devops"
    if agent == "qa-worker":
        return "test"
    if agent == "scaffold-agent":
        return "scaffold"
    if agent == "frontend-worker":
        return "implement-frontend"
    if agent in {"backend-worker", "admin-worker", "ai-worker", "security-worker"}:
        return "implement-backend"

    phase_scores: dict[str, int] = {}
    for phase, hints in PHASE_HINTS.items():
        phase_scores[phase] = len(terms & hints)

    for domain in domains:
        if domain == "frontend":
            phase_scores["implement-frontend"] = phase_scores.get("implement-frontend", 0) + 2
        if domain == "backend":
            phase_scores["implement-backend"] = phase_scores.get("implement-backend", 0) + 2
        if domain == "database":
            phase_scores["database"] = phase_scores.get("database", 0) + 2
        if domain == "devops":
            phase_scores["devops"] = phase_scores.get("devops", 0) + 2
        if domain == "design":
            phase_scores["design"] = phase_scores.get("design", 0) + 2

    if not phase_scores or max(phase_scores.values()) == 0:
        return "implement-backend"

    return max(phase_scores, key=phase_scores.get)


def detect_complexity(terms: set[str], path_hints: list[str]) -> str:
    if terms & HIGH_COMPLEXITY_HINTS:
        return "high"
    if len(path_hints) > 3:
        return "high"
    if terms & LOW_COMPLEXITY_HINTS and len(path_hints) <= 1:
        return "low"
    return "medium"


def is_protected(root: Path, path_hints: list[str]) -> bool:
    config_path = root / ".cursor" / "config" / "protected-paths.json"
    if not config_path.exists():
        return False

    config = load_json(config_path)
    globs = config.get("genericProtectedGlobs", []) + config.get("projectProtectedGlobs", [])
    globs = [g for g in globs if not g.startswith("(_")]

    for hint in path_hints:
        normalized = hint.replace("\\", "/")
        for pattern in globs:
            if fnmatch.fnmatch(normalized, pattern) or fnmatch.fnmatch(
                f"**/{normalized}", pattern
            ):
                return True
    return False


def detect_intent(
    task: str,
    *,
    agent: str | None = None,
    phase: str | None = None,
    path_hints: list[str] | None = None,
    keywords: list[str] | None = None,
    root: Path | None = None,
) -> dict:
    root = root or detect_root()
    path_hints = path_hints or []
    terms = tokenize(task)
    if keywords:
        terms |= {k.lower().replace("_", "-") for k in keywords}

    domains = detect_domains(terms)
    resolved_phase = detect_phase(terms, domains, phase, agent)
    complexity = detect_complexity(terms, path_hints)
    protected = is_protected(root, path_hints)

    return {
        "phase": resolved_phase,
        "domains": domains,
        "complexity": complexity,
        "protected": protected,
        "pathHints": path_hints,
        "terms": sorted(terms),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect task intent for context builder")
    parser.add_argument("--task", required=True)
    parser.add_argument("--agent", default="")
    parser.add_argument("--phase", default="")
    parser.add_argument("--paths", default="", help="Comma-separated path hints")
    parser.add_argument("--keywords", default="", help="Comma-separated keywords")
    parser.add_argument("--root", default="")
    args = parser.parse_args()

    root = detect_root(args.root or None)
    path_hints = [p.strip() for p in args.paths.split(",") if p.strip()]
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]

    result = detect_intent(
        args.task,
        agent=args.agent or None,
        phase=args.phase or None,
        path_hints=path_hints,
        keywords=keywords,
        root=root,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
