## What it does

`independent-pr-review` checks a complete proposed change for actionable defects using a fresh
[subagent](https://www.aihero.dev/ai-coding-dictionary/subagent) or isolated review
[session](https://www.aihero.dev/ai-coding-dictionary/session). It reads
the exact committed head, full base diff, and applicable repository guidance without inheriting the
implementation discussion or earlier reviewer conclusions.

## When to reach for it

Type `/independent-pr-review`, or the
[agent](https://www.aihero.dev/ai-coding-dictionary/agent) reaches for it when the task fits.

| Situation | Review practice |
| --- | --- |
| A committed change that could really hurt something, or you ask for a review | `independent-pr-review` |
| A small change | Its tests, run by whoever built it; no reviewer needed |
| Separate Standards/Spec checks, including uncommitted work | [code-review](./code-review.md) |

## Prerequisites

A pinned base and head, settled requirements, source access, and an available fresh reviewer within
the delegation budget. Posting findings requires explicit authority; private review is the default.

## Fixing what it finds

The reviewer reports; whoever built the change fixes it and checks the fixes. A second full review
happens only when the fixes changed what was reviewed, never as a matter of course: each round
costs time and money, and depth is no substitute for judging what could break. Authorized
findings go into one consolidated PR comment; a clean review posts nothing.

## The promotion PR

Where `main` is human-owned and `dev` is agent-owned, finished work reaches you as one open PR
from `dev` into `main`. The agent opens or updates it when you ask for a release, after checking
one pinned `dev` SHA: pushed, tests passing, CI green. The report says, for each piece of work,
what was asked, what changed, how it was checked, and what's left open, and lists anything else on
`dev`. When you comment, the agent fixes it through `dev`, which updates the same PR, and replies
on each thread with `🤖 Agent:`. You merge with **Create a merge commit**. The steps live in
[promotion PR](../../skills/engineering/independent-pr-review/references/promotion-pr.md).

## Common questions

**Does this replace Standards and Spec review?**

No. It hunts defects; [code-review](./code-review.md) checks standards and the request. Neither
runs on every change: the builder judges what the change needs.

**Will it post findings or merge automatically?**

Commenting depends on the active request's explicit authority. Delivery follows repository branch
ownership and applicable standing grants once its checks pass; explicit task restrictions win.

| Boundary | Settled result |
| --- | --- |
| Authorized agent-owned integration | Complete and verify integration without repeat approval |
| Human-owned promotion | Request its stated human decision on the exact proposal |
| Missing policy or authority | Preserve a reviewable result and identify the dependent decision |

Tests and clean review cannot supply authority. Installation remains separate: updated source
does not prove an active installed skill changed.

**Can an agent merge the promotion PR, even by accident?**

Not through any command the plugin hook can read. It lets agents open the PR only from head `dev`.
It blocks `gh pr merge` and auto-merge into `main` (and blocks them too when the base can't be
checked), along with `gh api` merges and ref writes, gh aliases, and force-pushes of `dev`. The
one write it lets through is creating a `main` that does not exist yet, with a plain `gh api`
call that GitHub itself rejects if the branch is already there. The
hook reads command text, so a command built at runtime or run from a script is outside what it
sees. For a hard guarantee, use branch protection on `main`, which you set on GitHub. Squash or
rebase merges make the release refuse, so use **Create a merge commit**.

**What if reviewer and developer keep disagreeing?**

The developer keeps the finding beside its answer and brings you a real deadlock. Another round
of the same review is not progress. You can interrupt the work at any point.

## It's working if

- Review receipts identify the exact head and full comparison, including coverage limits.
- Actionable comments state a precise trigger, impact, location, and evidence.
- Small changes ship on their tests; fixes are checked, not re-reviewed in full; clean passes add no noise to the PR.
- Final delivery states tests, review, and CI separately without claiming universal correctness.
- There is never more than one open promotion PR, its head matches `dev`, and every review comment
  you sent back has a `🤖 Agent:` reply naming its commit.

## Where it fits

The fresh eye that [implement](./implement.md) and the autonomous pilots bring in when a change
earns it. [Code-review](./code-review.md) retains its distinct two-axis purpose;
[advise](./advise.md) maps the flows.
