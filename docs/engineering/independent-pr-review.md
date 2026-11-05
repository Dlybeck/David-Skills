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
| Committed proposal needing fresh actionable defect review, with or without a PR | `independent-pr-review` |
| Separate Standards/Spec checks, including uncommitted work | [code-review](./code-review.md) |

## Prerequisites

A pinned base and head, settled requirements, source access, and an available fresh reviewer within
the delegation budget. Posting findings requires explicit authority; private review is the default.

## The independent loop

The reviewer reports; the developer repairs and validates. Each repair receives another fresh
full-change review. Authorized intermediate findings go into one consolidated PR comment for the
reviewed head. A clean review produces no PR comment. The settled result reaches you with exact-head
evidence, while scope or approval blockers surface earlier.

## The promotion PR

Where `main` is human-owned and `dev` is agent-owned, finished work reaches you as one open PR
from `dev` into `main`. The agent opens or updates it only when you or the TPM paste a ready
signal, after it checks one pinned `dev` SHA: pushed, tests passing, CI green, the task merged in,
no open findings. The report gives each task what you asked for, the plan you okayed, your calls along the way,
what changed, how that differs from the plan, how it was tested, and what's left open. It lists anything else on `dev`, and ends with a prompt you can paste into
a fresh cloud review session that checks each task against your plan. Your comments come back as a pasted review fix. The agent fixes
them through `dev`, which updates the same PR, and replies on each thread with `🤖 Agent:`. You
merge with **Create a merge commit**. The steps live in
[promotion PR](../../skills/engineering/independent-pr-review/references/promotion-pr.md).

## Common questions

**Does this replace Standards and Spec review?**

No. Ordinary defect findings remain separate from those two axes and from developer self-review.

**Will it post findings or merge automatically?**

Commenting depends on the active request's explicit authority. Delivery follows repository branch
ownership and applicable standing grants after all gates pass; explicit task restrictions win.

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

The loop preserves the finding and response and brings a genuine deadlock to you. Repeating
unchanged unsupported advice is not progress. You can interrupt the work at any point.

## It's working if

- Review receipts identify the exact head and full comparison, including coverage limits.
- Actionable comments state a precise trigger, impact, location, and evidence.
- Repairs receive a new reviewer; clean passes add no noise to the PR.
- Final delivery states tests, review, and CI separately without claiming universal correctness.
- There is never more than one open promotion PR, its head matches `dev`, and every review comment
  you sent back has a `🤖 Agent:` reply naming its commit.

## Where it fits

A standalone review practice and delivery gate for [implement](./implement.md) and the autonomous
pilots. [Code-review](./code-review.md) retains its distinct two-axis purpose;
[advise](./advise.md) maps the flows.
