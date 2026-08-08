Status: resolved

# Philosophy audit refinements: declare the fork's identity, fix the drift the audit found

## Problem Statement

David forked `mattpocock/skills` for two reasons: focus the set on Denali's AI team's work, and
extend it to mesh with Denali's existing practices — while matching the original's methodology as
closely as possible, because that methodology is the best available. A full three-way audit
(upstream philosophy distilled from `upstream/main`; the fork's additions; the fork's edits to
shared skills) confirmed the core is faithful: the methodology skills are byte-identical to
upstream, no phase gate or STOP rule was weakened, and the two deliberate divergences (always-on
hooks, the unattended tier) are ADR-documented in exactly the analyze-before-diverging way ADR
0004 demands.

But the audit also found real drift, concentrated in two places. First, an unanswered identity
question: the README claims a portable skills collection, while `autopilot`/`yolopilot` and the
hooks quietly assume Denali's own environment (a `dev` integration branch, this repo's file
layout, plugin-only hook delivery). Every portability finding is a symptom of that unmade
decision. Second, the new skills' *writing* drifts from the repo's own `writing-for-agents`
discipline: duplicated definitions where upstream demands a single source of truth, negation
density far above any upstream skill, and in-body design justification that belongs in ADRs.
There are also concrete defects: docs-page links that point at `aihero.dev` URLs that don't
exist, a literal repo path in `autopilot`'s launch string that only resolves in this checkout,
a pointer to a `.scratch/` file no install ships, and a quoting bypass in
`block-dangerous-git.py` — the mechanical guard for a rule that already failed once as prose.

## Solution

Make the identity call explicit, then fix everything downstream of it. David's decision: this
plugin is **Denali's in-house practice**, forked from upstream — not a portable collection with
a Denali layer. An ADR records that, and the README stops claiming otherwise. With that settled,
the Denali-specific assumptions (`dev` branch, always-on hooks) stay assertive and get *stated*
rather than generalized away; only the outright lies get fixed — the dead docs URLs, the
checkout-relative path in the launch string, the pointer to an unshipped file. The writing drift
is repaired per the repo's own `writing-for-agents` rules: one owner per fact, prohibitions
converted to positive phrasing except at genuine hard guardrails, justification moved to the
ADRs that already exist. The hook quoting bypass is closed and — because this is a true rule
David added, one that exists precisely because prose enforcement failed — it gets the repo's
first executable test, at the hook's existing stdin→exit-code contract.

## User Stories

1. As the repo owner, I want an ADR declaring this plugin encodes Denali's in-house practice, so
   that every future addition has a ruling on "generalize or assume Denali" instead of each
   author guessing.
2. As a teammate reading the README, I want its framing to match what the skills actually
   assume, so that I'm not promised portability the unattended tier doesn't deliver.
3. As a teammate on a repo without a `dev` branch, I want `autopilot`'s and `yolopilot`'s docs
   pages and prerequisites to state the `dev`-integration-branch assumption plainly, so that I
   find out before an unattended run, not during one.
4. As an unattended autopilot run launched from a plugin install, I want the `claude --bg`
   launch argument to carry its instructions as content rather than a path into this repo's
   checkout, so that the goal resolves no matter where the skill physically lives.
5. As an autopilot session consulting its own guardrails, I want the run's Out of Scope
   guidance owned by material every install ships, so that the skill never points at a
   `.scratch/` file that only exists in this repo.
6. As the repo owner, I want `git push origin "main"` (and other quoted or equivalent spellings)
   blocked exactly like `git push origin main`, so that the mechanical guard can't be sidestepped
   by trivial re-quoting.
7. As the maintainer of a true, mechanized rule, I want an executable test feeding the hook
   real payloads and asserting allow/block per case, so that the one enforcement mechanism in
   the repo is itself protected against regression.
8. As a future editor of any hook, I want the test to cover the fail-open contract (malformed
   stdin exits 0, silently), so that a hook bug can never lock up normal sessions.
9. As a reader of any fork docs page, I want every cross-link to resolve, so that the docs tree
   meets its own `writing-docs.md` bar ("every link is absolute, and every one resolves").
10. As the repo owner, I want the docs-URL convention re-declared as internal (repo links), so
    that `CLAUDE.md` and `writing-docs.md` stop describing a publishing pipeline this fork
    doesn't have.
11. As an agent loading `CONTEXT.md`, I want the Confidence guideline defined in exactly one
    place with pointers everywhere else, so that the definition can't drift into six diverging
    copies.
12. As an agent reading the local-tracker seed template in a fresh repo, I want the
    commit-before-dispatch rule stated as the generic git truth it is, so that harness-specific
    mechanics don't ride along into every consumer repo's config.
13. As an agent following `delegate`, I want its instructions phrased as positive behavior
    wherever the behavior has a positive phrasing, so that the skill steers by target rather
    than by elephant.
14. As a future maintainer, I want the design arguments currently living inside skill bodies
    moved to (or deduplicated against) their ADRs, so that process files state process and the
    why lives where the repo says it lives.
15. As a reader of `delegate`'s SKILL.md, I want its `## Common questions` section gone, so that
    docs-page material lives only on the docs page that already carries it.
16. As the repo owner, I want `delegate-recommend.py` covered by a dated ADR 0003 update like
    its two sibling hooks, so that no hook ships without a recorded decision.
17. As a future reader of ADR 0005, I want autopilot's fenced bypass of `re-architect`'s
    human-gated steps recorded as a dated note, so that the one place the fork crosses an
    upstream human gate is a documented precedent, not a silent one.
18. As a teammate scanning the engineering README, I want the model-invoked list unbroken and
    headings consistently cased, so that registry surfaces stay clean.
19. As a user reading frontmatter descriptions in pickers and READMEs, I want `autopilot`'s and
    `yolopilot`'s descriptions near upstream's one-short-line discipline, so that the four
    places each string is pasted stay scannable.
20. As the repo owner merging upstream regularly, I want all of these fixes to land without
    touching upstream-owned skill bodies, so that future `git merge upstream/main` runs stay
    as quiet as the audit found them.

## Implementation Decisions

- **Identity ADR (0006).** Records the call made in this session: the plugin encodes Denali's
  in-house practice. Names what that licenses (assuming `dev ← feature/**` with `main`
  human-gated; always-on plugin-root hooks; Denali-specific skills) and what it does not
  (checkout-relative paths, pointers to unshipped files, dead URLs — assumptions must be *true
  in every install of this plugin*, not just in this checkout). README's framing sentence
  updated to match; the Credit section is untouched.
- **Autopilot/yolopilot keep `dev`, lose the checkout paths.** The integration branch stays
  hardcoded — that's now a declared house assumption — but each skill states it as a
  prerequisite (SKILL.md and docs page). The launch argument is rebuilt to carry the goal
  condition and guardrails inline as content; the Out of Scope guidance moves from the
  `.scratch/` spec pointer into the skill's own body, which every install ships.
- **Hook fix + first executable test.** `block-dangerous-git.py` normalizes shell quoting on
  tokens before pattern-matching, closing the `"main"` bypass for both the push and PR
  patterns. A test script (Python standard library only, same no-dependency discipline as the
  hooks themselves) drives each hook as a subprocess through its existing contract — JSON on
  stdin, allow/block via exit code — over a table of cases: plain, quoted, and
  interpolation-adjacent spellings that must block; feature-branch pushes and the four
  destructive-op patterns' safe lookalikes that must pass; malformed stdin that must fail open.
  Runnable directly (`python3 <test file>`), no framework, no new dependencies.
- **Docs links become internal.** Every fork-added or renamed docs page's cross-links point at
  repo-relative paths; `writing-docs.md` and `CLAUDE.md`'s published-URL convention is rewritten
  to say the docs tree is internal, with the aihero.dev note kept only as the historical origin
  of the format. Upstream-named skills whose aihero.dev pages genuinely exist may keep those
  links where they refer to Matt's published writing rather than to this fork's pages.
- **Single source of truth restored.** The Confidence guideline's full definition lives in
  `CONTEXT.md` alone; `autopilot`, `yolopilot`, `ask-claude`, and both docs pages carry a
  pointer plus at most a one-clause gloss. The worktree-from-last-commit fact is owned by the
  tracker doc convention; the seed template keeps the generic git truth (dispatched work starts
  from the last commit, so commit claims/resolves immediately) without naming `claude --bg` or
  `Workflow`; the hook docstring and `delegate` reference the convention instead of restating
  it.
- **Negation and justification pass.** `delegate` and `yolopilot` prohibitions are rephrased
  positively where a positive phrasing exists; the genuine hard guardrails (Router never
  decomposes/judges/rescues; yolopilot never merges into `dev` unattended) stay as prohibitions
  paired with their positive counterpart, per `writing-for-agents`' own exception. In-body
  design arguments ("confirmed the hard way", prior-art asides) are cut where an ADR or
  changeset already carries them; anything not yet recorded moves into the relevant ADR as a
  dated note.
- **Mechanical cleanups.** `delegate`'s `## Common questions` section deleted (docs page owns
  it). `soc2`'s docs H1 recased to match siblings. The stray blank line in the engineering
  bucket README removed. `autopilot`/`yolopilot` frontmatter descriptions trimmed toward one
  line, with the same trimmed string propagated to both READMEs and `CONTEXT.md`.
- **ADR bookkeeping.** ADR 0003 gains a dated update covering `delegate-recommend.py` (third
  hook, informational-only, fail-silent). ADR 0005 gains a dated note recording the fenced
  `re-architect` gate bypass as deliberate: `Strong`-scored candidates only, everything else
  logged for review — behavior unchanged, now on the record.
- **Upstream-owned skill bodies stay untouched.** All edits land in fork-added skills, fork
  docs, hooks, seed templates, `.agents/` records, and registry surfaces — preserving the
  audit's headline property that shared-skill diffs stay merge-quiet.

## Testing Decisions

- A good test here exercises external behavior at an existing seam and never implementation
  details: the hook tests assert only the contract Claude Code itself uses — JSON in, exit
  code out — never the script's internal pattern list or function names.
- **Hook tests** are the repo's first executable tests and the only automated ones this spec
  adds: table-driven cases through the subprocess seam for `block-dangerous-git.py` (quoted and
  unquoted push/PR spellings, safe feature-branch pushes, the four destructive-op patterns and
  near-miss lookalikes like `feature/main-page`, malformed stdin failing open). Prior art: none
  in this repo — the discipline for what makes the cases good is upstream's `tdd` reference on
  behavior-not-implementation.
- **Structural validation**: `claude plugin validate . --strict` after any change touching
  manifests or skill directories, before each commit — same as every prior pass.
- **Reference sweeps**: full-repo greps proving the drift is actually gone — no surviving
  `aihero.dev/skills-` link to a nonexistent page, exactly one full definition of the
  Confidence guideline, no `claude --bg`/`Workflow` mentions in seed templates, no
  `## Common questions` inside any SKILL.md, no checkout-relative launch paths.
- **Link resolution**: every docs link touched by the internal re-pointing is verified to
  resolve to a real file in the repo.

## Out of Scope

- Generalizing `autopilot`/`yolopilot` to arbitrary branch models — the identity decision
  explicitly licenses the `dev` assumption; revisit only if the plugin ever ships outside
  Denali.
- Closing ADR 0003's known `skills.sh` gap (hooks don't ship to non-plugin installs) — the gap
  stays named, not fixed; a Codex-side equivalent remains its own future investigation.
- Changing the `re-architect` bypass behavior itself — this spec documents it; loosening or
  tightening the fence is a separate decision after autopilot has more real runs (per ADR
  0005's own revisit note).
- Stuck/no-progress detection for unattended runs — deliberately deferred by ADR 0005,
  unchanged here.
- Publishing the docs tree anywhere public, or building any docs pipeline.
- Contributing generalized pieces (the claim/resolve/frontier tracker conventions, the
  `implement` ticket-resolution step) back upstream — worth considering someday, not this pass.
- Any edit to upstream-owned SKILL.md bodies, including trimming `ask-claude`'s inherited
  router prose beyond the fork-added unattended section.

## Further Notes

- The audit itself (three parallel reviews: upstream philosophy charter, additions audit,
  edits audit) lives in this conversation; its ranked findings map to this spec's decisions
  one-to-one. The headline finding worth preserving: the fork's shared-skill surface is
  byte-identical to upstream at the core, and this spec deliberately keeps it that way.
- House practice for landing: separate chore/feature branches into `dev` per finding cluster,
  `--no-ff`, with `/code-review` before merge — the same flow the last spec's comments record.
- The hook test file is a precedent: any future hook lands with cases added to it. Worth a
  line in ADR 0006 or the hooks' own docstrings so the precedent is discoverable.

## Comments

- 2026-08-08 — Split into five tickets via `/to-tickets`: `issues/01-record-the-decisions.md`,
  `issues/02-hook-bypass-and-first-test.md`, `issues/03-unattended-tier-declares-assumptions.md`,
  `issues/04-docs-tree-goes-internal.md`, `issues/05-writing-pass.md`. Edges: 03 and 04 blocked
  by 01 (they cite ADR 0006's ruling); 05 blocked by 03 and 04 (file contention on the same
  skill bodies and docs pages, not logical dependency). Frontier at publish: 01 and 02 in
  parallel.
- 2026-08-08 — All five tickets resolved. 01 implemented in-session; 02/03/04 dispatched in
  parallel to sonnet workers via `/delegate` (isolated worktrees, merged `--no-ff` in order);
  05 dispatched after 03+04 merged. Post-merge verification each round: hook test suite green
  (49/49), `claude plugin validate . --strict` passing, disk-vs-HEAD spot checks. One incident
  worth a future look: the `require-committed-claim` hook false-positived on the literal string
  "claude --bg" inside a commit *message* (not a dispatch), forcing worker 05 to fold its
  commits into one.
