Status: resolved

# `autopilot`: unattended work mode

## Problem Statement

David wants to hand off in-flight work when he's stepping away — "I'm leaving, keep working
without me" — and have real progress keep happening unattended, without either extreme: running
forever burning tokens on a mis-specified goal, or quietly doing something he'd disagree with on
return, with nobody there to catch it. Neither `/goal` alone (session-scoped, no persistence
across disconnection) nor a scheduled/recurring mechanism (which is a different problem —
`loop-me` already owns that) covers this on its own.

## Solution

A new user-invoked skill, `autopilot`. Manually triggered only, never scheduled. Before
departure, it runs a `/grilling` session to lock the goal condition and any scope/token
guardrails. It then launches as a `claude --bg` background agent — the one Claude Code mechanism
confirmed to survive the user disconnecting entirely — driving native `/goal <condition>` so work
continues turn-to-turn without further prompts.

In place of a hard time/token ceiling (rejected — see ADR 0005 — because Denali's AI team
routinely kicks off legitimately long-running work, like a multi-hour model refinement job, as
the actual task, and a blunt cap would kill that mid-flight), `autopilot` is bounded by the
**Confidence guideline** (see `CONTEXT.md`): act freely inside the locked scope or on an existing
strong confidence signal; anything outside that scope, or hard to reverse, gets logged and left in
the closing report rather than acted on.

Each unit of work ends with `/code-review` (fully autonomous — no human needed to run it) and any
real finding gets fixed before it's considered done. Idle capacity goes to tech-debt cleanup via
`/re-architect`'s scan, but only its `Strong`-scored candidates get acted on; `Worth
exploring`/`Speculative` candidates are left in the closing report instead, preserving
`re-architect`'s own pick-and-grill safety valve for anything less than clearly safe.

`autopilot` completes the entire git cycle itself once a unit of work is clean — commit, merge
`--no-ff` into `dev`, push, delete the feature branch — exactly like every other agent-driven
change in this repo. `dev` is the agent's own fully-controlled branch; only `main` is human-gated,
and that's already covered unconditionally by the existing `hooks/block-dangerous-git.py`, with no
changes needed for this feature.

The closing report is `autopilot`'s own final message in the background session, read via `claude
agents` when David checks in — no separate saved file. Git history (commits, the merged branch)
is the durable record of what actually happened; the message is just the human-readable summary of
it.

## User Stories

1. As David, I want to tell Claude "I'm leaving, keep working without me" and have it lock down
   exactly what it's going to do before I go, so that I'm not guessing at scope after the fact.
2. As David, I want the pre-departure conversation to be a real `/grilling` session, not a rubber
   stamp, so that an ambiguous goal gets sharpened before I'm not there to clarify it.
3. As David, I want the work to keep running even after I close my laptop, so that "keep working
   without me" means what it says.
4. As David, I want the mechanism to be a background agent, not a scheduled wake-up loop, so that
   it doesn't burn tokens on periodic re-priming while it's just continuously working.
5. As David, I want `autopilot` to use Claude Code's native `/goal` mechanism for its stopping
   condition, so that the plugin doesn't reinvent turn-continuation logic that already exists.
6. As David, I want there to be no hard time or token ceiling, so that a legitimately long task
   (like a multi-hour model refinement run) isn't killed mid-flight by an arbitrary cutoff.
7. As David, I want `autopilot` to hold back from anything outside what I explicitly agreed to
   before leaving, or anything hard to reverse, so that I don't come back to a surprise I'd have
   pushed back on.
8. As David, I want those held-back items logged clearly rather than silently dropped, so that I
   can pick them up myself instead of them vanishing.
9. As David, I want every unit of work reviewed by `/code-review` before it's considered done, so
   that Standards and Spec violations get caught the same way they would in a session I'm
   watching.
10. As David, I want real findings from that review actually fixed, not just reported, so that
    "unattended" doesn't mean "unreviewed."
11. As David, I want idle capacity spent on tech-debt cleanup via `/re-architect`, so that time
    without an active task isn't wasted.
12. As David, I want `autopilot` to only act on `re-architect`'s `Strong`-scored candidates
    unattended, so that a genuinely judgment-call refactor still waits for me to pick and grill
    it, same as it would in a normal session.
13. As David, I want `autopilot` to complete the whole git cycle itself — branch, commit, merge
    into `dev`, push, cleanup — so that I don't come back to a pile of unmerged branches I have to
    process by hand.
14. As David, I want `dev` treated as the agent's own fully-controlled branch, with no special
    unattended-mode restriction on it, so that `autopilot`'s git behavior matches how every other
    workflow in this repo already works.
15. As David, I want `main` to stay completely off-limits regardless of mode, so that the one hard
    boundary in this repo is never weakened by a new feature.
16. As David, I want `autopilot` to stop and report when it hits a blocker only I can resolve, so
    that it doesn't spin indefinitely on something it genuinely can't get past.
17. As a future contributor reading `CONTEXT.md`, I want "autopilot" defined clearly enough that
    I don't confuse it with a scheduled or time-of-day-triggered mode, so that the name doesn't
    mislead about when it actually runs.
18. As David, I want the closing report to be plain, high-level English — not a technical
    agent-to-agent handoff document — so that I can read it in ten seconds when I check in.
19. As David, I want that report to just be `autopilot`'s own closing message, not a separate
    saved file, so that no new document convention gets invented for something git history already
    records durably.
20. As a teammate on the AI Innovation team who also wants to use `autopilot`, I want it to work
    the same way for me as for David — manual trigger, locked scope, Confidence-guideline-bounded
    — so that it's a real team feature, not tuned to one person's workflow.

## Implementation Decisions

- New user-invoked skill `autopilot` at `skills/engineering/autopilot/` — `disable-model-invocation:
  true` in `SKILL.md`, matching `policy.allow_implicit_invocation: false` in its
  `agents/openai.yaml`, per `.agents/invocation.md`.
- Registry integration: add to `.claude-plugin/plugin.json`'s `skills` array; add a linked entry
  in the top-level `README.md` and `skills/engineering/README.md` (User-invoked section); add
  `docs/engineering/autopilot.md` following `.agents/writing-docs.md`'s four-section template; add
  an entry to `ask-claude`'s `SKILL.md` map, since it's a new user-reachable flow.
- Process: pre-departure `/grilling` session (locks goal condition + scope/guardrails) → launch
  `claude --bg` running `/goal <condition>` → work loop using existing conventions (branch,
  implement, `/code-review` self-fix pass) → idle-capacity `/re-architect` scan, acting only on
  `Strong` candidates → complete the git cycle autonomously (commit, merge `--no-ff` into `dev`,
  push, delete branch) → close with a plain-English summary message.
- Safety model: the **Confidence guideline** (formalized in `CONTEXT.md`) replaces a hard
  time/token ceiling, per ADR 0005. `Autopilot` and `delegate` both answer to the same guideline
  rather than each deriving their own version.
- No changes to `hooks/block-dangerous-git.py` — investigated and explicitly rejected. The
  existing `main`-only gate already covers the one real hard boundary; `dev` is unrestricted for
  the agent, matching this repo's own established practice throughout its history.
- `/implement` gets a small, root-cause addition: mark its ticket's `Status:` line `resolved`
  after `/code-review` and commit. This is a pre-existing gap in the tracker convention (nothing
  currently marks a ticket done) that both `autopilot`'s own work-tracking and, separately,
  `delegate`'s router depend on — fixed once at the source rather than duplicated per consumer.
- Stuck/no-progress detection is explicitly deferred — see Out of Scope.

## Testing Decisions

- No automated test suite exists for this repo (it's markdown/prose, not application code) —
  matches this repo's own established precedent (see `.scratch/plugin-cleanup-and-integrations/spec.md`).
- Structural: `claude plugin validate . --strict` after the new skill folder exists and the
  registry files are updated.
- Scenario-based dry run: invoke `autopilot` against a small, real, low-stakes task. Confirm it
  (a) runs a real pre-departure grilling rather than a rubber-stamp confirmation, (b) survives
  being backgrounded, (c) logs rather than acts on anything outside the locked scope, (d) runs
  `/code-review` and fixes real findings before finishing, (e) completes the full git cycle itself
  with no pending human step, and (f) produces a plain-English closing message.
- Standard `/code-review` (two-axis: Standards + Spec) against the merge-base, on `autopilot`'s
  own implementation branch, before it merges into `dev` — this repo's own established practice.

## Out of Scope

- Detailed stuck/no-progress detection heuristics (what exactly counts as "stuck," how many turns,
  what triggers the blocker exit) — `/goal`'s evaluator only judges its stated success condition
  and has no native "give up" exit. Explicitly parked for its own dedicated future grilling
  session; understood as a special case of the Confidence guideline (low confidence you're headed
  anywhere good), not an unrelated problem.
- A lighter, riskier "spontaneous" mode ("just send it," AI does its best with an upfront warning,
  git-discipline non-negotiable regardless) — a related but separate future addition, explicitly
  parked rather than folded into this spec.
- A persisted report file beyond `autopilot`'s own closing message — revisit only if the
  background-job lifecycle is found in practice to lose messages before David reads them.
- Any change to `hooks/block-dangerous-git.py` — investigated and explicitly rejected during
  grilling (see Implementation Decisions).
- Cloud Routines as an alternative persistence mechanism — surfaced during research as an option
  that survives everything `claude --bg` does, but on Anthropic-managed cloud infrastructure
  rather than this server; `claude --bg` was judged sufficient and simpler for this use case.

## Further Notes

- Corrects an assumption made mid-grilling: an early pass of this design held that merging into
  `dev` should stay a human checkpoint, treating it as the one irreversible unattended action.
  That was wrong — `dev` is already the agent's own fully-controlled branch throughout this
  repo's history (this very session merged multiple feature branches into `dev` autonomously); the
  actual, only hard line is `main`, already covered unconditionally by the existing hook. Caught
  and corrected before any file reflected the wrong assumption.
- Background-agent persistence (`claude --bg`) was chosen over the harness's session-scoped
  `/loop`/`ScheduleWakeup` mechanism specifically because the latter is documented to not survive
  full disconnection — verified directly against Claude Code's own docs during grilling, not
  assumed.
- Shares the Confidence guideline with `delegate` (see that spec) — the same principle, applied to
  a fully unattended context here versus a live, human-present one there.
