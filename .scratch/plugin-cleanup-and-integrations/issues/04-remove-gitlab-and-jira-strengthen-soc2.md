# 04 — Remove GitLab and Jira as setup tracker options; strengthen soc2's integration record

**What to build:** `/setup` offers only GitHub and local markdown as first-class tracker
options — GitLab and Jira both fold back into the freeform "other" path. `soc2`'s docs page
gets its "why is this separate" answer strengthened with the actual pattern-comparison
reasoning (matching `research`'s defer-to-primary-source shape, `wait-what`'s on-demand-only
shape, and `code-review`'s own separated-axes shape), closing the gap a follow-up grilling
session found: `soc2` was reasoned through directly with the user rather than checked against
the plugin's existing patterns first.

This ticket is also the first real case of the standing rule recorded as `.agents/adr/0004`:
analyze an existing pattern's reasoning before building against it. Applied here in reverse — to
a decision about what to *remove*, not add — the same discipline held: GitLab and Jira weren't
cut for being unused, but for concrete reasons (no license; too much per-project variance to be
worth the complexity), reached by actually walking through how GitHub/GitLab's uniform CLI shape
differs from Jira's per-project scheme variance, not by assumption.

**Blocked by:** None — can start immediately

**Status:** resolved

- [x] `issue-tracker-gitlab.md` and `issue-tracker-jira.md` seed templates deleted
- [x] `setup/SKILL.md`, `docs/engineering/setup.md`, `README.md`, `docs/engineering/wayfinder.md`
      updated — every claim that GitLab/Jira "ship as a ready-made template" removed; both
      folded into the "other" path's examples instead
- [x] `.out-of-scope/mainstream-issue-trackers-only.md` reverted to its pre-session text (Jira's
      "shipped as a first-class template" note removed; GitLab's mainstream classification,
      which predates this session, left untouched — its removal was about licensing, not
      mainstream-ness, so it doesn't belong in this file's reasoning)
- [x] `.changeset/jira-issue-tracker.md` deleted outright — documented an addition that never
      reached a release and was reverted in the same unreleased window, so there's nothing to
      record in `CHANGELOG.md`
- [x] Illustrative, non-claim mentions of GitLab left untouched (e.g. `!67` as a merge-request
      reference-format example in `code-review`'s docs; community-usage anecdotes in `triage.md`
      and `wayfinder.md`'s FAQ) — these don't claim first-class support, so reverting the
      feature doesn't make them false
- [x] `docs/engineering/soc2.md`'s "why isn't this a third axis on code-review" answer
      strengthened with the actual pattern comparison, rather than left as a bare assertion
- [x] `.agents/adr/0004` left untouched — its value is specifically as the historical record of
      the Jira episode, true regardless of whether Jira ships now

## Comments
