# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root, or
- **`CONTEXT-MAP.md`** at the repo root if it exists — it points at one `CONTEXT.md` per context. Read each one relevant to the topic.
- **`.agents/adr/`** — read ADRs that touch the area you're about to work in. (This repo's own convention — it's the skills' source repo, not a normal consumer, so ADRs live at `.agents/adr/` rather than the usual `docs/adr/`.) In multi-context repos, also check `src/<context>/docs/adr/` for context-scoped decisions.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `/domain-modeling` skill (reached via `/grill-with-docs` and `/re-architect`) creates them lazily when terms or decisions actually get resolved.

## File structure

Single-context repo (this one, and most repos):

```
/
├── CONTEXT.md
├── .agents/adr/
│   ├── 0001-explicit-setup-pointer-only-for-hard-dependencies.md
│   ├── 0002-ship-as-a-claude-code-plugin.md
│   └── 0003-plugin-root-hook-for-personal-git-workflow.md
└── skills/
```

Multi-context repo (presence of `CONTEXT-MAP.md` at the root) — not this repo's shape, shown for reference:

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0003 (plugin-root hook) — but worth reopening because…_
