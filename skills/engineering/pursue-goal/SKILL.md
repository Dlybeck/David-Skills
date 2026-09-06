---
name: pursue-goal
description: Drive an explicitly authorized, long-horizon objective through adaptive research, discovery, delivery, or optimization loops until a verifiable stopping condition is reached. Use when an autopilot-style handoff or an active durable goal needs autonomous planning, evidence gathering, implementation, validation, and replanning across many steps; do not use for ordinary bounded tasks.
---

# Pursue Goal

Treat the **goal contract** as stable and the plan as provisional. Select the loop that reduces the
current uncertainty, produce evidence, and replan from what the evidence says. This is the shared
engine underneath `/autopilot` and `/yolopilot`; their wrappers decide how much authority the run
has earned.

## Activate the run

1. Require a self-contained goal contract containing:
   - **Objective** — the outcome, not a list of steps.
   - **Evidence** — observable conditions that prove the outcome.
   - **Scope** — relevant systems and explicit exclusions.
   - **Authority** — allowed writes, compute, dependencies, git delivery, and external actions.
   - **Safety boundary** — actions requiring fresh human authority.
   - **Delivery target** — report, research artifact, review branch, integration branch, or another
     named destination.
2. Read exactly one harness adapter before activating durable continuation:
   - Codex: [references/codex.md](references/codex.md)
   - Claude Code: [references/claude-code.md](references/claude-code.md)
3. Establish isolation before the first mutation. Reuse the current checkout when it is already a
   linked worktree. For mutating work in a primary checkout, create a dedicated linked worktree and
   `pilot/<goal-slug>` feature branch without altering or carrying over unrelated dirty changes.
   Read-only research may remain in the current checkout. If required input exists only as
   uncommitted user work, request authority instead of copying, stashing, or committing it.
4. Record the worktree, branch, base revision, contract, and validation commands in the first
   progress update. Keep all subsequent commands scoped to that worktree.

The contract may be clarified by new evidence, but changing the objective, authority, safety
boundary, or delivery target requires the human. Replanning inside that envelope does not.

## Select the next loop

Choose the loop from the uncertainty in front of the goal, not from the kind of project:

| Current uncertainty | Loop | Evidence produced |
| --- | --- | --- |
| Facts, APIs, prior art, or feasibility are unknown | **Research** | Cited primary-source findings or a reproducible experiment |
| The solution, UX, model, or architecture is unclear | **Discovery** | A decision, prototype, comparison, or falsified option |
| The behavior is understood and needs building | **Delivery** | Tested vertical slices, review findings, and a clean diff |
| A measurable result needs improvement | **Optimization** | Baseline, controlled change, measurement, and retained or reverted result |

Invoke model-reachable skills when their discipline fits: `/research`, `/prototype`,
`/diagnosing-bugs`, `/tdd`, `/codebase-design`, `/domain-modeling`, and `/code-review`. Follow a
human-only skill's process only when the outer pilot contract explicitly delegates that process.
That is delegated continuation of the user's wrapper invocation, not a new invocation of the
human-only skill.

Create a spec or issues only when stable decomposition, coordination, or restart cost makes the
artifact pay for itself. Discovery is allowed to go straight into experiments. Delivery may stay
as one evolving plan when the work remains coherent and independently verifiable.

## Run an evidence checkpoint

After every material result:

1. Compare the new evidence with the goal's proof conditions.
2. Preserve useful artifacts and revert failed optimization changes.
3. Update the plan and select the next loop; do not preserve a stale pipeline for ceremony's sake.
4. Run the smallest credible validation now, then broaden validation as delivery risk grows.
5. Record only a material transition: hypothesis resolved, checkpoint reached, direction changed,
   authority needed, completed, or failed.

For work that must survive sessions, maintain one compact checkpoint in the project's existing
notes location: stable contract, current evidence and revision, decisions/failed approaches worth
retaining, unresolved questions, and next action. Reuse an existing plan or report when it serves
this purpose; link receipts rather than copying logs. On resumption, reconcile it with live state
before acting. A checkpoint is continuity context, not a mandatory spec or another roadmap.
Derive recorded execution metadata from command results, including branch, revision, and dirty
state; keep it distinct from the worker's narrative. Recheck it before Git delivery rather than
inferring it from a checkout path or an earlier checkpoint.

For an external command expected to exceed ten minutes, state its expected duration when known,
launch it as a resumable operating-system process, and give it a local progress log plus terminal
success/failure receipt. Return control after launch. Continue from the receipt on a later turn;
never spend model turns polling unchanged state.

## Apply authority continuously

Treat the wrapper's authority as a capability boundary, not a suggestion. The normal pilot
envelope may include research, local file changes, tests and evaluations, dependency installation,
local compute, commits, and an authorized push. It never implies permission to spend money,
introduce credentials, deploy production, delete material data, weaken safeguards, touch `main`,
or expand into unrelated work.

Before each irreversible or externally visible action, verify that the contract names it. Log a
useful recommendation when it does not.

## Stop deliberately

Stop only at one of these boundaries:

- **Target reached** — every proof condition passes and the authorized delivery target is complete.
- **Authority boundary** — the next meaningful step requires a human decision or new capability.
- **Evidence plateau** — materially different attempts no longer change the evidence, and the next
  step would repeat an already-tested route rather than reduce uncertainty.

There is no arbitrary turn, token, or duration ceiling. Difficulty is not a stopping condition.
When stopping, run the broadest validation justified by the changes, inspect the whole result
against the contract, and leave a concise receipt containing outcome, evidence, validation,
delivery location, assumptions, residual risks, and the exact stopping boundary.
