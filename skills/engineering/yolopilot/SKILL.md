---
name: yolopilot
description: Start an autonomous long-horizon run immediately from a provisional interpretation, then deliver within repository policy and existing authority and explain what the run learned.
disable-model-invocation: true
---

# Yolopilot

Enter only through an explicit last-second human handoff. Yolopilot skips Autopilot's understanding
session, so its objective starts provisional and its default delivery stops at a review branch.
Applicable standing integration grants still apply; skipping grilling creates no new authority.

## Launch without waiting

Run these steps straight through without pausing for a reply:

1. Give a one- or two-sentence warning that the run will act on its own interpretation and invite
   an immediate objection without waiting for one.
2. Inspect the live workspace and state a concise provisional interpretation: objective, proof,
   scope, assumptions, and intended approach.
3. Build the goal contract from that interpretation with this default authority:
   - Allow research, local file changes, tests and evaluations, dependency installation, local
     compute, small feature-branch commits, and a pushed review branch.
   - What is the owner's alone (`/implement`'s "What needs the owner") stays outside the
     contract. Integrate into an agent-owned branch only where repository policy or the owner
     already allows it; otherwise stop at the review branch.
   - Apply any narrower authority the user supplied; defaults cannot override an explicit
     no-push, no-commit, read-only, or other boundary.
   - Preserve any user-supplied deadline and reporting agreement. Resolve a duration once;
     missing timing choices remain unset rather than invented by the provisional interpretation.
4. Invoke `/pursue-goal` immediately with the provisional contract. This is delegated continuation
   of the human-triggered Yolopilot process, not a new invocation of the human-only wrapper.

Refine the plan and working interpretation from evidence. Preserve the original interpretation in
the receipt so the user can see where the run learned or changed direction. Changing the objective
or expanding authority remains a human boundary, even when a broader move looks promising.
Use `/pursue-goal`'s steering discipline when the human checks in: incorporate clear corrections,
retain provisional assumptions as history, and do not turn a question into a changed objective.

## Delivery boundary

Commit in small, intelligible steps. Before delivery, check the change the way `/implement`'s
"Check by judgement" says, using the provisional interpretation and later corrections as the
request. Route the result as `/independent-pr-review` describes: a review branch by default, or
the agent-owned target where policy already allows it. Neither the provisional interpretation
nor the Yolopilot label can widen authority or override an explicit task restriction.

## Postflight

Close with a quick learning digest:

- What Yolopilot initially assumed.
- What it did and what evidence it produced.
- What changed in its understanding.
- What remains uncertain or risky.
- The branch, validation, and review result the user should inspect.

Offer to explain any finding immediately. For durable, multi-session learning, offer `/teach` as an
optional user-invoked next step in a dedicated teaching workspace. Recommend a retrospective spec
only when the run exposed a lasting product decision, unresolved requirement, or coordination need;
routine completed work does not need one.
