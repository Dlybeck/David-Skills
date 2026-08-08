## Right now (2026-08-08)

v1.5.0 just shipped: the upstream-philosophy audit's fixes are all merged (ADR 0006 in-house
identity, hooks regression-tested, docs internal, writing pass), and `delegate` was reworked
from a toggled mode into a bounded on-call dispatch run (ADR 0007). A final pre-main fork
audit (five verified auditors over the full upstream diff) came back clean — three cosmetic
fixes applied, `dev` is ready for David to promote. Open work lives in
`.scratch/*/issues/` — the hook false-positive fix and pilots-docs wording are agent-ready;
delegate×wayfinder awaits a grilling session. See `HANDOFF.md` for the session log.

## Layout

Skills are organized into bucket folders under `skills/`:

- `engineering/` — daily code work
- `productivity/` — daily non-code workflow tools
- `misc/` — kept around but rarely used, not promoted
- `in-progress/` — beta: public on purpose, feedback wanted, not shipped in the plugin
- `deprecated/` — no longer used

Every skill in `engineering/` or `productivity/` (the **promoted** buckets) must have a reference in the top-level `README.md` and an entry in `.claude-plugin/plugin.json`'s `skills` array (the Claude Code plugin ships exactly the promoted set). Skills in `misc/`, `in-progress/`, and `deprecated/` must not appear in either.

Install commands are copied verbatim from [.agents/install-block.md](./.agents/install-block.md). `.claude-plugin/marketplace.json` makes the repo its own single-plugin marketplace — a fallback the install block explains, not the documented route. Run `claude plugin validate . --strict` after touching either manifest. Why a Claude plugin but not (yet) a Codex one lives in [.agents/adr/0002-ship-as-a-claude-code-plugin.md](./.agents/adr/0002-ship-as-a-claude-code-plugin.md).

Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.

Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`. The promoted buckets' `README.md`s and the top-level `README.md` group entries into **User-invoked** and **Model-invoked**; non-promoted bucket `README.md`s (`misc/`, `in-progress/`) use a flat list.

Skills in `engineering/` and `productivity/` also have a human-facing docs page at `docs/<bucket>/<skill-name>.md` (the docs tree mirrors those two bucket folders under `skills/`). This docs tree is internal — it is not published anywhere, and `docs/<bucket>/<skill-name>.md` is repo organisation only (the page format's historical origin is Matt Pocock's `aihero.dev/skills-<name>` template, nothing more). Cross-links between this repo's docs pages are repo-relative; see [.agents/writing-docs.md](./.agents/writing-docs.md) for the exact convention. When you add, rename, or change the behaviour of a skill in `engineering/` or `productivity/`, create or re-sync its docs page following that file. A finished page carries four sections — **What it does**, **When to reach for it**, **Common questions**, **It's working if** — and `writing-docs.md` holds the template, the section order, and where to hunt for the questions. Skills in the non-promoted buckets (`misc/`, `in-progress/`, `deprecated/`) get **no** docs page.

Every `SKILL.md` is either user-invoked (`disable-model-invocation: true` plus `policy.allow_implicit_invocation: false` in `agents/openai.yaml`, reachable only by the human) or model-invoked (model- or user-reachable). See [.agents/invocation.md](./.agents/invocation.md).

[`ask-claude`](./skills/engineering/ask-claude/SKILL.md) is the router that maps every user-reachable skill and how they relate. The same trigger that re-syncs a docs page applies to it: whenever you add, rename, remove, or change how a user-reachable skill fits the flows, re-read `ask-claude`'s `SKILL.md` and update it so the map stays accurate — a new skill it never mentions, or a stale one it still routes to, is a router that lies.

To (re)link every skill into the local harness skill directories (`~/.claude/skills`, `~/.agents/skills`), run `scripts/link-skills.sh`. Each entry is a symlink into this repo, so a `git pull` keeps installed skills current; re-run the script after adding, removing, or renaming a skill.

## Agent skills

### Issue tracker

Local markdown, under `.scratch/` — chosen over GitHub Issues to keep dev noise off the org
repo's Issues tab. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five canonical roles, unchanged (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` at the repo root. ADRs live at `.agents/adr/` (not the default `docs/adr/` — this repo's own pre-existing convention). See `docs/agents/domain.md`.
