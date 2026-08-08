# Delegate is an on-call dispatch skill, not a mode

`delegate` shipped as a toggled session mode: `/delegate` turned it on, the session "stayed" in
it, `/delegate` turned it off. Its first real use (2026-08-08, dispatching the
philosophy-audit-refinements tickets) showed the mode framing failing in practice, in three ways
observed directly:

- Every prompt to use it arrived per-work-item, not per-session: the `SessionStart` hook
  recommended it before any tickets existed (it triggers on model match, not work state), the
  assistant pitched it as an `/implement`-stage alternative each time a frontier appeared, and
  `ask-claude` positioned it at the ticket-working step — while the skill's own identity section
  insisted it was "a mode, not a one-off task."
- The mode had an entry trigger but no exit trigger, so it outlived its work: after the frontier
  drained it sat ON and inert, meaning nothing.
- The ON state had no mechanism behind it — "ordinary conversational memory," i.e. the memory of
  having read the skill once. A toggle over nothing: nothing enforced the posture, and nothing
  but recall preserved it across a long session.

## Decision

`/delegate` is a **bounded, on-call dispatch run**: invoke it when a frontier of ready tickets
exists; it claims, dispatches whole tickets to worker subagents, tracks `resolved`, integrates,
and is over when the frontier is drained. Nothing persists between runs. Run it again next time.

Two coherent alternatives were weighed and rejected:

- **Mechanize the mode** (a marker file the toggle writes, a hook re-injecting the Router
  contract each turn). Buildable, but it would be this repo's first per-turn context-injection
  mechanism, invented to preserve a posture whose entire content is "when tickets exist,
  dispatch them" — heavy machinery for a thin posture. Also moot under the chosen design: the
  bounded run has no standing state to mechanize at all, which beats mechanizing it well.
- **Delete the skill entirely** (the harness's orchestration tooling already runs parallel
  agents). Rejected because the tool is mechanism and the skill is process: the frontier scan,
  the committed claim before dispatch (a rule that already failed once and grew a hook), the
  worker brief (delegated `/implement` continuation, fix-review-findings-before-commit,
  fast-forward the stale worktree), and sequential `--no-ff` integration with a disk-vs-HEAD
  check live nowhere else — deleting the skill re-improvises them every session. The line-by-line
  test that came out of this: **house process stays in the skill; orchestration mechanics belong
  to the harness and got deleted** (the "Dispatch mechanism" Setup question and
  "Average agents per phase" config line went with them; Setup now asks two questions with one
  precise unit each — Worker model, and Max concurrent workers as tickets-in-flight-at-once).

The mode was also the sole toggle in the skill set — every other skill is an invoked process,
which is the upstream philosophy this fork tracks. The bounded run restores that shape, and as a
side effect removes the mode's one real asymmetry (orchestration consent outliving the mode it
was granted for — consent is now per-invocation).

The Router contract survives unchanged at every model tier: dispatch whole tickets; never
decompose, never judge a worker's result, never rescue a stuck worker. Judging duplicates the
review the worker already ran with fresh-context sub-agents; safety comes from that review plus
mechanical verification (tests, validation, sweeps), the human gate staying at `main`, and cheap
`--no-ff` revert — never from a second, lower-context opinion in the dispatcher.
