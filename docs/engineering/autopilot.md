## What it does

`autopilot` turns a jointly understood outcome into a durable autonomous run. It first grills the
goal, proof, authority, and delivery boundary while you are present; only then does it hand the
contract to [pursue-goal](./pursue-goal.md).

It is a trust level rather than a software pipeline. Research-heavy AI work, an optimization
experiment, and a conventional feature can all enter through the same wrapper because the engine
selects its loop from the uncertainty it encounters.

## When to reach for it

You invoke this by typing `/autopilot` — the agent will not reach for it on its own.

Reach for it when the work may take many steps or sessions, you are available for one serious
understanding round now, and you want the agent to continue from evidence afterward. For a
last-second handoff with no interview, use [yolopilot](./yolopilot.md).

## The goal contract

The leading idea is the **goal contract**: the destination and authority stay stable while the plan
changes. The contract names the observable proof, scope, allowed side effects, git delivery target,
and actions that require you to return.

That is why a spec is optional. A stable, multi-person decomposition may deserve a spec and issues;
open-ended discovery may learn faster through cited research and experiments first.

## Delivery authority

Autopilot may commit and push a feature branch inside the confirmed contract. It may merge into
`dev` only when that exact delivery target was authorized during the understanding session and the
full validation and review gates pass. It never inherits authority over `main`.

An unmet integration gate leaves work on the review branch. That branch stays local unless the
contract separately authorizes pushing it; a fallback is not permission to publish.

## Common questions

**Does Autopilot keep following the plan when research changes the answer?**

No. The plan is provisional. The engine can move between research, discovery, delivery, and
optimization loops while preserving the contract.

**Does it run forever if the target cannot be reached?**

No arbitrary time or token ceiling exists. It stops when the target is proved, the next meaningful
step requires new human authority, or materially different attempts stop changing the evidence.

**Can I keep using the original checkout?**

Yes. Mutating work runs in a linked worktree and feature branch unless the task already has one.
Read-only research can stay in place.

## It's working if

- You approve one compact contract before the durable goal starts.
- The trace changes loops when evidence changes rather than preserving a ceremonial pipeline.
- Every externally visible action is named by the authority contract.
- The receipt proves the stopping condition and points to the exact delivered branch or artifact.

## Where it fits

`autopilot` is the understanding-first autonomous entrance. [pursue-goal](./pursue-goal.md) is its
model-invoked engine; [yolopilot](./yolopilot.md) is the provisional-interpretation sibling. Use
[advise](./advise.md) when you are unsure whether autonomous or interactive work fits.
