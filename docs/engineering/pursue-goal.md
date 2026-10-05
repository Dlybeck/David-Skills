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
[Tool fit](../productivity/tool-fit.md) helps it inspect current sources and present results in a
form the host can show, without making any one app or output format mandatory.

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

The goal stays active through waits. A supported blocking wait keeps the run pending and returns
control to the agent afterward; it does not require a completion callback or repeated AI checks.
The engine establishes a continuation mechanism on the current host before unattended work.
A completed background job alone is not proof that the conversation will resume. When the host
cannot support continuation, the engine identifies that limitation and leaves autonomy explicitly
unmet rather than calling ordinary waiting a blocker.

## Human steering

Check in through ordinary conversation. Questions get answers without changing the goal;
suggestions stay provisional until adopted; clear corrections update the working plan and
checkpoint. The agent reconciles affected jobs and evidence without reopening settled decisions.
A stop request stops new work and accounts for identified running work safely.
[Attention modes](../productivity/attention-modes.md) makes a brief On the side check-in easy to
answer while unrelated authorized work continues.

## Independent delivery review

When a goal changes source, [independent-pr-review](./independent-pr-review.md) handles fresh
ordinary review and the authorized repair loop. Research-only reports need no fabricated PR.

## Common questions

**Why is this model-invoked when the pilots are human-invoked?**

The pilots carry human trust and authority. Their shared engine must be reachable from either
wrapper without duplicating the execution discipline.

**When does it stop?**

When the proof passes, new human authority is required, or materially different attempts no longer
change the evidence. A user-selected deadline is also a stopping boundary; time expiring never
counts as proof that the goal succeeded.

**How often does the agent hear about remaining time?**

Managed-plugin hooks normally supply only remaining time at five-minute spacing during existing
tool activity, and restore it after a context refresh. They are silent until that chat has an
agreed deadline. The agent decides what the clock means for its current work. Editable skill
copies without plugin hooks use the host's available clock instead.

**What if nothing has changed before the next scheduled report?**

An explicitly agreed maximum-gap report still arrives: current work, verified progress, intended
next work, and why progress is limited. Milestone reports reset the reporting clock. Reports use
existing evidence and do not require your reply before the run continues. Exact delivery during
a long wait needs verified host support; the timer helper is not a chat-wakeup service.

**Will it rerun the whole test suite after every small edit?**

Checks follow changed behavior and delivery risk. Passing evidence is reused until a relevant
change or unresolved concern invalidates it. Required delivery checks still run.

**Can it decide to deploy or merge because that would finish the goal?**

Only when the contract explicitly grants that capability. The objective never expands its own
authority.

**Does a missing local dependency stop an implementation run?**

No. Routine project-compatible toolchain, dependency, and isolated test setup is part of an
authorized implementation goal unless excluded. The agent uses applicable standing grants and
continues after setup. A real host denial or a new external capability still needs its own path.

**Will a long job make me restart the goal manually?**

Waiting alone must not cause a handoff. The agent does useful independent work or waits quietly,
then continues. Blocking waits and non-AI completion callbacks can provide that continuation;
repeated model status checks do not. Actual host restrictions still apply, and a short successful
wait does not establish that hours of waiting or interruption have been tested.

## It's working if

- The first progress update names the contract, worktree, branch, and validation surface.
- Research can become a prototype, benchmark, or delivery slice without a forced pipeline reset.
- Updates report material evidence transitions, plus brief unchanged-progress reports when
  your reporting agreement requires them.
- The final receipt ties every completion claim to observable proof.
- Resumption preserves useful decisions while correcting stale checkpoint claims against current evidence.
- Your correction changes subsequent work and survives a context transfer.
- A status question does not become a new objective or withdraw autonomy.
- A long-running job leads to quiet waiting and further work without a manual restart, when the
  host supports it; any actual host limitation is named explicitly.

## Where it fits

`pursue-goal` is the model-invoked autonomous engine. [autopilot](./autopilot.md) and
[yolopilot](./yolopilot.md) are its human authority wrappers; [advise](./advise.md) helps choose
between those entrances and the interactive engineering flow.
