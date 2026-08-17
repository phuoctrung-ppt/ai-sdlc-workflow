# Repo Trust Rubric (skill-scout / research-practices)

**Status:** experiment — portable doc only. Not wired into day-path (`/fix`, `/shape-lite`) or `@learning-agent` by default.

**Purpose:** Score external GitHub (or similar) sources before distilling best practices into a thin skill proposal. Prevent skill bloat, license risk, and false authority.

**Pipeline slot (proposed):**

```text
Brief (stack from AGENTS §0 / task)
  → search
  → hard gates
  → score A–J
  → shortlist ≤3
  → STOP: human picks source(s)
  → distill thin skill + attribution
  → skill-update proposal (PENDING_APPROVAL)
  → approve → apply + manifest (low priority default)
```

---

## 1. Hard gates (fail any → reject)

| # | Gate | Fail when |
|---|------|-----------|
| G1 | **Clear license** | No LICENSE, or license forbids reuse/derivatives |
| G2 | **No malware / secrets** | Real secrets, unexplained binaries, hostile install scripts |
| G3 | **Scope matches ask** | Fullstack/monorepo dump when the ask is one craft (e.g. pytest only) |
| G4 | **Minimum liveness** | No commits ≥ 24 months **and** no stable citable release/tag |
| G5 | **Not junk mirror** | Empty fork, star-farm, scraped content without attribution |

On fail: one-line reason, do not shortlist.

---

## 2. Scoring (0–2 each → total 0–20)

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| **A. Maintainer** | Anonymous one-off | Individual with some track record | Org/team with real product, or known domain author |
| **B. Activity** | Dead / cosmetic only | Sparse but issues answered | Releases or clear changelog within 12 months |
| **C. Technical evidence** | Slogans / marketing shots | Code + decent README | Tests, runnable examples, ADR/design, anti-patterns |
| **D. Scope & portability** | Hard vendor/framework lock | Partly reusable | Patterns extractable without one monorepo |
| **E. Community signal** | Fake stars / zero discussion | Moderate stars + real issues | Quality issues/PRs from outsiders |
| **F. Documentation** | Empty / paste README | Getting started exists | Limitations, “when not to use”, versioning |
| **G. Security / supply chain** | `curl \| bash`, vague deps | Deps listed, few warnings | Pin/lockfile, SECURITY.md or safe practice |
| **H. License reuse** | Unclear | MIT/Apache/BSD clear | + easy NOTICE/attribution for proposals |
| **I. Fit to target stack** | Wrong runtime/ecosystem | Same language, different framework | Matches language + practice needed |
| **J. Noise & bloat** | 50k+ token essay, multi-domain mix | Long but structured | Narrow target; entry skill ≤ ~1–1.5k tokens |

### Thresholds

| Score | Decision |
|-------|----------|
| **0–8** | Reject |
| **9–13** | Only if no better source; mark **weak** |
| **14–17** | Shortlist (**candidate**) |
| **18–20** | Prefer for distill |

Stars alone never justify score 2 on **E**.

### Fast path (≈2 minutes)

1. G1–G5  
2. **C** + **D** + **I**  
3. **A** + **H**  
4. B / E / F / G / J as time allows  

---

## 3. Source preference by skill type

| Need | Prefer | Treat carefully |
|------|--------|-----------------|
| Language style | Official style guides, core-team orgs | Unversioned personal blogs |
| Test / QA | Framework docs + official examples | “1000 patterns” list repos |
| Security | OWASP, official hardening | Random GitHub checklists |
| Architecture | ADRs from teams that shipped | Slide decks with no code |
| Agent/Cursor skills | Licensed thin `SKILL.md` used in practice | Monorepo skill dumps |

Order of trust: **official docs > maintained org repo > strong individual > awesome-list aggregator**.

---

## 4. Shortlist output template

Use one block per candidate (max 3):

```markdown
### Candidate: {owner}/{repo}
- URL:
- Score: {n}/20 (A–J: …)
- Hard gates: PASS | FAIL ({reason})
- Fit: {stack} — {why match / skew}
- Portable extract: {3–7 bullets for skill body}
- Drop: {vendor / monorepo / essay parts}
- License: {SPDX} — attribution: {how}
- Risk: weak | ok | strong
- Decision: shortlist | reject
```

Human selects ≤1–2 sources → distill → `docs/reviews/YYYY-MM-DD-skill-update-proposal.md` (`PENDING_APPROVAL`). **Do not** auto-write `SKILL.md` or manifest.

---

## 5. Anti-patterns (reject or heavy penalty)

- README is emoji + “production-ready” with no tests  
- Verbatim copy of another repo without license/NOTICE  
- “Best practices” locked to one boilerplate (e.g. Nest + Prisma + multi-tenant) when the task needs one layer  
- Archived project sold as current standard  
- Heavy toolchain pull for one small rule  

---

## 6. Non-goals (this experiment)

- No default agent in matrix  
- No auto-apply into `.cursor/skills/**`  
- No coupling to `/fix` or `/shape-lite`  
- No replacement of internal retrospective learning (`skill-updater`) — external scout **feeds** the same approval gate  

---

## 7. Port notes

Copy this file alone to try the rubric on a real search (e.g. “pytest best practices”, “Playwright POM”).  
If useful later: thin `skill-scout` command + references this path; still optional and gated.
