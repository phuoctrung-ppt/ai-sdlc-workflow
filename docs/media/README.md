# Media

## `ai-sdlc-workflow-explained.mp4`

Slideshow walkthrough of the **v2** three-layer workflow (Execute / Memory / Learning), which files agents call, and where token cost concentrates.

| Item | Detail |
|------|--------|
| Path | [`ai-sdlc-workflow-explained.mp4`](./ai-sdlc-workflow-explained.mp4) |
| Length | ~1 minute (frame slideshow) |
| Branch | `v2` |

### Outline

1. **Execute** — `/architecture-plan` → `/dev-module` → workers → judge  
2. **Memory** — `docs/memory/{decisions,gotchas,shortcuts}.md` (SoT); `.memory/*` is AGENTS cache only  
3. **Learning** — retrospective + `modulesSinceLastProposal` → `@learning-agent` / `skill-updater`  
4. **Context CLI** — always `python3 .cursor/context/context-builder.py` (hyphen entrypoint)  
5. **Token tips** — skip re-plan when approved; Critical-only fix loops; product UI blocks not full taste-skill  

### If the MP4 is missing

Binary may be supplied from the design session artifact (`ai-sdlc-workflow-explained.mp4`, ~550KB). Place it next to this README:

```bash
mkdir -p docs/media
cp /path/to/ai-sdlc-workflow-explained.mp4 docs/media/
git add docs/media/ai-sdlc-workflow-explained.mp4
git commit -m "docs(media): add workflow explainer video"
```

Linked from the root [README](../../README.md).
