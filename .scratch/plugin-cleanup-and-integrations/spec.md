Status: resolved

# Denali-DEV: fork identity cleanup, personal-git-workflow retirement, Jira + soc2 integration

## Problem Statement

David forked `mattpocock/skills` to get a working engineering-skills practice for Denali fast,
renaming the fork twice along the way (`Denali-Skills-DEV` → `Denali-DEV`, plugin identity
`denali-skills-dev` → `denali-dev`). Two "de-brand" passes had already run before this session,
but both only renamed three skill *command names* — the fork's actual *identity* (its README's
voice, its install instructions, its `CONTEXT.md` title) was still 100% verbatim Matt Pocock
content, including install instructions that silently pointed a Denali engineer at Matt's
unmodified upstream plugin instead of this fork. Separately, the GitHub repo carried 86 stale
branches mirrored in from the original fork, none of them Denali's own work. And two decisions
made *during* the fork — adding a `personal-git-workflow` skill, and never adding first-class
Jira support despite Denali actually using Jira — needed revisiting once actually used: was the
git-workflow skill's teaching prose pulling its weight over the mechanical hook underneath it,
and could Jira become a real option (not forced) for other repos/teammates rather than staying
stuck in the freeform "other" tracker path.

## Solution

Three passes, each verified rather than assumed:

1. **Identity cleanup.** Delete the 86 stale mirrored branches (verified byte-identical to
   `upstream/*`, none of them Denali's own work). Rewrite `README.md`, `CONTEXT.md`, and
   `.agents/install-block.md` so they describe this fork's actual identity and actual install
   path (this fork's own single-plugin marketplace, not Matt's official one) — while keeping
   clear, generous credit to Matt as the original author, not stripping attribution along with
   the branding.
2. **Retire `personal-git-workflow`.** Remove the skill's teaching prose (branch caps,
   staleness audits, merge-vs-PR guidance) entirely. Keep the mechanical enforcement — the
   plugin-root hook blocking any push/PR into `main`, plus four branch-agnostic destructive-op
   blocks — exactly as it was, since it was already independent of the skill by design.
3. **Add Jira as a real `setup` option; add a `soc2` compliance gate.** Jira becomes a
   first-class `setup` tracker choice alongside GitHub/GitLab/local-markdown — not forced on
   anyone, discovered live per-project rather than hardcoded (verified two real Denali Jira
   projects have different issue-type schemes, proving hardcoding would have broken on at least
   one of them). A new `soc2` skill gives an on-demand, deliberately manual gate that defers
   entirely to the existing `denali-soc2-compliance` skill for policy — no duplicated rules, not
   wired into `code-review` automatically, because most work this plugin touches never needs it.

All three passes were verified with `claude plugin validate . --strict` and, for the last two,
an actual two-axis `/code-review` pass (Standards + Spec) against the merge-base — which caught
one real scope-creep finding (an unrequested policy argument added to
`.out-of-scope/mainstream-issue-trackers-only.md`) that was trimmed before merging.

## User Stories

1. As the repo owner, I want the top-level README to describe this fork rather than Matt's
   personal project, so that a teammate opening it understands whose repo this is.
2. As a teammate reading `CONTEXT.md`, I want its title to name this fork, not "Matt Pocock
   Skills", so that the domain doc doesn't misidentify the project at a glance.
3. As a teammate following the install instructions, I want them to install *this fork's*
   plugin, so that I get Denali's own `setup` config and hooks rather than Matt's unmodified
   upstream.
4. As the repo owner, I want Matt credited clearly and generously in the README — his repo
   linked, his site linked, an explicit statement that this fork tracks his `main` via the
   `upstream` remote — so that de-branding the fork's identity doesn't read as erasing where it
   came from.
5. As anyone browsing the GitHub repo, I want its branch list to show only branches that are
   actually this fork's own work, so that 86 stale upstream mirrors don't read as abandoned
   feature work or clutter the branch picker.
6. As the repo owner, I want the `main`-push/PR guard and the four destructive-op blocks to keep
   working exactly as before, so that retiring a skill's teaching prose never silently weakens
   what's actually enforced.
7. As a future reader of `hooks/block-dangerous-git.py`, I want its own comments and error
   messages to be self-contained, so that a removed skill's name doesn't leave a dangling
   pointer in the one place that fires under real conditions (a blocked git command).
8. As the repo owner, I want the `personal-git-workflow` removal recorded as a dated update on
   ADR 0003 (the ADR that already reasons about the hook) rather than as a rewrite of that ADR's
   original decision text, so that the ADR's history stays honest.
9. As a teammate on a different Denali project, I want `/setup` to offer Jira as a real,
   first-class tracker option, so that I don't have to fall back to freeform "other" prose to
   get `to-tickets`/`triage`/`wayfinder` working against Jira.
10. As a teammate whose Jira project has a different issue-type/workflow scheme than another
    Denali project, I want the Jira tracker template to discover that scheme live rather than
    assume a fixed set of names, so that it doesn't break on a project whose scheme differs (as
    verified between two real Denali projects in this session).
11. As a teammate who doesn't want a heavier Jira practice, I want the template's nesting/
    required-fields/audit conventions to be optional, asked-about choices, not defaults baked in
    from one person's personal project.
12. As the repo owner, I want the Jira template to call the Atlassian MCP tools that are
    actually connected in a real session, not tool names copied from a skill that turned out to
    be stale, so that the first real use of this tracker option doesn't fail on a wrong tool
    name.
13. As the owner of a personal, account-specific, hard-scoped Jira skill, I want that skill kept
    entirely out of the shared `denali-dev` plugin, so that its personal assumptions (auto-assign
    to one account, hard-refuse every project but one) never leak into a template meant for
    anyone on the team.
14. As a teammate who wants a SOC2 compliance check on something specific (a diff, a spec, a
    ticket, a wizard script), I want a single command that runs the existing `denali-soc2-
    compliance` policy against it, so that I don't have to remember or re-derive Denali's SOC2
    rules by hand.
15. As the maintainer of Denali's actual SOC2 policy, I want `soc2` to own no policy content of
    its own, so that there's exactly one place the real ruleset can drift, not two.
16. As a teammate on a repo that never touches regulated data, I want `soc2` to stay off by
    default (manual, not wired into `code-review` or `to-tickets`), so that a compliance pass
    doesn't fire as noise on work that doesn't need it.
17. As the repo owner, I want a `.out-of-scope/` policy file to state facts about what shipped,
    not carry an unrequested reinterpretation of upstream's own reasoning, so that a future
    reader isn't handed an argument nobody asked for as if it were part of the original ask.
18. As the repo owner, I want this session's work to leave an actual record in the tracker this
    repo is configured to use — not just conversation and commit messages — so that "what
    happened and why" survives independently of this conversation's transcript.

## Implementation Decisions

- **Branch cleanup**: every `origin` branch except `main`/`dev` was verified byte-identical to
  its `upstream` counterpart (spot-checked four, then confirmed via a full `comm` diff) before
  deletion. `upstream` remains as the read-only path back to all of it if ever needed.
- **Identity rewrite**: `README.md`'s opening pitch, install-command blocks, and its dedicated
  `## Credit` section; `CONTEXT.md`'s title line only (its glossary body is unrelated content,
  untouched); `.agents/install-block.md` rewritten so the fork's own single-plugin marketplace
  is the documented primary route, with Matt's official listing explicitly demoted to "not the
  install story." `.agents/adr/0002` (which documents *Matt's* official-marketplace shipping
  mechanics) got a dated update note rather than a rewrite, clarifying which parts describe
  upstream vs. this fork.
- **`personal-git-workflow` retirement**: the skill and its docs page deleted outright, per this
  repo's own established removal convention (delete, don't archive; name what replaces it in
  the changeset — here, nothing replaces it, the hook already stood alone). Every registry
  reference removed (both bucket README lists, the plugin manifest's skill array, the router
  skill's routing list). The hook's own source comments and blocked-command error messages,
  which previously named the skill for further explanation, were reworded to be self-contained.
  ADR 0003 (the hook's own design record) got a dated update note appended below its original,
  untouched decision text.
- **Jira tracker template**: modeled on the existing GitHub/GitLab seed templates' shape
  (conventions, "as a triage surface," wayfinding operations), but calling the Atlassian MCP
  tools directly by their verified names rather than assuming a name from an unverified source.
  Project-specific facts (project key, site, any nesting/required-field/audit conventions a team
  wants) are `setup`-time questions recorded per-repo, not hardcoded. No "PRs as a request
  surface" flag on this template — Jira has no native pull-request concept, so a repo also using
  GitHub/GitLab for code triages PRs through that tracker's own flag instead.
- **`soc2` skill**: a new user-invoked skill (`disable-model-invocation: true`, matching
  `agents/openai.yaml` policy) that takes a diff/spec/ticket/wizard-script and delegates entirely
  to the `denali-soc2-compliance` skill (a different plugin) for policy content, reporting
  findings verbatim. Deliberately not folded into `code-review` as a third axis, and deliberately
  not model-invoked — both were explicit calls, not defaults.
- **`.out-of-scope/mainstream-issue-trackers-only.md`**: updated to note Jira shipped as a
  first-class template; an initial draft also added an argument reinterpreting the file's public-
  repo-scoped policy reasoning for this private fork — flagged as scope creep by `/code-review`'s
  Spec axis and trimmed back to the factual note only.

## Testing Decisions

- **Structural validation**: `claude plugin validate . --strict` run after every change in this
  spec, before every commit — the cheapest possible check that the plugin/marketplace manifests
  and skill directory structure stay internally consistent.
- **Dangling-reference sweeps**: a full-repo grep for each removed/renamed name (`personal-git-
  workflow`, the old plugin/repo names) after every structural change, confirming the only
  surviving mentions are historical records (`CHANGELOG.md`, ADR original text) rather than live
  pointers.
- **`/code-review`, retroactively**: run properly for the first time this session, two-axis
  (Standards + Spec) against the merge-base, on both of the substantive branches
  (`personal-git-workflow` removal; Jira tracker + `soc2`). This is the prior art this repo's own
  process expects *before* a merge — it ran after, for these two, which is itself one of the
  findings this spec exists to record. It caught one real issue (the `.out-of-scope` scope
  creep) that manual review had missed.
- **Live verification over assumption**: the Jira template's "don't hardcode a scheme" decision
  was tested directly against two real Denali Jira projects (confirmed genuinely different
  issue-type naming), not asserted from general Jira knowledge. The Atlassian MCP tool names
  were verified live in-session (`atlassianUserInfo`, `getVisibleJiraProjects`, etc.) rather than
  trusted from an existing skill's documentation, which turned out to be stale.
- No automated test suite exists for this repo (it's markdown/prose, not application code) —
  "testing" here means the structural/behavioral checks above, plus the two-axis review.

## Out of Scope

- Wiring `soc2` into `code-review` or `to-tickets` automatically — an explicit, deliberate
  non-goal, revisit only as its own future decision.
- Caching a Jira project's discovered issue-type/transition scheme into `docs/agents/issue-
  tracker.md` at `setup` time (discussed as a real gap — live discovery costs an extra tool call
  per operation — but not built; revisit if that cost ever actually becomes a problem).
- Fixing `denali-platform:denali-jira`'s stale tool-name table — a different plugin/repo, flagged
  but not this fork's to edit unilaterally.
- Renaming any *other* existing skill for brevity — raised as a standing preference ("keep names
  shorter, as a greater task") but explicitly not part of this pass; only `soc2` was named short
  from the start.
- Resolving the remaining blank rows in `.agents/phase2-rename-review.md` (most engineering/
  productivity skills still undecided) — out of scope for this pass specifically.
- GitHub Dependabot (2 high, 1 moderate) and `npm audit` findings — explicitly deprioritized by
  the repo owner ("we can probably ignore that").

## Further Notes

- The repo owner's own AIIP-scoped, account-specific Jira skill was provided mid-session,
  installed to `~/.claude/skills/jira/` (personal scope, outside this repo and outside any
  plugin), left byte-for-byte as delivered. It's the source the generalized template's optional
  practices (nesting discipline, ask-don't-guess required fields, comment conventions, audit
  routine) were drawn from — deliberately not copied wholesale, since its literal values (project
  key, transition IDs, custom field IDs, label taxonomy) are specific to one project and one
  account.
- This spec itself is the first real use of this repo's own local-markdown tracker on itself —
  `.scratch/` didn't exist before this file. All work described here is already implemented and
  merged to `dev`; `/to-tickets` will need to mark each resulting ticket resolved rather than
  treat them as a live backlog.

## Comments

- 2026-08-07 — Split into three tickets via `/to-tickets`: `issues/01-fork-identity-cleanup.md`,
  `issues/02-retire-personal-git-workflow.md`, `issues/03-jira-tracker-and-soc2-gate.md`. No
  blocking edges between them — each touched disjoint files with no functional dependency on
  another, confirmed on review. All three marked `Status: resolved`, since all work predates
  this spec and was already merged to `dev`.
- 2026-08-07 — A follow-up `/grill-with-docs` + `/wayfinder` session revisited ticket 03: Jira
  reverted (per-project scheme variance judged not worth the complexity), and GitLab removed
  too (no license) — both decided by actually checking why GitHub/GitLab's uniform CLI shape
  differs from Jira's, not by assumption (the reasoning behind `.agents/adr/0004`). `soc2`
  confirmed to stay, its integration reasoning strengthened. Recorded as
  `issues/04-remove-gitlab-and-jira-strengthen-soc2.md`.
