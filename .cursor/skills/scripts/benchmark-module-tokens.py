#!/usr/bin/env python3
"""Estimate input-token cost: chat/no-flow vs /dev-module full-flow for one feature module.

Static footprint benchmark (on-disk bytes + skill-loader + turn model).
Not a live Cursor billing meter — for relative cost drivers.

Usage:
  py -3 .cursor/skills/scripts/benchmark-module-tokens.py
  py -3 .cursor/skills/scripts/benchmark-module-tokens.py --json
  py -3 .cursor/skills/scripts/benchmark-module-tokens.py --out docs/reviews/token-benchmark.md

Token proxy: UTF-8 chars / 4.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RULES = ROOT / ".cursor" / "rules"
AGENTS_DIR = ROOT / ".cursor" / "agents"
SKILLS = ROOT / ".cursor" / "skills"
LOADER = SKILLS / "scripts" / "skill-loader.py"

# Baseline always-on size before this slim (all 6 rules alwaysApply true), measured from git HEAD bodies.
BASELINE_ALWAYS_ON_CHARS = 10_248


def chars_to_tokens(n: int) -> int:
    return max(0, (n + 3) // 4)


def file_chars(path: Path) -> int:
    if not path.exists():
        return 0
    return len(path.read_text(encoding="utf-8", errors="ignore"))


def parse_always_apply(path: Path) -> bool | None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"^---\n(.*?)\n---", text, re.S | re.M)
    if not m:
        return None
    m2 = re.search(r"alwaysApply:\s*(true|false)", m.group(1))
    if not m2:
        return None
    return m2.group(1) == "true"


def turn_total(sticky_tokens: int, turns: int) -> int:
    """Sum over turns of sticky + 15% growth per prior turn (transcript creep)."""
    total = 0
    for t in range(turns):
        total += sticky_tokens + int(sticky_tokens * 0.15 * t)
    return total


@dataclass
class LineItem:
    label: str
    chars: int
    note: str = ""

    @property
    def tokens(self) -> int:
        return chars_to_tokens(self.chars)


@dataclass
class PhaseEst:
    phase: str
    agent: str
    turns: int
    sticky_tokens: int
    total_tokens: int
    skills: list[str] = field(default_factory=list)


def always_on_items() -> list[LineItem]:
    items: list[LineItem] = []
    for path in sorted(RULES.glob("*.mdc")):
        if parse_always_apply(path):
            items.append(LineItem(f"always-on {path.name}", file_chars(path), "every turn"))
    return items


def glob_rules_chars() -> int:
    total = 0
    for path in sorted(RULES.glob("*.mdc")):
        if parse_always_apply(path) is False:
            total += file_chars(path)
    return total


def run_loader(phase: str, agent: str, task: str, keywords: str) -> dict:
    cmd = [
        sys.executable,
        str(LOADER),
        "--phase",
        phase,
        "--task",
        task,
        "--agent",
        agent,
        "--keywords",
        keywords,
        "--root",
        str(ROOT),
    ]
    out = subprocess.check_output(cmd, text=True, cwd=str(ROOT))
    return json.loads(out)


def skill_chars(loader_json: dict, read_top_n: int = 2, read_refs: int = 1) -> tuple[int, list[str]]:
    chars = 0
    labels: list[str] = []
    seen: set[str] = set()
    for skill in loader_json.get("matchedSkills", [])[:read_top_n]:
        entry = skill.get("entry", "")
        path = ROOT / entry
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        c = file_chars(path)
        chars += c
        labels.append(f"{skill.get('id')} ({chars_to_tokens(c)} tok)")
    for ref in loader_json.get("referenceFiles", [])[:read_refs]:
        path = ROOT / ref.get("path", "")
        key = str(path)
        if key in seen or not path.exists():
            continue
        seen.add(key)
        c = file_chars(path)
        chars += c
        labels.append(f"ref:{path.name} ({chars_to_tokens(c)} tok)")
    return chars, labels


def agent_chars(name: str) -> int:
    return file_chars(AGENTS_DIR / f"{name}.md")


def build() -> dict:
    always = always_on_items()
    always_chars = sum(i.chars for i in always)
    agents_md = file_chars(ROOT / "AGENTS.md")
    session = file_chars(ROOT / ".cursor" / "hooks" / "session-start.sh")
    command = file_chars(ROOT / ".cursor" / "commands" / "dev-module.md")
    code_est = 40_000
    prompt_est = 2_000
    artifacts_est = 12_000
    glob_chars = glob_rules_chars()

    # No-flow: 3 turns in one chat; glob rules on 2 coding turns
    no_sticky = always_chars + agents_md + session + code_est + prompt_est
    no_turns = 3
    no_total = turn_total(chars_to_tokens(no_sticky), no_turns)
    no_total += chars_to_tokens(glob_chars) * 2

    # Full-flow: each phase is a fresh subagent context (skills do NOT carry across agents)
    shared_base = always_chars + agents_md + session + code_est + prompt_est
    phases_spec = [
        ("brainstorm", "architect-planner", "notifications module", "plan,module,api,ui", 2, False),
        ("plan", "architect-planner", "notifications module", "plan,module,api,ui", 2, False),
        ("scaffold", "scaffold-agent", "notifications scaffold", "module,scaffold,entity,migration,stub", 1, False),
        ("design", "designer-worker", "notifications UI", "design,taste,ui,hero", 2, False),
        ("implement-backend", "backend-worker", "notifications CRUD API", "module,service,controller,api,crud,backend", 2, True),
        ("implement-frontend", "frontend-worker", "notifications settings page", "react,next,page,form,ui", 2, True),
        ("test", "qa-worker", "notifications tests", "unit-test,e2e,jest,playwright", 1, True),
        ("review", "judge-agent", "notifications review", "workflow,judge,security,test", 1, False),
    ]

    phase_rows: list[PhaseEst] = []
    full_total = 0
    # Orchestrator reads command once (2 turns: kickoff + wrap)
    orch_sticky = shared_base + command + artifacts_est
    orch_turns = 2
    orch_tok = turn_total(chars_to_tokens(orch_sticky), orch_turns)
    full_total += orch_tok

    for phase, agent, task, keywords, turns, coding in phases_spec:
        data = run_loader(phase, agent, task, keywords)
        s_chars, labels = skill_chars(data)
        sticky = shared_base + agent_chars(agent) + s_chars
        # plan/review text present in later phases
        if phase in ("implement-backend", "implement-frontend", "test", "review"):
            sticky += artifacts_est
        sticky_tok = chars_to_tokens(sticky)
        total = turn_total(sticky_tok, turns)
        if coding:
            total += chars_to_tokens(glob_chars) * turns
        phase_rows.append(
            PhaseEst(phase, agent, turns, sticky_tok, total, labels)
        )
        full_total += total

    ratio = full_total / no_total if no_total else 0.0
    baseline_always_tok = chars_to_tokens(BASELINE_ALWAYS_ON_CHARS)
    now_always_tok = chars_to_tokens(always_chars)

    # Chat-only always-on savings per turn
    per_turn_saved = baseline_always_tok - now_always_tok

    return {
        "always_on_tokens_now": now_always_tok,
        "always_on_tokens_baseline": baseline_always_tok,
        "always_on_per_turn_saved": per_turn_saved,
        "always_on_files": [i.label for i in always],
        "glob_rules_tokens": chars_to_tokens(glob_chars),
        "no_flow": {
            "turns": no_turns,
            "sticky_tokens": chars_to_tokens(no_sticky),
            "total_input_tokens": no_total,
        },
        "full_flow": {
            "orchestrator_tokens": orch_tok,
            "orchestrator_turns": orch_turns,
            "phases": [
                {
                    "phase": p.phase,
                    "agent": p.agent,
                    "turns": p.turns,
                    "sticky_tokens": p.sticky_tokens,
                    "total_tokens": p.total_tokens,
                    "skills": p.skills,
                }
                for p in phase_rows
            ],
            "total_input_tokens": full_total,
            "total_turns": orch_turns + sum(p.turns for p in phase_rows),
        },
        "ratio_full_over_no": round(ratio, 2),
    }


def render_markdown(d: dict) -> str:
    no = d["no_flow"]
    full = d["full_flow"]
    lines = [
        "# Token footprint benchmark — one module",
        "",
        "> Static estimate from on-disk bytes + skill-loader. Proxy: `tokens ~= chars/4`.",
        "> Scenario: **notifications** (API CRUD + settings UI + tests + judge).",
        "> Model: **each worker phase = separate context** (skills do not pile across agents).",
        "",
        "## Always-on slim (this change)",
        "",
        f"| | Tokens / turn |",
        f"|---|---:|",
        f"| Before (001–006 alwaysApply) | {d['always_on_tokens_baseline']:,} |",
        f"| After (only slim 006) | {d['always_on_tokens_now']:,} |",
        f"| **Saved every chat turn** | **{d['always_on_per_turn_saved']:,}** |",
        "",
        f"Active always-on: {', '.join(d['always_on_files']) or '(none)'}.",
        f"Glob rules 001–005 (only when editing matching files): {d['glob_rules_tokens']:,} tok.",
        "",
        "## Headline: build one module",
        "",
        "| Path | Turns | Sticky / typical turn | Est. total **input** tokens |",
        "|---|---:|---:|---:|",
        f"| **No-flow** (chat + @files) | {no['turns']} | {no['sticky_tokens']:,} | **{no['total_input_tokens']:,}** |",
        f"| **Full-flow** (`/dev-module`) | {full['total_turns']} | (varies by phase) | **{full['total_input_tokens']:,}** |",
        f"| **Ratio** |  |  | **{d['ratio_full_over_no']}×** |",
        "",
        "### Full-flow phase breakdown",
        "",
        "| Phase | Agent | Turns | Sticky | Phase total |",
        "|---|---|---:|---:|---:|",
        f"| orchestrator | (main) | {full['orchestrator_turns']} | — | {full['orchestrator_tokens']:,} |",
    ]
    for p in full["phases"]:
        lines.append(
            f"| {p['phase']} | {p['agent']} | {p['turns']} | {p['sticky_tokens']:,} | {p['total_tokens']:,} |"
        )

    lines += [
        "",
        "## Trade-off (what you get for the tokens)",
        "",
        f"- Full-flow spends about **{d['ratio_full_over_no']}×** input tokens vs a 3-turn direct chat for the same module shape.",
        "- **Always-on slim** cuts ~{0} tok/turn on *every* conversation (hotfix and features). That is the main cost win for daily chat.".format(
            f"{d['always_on_per_turn_saved']:,}"
        ),
        "- Full-flow still costs more because of **more turns + large design/taste skills + agent prompts** — not because of always-on rules.",
        "- Heaviest phases: **design** and **implement-frontend** (taste-design skill).",
        "",
        "| Choose | When | Token posture |",
        "|---|---|---|",
        "| No-flow chat | Hotfix, 1–3 files, clear bug | Cheap |",
        "| Full `/dev-module` | New module, UI+API, protected paths | Pay ~{0}× for plan/design/tests/judge |".format(
            d["ratio_full_over_no"]
        ),
        "",
        "## Quality return (qualitative, not a token metric)",
        "",
        "| Full-flow buys | No-flow usually skips |",
        "|---|---|",
        "| Written plan + acceptance criteria | Ad-hoc intent |",
        "| Design-first UI gate | UI invented in-code |",
        "| Scoped workers (fewer wrong-layer edits) | One agent touches anything |",
        "| QA + judge artifact | Best-effort self-check |",
        "| Protected-path compliance | Easy to miss gates |",
        "",
        "Rough rule of thumb: if the module is **>1 layer** or **protected**, the extra tokens buy fewer reopen/fix cycles — often worth it. If it is a **1-file bugfix**, full-flow is pure overhead.",
        "",
        "## Re-run",
        "",
        "```bash",
        "py -3 .cursor/skills/scripts/benchmark-module-tokens.py --json",
        "py -3 .cursor/skills/scripts/benchmark-module-tokens.py --out docs/reviews/YYYY-MM-DD-token-benchmark.md",
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    data = build()
    md = render_markdown(data)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(md, encoding="utf-8")
        print(f"Wrote {args.out}")

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        # Avoid Windows console UnicodeEncodeError
        sys.stdout.buffer.write((md + "\n\n--- JSON ---\n" + json.dumps(data, indent=2) + "\n").encode("utf-8", errors="replace"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
