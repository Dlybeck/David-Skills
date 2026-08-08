# Ship David Skills as private Claude Code and Codex plugins

## Context

The promoted skills live in multiple bucket directories. Installing only one directory loses
part of the collection, while asking users to install each skill separately makes updates
fragmented and easy to miss.

## Decision

Ship the collection as a managed plugin named `david-skills` for both Claude Code and Codex.
Each harness gets its own manifest and single-plugin marketplace in the locations it discovers.
Both marketplaces resolve their plugin from this repository root, so hooks and supporting files
travel with the skills.

The canonical Claude Code route is:

```
/plugin marketplace add Dlybeck/David-Skills
/plugin install david-skills@david-skills
```

Claude Code ships all 28 promoted skills. Codex ships the 25 portable promoted skills and omits
`ask-claude`, `autopilot`, and `yolopilot`; the latter two require Claude Code's `claude --bg`
and `/goal` continuation, and the router is named for and advertises that Claude-only surface.
Exclusion is preferable to presenting unavailable flows as portable.

The canonical Codex route is:

```bash
codex plugin marketplace add Dlybeck/David-Skills --ref main
codex plugin add david-skills@david-skills
```

skills.sh remains an optional file-based route for other agents and for users who deliberately
want editable copies. It is not the default Codex install and does not carry the hooks.

The canonical and current installation wording lives in
[install-block.md](../install-block.md).
