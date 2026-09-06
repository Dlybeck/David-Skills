---
name: yolopilot
description: Start an autonomous long-horizon run immediately from a provisional interpretation, then leave a review branch and explain what the run learned.
disable-model-invocation: true
---

# Yolopilot

Enter only through an explicit last-second human handoff. Yolopilot skips Autopilot's understanding
session, so it trades upfront alignment for a narrower delivery boundary and a stronger audit trail.

## Launch without waiting

Run these steps straight through without pausing for a reply:

1. Give a one- or two-sentence warning that the run will act on its own interpretation and invite
   an immediate objection without waiting for one.
2. Inspect the live workspace and state a concise provisional interpretation: objective, proof,
   scope, assumptions, and intended approach.
3. Build the goal contract from that interpretation with this default authority:
   - Allow research, local file changes, tests and evaluations, dependency installation, local
     compute, small feature-branch commits, and a pushed review branch.
   - Keep money, new credentials, production deployment, material deletion, safeguard weakening,
     unrelated scope, integration branches, and `main` outside the contract.
   - Apply any narrower authority the user supplied; defaults cannot override an explicit
     no-push, no-commit, read-only, or other boundary.
4. Invoke `/pursue-goal` immediately with the provisional contract. This is delegated continuation
   of the human-triggered Yolopilot process, not a new invocation of the human-only wrapper.

Refine the plan and working interpretation from evidence. Preserve the original interpretation in
the receipt so the user can see where the run learned or changed direction. Changing the objective
or expanding authority remains a human boundary, even when a broader move looks promising.

## Review-branch boundary

Commit in small, intelligible steps. Before stopping, run the relevant full validation surface and
one `/code-review` over the entire branch, using the provisional contract as the spec. Fix every real
finding, push the feature branch only within the active contract, and leave it unmerged for human
review. With no push authority or no remote, leave the result local and state that limitation.

Yolopilot never merges into `dev` or another integration branch. A later, explicit approval may
authorize the merge as a separate action.

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
