## What it does

`implement` builds work that has already been decided. You point it at a [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket), a [spec](https://www.aihero.dev/ai-coding-dictionary/spec), or the plan you just agreed in the conversation, and it writes the code, drives [tdd](./tdd.md) at the seams, typechecks as it goes, runs [code-review](./code-review.md) at the end, and commits to the current branch.

It never reopens the plan. There is no interview, no clarifying round, no proposal of a different approach. Whatever was settled upstream is the input, and the skill's whole job is to turn that into a commit. That is what separates it from typing "build this" at a fresh [agent](https://www.aihero.dev/ai-coding-dictionary/agent), which will happily redesign the work while it builds it.

## When to reach for it

You invoke this by typing `/implement` — the agent won't reach for it on its own. It ships with `disable-model-invocation: true`, so no other skill can call it either. Wherever [advise](./advise.md) or [to-tickets](./to-tickets.md) says "then `/implement` per ticket", that is an instruction to you, not something the agent will do unprompted.

Where the work currently lives decides whether this is the right skill:

| The work is… | Reach for |
| --- | --- |
| A ticket on the tracker | `/implement #42`, one ticket per [session](https://www.aihero.dev/ai-coding-dictionary/session), [clearing](https://www.aihero.dev/ai-coding-dictionary/clearing) context between tickets |
| A spec, not yet split up, and the build spans sessions | [to-tickets](./to-tickets.md) first, then `/implement` per ticket |
| A spec, and the build is small | `/implement` directly against the spec |
| Only in the conversation you just had, and it's still small | `/implement` right there, in the same window |
| Not written down anywhere yet | [grill-with-docs](./grill-with-docs.md), or [grill-me](../productivity/grill-me.md) if there's no codebase |
| One concrete behaviour you want test-first, with no spec | [tdd](./tdd.md) directly |
| Already built, and you want it checked | [code-review](./code-review.md) directly |

The same-session case needs no extra document: the settled conversation can be the requirements source. If the work is already clear, invoke implementation directly rather than creating a spec or tickets just to satisfy a sequence.

## Prerequisites

`implement` commits to the branch you are on. It does not create one, and it does not ask. Check you are on the branch you want the work on before you start.

If the tickets came from [to-tickets](./to-tickets.md), the tracker they live on was configured by [setup](./setup.md). `code-review` reads the same configuration to find the originating spec at close-out.

## What one run does

A run is six beats, in order:

1. Read the ticket or spec and work out the seams.
2. Drive [tdd](./tdd.md) at the pre-agreed seams, one red-green slice at a time.
3. Typecheck often, run single test files as it goes.
4. Run the full test suite once, at the end.
5. Run [code-review](./code-review.md), then commit to the current branch.
6. If the work came from a ticket, mark it resolved on the tracker.

One run covers one ticket. The tickets [to-tickets](./to-tickets.md) produces are tracer-bullet vertical slices sized to fit a single fresh [context window](https://www.aihero.dev/ai-coding-dictionary/context-window), so the intended rhythm is: clear context, implement one ticket, commit, clear again. Each ticket is self-contained, which is what makes the previous ticket's context disposable.

## Pre-agreed seams

The idea the skill runs on is the **seam**: the public boundary you observe behaviour at, without reaching inside. Tests live at seams. Working at a seam agreed before any code is written is what keeps the tests durable, because the implementation underneath can be rewritten without the tests moving.

The seam choice can already be settled in your request, spec, or goal contract. If implementation and test design are delegated, [tdd](./tdd.md) can choose relevant existing public interfaces and state the choice. An unresolved choice that changes behavior, scope, or authority comes back to you; previously agreed decisions should not generate another interview.

## Common questions

**My ticket is marked resolved, but the acceptance criteria are still unchecked.**

Expected — `implement` now marks the ticket resolved as its last beat (a plain completion marker: the work was committed), but that is still the full extent of it. It does not tick the `- [ ]` boxes, and it does not act on the findings `code-review` produced — reconciling both against what actually shipped is still yours to do. This used to bite harder, because nothing ever closed a ticket at all, which meant a dependency chain never became visibly unblocked (`to-tickets` defines the frontier as tickets whose blockers are all closed). That specific failure mode is fixed; the criteria/findings gap is not.

**Can I point it at all my tickets at once, or run several in parallel?**

Use [delegate](./delegate.md) when ready independent tickets warrant bounded worker dispatch. It briefs each worker with implementation discipline and uses separate worktrees for parallel work. Several sessions sharing one checkout also share an index and HEAD, so avoid treating that as isolation. A small coherent task can still be implemented directly without a dispatch layer.

**Can it open a pull request instead of committing?**

Not built in. It commits straight to the current branch, which several people find too eager: the code lands before they have had a chance to verify it works. There is no configuration flag and no PR mode. People override it in the invocation ("commit to a branch and open a PR") or by editing their local copy of the skill.

**`code-review` says it cannot see my changes.**

The current [code-review](./code-review.md) covers relevant staged, unstaged, and untracked files for pre-commit and WIP reviews. Both reviewers receive the same evidence, even if they use isolated worktrees. You do not need to commit or stash merely to make the changes visible. A committed-only review still excludes local work unless you ask to include it.

Separately, some people deliberately do not want the review inside the run at all, because an agent reviewing the code it just wrote is biased toward its own solution. Running [code-review](./code-review.md) in a fresh session against a fixed point is a legitimate alternative, and is the same reason that skill runs its two axes in separate sub-agents.

**One ticket burned 150k tokens. Am I using it wrong?**

Probably the ticket is too big rather than the skill being misused. A run does codebase exploration, a red-green loop per seam, a full suite, and a review, so a non-trivial ticket exceeding 100k [tokens](https://www.aihero.dev/ai-coding-dictionary/token) is normal rather than a sign something broke. The lever is upstream: right-size the tickets in [to-tickets](./to-tickets.md) so each fits one fresh window. If a single ticket keeps blowing out, split it rather than raising the [effort](https://www.aihero.dev/ai-coding-dictionary/effort) level.

**`/implement #2` in a fresh session worked on something completely unrelated.**

`#2` is resolved against whatever numbered list the agent can see, which in a fresh session may be a todo file, a checklist, or another work list rather than the configured tracker. The resolution is confident rather than fail-closed, so the mistake is not obvious until it has started. Pass the full reference, the issue URL or `owner/repo#2`, and ask it to confirm the title back before it begins.

## It's working if

- The session opens by reading the ticket or spec and restating what it will build, rather than asking you what to build.
- You can see an actual `/tdd` invocation in the trace, not just tests appearing in the diff.
- Typechecks and single test files run repeatedly during the run, and the full suite runs once near the end.
- The run reaches a commit on your current branch without you prompting it to carry on.
- The diff is one ticket's worth of change: a vertical slice through every layer, not several tickets swept together.
- If the ticket came from the tracker, it's marked done on that tracker once the run finishes — `Status: resolved` on the local markdown tracker, closed on GitHub Issues.

## Where it fits

`implement` is the build step of the main chain, second from the end:

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

Its neighbours are [to-tickets](./to-tickets.md), which produces the tickets it consumes and declares the blocking edges that decide their order; [tdd](./tdd.md), which it drives internally at each seam; and [code-review](./code-review.md), which it runs before committing. It sits downstream of the planning skills and trusts them. It does not re-validate the shape of what it was handed, so a badly-structured map or a horizontally-layered ticket gets built as written.

That trust is why [wayfinder](./wayfinder.md) merges onto the chain at [to-spec](./to-spec.md) rather than looping its map straight into `implement`. Go straight to `implement` from a map only when the effort turned out genuinely small.

[advise](./advise.md) is the router over the whole set when you are not sure which flow you are in.
