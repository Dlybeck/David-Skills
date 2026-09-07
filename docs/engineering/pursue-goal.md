## What it does

`pursue-goal` drives an authorized long-horizon objective through whatever evidence loop it needs:
research, discovery, delivery, or optimization. The goal contract stays stable while the plan and
loop evolve; its human owner can correct it during the run.

This is the reusable autonomous engine beneath the two pilots, not a third trust mode. The wrapper
decides what the run may do; the engine decides what useful work comes next.

## When to reach for it

Type `/pursue-goal`, or the agent reaches for it automatically when an explicitly authorized durable
goal needs adaptive execution. Ordinary bounded tasks should stay in their current session and use
the narrower skill that fits.

## The evidence loop

| Uncertainty | Loop | Proof |
| --- | --- | --- |
| Facts or feasibility | Research | Primary sources or reproducible experiment |
| Solution, UX, model, or architecture | Discovery | Decision, prototype, comparison, or falsified option |
| Understood behavior | Delivery | Tested slices and reviewed change |
| Measurable result | Optimization | Baseline, controlled change, and measurement |

At each checkpoint the engine compares evidence with the goal, preserves or reverts the result,
replans, and chooses again. A spec or issues appear only when stable decomposition or coordination
makes them valuable.

For work spanning sessions, it keeps one compact checkpoint in the project's existing notes,
plan, or report: the contract, evidence and revision, useful decisions and failed approaches,
open questions, and next action. On resumption it checks that snapshot against live state.
Branch, revision, and dirty-state claims come from command results and are rechecked before
Git delivery. This is continuity context, not a mandatory spec or a second roadmap.

## Durable continuation

Codex uses its native goal capability and creates a linked Git worktree when mutating work is still
in a primary checkout. Claude Code uses its background `/goal` mechanism and the worktree that
mechanism supplies. Both keep long-running external jobs outside the model loop: the process writes
its own log and terminal receipt.

Actual continuation after waiting must be verified on the current host within account policy.
A completed background job is not proof that the conversation will resume. When no permitted
mechanism exists, the engine records that limitation instead of promising an automatic return.

## Human steering

Check in through ordinary conversation. Questions get answers without changing the goal;
suggestions stay provisional until adopted; clear corrections update the working plan and
checkpoint. The agent reconciles affected jobs and evidence without reopening settled decisions.
A stop request stops new work and accounts for identified running work safely.

## Common questions

**Why is this model-invoked when the pilots are human-invoked?**

The pilots carry human trust and authority. Their shared engine must be reachable from either
wrapper without duplicating the execution discipline.

**When does it stop?**

When the proof passes, new human authority is required, or materially different attempts no longer
change the evidence. It does not stop merely because the work is long or difficult.

**Can it decide to deploy or merge because that would finish the goal?**

Only when the contract explicitly grants that capability. The objective never expands its own
authority.

## It's working if

- The first progress update names the contract, worktree, branch, and validation surface.
- Research can become a prototype, benchmark, or delivery slice without a forced pipeline reset.
- Updates report material evidence transitions rather than unchanged status.
- The final receipt ties every completion claim to observable proof.
- Resumption preserves useful decisions while correcting stale checkpoint claims against current evidence.
- Your correction changes subsequent work and survives a context transfer.
- A status question does not become a new objective or withdraw autonomy.

## Where it fits

`pursue-goal` is the model-invoked autonomous engine. [autopilot](./autopilot.md) and
[yolopilot](./yolopilot.md) are its human authority wrappers; [advise](./advise.md) helps choose
between those entrances and the interactive engineering flow.
