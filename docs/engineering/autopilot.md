## What it does

`autopilot` turns a jointly understood outcome into a durable autonomous run. It first grills the
goal, proof, authority, and delivery boundary while you are present; only then does it hand the
contract to [pursue-goal](./pursue-goal.md).

It is a trust level rather than a software pipeline. Research-heavy AI work, an optimization
experiment, and a conventional feature can all enter through the same wrapper because the engine
selects its loop from the uncertainty it encounters.

## When to reach for it

You invoke this by typing `/autopilot` — the agent will not reach for it on its own.

Reach for it when the work may take many steps or sessions and you want the agent to continue
from evidence after an understanding session. [Attention modes](../productivity/attention-modes.md)
keeps that session usable when you can answer only briefly: On the side starts with the most
consequential missing intent or boundary. For a last-second handoff with no interview, use
[yolopilot](./yolopilot.md).

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

## Independent delivery review

Completed committed proposals also use [independent-pr-review](./independent-pr-review.md).
A fresh reviewer checks the full base diff without implementation history; the developer repairs
and tests within scope, then receives another fresh review. Ordinary findings remain separate from
Standards/Spec. Authorized actionable comments are consolidated; clean reviews stay quiet.
The settled PR follows exact-head checks, while material blockers surface earlier. Review never
supplies posting or merge authority.

## Common questions

**Do I need to answer every technical question before leaving?**

No. The understanding session resolves consequential human decisions, reuses existing answers,
and leaves delegated technical choices to the agent. Depth follows the ambiguity, not a fixed
question count. If you leave before the contract is complete, the agent can continue useful work
within existing authority; Autopilot starts its durable goal only after the compact contract is
confirmed. A clear "just go" can confirm the concrete contract immediately before it, but cannot
fill in permissions or product choices that were never stated.

Routine local toolchain and dependency setup belongs to an implementation and test goal unless
you exclude it. A standing grant already available in the conversation or durable instructions
does not need to be requested again for each task.

**Can I change direction while it works?**

Yes. Ordinary corrections flow through [pursue-goal](./pursue-goal.md), which updates the working
understanding and accounts for affected work. A check-in does not require restarting the interview.

**Does Autopilot keep following the plan when research changes the answer?**

No. The plan is provisional. The engine can move between research, discovery, delivery, and
optimization loops while preserving the contract.

**Does it run forever if the target cannot be reached?**

It stops when the target is proved, authority is missing, evidence plateaus, or your agreed
deadline arrives. A run without a deadline keeps the existing open-ended behavior.

**Can I give it a deadline and get reports while it works?**

Yes. Include those choices in the contract: a fixed endpoint, milestone reports, and a maximum
reporting gap such as 45 minutes. A short update still appears when little has changed. The agent
gets time facts and chooses its own approach. Exact delivery during waits and stopping at the
endpoint depend on verified runtime support; hooks alone cannot interrupt a running command.

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
