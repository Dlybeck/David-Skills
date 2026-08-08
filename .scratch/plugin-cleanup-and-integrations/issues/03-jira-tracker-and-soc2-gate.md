# 03 — Add Jira as a first-class setup tracker option, and a soc2 compliance gate

**What to build:** `/setup` offers Jira alongside GitHub/GitLab/local-markdown as a real,
unforced tracker option. A new `soc2` skill gives an on-demand compliance gate that defers
entirely to the existing `denali-soc2-compliance` skill for policy.

Split by scope, integrated vs. kept separate:

- **Integrated into `denali-dev`**: a generalized, shared `issue-tracker-jira.md` template —
  verified Atlassian MCP tool names (not assumed from a source that turned out stale), no
  hardcoded project/scheme (per-project issue-type schemes verified to genuinely differ between
  two real Denali Jira projects), the *shape* of good practice (nesting discipline, ask-don't-
  guess required fields, comment conventions, an audit routine) offered as optional setup-time
  questions rather than baked-in defaults. This is the part any repo or teammate can turn on.
- **Kept separate, not integrated**: the repo owner's own actively-used Jira skill — hard-scoped
  to one project, auto-assigns every issue to his account by design — was not folded into the
  shared plugin. Installed instead to `~/.claude/skills/jira/`, personal scope, outside this
  repo and outside any plugin, left byte-for-byte as delivered. It was the source the
  generalized template's optional practices were drawn from, not a dependency of it.

**Blocked by:** None — can start immediately

**Status:** resolved

- [x] `issue-tracker-jira.md` seed template added, matching the depth/shape of the existing
      GitHub/GitLab templates
- [x] `setup/SKILL.md` and `docs/engineering/setup.md` updated to list Jira as a first-class
      option
- [x] `soc2` skill added: user-invoked (`disable-model-invocation: true`, matching
      `agents/openai.yaml`), delegates entirely to `denali-platform:denali-soc2-compliance` for
      policy content, not wired into `code-review` or `to-tickets` automatically
- [x] Wired into both bucket READMEs, `plugin.json`'s skill array, `ask-claude`'s routing, and a
      docs page per this repo's own writing-docs.md template
- [x] Personal AIIP-scoped Jira skill confirmed absent from this repo's tracked files
- [x] Verified via `/code-review` (Standards + Spec, against the branch's merge-base): 0
      Standards findings needing action; 1 real Spec finding (an unrequested policy
      reinterpretation added to `.out-of-scope/mainstream-issue-trackers-only.md`) — trimmed
      back to the factual note before merging

## Comments

- 2026-08-07 — Jira reverted, along with GitLab (unrelated to this ticket originally, removed in
  the same pass). Further grilling surfaced real reasons beyond "unused": no license for GitLab,
  and Jira's per-project scheme variance made it more complexity than the team wanted to carry.
  See `issues/04-remove-gitlab-and-jira-strengthen-soc2.md` for the reversal itself. The `soc2`
  half of this ticket is unaffected — confirmed to stay, and its integration reasoning was
  strengthened per ADR 0004 (see that ticket).
