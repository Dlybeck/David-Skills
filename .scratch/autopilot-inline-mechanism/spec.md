Status: resolved

# `autopilot`: drop `claude --bg`, run inline via subagent dispatch + self-set `/goal`

## Problem Statement

David tested `autopilot`'s first real run using `claude --bg`, and the run itself succeeded — but
the underlying justification for using a separate background CLI process turned out to be wrong
for how he actually works. He already runs every session inside tmux and only ever disconnects
via an SSH drop, which tmux already survives with no extra mechanism at all. `claude --bg` paid a
real, confirmed cost for a survival guarantee he didn't need: the background job's own network
sandbox blocked its `git push` over SSH, forcing an HTTPS workaround nothing in the original design
anticipated. Simply dropping the separate process wasn't a clean answer either — David flagged a
real, separate risk: if `autopilot` just ran inline in the conversation he was already using,
continuing to chat in that same session risks either derailing the unattended work or losing track
that it's still running at all.

## Solution

`autopilot` no longer spins up a separate CLI process or window. It keeps running as the same
session it was invoked in, relying on whatever already makes that session durable across
disconnection (tmux, in David's case) rather than providing that guarantee itself. Separateness —
not derailing the loop, not losing track of it — comes from dispatching the actual chunks of work
as background subagents, the same pattern `/code-review` already uses for its two axes, so the
session isn't sitting synchronously blocked and a further turn gets triggered automatically once a
dispatched chunk reports back, with no human needing to be present to trigger it. To close the
real risk of the session pausing to ask "should I continue?" instead of actually continuing,
`autopilot` sets Claude Code's native `/goal` itself, right after the pre-departure grill locks the
condition — nobody types it, and its Stop-hook mechanism forces continuation rather than deferring
to the model's own judgment about whether to keep going.

## User Stories

1. As David, I want `autopilot` to keep running in the same session I invoked it in, so that I
   don't need a separate mechanism just to survive an SSH disconnect tmux already handles.
2. As David, I want the actual chunks of work dispatched as background subagents, so that the
   session isn't sitting there synchronously blocked while a build or review step runs.
3. As David, I want the session to automatically continue once a dispatched chunk of work reports
   back, so that "keep working without me" doesn't quietly stop being true the moment I'm not
   there to prompt the next step.
4. As David, I want `autopilot` to set `/goal` itself, immediately after the pre-departure grill
   locks the condition, so that I never have to type it myself.
5. As David, I want `/goal`'s Stop hook forcing continuation, so that the session doesn't pause and
   ask "should I continue?" instead of actually continuing — a real failure mode, not a
   hypothetical one.
6. As David, I want to be able to keep using other sessions or panes for anything else while
   `autopilot` runs, so that starting it doesn't monopolize my whole workflow.
7. As David, I want `autopilot` to avoid `claude --bg`'s separate network sandbox, so that a
   routine git push doesn't hit an unexplained timeout the way the first real run did.
8. As David, I want whatever a dispatched subagent found to actually show up in `autopilot`'s own
   visible response, so that `/goal`'s evaluator — which only judges what's visible in the
   conversation — has real progress to judge against.
9. As David, I want the closing report to just be this same conversation's own final message, so
   that checking in later means reopening the same thread, not remembering a separate job id or
   running a separate command.
10. As a future contributor reading `autopilot`'s `SKILL.md`, I want the reasoning for why it
    doesn't use `claude --bg` recorded, not just the current behavior, so that a future "let's
    background this for real" suggestion doesn't get re-tried without knowing it was already tried
    and rejected for a documented reason.
11. As a future contributor, I want ADR 0005 to carry a dated update note reflecting this
    correction rather than a rewritten original decision, so that the ADR's own history stays
    honest about what was believed and when.
12. As David, I want `CONTEXT.md`'s `Autopilot` definition corrected away from "backgrounded
    session," since that phrasing is no longer accurate for the default mechanism.
13. As David, I want the `/re-architect` "delegated continuation" reasoning kept exactly as it was,
    since dropping the separate-process step doesn't change anything about that piece.
14. As David, I want this verified with a real run before I trust it the way I now trust the
    original `claude --bg` version, so that a plausible-sounding redesign doesn't ship on reasoning
    alone after everything else this session has been fact-checked rather than assumed.
15. As David, I want the specific unresolved unknown — whether this holds up over a genuinely long
    unattended stretch, not just the few minutes the original test ran — named explicitly as a
    residual risk rather than quietly assumed away.
16. As a teammate on the AI Innovation team who doesn't use tmux, I want to know this design
    assumes an already-durable session, so that I don't invoke `/autopilot` expecting a survival
    guarantee my own setup doesn't actually provide.

## Implementation Decisions

- `autopilot`'s "Entering the mode" section is rewritten: no `claude --bg` launch step. After the
  pre-departure `/grilling` session locks the goal condition and guardrails, `autopilot` runs
  `/goal <condition>` itself, in the current session — a native CLI primitive, not a skill
  invocation, so no `.agents/invocation.md` concern applies to this step. This removes the
  "delegated continuation" citation that previously justified the `claude --bg` seed-prompt step,
  since there is no longer a separate session to justify.
- The working loop's chunks of work (build, `/code-review`, idle-capacity `/re-architect` scan) are
  dispatched as background subagents via the `Agent`/`Workflow` tool, mirroring `/code-review`'s
  own existing pattern of dispatching its Standards/Spec axes as parallel sub-agents. This is what
  keeps the session from sitting synchronously blocked, and is what gets a further turn triggered
  without a human present, via the harness's own automatic task-notification re-invocation.
- `/goal`'s Stop hook is the mechanism that forces the session to actually continue on that
  re-invoked turn rather than pausing to ask permission — documented explicitly as the reason
  `/goal` is kept rather than dropped, since notification-driven re-invocation alone doesn't
  guarantee that.
- Documents explicitly that `/goal`'s evaluator only judges what's visible in the conversation, so
  `autopilot`'s own turns must surface a dispatched subagent's findings, not just act on them
  silently.
- The `/re-architect` "delegated continuation" citation to `.agents/invocation.md` is unchanged and
  kept.
- `claude --bg` is dropped entirely, not kept as a documented alternative. Its only genuine
  benefit (freeing the current pane) is already available more simply by opening another tmux
  window manually; its confirmed cost (a different, more restrictive network sandbox — the
  SSH-push-timeout finding from the first real run) isn't worth carrying as a standing option for
  a benefit that doesn't require it.
- Closing report: unchanged in spirit, corrected in mechanism. It's this same session's own final
  message, read by returning to the same conversation — not via `claude agents`/`claude logs`,
  which only ever applied to the now-dropped `claude --bg` path.
- `CONTEXT.md`'s `Autopilot` entry is reworded away from "backgrounded session" to reflect that
  the default mechanism is the same session, kept going by dispatched subagents and a self-set
  `/goal`.
- ADR 0005 gets a dated update note (not a rewrite) recording this correction. The original
  decision it records (no hard time/token ceiling, Confidence guideline instead) stands unchanged;
  the update note is specifically about the mechanism this spec revises, not that decision.
- This design assumes the invoking session is already durable across disconnection by some means
  outside `autopilot`'s own control (tmux, in this case) — documented as an assumption `autopilot`
  relies on, not a guarantee it provides itself.

## Testing Decisions

- No automated test suite exists for this repo (prose/config, not application code) — same
  precedent as every other spec this session.
- Structural: `claude plugin validate . --strict`.
- Scenario-based dry run, real and live: run `/autopilot` for real on a second small, real task
  and confirm (a) it sets `/goal` itself without being asked, (b) work dispatches as background
  subagents rather than running synchronously inline, (c) the session actually continues
  automatically on re-invocation rather than pausing to ask permission, (d) it survives a
  meaningfully longer unattended stretch than the first test's few minutes, (e) the closing report
  is legible by simply reopening the same conversation.
- The "does this survive a genuinely long unattended stretch" question is named as the one thing
  a single dry run can't fully retire — it proves the mechanism fires correctly, not that it holds
  for hours. Recorded in Further Notes as a residual risk rather than assumed away.

## Out of Scope

- Detailed stuck/no-progress heuristics — still parked from the original spec, unaffected by this
  revision.
- The lighter "spontaneous" mode — still parked, unaffected.
- `claude --bg` as an optional path for users who want the pane freed up — considered and
  explicitly dropped rather than kept as a documented alternative; revisit only if someone hits a
  real case where opening another tmux window manually genuinely isn't sufficient.
- Confirming whether `claude --bg`'s network-sandbox difference is specific to its supervisor
  process or common to all backgrounding mechanisms — moot now that `claude --bg` is dropped
  entirely rather than kept as an option, so this no longer needs resolving.
- Supporting the design for a user without an already-durable session convention (no tmux, no
  equivalent) — out of scope; the design explicitly assumes that durability is provided
  externally, and does not attempt to provide it itself.

## Further Notes

- This spec revises `.scratch/autopilot/spec.md` and `autopilot/01`'s shipped implementation,
  discovered by actually running the original design for real rather than by review. The first
  real-world test succeeded at its own stated goal (the hooks deduplication landed cleanly) while
  simultaneously invalidating part of its own design's justification — both are true at once, and
  both are worth recording plainly rather than only keeping the flattering half.
- The original `.scratch/autopilot/spec.md` is left untouched as the historical record of what was
  believed and why at the time; this spec supersedes its mechanism decisions specifically, not the
  rest of the design — the Confidence guideline, the `/code-review` gate, `Strong`-only
  `/re-architect` idle work, and the autonomous git cycle into `dev` are all unchanged.
- The reasoning that got here arrived in stages, not in one jump: first "tmux already solves
  survival," then "but separateness still has a real risk David named," then "but the existing
  Agent-tool subagent-plus-notification mechanism already solves separateness too, and it's
  already been proven twice in this very conversation," then finally "but dropping `/goal` risks
  losing the anti-stall property nothing else here provides." Recording the sequence, not just the
  final answer, in case this gets revisited again.
- **Residual risk, stated plainly rather than assumed away**: this design has been proven in short
  bursts — two research-subagent notifications a few minutes apart, one live `claude --bg` run
  that finished quickly — never over a genuinely long unattended stretch (hours). Nothing here
  demonstrates the notification-driven loop, or `/goal`'s Stop hook, holds up at that length. The
  live dry run this spec's Testing Decisions calls for is what retires this risk; reasoning about
  the architecture is not a substitute for watching it actually happen.

## Comments
