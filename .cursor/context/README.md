# Context tooling (canonical layout)

This is **not** an unfinished rename. Two naming styles are intentional:

| Path | Role | Call from |
|------|------|-----------|
| `context-builder.py` | **CLI entry** (hyphen) | Shell, agents, docs, `workflow-policy.json` |
| `intent-detector.py` | CLI entry | policy / manual |
| `memory-loader.py` | CLI entry (`--sync`) | porting / session bootstrap |
| `pattern-matcher.py` | CLI entry | policy / manual |
| `context_builder.py` | **Library** (underscore) | imported by CLI only |
| `intent_detector.py` | Library | imported by `context_builder` |
| `memory_loader.py` | Library | imported by `context_builder` |
| `pattern_matcher.py` | Library | imported by `context_builder` |
| `_lib.py` | Shared helpers | library modules |

**Agents and humans must invoke the hyphen CLI only**, e.g.:

```bash
python3 .cursor/context/context-builder.py --task "..." --agent frontend-worker
python3 .cursor/context/memory-loader.py --sync
```

Do **not** run `context_builder.py` as a script unless debugging imports.
