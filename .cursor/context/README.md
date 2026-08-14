# Context tooling (canonical layout)

This is **not** an unfinished rename. Two naming styles are intentional:

| Path | Role | Call from |
|------|------|-----------|
| `context-builder.py` | **CLI entry** (hyphen) | Shell, agents, docs, `workflow-policy.json` |
| `intent-detector.py` | CLI entry | policy / manual |
| `memory-loader.py` | CLI entry (`--sync`) | porting / session bootstrap |
| `pattern-matcher.py` | CLI entry | policy / manual |
| `profile-sync.py` | CLI entry | porting — AGENTS.md §0 → active-layers.json |
| `context_builder.py` | **Library** (underscore) | imported by CLI only |
| `intent_detector.py` | Library | imported by `context_builder` |
| `memory_loader.py` | Library | imported by `context_builder` |
| `pattern_matcher.py` | Library | imported by `context_builder` |
| `profile_sync.py` | Library | imported by CLI + context_builder |
| `_lib.py` | Shared helpers | library modules |

**Agents and humans must invoke the hyphen CLI only**, e.g.:

```bash
python3 .cursor/context/context-builder.py --task "..." --agent frontend-worker
python3 .cursor/context/memory-loader.py --sync
python3 .cursor/context/profile-sync.py --from-agents
python3 .cursor/context/profile-sync.py --detect
```

Do **not** run `context_builder.py` / `profile_sync.py` as scripts unless debugging imports.

## Project profile

After filling `AGENTS.md` **§0 Project Profile**, run `profile-sync.py --from-agents`.
It writes `.cursor/config/active-layers.json`. Context builder then drops agents/skills for layers that are off.

See `docs/vision/project-profile-layers.md`.
