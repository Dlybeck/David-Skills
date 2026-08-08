# Map: Team rollout readiness (wayfinder:map)

## Destination

A go/no-go verdict on rolling `denali-dev` out to the AI team as their installed tooling, backed
by a deployment & setup runbook (`docs/agents/deployment.md`) that compares this fork's
install / update / repo-onboarding story to upstream mattpocock/skills — with both install
routes (Claude Code plugin, skills.sh for Codex) verified end-to-end and the plugin-update
nudge mechanized.

## Notes

- Charting decisions (2026-08-08 grilling): audience is the **AI team**, not all of Denali.
  Deliverable is **both** the comparison and the verdict. Comparison dimensions: install +
  update story + `/setup` repo onboarding, with "installs as easily as a plugin, no repo clone
  needed" as the bar. Codex acceptance bar is **parity with upstream's own Codex/skills.sh
  experience**, not parity with the plugin. Update story gets **mechanized** (nudge hook), not
  documented-only. Comparison + runbook live in `docs/agents/deployment.md`; the verdict is a
  moment-in-time call recorded in HANDOFF and this map, not living docs.
- **f9553h4 is a shared machine.** Any install/config experiment must stay inside David's own
  user — isolated `$HOME`-style env (e.g. temp `CLAUDE_CONFIG_DIR`), no system or other-user
  impact.
- David has a Codex account on **another machine**; testing there is a pain, so ticket 05 only
  fires after ticket 02 has triple-checked the route on paper and in a local dry-run.
- Dispatched workers and subagents run on **sonnet** (cost ceiling — no fable subagents).
- Canonical install wording lives in `.agents/install-block.md`; anything the runbook says must
  match it or update it first.
- Tracker conventions: `docs/agents/issue-tracker.md` (commit claims/resolutions immediately).

## Decisions so far

<!-- one line per closed ticket: gist + link -->

- [Private-marketplace update semantics](issues/01-private-marketplace-update-semantics.md) — auto-update exists but defaults off for private marketplaces (official only), `/plugin marketplace update` refreshes the catalog only (plugin content is a per-version snapshot cache, refreshed separately), and GitHub-shorthand adds default to SSH (background auto-update pulls are HTTPS-blind) — this box's actual `denali-dev` marketplace is a local directory source, not the GitHub path the ticket assumed, so ticket 03 must test that path fresh.
- [skills.sh private-repo mechanics](issues/02-skills-sh-private-repo-mechanics.md) — git-clone
  over HTTPS with a 3-tier auth fallback (credential helper → `gh` → SSH), verified working
  end-to-end including `update`; but the documented `--skill=<name>` syntax is silently broken
  (installs everything) and `main` lacks the renamed `setup` skill — checklist targets `#dev`
  with `--skill <name>` (space) until both are fixed/promoted.
- [Sandboxed plugin install test](issues/03-sandboxed-plugin-install-test.md) — GitHub-shorthand
  install works end-to-end over HTTPS **but only pinned to `#dev`**: the unpinned add clones
  `main`, whose manifest still registers upstream's `mattpocock` marketplace, so the documented
  flow fails until promotion. All 29 skills + both hooks verified in the snapshot; updates need
  the qualified `denali-dev@denali-dev` name; snapshot carries 27M of `node_modules` (→ ticket 08).

## Not yet specified

- Whether the update-nudge hook is **built inside this effort** or ticketed as a fast-follow —
  depends on how ticket 04's design lands (size, and whether rollout should wait for it).
- **Teammate-auth validation**: the shared-machine constraint means every test here runs under
  David's (org-owner) auth — the best case. Whether a plain-member teammate's `gh`/git auth
  clears the private-repo paths is unproven until a teammate or second account is available;
  graduates to a ticket when one is.
- Rollout communication — how the team is told to install, and whether that's a doc, a demo, or
  both. May collapse into ticket 06's runbook.

## Out of scope

- **Plugin-parity distribution for Codex** — inventing managed-bundle tooling upstream doesn't
  have. The bar for Codex is upstream parity (charting decision, Q4).
- **Org-wide (all-Denali) rollout** — audience is fixed at the AI team; widening is a fresh
  effort with its own map.
- **The `main` promotion itself** — human-only act, already covered by the 2026-08-08 pre-main
  audit; this map is about what comes after.
