# Skill Scout — Best practices (distill + load map)

Practices for this workflow so ingested skills stay **thin, loadable, and non-hostile** to core loops.

---

## 1. One craft per skill

| Do | Don't |
|----|--------|
| `python-pytest` or `playwright-pom` | `python-qa-and-docker-and-security` |
| Split if sources cover unrelated crafts | Merge unrelated domains to “save” manifest rows |

Agents match **keywords ∩ task**. A kitchen-sink skill either never ranks or always pollutes context.

---

## 2. Thin entry, fat references (lazy)

| Layer | Budget | Content |
|-------|--------|--------|
| `SKILL.md` entry | ~800–1500 tokens | When-to-use, hard rules, anti-patterns, pointer to refs |
| `references/*.md` | Unlimited but **lazy** | Long examples, tables, upstream distill |

**Never** put 50KB essays in entry (taste-design lesson).

Entry structure (recommended):

```markdown
---
name: {id}
description: one line; when to load
---

# Title

## When to use
## Hard rules
## Anti-patterns
## References (read only if needed)
## Attribution
```

---

## 3. Keyword design (load accuracy)

Loader scores **intersection** of task tokens and `keywords[]`.

| Prefer | Avoid as sole keywords |
|--------|-------------------------|
| `pytest`, `fixture`, `parametrize`, `monkeypatch` | only `test` |
| `playwright`, `locator`, `page-object` | only `e2e` |
| `alembic`, `migration`, `postgres` | only `database` |

**Rules**

1. Include **stack noun** + **practice nouns** (3–12 keywords).
2. Include skill `id` tokens if multi-word (`python-pytest` → also list `pytest`).
3. Do not rely only on generic verbs (`build`, `create`, `fix`).
4. After apply, run **positive** verify (should match) and **negative** verify (wrong phase/keywords should not force this skill to top).

---

## 4. Phases & agents (who sees it)

Map to **execution**, not aspiration.

| Skill type | Typical phases | Typical agents |
|------------|----------------|----------------|
| Unit/integration test | `test`, `fix`, maybe implement-* | `qa-worker`, implement worker |
| E2E UI | `test`, `fix`, `implement-frontend` | `qa-worker`, `frontend-worker` |
| API contract | `plan`, `implement-backend`, `implement-frontend` | `contract-agent`, workers |
| Security pattern | `implement-*`, `review`, `fix` | `security-worker`, `judge-agent` |
| Scout itself | `skill-authoring`, `review` only | `learning-agent` |

**Do not** put scout-ingested product skills on `skill-authoring` only — they will never load in real work.

---

## 5. Priority ceiling

| Band | Use |
|------|-----|
| 18–20 | Core workflow (agentic-workflow, error-recovery) — **never** scout default |
| 12–17 | High-signal portable product skills |
| **6–10** | **Scout-ingested default** |
| ≤5 | Experimental / narrow |

Raise priority only after the skill proved useful in retrospectives — not on first ingest.

---

## 6. Source selection (trust)

Follow `docs/vision/repo-trust-rubric.md`.

Extra practices:

1. Prefer **official docs** over “awesome list” aggregators for the first shortlist seat.
2. One strong source > three mediocre.
3. Record SPDX + URL; refuse no-license copy.
4. Drop vendor lock-in sections even if the rest scores high.

---

## 7. Merge vs new

| Signal | Action |
|--------|--------|
| Same stack + same craft as existing id | **Merge** (patch SKILL + maybe keywords) |
| New craft or incompatible rules | **New** id |
| Contradicts existing hard rule | Call out in proposal; human chooses |

---

## 8. Apply hygiene

1. Require `status: APPROVED` in proposal frontmatter (or explicit task approve).
2. Write files → manifest → mark `APPLIED` → verify load.
3. Optional: `python3 .cursor/skills/scripts/manifest-register.py --dry-run …` then without `--dry-run`.
4. Never edit `workflow-state.json` by hand.
5. Do not add scout skills to day-path command docs as required steps.

---

## 9. Negative verify (best practice)

Positive: phase/agent/keywords from the entry → skill appears in matches.

Negative examples:

- Phase `brainstorm` + marketing task → pytest skill **must not** dominate
- Agent `designer-worker` + “landing hero” → backend test skill **must not** load

If negative fails, keywords/phases are too broad — tighten before shipping.

---

## 10. Relationship to skill-updater

| Path | Learns from |
|------|-------------|
| `/skill-update` | Internal retrospective / memory |
| `/skill-scout` | External trusted sources |

Both end in **proposal → human → apply**. Scout must not bypass that gate.
