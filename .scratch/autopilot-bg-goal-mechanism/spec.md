Status: resolved

# `autopilot`: restore `claude --bg`, this time to actually self-set `/goal`

## Problem Statement

David wants a genuinely hands-off `autopilot` — zero required keystroke to enter unattended
work. The just-shipped inline design (running in the same session, dispatching chunks as
subagents) can't deliver that: `/goal` turned out to be strictly human-input-only from within an
already-running interactive session, so the inline design's core premise — "`autopilot` sets
`/goal` on itself" — was never actually true. The one thing that does let `/goal` be set
programmatically — passing it as a fresh `claude --bg` session's own launch argument — is exactly
the mechanism the previous revision dropped, for reasons (a redundant survival guarantee, an
apparent network-sandbox cost) that a live test has now shown didn't hold up: the network cost
didn't reproduce on a second run, and nothing in Claude Code's own documentation supports it as a
general property.

## Solution

`autopilot` returns to launching via `claude --bg`, this time for a validated reason instead of an
unverified one: it's the only mechanism that lets `/goal`'s Stop-hook enforcement actually apply
without a human typing anything. The launch argument stays a crisp, evaluable `/goal` condition
with a pointer to `autopilot`'s own `SKILL.md` for the working-loop discipline, rather than
duplicating that discipline into the condition text itself — a lesson learned directly from
watching a bare-condition run skip the branch-then-merge git cycle it was never told about.
`--bg`'s own automatic worktree isolation is documented as a property of the mechanism, not
something `autopilot` builds itself, and it incidentally resolves the "keep chatting here and lose
track of it" risk that originally motivated dropping `--bg` — a separate, `claude
agents`-trackable job doesn't share a window with whatever else the user does next.

## User Stories

1. As David, I want `/autopilot` to require zero keystrokes once the goal is locked, so that
   "hands-off" is actually true rather than needing one more manual step.
2. As David, I want `autopilot` to launch as a `claude --bg` session whose launch argument is
   itself the `/goal` invocation, so that the Stop hook's continuation-forcing actually applies,
   mechanically verified rather than assumed.
3. As David, I want the `/goal` condition to stay crisp and evaluable, not bloated with the full
   working-loop discipline, so that the evaluator's job — judging whether the condition holds —
   stays reliable.
4. As David, I want the launched session to learn the working-loop discipline (git cycle,
   Confidence guideline, `/code-review` gate, `Strong`-only `/re-architect` idle work) by reading
   `autopilot`'s own `SKILL.md` directly, so that behavior stays defined in one place rather than
   duplicated into every goal condition.
5. As David, I want the git cycle stated as a hard rule — never commit directly to `dev`, always
   branch then merge `--no-ff` — rather than descriptive prose, so that a hands-off run doesn't
   quietly skip it the way the live test did when it wasn't told explicitly enough.
6. As David, I want `--bg`'s automatic worktree isolation documented as a property of the
   mechanism, so that a future reader doesn't think `autopilot` has to build isolation itself.
7. As David, I want the separateness a background job provides — its own trackable identity via
   `claude agents`, independent of whatever conversation launched it — named as the actual fix for
   "I keep chatting here and lose track of it," so that the reasoning that dropped `--bg` doesn't
   quietly resurface without addressing why it came back.
8. As David, I want the "dispatch each chunk of work as a background subagent" mechanic removed
   from the working loop, since it existed specifically to force continuation without a
   self-settable `/goal` — `/goal`'s own Stop hook does that job directly once `--bg` is back, and
   keeping a redundant mechanism around is exactly the kind of unexamined leftover this session has
   repeatedly caught and removed elsewhere.
9. As David, I want `.agents/invocation.md`'s "Delegated continuation" section to cite
   `autopilot`'s self-continuation as an example again, since it's true again — restoring what the
   previous revision removed, and dropping the clarifying paragraph that described a case
   `autopilot` no longer is.
10. As David, I want the closing report to go back to being read via `claude agents`/`claude
    logs`, since it's a separate job again, not this same conversation.
11. As a future contributor reading ADR 0005, I want a further dated update note (not a rewrite of
    the previous ones) recording that the network-sandbox cost didn't reproduce and that `/goal`
    turned out to be launch-argument-only — a constraint discovered after the inline revision
    shipped, not something known and ignored.
12. As David, I want the two live dry runs that already happened credited as real evidence already
    gathered, rather than the spec pretending nothing's been tested yet.
13. As David, I want a fresh dry run of the *combined* design — proper `/goal` condition wording,
    the hard git-cycle rule, and the full working-loop discipline together in one run — since no
    single run so far has tested all of those pieces at once.
14. As a teammate discovering `autopilot` for the first time, I want its `SKILL.md` to read as a
    coherent design, not as a record of three iterations layered on top of each other, so that
    reading it doesn't require knowing this history to make sense of it.
15. As David, I want the docs page's FAQ entry about the mechanism's history updated to reflect
    this reversal honestly, rather than leaving the previous "why we dropped `--bg`" answer
    standing as if it were still the final word.
16. As a future contributor, I want the sequence of corrections recorded somewhere, so that a
    future "let's simplify this" pass doesn't re-discover the same dead ends from scratch.
17. As David, I want `CONTEXT.md`'s `Autopilot` entry checked for accuracy against this final
    mechanism, so that the glossary doesn't quietly drift from what's actually shipped a third
    time.

## Implementation Decisions

- `autopilot/SKILL.md`'s "Entering the mode" section rewritten again: after the pre-departure
  grill locks the condition, launch `claude --bg --name "<descriptive name>" "/goal <condition>,
  per skills/engineering/autopilot/SKILL.md's working loop, Confidence guideline, and git cycle"`
  — the launch argument itself, verified to be parsed as a real `/goal` invocation with an active
  Stop hook, not assistant-emitted text.
- The `/goal` condition text stays crisp; the working-loop discipline is referenced by pointer, not
  duplicated into it, so the evaluator's job stays focused and the launched session reads the
  actual `SKILL.md` for the how.
- The working loop's git-cycle step is stated as a hard rule: never commit directly to `dev`;
  always branch, then merge `--no-ff`, push, delete the branch. Adopted per the recommendation
  made in conversation, absent objection — flagged here rather than silently assumed, since it
  wasn't explicitly confirmed before this spec was written.
- The "dispatch chunks as background subagents" mechanic is removed from the working loop. It
  existed specifically to force continuation without a self-settable `/goal`; `/goal`'s own Stop
  hook does that job directly once `--bg` is restored, and no other reason to force subagent
  dispatch survived scrutiny.
- `--bg`'s automatic worktree isolation is documented as an inherent property of the mechanism
  (confirmed via the goal-mechanism-test run), not something `autopilot` sets up — this also
  resolves the earlier "keep chatting here, lose track of it" concern, since a `--bg` job has its
  own separate, `claude agents`-trackable identity independent of the conversation that launched
  it.
- `.agents/invocation.md`'s "Delegated continuation of a user-invoked skill's own process"
  section: restore `autopilot`'s self-continuation as an example (true again now that it's a
  genuinely separate session), and remove the clarifying paragraph added in the previous revision
  that described the same-session case `autopilot` no longer is.
- Closing report: the background session's own final message, read via `claude agents`/`claude
  logs` — reverted from "reopen this same conversation."
- ADR 0005 gets a further dated update note (not a rewrite of either previous one): the
  network-sandbox cost that motivated dropping `--bg` did not reproduce on a second run and isn't
  documented Claude Code behavior; separately, `/goal` was discovered to be strictly
  launch-argument-settable, not self-settable from within an already-running session — a
  constraint not known when the inline revision was written. `autopilot` returns to `claude --bg`
  for this newly-verified reason, not the original, now-superseded survival reasoning.
- `docs/engineering/autopilot.md`'s FAQ entry on the mechanism's history is rewritten to reflect
  this reversal honestly, rather than leaving the previous answer standing as though it were still
  current.
- `CONTEXT.md`'s `Autopilot` entry is checked against this final design and corrected if it's
  drifted (matching the same check done, and found already-satisfied, during the previous
  revision).

## Testing Decisions

- No automated test suite exists for this repo (prose/config, not application code) — same
  precedent as every other spec this session.
- Structural: `claude plugin validate . --strict`.
- Two real dry runs already happened and count as evidence, not just planning: the original
  hooks-dedup test (proved the working-loop shape — code-review, git cycle, closing report — works
  when driven by `claude --bg`, under the old, since-superseded self-set-goal assumption) and the
  goal-mechanism-test (proved `/goal`-via-launch-argument actually works, with a real Stop hook,
  and that the network-sandbox cost doesn't reliably reproduce).
- What hasn't been tested together in one run: the crisp-condition-plus-`SKILL.md`-pointer
  wording, the hard git-cycle rule, and the full working-loop discipline (Confidence guideline,
  `/code-review` gate, `Strong`-only `/re-architect` idle work) all operating in the same combined
  design. A fresh dry run against this combined design is the one thing that actually retires that
  gap — reasoning about the pieces separately isn't a substitute for watching them work together,
  same principle as every other testing decision this session.

## Out of Scope

- Detailed stuck/no-progress heuristics — still parked from the original spec, unaffected by this
  revision.
- The lighter "spontaneous" mode — still parked, unaffected.
- Re-verifying whether the network-sandbox cost is real on a third occurrence — two data points
  (one fail, one pass) aren't enough to settle it either way; revisit only if it recurs.
- Re-litigating whether `--bg`'s survival-across-disconnection guarantee is redundant with tmux —
  it is, and that reasoning from the previous revision's ADR update stands; this spec restores
  `--bg` for a different, additional reason (the only way to self-set `/goal`), not by disputing
  that one.

## Further Notes

- This is the third mechanism revision for `autopilot` in one extended session. Recording the
  sequence plainly rather than only the final answer, per the standing practice this session has
  followed throughout: (1) the original design assumed `claude --bg` was needed for survival;
  (2) a live run succeeded at its task while exposing that survival was redundant with tmux, and
  that `--bg` carried a real-seeming network cost — dropped in favor of running inline; (3) the
  inline design assumed the assistant could self-set `/goal`, which turned out to be false —
  `/goal` is strictly human-input-only from within an existing session; (4) verifying the
  alternative (setting `/goal` via a fresh session's own launch argument) confirmed it works, and a
  second dry run showed the network cost from step 2 doesn't reliably reproduce; (5) `autopilot`
  returns to `claude --bg`, this time because it's the only mechanism that can self-set `/goal` at
  all, not because of the original, redundant survival reasoning.
- The two already-completed dry runs are real primary sources for this design, not hypothetical —
  their transcripts are referenced in the Implementation and Testing Decisions above rather than
  re-described from memory.

## Comments
