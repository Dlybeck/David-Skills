## What it does

`independent-pr-review` checks a complete proposed change for actionable defects using a fresh
[subagent](https://www.aihero.dev/ai-coding-dictionary/subagent) or isolated review session. It reads
the exact committed head, full base diff, and applicable repository guidance without inheriting the
implementation discussion or earlier reviewer conclusions.

## When to reach for it

Type `/independent-pr-review`, or the agent reaches for it after authorized implementation when a
committed proposal needs independent defect review. Local committed branches work before a PR
exists. Use [code-review](./code-review.md) for the separate Standards/Spec axes or uncommitted work.

## Prerequisites

A pinned base and head, settled requirements, source access, and an available fresh reviewer within
the delegation budget. Posting findings requires explicit authority; private review is the default.

## The independent loop

The reviewer reports; the developer repairs and validates. Each repair receives another fresh
full-change review. Authorized intermediate findings go into one consolidated PR comment for the
reviewed head. A clean review produces no PR comment. The settled result reaches you with exact-head
evidence, while scope or approval blockers surface earlier.

## Common questions

**Does this replace Standards and Spec review?**

No. Ordinary defect findings remain separate from those two axes and from developer self-review.

**Will it post findings or merge automatically?**

Commenting depends on the active request's explicit authority. Every main merge requires separate
final human approval; tests and a clean review cannot supply it.

**What if reviewer and developer keep disagreeing?**

The loop preserves the finding and response and brings a genuine deadlock to you. Repeating
unchanged unsupported advice is not progress. You can interrupt the work at any point.

## It's working if

- Review receipts identify the exact head and full comparison, including coverage limits.
- Actionable comments state a precise trigger, impact, location, and evidence.
- Repairs receive a new reviewer; clean passes add no noise to the PR.
- Final delivery states tests, review, and CI separately without claiming universal correctness.

## Where it fits

A standalone review practice and delivery gate for [implement](./implement.md) and the autonomous
pilots. [Code-review](./code-review.md) retains its distinct two-axis purpose;
[advise](./advise.md) maps the flows.
