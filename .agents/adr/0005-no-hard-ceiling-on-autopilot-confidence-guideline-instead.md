# No hard time/token ceiling on autopilot — the Confidence guideline is the safety net instead

`autopilot` (unattended work triggered by an explicit "I'm leaving, keep working without me")
deliberately carries no automatic time or token cap that force-stops a run. The obvious
alternative — bound every run with a ceiling — was considered and rejected: Denali's AI team
routinely kicks off legitimately long-running work (a multi-hour model refinement job, for
instance) as the actual task, and a blunt ceiling would kill that work exactly when it's doing
what it was asked to do.

The **Confidence guideline** (see `CONTEXT.md`) is the safety net instead: act freely inside the
scope locked by the pre-departure grilling session, or on an existing strong confidence signal;
anything outside that scope, or hard to reverse, gets logged and left for human review rather than
acted on. Stuck/no-progress detection is a related but separate concern, deliberately left for a
dedicated future design session rather than folded in here.

## Update, 2026-08-07: loosen if it can't hold up

David's own caveat going in: this may need loosening later if the guideline can't sustain long,
unsupervised reasoning before getting stuck. Revisit once autopilot has actually run a few times,
not preemptively.

## Update, 2026-08-07: dropped the separate `claude --bg` process, unrelated to the decision above

Autopilot's first real run used `claude --bg` to background itself, on the reasoning that it was
the one mechanism confirmed to survive the user disconnecting. That reasoning didn't hold for how
`autopilot` is actually used: David's own sessions already run inside a terminal multiplexer, and
disconnecting there is an SSH drop, not a terminal close — the multiplexer already keeps the
session alive across exactly that event, with no extra mechanism needed. `claude --bg` was
therefore paying for a survival guarantee that existed already, while introducing a real cost: its
own, more restrictive network sandbox caused a `git push` to time out on that same first real run.

`autopilot` now stays in the session it was invoked in, relying on whatever already makes that
session durable rather than providing that guarantee itself. The separateness `claude --bg` also
happened to provide (not derailing the loop by continuing to chat in the same window) is covered
instead by dispatching each chunk of work as a background subagent and letting the harness's own
notification mechanism re-invoke the session — already proven, independently of this decision,
earlier in the same conversation that surfaced this correction. None of this touches the decision
this ADR actually records: there is still no hard time/token ceiling, and the Confidence guideline
is still the reason why.

## Update, 2026-08-07: `claude --bg` restored — this time to self-set `/goal`, not for survival

The update above dropped `claude --bg` because its survival guarantee was redundant with an
already-standard terminal multiplexer, and because it appeared to cost a more restrictive network
sandbox (a `git push` timeout on the first real run). Both parts of that reasoning have since been
revisited. The network cost did not reproduce on a second live run over the same remote, and
nothing in Claude Code's own documentation supports background sessions having a different
network posture — treat the original finding as unconfirmed, not a property to design around.
Separately, and decisively: `/goal` turned out to be settable only via literal input to a session
— a human typing it, or a fresh session's own launch argument — never by the assistant's own
output from within an already-running session. The inline design assumed the assistant could set
`/goal` on itself; it couldn't, and the "hands-off" property it was meant to provide was never
actually true.

`autopilot` now launches via `claude --bg` with `/goal` as the literal launch argument — verified
directly, with a real Stop hook confirmed active, not inferred. This is the one mechanism that
delivers a genuinely zero-keystroke unattended run. None of this touches the decision this ADR
actually records: there is still no hard time/token ceiling, and the Confidence guideline is still
the reason why.

## Update, 2026-08-08: the fenced `re-architect` bypass, on the record

An audit against upstream flagged that `autopilot` runs `re-architect`'s exploration while
skipping its human-gated pick-and-grill steps — the one place this plugin crosses a human gate
an upstream skill deliberately holds. Recording here that this is intentional and why it's
licensed: the Confidence guideline this ADR establishes is exactly what fences it. Autopilot
acts only on candidates `re-architect` itself scored `Strong` (an existing strong confidence
signal, the guideline's second prong); everything below that threshold is logged for human
review, never acted on. The gate isn't removed — its human side is deferred to the review of
the run's log, the same trade the rest of autopilot makes. Behavior is unchanged by this note;
it exists so the precedent is a documented decision rather than a silent one. If the fence ever
loosens (acting below `Strong`, or skipping another skill's gate), that's a new decision, not
an extension of this note.
