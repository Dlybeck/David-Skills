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
boundary, or delivery target requires the human. A clear mid-run instruction from that human
can supply the change; the contract is not frozen against its owner. Replanning inside that
envelope does not require renewed approval.

## Select the next loop

Choose the loop from the uncertainty in front of the goal, not from the kind of project:

| Current uncertainty | Loop | Evidence produced |
| --- | --- | --- |
| Facts, APIs, prior art, or feasibility are unknown | **Research** | Cited primary-source findings or a reproducible experiment |
| The solution, UX, model, or architecture is unclear | **Discovery** | A decision, prototype, comparison, or falsified option |
| The behavior is understood and needs building | **Delivery** | Tested vertical slices, review findings, and a clean diff |
| A measurable result needs improvement | **Optimization** | Baseline, controlled change, measurement, and retained or reverted result |

Invoke model-reachable skills when their discipline fits: `/research`, `/prototype`,
`/diagnosing-bugs`, `/tdd`, `/codebase-design`, `/domain-modeling`, and `/code-review`. Use
`/to-spec`, `/to-tickets`, or `/implement` when requirements capture, decomposition, or delivery
helps; `/handoff` serves an actual authorized transfer, not ordinary checkpointing. Follow a
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
retaining, consequential user corrections and what they supersede, unresolved questions, and next
action. Reuse an existing plan or report when it serves
this purpose; link receipts rather than copying logs. On resumption, reconcile it with live state
before acting. A checkpoint is continuity context, not a mandatory spec or another roadmap.
Derive recorded execution metadata from command results, including branch, revision, and dirty
state; keep it distinct from the worker's narrative. Recheck it before Git delivery rather than
inferring it from a checkout path or an earlier checkpoint.

## Incorporate human steering

The human can inspect and steer an active run in ordinary conversation; no interruption skill
is required. Classify the intent before changing the plan:

| Input | Response |
| --- | --- |
| Question or status check | Answer from evidence; retain the objective and authorized next action. |
| Tentative suggestion | Assess it as a candidate, not a new requirement. Ask only if ambiguity would materially change the work. |
| Clear correction or changed priority | Briefly state the impact, update the contract or plan as appropriate, and persist the correction before further affected work. Reuse settled decisions. |
| Stop request | Stop initiating work immediately; safely cancel only identified task-owned work where authorized, preserve a receipt, and report anything still running. |

For a correction, reconcile pending changes and exact running job handles. Keep still-useful
results, mark superseded experiments as historical evidence, and withdraw affected completion
claims. Cancel or restart only within existing authority; do not kill unrelated processes or
overwrite user changes. An unaffected authorized branch may continue while a material ambiguity
is resolved. Propagate revised instructions to existing authorized workers without creating more.

On resumption, prefer the latest explicit user direction over a stale checkpoint; distinguish it
from unadopted suggestions. Use the harness's supported goal controls, never invent a goal-edit
API or mark old work complete to replace it. If persistent goal text cannot be amended, record
the correction in the checkpoint and disclose that limitation. Continue after questions and
corrections when supported; do not treat the user's check-in as withdrawal of autonomy.

## Wait without abandoning the work

Waiting is an execution state, not a reason to pause, block, or end the goal. Preserve the active
run through the wait and continue meaningful work when the dependency finishes.

For an external command expected to exceed ten minutes, state its expected duration when known,
launch it as a resumable operating-system process, and give it an exact job handle, local progress
log, and terminal success/failure receipt. Choose meaningful independent work within scope when it
does not interfere with the job's resources or evidence. Otherwise keep the run pending in the
adapter's supported blocking wait or use a verified non-AI completion callback within host and
account limits. A blocking wait does not require a callback and is not recurring AI polling.
Prefer a wait tied to job completion; a duration-based sleep may also preserve the run. Verify
the identified job after waking rather than assuming elapsed time proves completion. Never use
model turns, repeated status calls, or subagents as a polling loop.

After completion, verify the receipt belongs to this job and attempt, distinguish success from
failure, timeout, or cancellation, and continue with the next meaningful action. A background
process finishing is not proof that agent continuation works. Establish the continuation path
before an unattended dependency. If no permitted mechanism can preserve or resume execution,
identify the actual host limitation and preserve the checkpoint; ordinary job duration does not
establish that limitation. Do not claim an ended turn will wake itself or that a skill can
override host instructions. A forced handoff leaves the requested autonomy unmet.

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
Offer an explanation or the optional user-invoked `/teach` path when there is useful learning.
Recommend a next stage if warranted; activate it only on user direction, not to fill available time.
