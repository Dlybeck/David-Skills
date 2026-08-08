# Ship David Skills as a private Claude Code plugin

## Context

The promoted skills live in multiple bucket directories. Installing only one directory loses
part of the collection, while asking users to install each skill separately makes updates
fragmented and easy to miss.

## Decision

Ship the promoted `engineering` and `productivity` skills as one Claude Code plugin named
`david-skills`. The repository's `.claude-plugin/marketplace.json` exposes a private
single-plugin marketplace, and `.claude-plugin/plugin.json` lists the exact promoted skill
paths.

The canonical Claude Code route is:

```
/plugin marketplace add Dlybeck/David-Skills
/plugin install david-skills@david-skills
```

For Codex and other agents, skills.sh remains the file-based installation route. A native Codex
plugin is separate future work; this repository does not claim that Claude-only behaviors such
as `claude --bg` are portable.

The canonical and current installation wording lives in
[install-block.md](../install-block.md).
