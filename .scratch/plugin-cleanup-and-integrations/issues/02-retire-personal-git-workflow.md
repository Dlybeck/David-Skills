# 02 — Retire personal-git-workflow, keep the main-guard hook standalone

**What to build:** the `personal-git-workflow` skill (teaching prose on branch caps, staleness
audits, merge-vs-PR guidance) is removed entirely. The mechanical enforcement it described —
the plugin-root hook blocking any push or PR into `main`, plus four branch-agnostic
destructive-op blocks — keeps working exactly as before, since it was already independent of
the skill by design (ADR 0003's whole point).

**Blocked by:** None — can start immediately

**Status:** resolved

- [x] Skill folder and its docs page deleted outright
- [x] Every registry reference removed: both bucket README lists, `plugin.json`'s skill array,
      `ask-claude`'s routing list
- [x] `hooks/block-dangerous-git.py`'s own comments and blocked-command error messages reworded
      to be self-contained — no longer name a skill that no longer exists
- [x] `hooks/block-dangerous-git.py`'s actual blocking logic (regexes, branch check, dispatch)
      verified byte-identical before and after — confirmed directly, not assumed
- [x] ADR 0003 given a dated update note below its original, untouched decision text
- [x] Full-repo grep sweep confirms the only surviving mentions of the skill's name are
      historical (`CHANGELOG.md`, ADR original text), not live pointers
- [x] Verified via `/code-review` (Standards + Spec, against the branch's merge-base): 0 findings
      on either axis

## Comments
