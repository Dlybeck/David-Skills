## Identity

David Skills is the private personal distribution of this skills collection. The package,
Claude Code and Codex plugins, marketplaces, repository links, and installation commands all use the
`david-skills` / `Dlybeck/David-Skills` identity. ADR 0006 records the personal-practice
boundary. External work-only adapters and rollout/session artifacts are intentionally excluded.

## Layout

Skills are organized into bucket folders under `skills/`:

- `engineering/` — daily code work
- `productivity/` — daily non-code workflow tools
- `misc/` — kept around but rarely used, not promoted
- `in-progress/` — beta: available for direct installation and testing, not shipped in the plugin
- `deprecated/` — no longer used

Every skill in `engineering/` or `productivity/` (the **promoted** buckets) must have a reference in the top-level `README.md` and entries in both plugin manifests. Harness-specific mechanics belong behind adapters so the promoted set remains available in Claude Code and Codex. Skills in `misc/`, `in-progress/`, and `deprecated/` must not appear in either plugin.

Install commands are copied from [.agents/install-block.md](./.agents/install-block.md). `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json` make this repository a private single-plugin marketplace for each harness. Run `npm test` after changing a manifest, catalog, skill path, or hook; also run `claude plugin validate . --strict` when Claude Code is available. The distribution decision lives in [.agents/adr/0002](./.agents/adr/0002-ship-as-private-agent-plugins.md).

Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.

Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`. The promoted buckets' `README.md`s and the top-level `README.md` group entries into **User-invoked** and **Model-invoked**; non-promoted bucket `README.md`s (`misc/`, `in-progress/`) use a flat list.

Skills in `engineering/` and `productivity/` also have a human-facing docs page at `docs/<bucket>/<skill-name>.md` (the docs tree mirrors those two bucket folders under `skills/`). This docs tree is internal — it is not published anywhere, and `docs/<bucket>/<skill-name>.md` is repo organisation only (the page format's historical origin is Matt Pocock's `aihero.dev/skills-<name>` template, nothing more). Cross-links between this repo's docs pages are repo-relative; see [.agents/writing-docs.md](./.agents/writing-docs.md) for the exact convention. When you add, rename, or change the behaviour of a skill in `engineering/` or `productivity/`, create or re-sync its docs page following that file. A finished page carries four sections — **What it does**, **When to reach for it**, **Common questions**, **It's working if** — and `writing-docs.md` holds the template, the section order, and where to hunt for the questions. Skills in the non-promoted buckets (`misc/`, `in-progress/`, `deprecated/`) get **no** docs page.

Every `SKILL.md` is either user-invoked (`disable-model-invocation: true` plus `policy.allow_implicit_invocation: false` in `agents/openai.yaml`, reachable only by the human) or model-invoked (model- or user-reachable). See [.agents/invocation.md](./.agents/invocation.md).

[`advise`](./skills/engineering/advise/SKILL.md) is the harness-neutral router that maps every user-reachable skill and how they relate. The same trigger that re-syncs a docs page applies to it: whenever you add, rename, remove, or change how a user-reachable skill fits the flows, re-read `advise`'s `SKILL.md` and update it so the map stays accurate — a new skill it never mentions, or a stale one it still routes to, is a router that lies.

`scripts/link-skills.sh` is a maintainer-only development convenience, never the installation route shown to users. It links only promoted skills and must refuse to replace a real directory on collision. Production installs come from the private GitHub remote through the relevant plugin marketplace.

## Release flow

Feature work is merged into `dev` and validated there. David alone promotes the tested `dev` tip
to `main`; that push is the human release approval. The repository does not use a version or
release pull request.

After a `main` promotion, the Release workflow consumes pending Changesets, synchronizes every
version surface, and tests the versioned tree. Its only permitted branch write is the mechanical
release commit: it atomically advances `main` and `dev` to that same commit while creating the
version tag, then creates the GitHub Release. It refuses to write if either branch moved or the two
branches were not aligned at the promoted commit. A manual workflow dispatch may only complete a
missing GitHub Release for an existing tag reachable from current `main`; it cannot consume a
Changeset or move a Git ref. Agents remain prohibited from pushing ordinary work directly to
`main`.

## Agent skills

### Issue tracker

Local markdown, under `.scratch/` — chosen over GitHub Issues to keep development noise out of
this repository's Issues tab. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five canonical roles, unchanged (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` at the repo root. ADRs live at `.agents/adr/` (not the default `docs/adr/` — this repo's own pre-existing convention). See `docs/agents/domain.md`.
