# 01 — Restore `claude --bg` as `autopilot`'s launch mechanism

**What to build:** `autopilot` launches via `claude --bg` with a crisp `/goal` condition — pointing
to its own `SKILL.md` for the working-loop discipline rather than duplicating it into the goal
text — as the launch argument, verified to actually set a real, Stop-hook-enforced goal (not
assistant-emitted text). The git cycle becomes a hard rule (never commit directly to `dev`); the
now-unnecessary subagent-dispatch mechanic (which existed only to force continuation without a
self-settable `/goal`) is removed; `--bg`'s automatic worktree isolation is documented as a
property of the mechanism, not something `autopilot` builds itself; the closing report reverts to
`claude agents`/`claude logs`; `.agents/invocation.md`'s delegated-continuation citation for
`autopilot`'s self-continuation is restored; ADR 0005 and the docs page are resynced to tell the
corrected story honestly, including the sequence of corrections that got here.

**Blocked by:** None — can start immediately.

**Status:** resolved

- [x] `autopilot/SKILL.md`'s "Entering the mode" section documents launching via `claude --bg`
      with `/goal <condition>, per skills/engineering/autopilot/SKILL.md's working loop,
      Confidence guideline, and git cycle` as the literal launch argument
- [x] The `/goal` condition text stays crisp; working-loop discipline is referenced by pointer to
      `SKILL.md`, not duplicated into the condition
- [x] The working loop states the git cycle as a hard rule: never commit directly to `dev`;
      always branch, then merge `--no-ff`, push, delete the branch
- [x] The "dispatch chunks as background subagents" mechanic is removed from the working loop
- [x] `--bg`'s automatic worktree isolation is documented as an inherent property of the
      mechanism, including that it resolves the earlier "keep chatting here, lose track of it"
      concern via a separate, `claude agents`-trackable identity
- [x] `.agents/invocation.md`'s "Delegated continuation" section cites `autopilot`'s
      self-continuation as an example again; the same-session clarifying paragraph added in the
      prior revision is removed
- [x] Closing-report guidance reverted: read via `claude agents`/`claude logs`, not by reopening
      the same conversation
- [x] `.agents/adr/0005-no-hard-ceiling-on-autopilot-confidence-guideline-instead.md` gets a
      further dated update note (not a rewrite of either previous one) recording that the
      network-sandbox cost didn't reproduce and that `/goal` is launch-argument-only, not
      self-settable from within an existing session
- [x] `docs/engineering/autopilot.md`'s FAQ entry on the mechanism's history is rewritten to
      reflect this reversal honestly, not left standing as the previous answer
- [x] `CONTEXT.md`'s `Autopilot` entry checked against this final design and corrected if drifted
      — checked, already accurate (never mentioned a specific mechanism), no change needed for
      the second time running
- [x] `claude plugin validate . --strict` passes

## Comments

- 2026-08-07 — `/code-review` (Standards axis) caught a real copy-paste bug in `.agents/
  invocation.md`: the removed clarifying paragraph was replaced with a duplicate of the section's
  own closing sentence, rather than a clean removal. Fixed. Also caught a genuine definitional
  inconsistency the restored citation reintroduced: the section's opening sentence says a worker
  carries out "a process a *different* user-invoked skill describes," but `autopilot`'s
  self-continuation example isn't cross-skill — it's `autopilot`'s own process, continued by a
  separate session. This inconsistency existed in the very first version of this section too; it
  just went unnoticed until now. Fixed the definition itself (not just reverted the wording) to
  honestly cover both the cross-skill case and the self-continuation case, rather than reproducing
  a latent bug a second time.
- 2026-08-07 — `/code-review` (Spec axis) caught something more consequential: the `/goal` launch
  argument as first written appended a trailing "per SKILL.md's working loop..." pointer clause
  onto the condition, untested — the live goal-mechanism-test that proved this mechanism only ever
  used a bare condition. Since the whole string after `/goal ` becomes the enforced condition
  (confirmed from that same test's transcript), a pointer the evaluator can't actually resolve
  risked being the only place the hard git-cycle rule lived. Fixed by stating the checkable
  essentials — the git cycle, the review gate — directly in the condition text itself, where the
  evaluator can judge them plainly; the `SKILL.md` pointer stays, but only for the working
  session's own benefit, not as something the evaluator depends on.
- 2026-08-07 — Also flagged, not fixed here, matching this ticket's own established precedent for
  deferred verification: the spec's Testing Decisions called for a fresh dry run of the *combined*
  design (this exact condition wording, the hard git-cycle rule, and the full working loop
  together) — that run hasn't happened yet. Two prior runs each proved one piece; neither proves
  this combination. **The combined dry run is still owed, not done.**
