## What it does

`delegate` runs one bounded dispatch pass over your ticket frontier: each ready [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket) is claimed on the tracker, handed whole to a worker [subagent](https://www.aihero.dev/ai-coding-dictionary/subagent), tracked until its status flips to `resolved`, and integrated — and the run is over when the frontier is drained. Nothing stays on afterward; there is no mode and no toggle.

The dispatching session acts strictly as a **Router**: it classifies and hands off. It never decomposes a ticket into subtasks it invented, never judges a worker's partial result, and never tries to recover a stuck worker — at any model tier. Withholding those duties is the whole point of the design.

## When to reach for it

You invoke this by typing `/delegate` — the agent won't reach for it on its own, and it ships with `disable-model-invocation: true`. Reach for it when the tracker holds ready, independent tickets and you want the dispatching off your plate. It pays off two different ways:

| Your session's model | What the run buys you |
| --- | --- |
| Light | Heavy work happens on heavier workers; your session stays cheap |
| Heavy | Tickets land in parallel, and your session's context stays clean for judgment work |

Each invocation is its own run. Next time a frontier exists, type it again.

## Prerequisites

The issue tracker should already be configured by [setup](./setup.md) — `delegate` reads its "find the frontier" and "claim the ticket" conventions directly. Separately, `delegate` owns one small config file, `docs/agents/delegate.md`, written the first time it runs in a repo: the **Worker model** (which model does ticket work) and **Max concurrent workers** (one number — tickets in flight at once), plus a `Router model` line only the session-start recommendation hook reads.

## The Router role

**Router** is the load-bearing word, and the three withheld duties above are why it's safe at both tiers. On a weak model, prior art on cheap-orchestrator/expensive-worker patterns is consistent that real decomposition or recovery duties are a documented failure mode. On a strong model, judging duplicates a review that already happened: each worker runs the full two-axis code review inside its own run, with fresh-context sub-agents, and its brief requires fixing real findings *before* committing. The Router asks one question of a dispatched ticket: has it resolved yet?

Safety comes from the layers around the run, not from a second opinion in the dispatcher — the full reasoning is recorded in the repo's ADR 0007.

## Common questions

**Wasn't this a mode with a toggle?**

It was, and the toggle governed nothing mechanical — the "mode" was conversational memory of having invoked the skill, it kept getting pitched per-frontier anyway, and it sat on-and-inert after the work drained. The bounded run is the honest shape; the full reasoning is recorded in the repo's ADR 0007.

**Why does this exist when the harness has orchestration tooling built in?**

The tooling is mechanism — it runs parallel agents well. The skill is process: find the frontier, commit the claim before dispatch, brief each worker with David's personal build-and-review discipline, integrate one branch at a time with verification. Without the skill that process gets re-improvised every session; with it, one word buys both.

**Why doesn't the Router try to unstick a stuck worker before bothering me?**

Because that's a judgment call, and judgment calls are exactly what this role withholds. You're present during a run — a stuck worker surfaces straight to you instead.

**Why doesn't it detect my model and recommend itself mid-session?**

Claude Code has no reliable way to know which model is running mid-session. The one hook that gets a model field at all (`SessionStart`) isn't guaranteed to have it, so the session-start recommendation is best-effort; manual invocation is the reliable path regardless of what fires.

## It's working if

- A run announces what it claimed at the start and "frontier drained, run over" at the end — and nothing delegate-shaped persists after that.
- Claims are visible on the tracker (committed) before any worker starts.
- A ticket only ever gets treated as done once its `Status:` line reads `resolved`, never earlier.
- Worker branches land on the integration branch one at a time, each merge verified against the checkout.
- A stuck worker shows up as a message to you, not as the Router quietly trying something else first.

## Where it fits

An on-call dispatch over [implement](./implement.md)'s place in the main chain (`grill-with-docs → to-spec → to-tickets → implement → code-review`) — the same per-ticket work, dispatched rather than driven by hand, one bounded run at a time. Its frontier and claim vocabulary comes from the same tracker configuration [wayfinder](./wayfinder.md) uses, generalized to cover plain ticket sets too. [ask-claude](./ask-claude.md) is the router over the whole skill set when you're not sure which flow you're in.
