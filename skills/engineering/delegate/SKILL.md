---
name: delegate
description: Dispatch ready tickets whole to worker subagents until the frontier is drained.
disable-model-invocation: true
---

# Delegate

A bounded dispatch run: `/delegate` works the current ticket frontier by handing each ticket,
whole, to a worker subagent, and the run is over when the frontier is drained. Invoke it when
tickets are ready; invoke it again next time there's a frontier — nothing stays on between runs.
Announce the run plainly at both ends: what's being claimed at the start, "frontier drained, run
over" at the end.

Your role during the run is strictly a **Router** (see `CONTEXT.md`): classify a ticket and hand
it off whole. Decomposing work, judging a worker's partial result, and recovering a stuck worker
are withheld from the role at every model tier — the worker's own process covers the first two,
and the third goes to the human (see Escalation). Say **Router**, not orchestrator or manager —
those words imply exactly the duties this role withholds.

The run pays off at any tier: on a light-model session it keeps heavy work off the cheap model
(the flagship case); on a heavy-model session it buys parallel tickets and keeps the session's
own context clean for judgment work.

The invocation itself is the user's confirmation for the harness's orchestration tooling, for
this run.

## Setup

The first time `/delegate` runs in a repo, ask two questions and write the answers — plus a fixed
`Router model: fable` line, explained below — to `docs/agents/delegate.md` (read that file
instead of asking again on later runs), using this template:

```markdown
# Delegate config

Router model: fable
Worker model: sonnet
Max concurrent workers: 4
```

1. **Worker model** — which model does the actual ticket work; default whatever you normally
   build with.
2. **Max concurrent workers** — one number with one meaning: tickets in flight at once.

`Router model:` isn't asked, and isn't about the current run — it's the match target for the
best-effort `SessionStart` hook (`hooks/delegate-recommend.py`), which recommends `/delegate` to
future sessions whose active model matches it, falling back to `fable` when the file doesn't
exist yet. The `model` field the hook reads isn't guaranteed present, so the recommendation not
firing is expected — manual invocation always works regardless. This is a `delegate`-owned config
file, separate from `/setup`'s issue-tracker/triage/domain scope.

## The run

1. **Find the frontier** — per `docs/agents/issue-tracker.md`'s "find the frontier" convention:
   open, unblocked, unclaimed tickets. An empty frontier is a complete run: say so and stop.
2. **Claim before dispatching** — per that doc's "claim the ticket" convention — so two
   concurrent dispatches never grab the same ticket. That convention requires *committing* the
   claim, not just saving it, since a dispatched worker's own worktree starts from the last
   commit (see `docs/agents/issue-tracker.md` for why). Commit (and push, if the worker won't
   share this checkout) before the dispatch call, every time. Claim at most "Max concurrent
   workers" at once.
3. **Dispatch** each claimed ticket whole to a worker subagent on the configured Worker model —
   in its own worktree whenever workers run in parallel. Brief the worker to build it the way
   `/implement` describes — read the ticket, drive `/tdd` at pre-agreed seams, typecheck, run
   `/code-review`, commit, then mark the ticket resolved, within the dispatch contract's authority.
   `/implement` is model-invoked and can be selected directly by that authorized worker. This does
   not authorize additional workers or broaden the Router's role. The brief retains two requirements:
   - **Fix any real `/code-review` finding before committing.** `Status: resolved` means
     "committed," not proof of review quality. `/implement` now requires real findings to be
     addressed; the Router still does not perform a second review by reading the report.
   - **Fast-forward the worktree branch to the dispatching branch's tip first.** A fresh
     worktree can spawn stale; starting from the tip is what makes the committed claim visible
     to the worker.
4. **Receive completion** from the worker's completion notification, including its branch and
   committed revision. Inspect the ticket's `Status: resolved` at that revision — not a stale
   copy in the dispatcher's checkout. This is the Router's completion signal, not a second code
   review. Without a completion notification, yield and let the user resume; do not poll ticket
   files or spend repeated AI turns waiting for an unchanged worker.
5. **Integrate** each finished worker branch as it completes: merge `--no-ff` into the
   integration branch, one branch at a time, then confirm the checkout took the merge — compare
   one merged file on disk against `git show HEAD:<path>` (a worktree merge has left a checkout
   stale here before). Merging is mechanical; the diff stays unread.
6. **Repeat** — tickets that unblock mid-run join the frontier and get dispatched the same way.
   The run is over when the frontier is empty and every dispatched ticket is integrated;
   announce it.

## Escalation

A worker stuck on something beyond its ticket's spec surfaces straight to you, in conversation,
the moment it happens, for you to decide — deciding is yours, not the Router's.
