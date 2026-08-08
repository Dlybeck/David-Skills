# Handoff log

Newest first. Each entry: what happened, where it stopped, what's next.

## 2026-08-08 — Final pre-main fork audit: clean, three cosmetic fixes

A five-auditor workflow (philosophy of upstream edits, philosophy of the four fork-added
skills, CLAUDE.md consistency invariants, docs/links/versions, stale-identity triage) with
per-finding adversarial verification ran over the full `upstream/main..dev` diff (122 files).
Verdict: **the fork is ready for promotion.** No upstream gate weakened, all four added skills
match their ADRs (0005/0006/0007), all 29 promoted skills consistent across README ↔
plugin.json ↔ bucket READMEs ↔ docs tree ↔ ask-claude router, zero broken links, versions
aligned at 1.5.0, and every remaining mattpocock/old-name reference is deliberate historical
record or upstream attribution.

Only three defects survived verification, all fixed in this session's commit: CONTEXT.md's
glossary cited a nonexistent `ready-for-afk` triage role (→ `ready-for-agent`),
`docs/productivity/grill-me.md` had Common questions / It's working if in reversed template
order, and `skills/in-progress/README.md`'s install command still pointed at
`mattpocock/skills` (→ `DenaliAI-Automation/Denali-DEV`). None touch shipped plugin skill
text, so no version bump was needed. `claude plugin validate --strict` and the 49 hook checks
pass after the fixes.

**Next:** `main` promotion is David's call (human-only, no agent exception). The three
known tickets stay open in `.scratch/` — hook-claim-false-positive and pilots-docs-heuristic
are agent-ready, delegate-wayfinder-composition awaits a grilling session — none blocks the
merge.

## 2026-08-08 — Upstream audit, its five fixes, and the delegate rework (v1.5.0)

A three-agent audit of this fork against `upstream/main` (philosophy charter, additions audit,
edits audit) found the core faithful — methodology skills byte-identical, no gate weakened — and
the drift concentrated in an unmade identity decision plus writing discipline in the fork-added
skills. Everything that followed is on `dev`, pushed, released as **1.5.0**:

- **`.scratch/philosophy-audit-refinements/`** — spec + 5 tickets, all resolved. ADR 0006
  (in-house identity; assumptions must hold in every install), hook quoting bypass closed with
  the repo's first executable test (`hooks/test_hooks.py`, 49 checks — run it after touching any
  hook), docs tree made internal, single-source-of-truth writing pass. Tickets 02–04 were the
  first real `/delegate` run: three sonnet workers in parallel worktrees, merged `--no-ff` in
  dependency order.
- **`delegate` reworked** (ADR 0007): the toggled session mode is gone — `/delegate` is now a
  bounded on-call run, invoked per frontier, over when drained. Setup asks two questions (Worker
  model; Max concurrent workers). The mode framing had failed observably in its first real use.
- **Design discussion settled** (recorded in ADRs/tickets, not yet all built): autopilot vs
  yolopilot is a coherent 2×2 — merge rights are earned by pre-departure grilling, and the
  ungrilled-unattended-merge corner is deliberately impossible.

**Open, in `.scratch/`:** `hook-claim-false-positive` (agent-ready — the claim hook matched
prose in a commit message; fix test-first), `pilots-docs-heuristic` (agent-ready — landing-vs-
progress wording for both pilots' docs pages), `delegate-wayfinder-composition`
(ready-for-human — needs a grilling session with David).

**Watch out for:** installed plugins snapshot at install — after changing skills, bump the
version (`GITHUB_TOKEN=$(gh auth token) npm run version` — the changelog generator needs the
token) and update installs, or sessions keep loading stale skill text. Worktrees for dispatched
workers can spawn stale; the delegate brief now tells workers to fast-forward first.
