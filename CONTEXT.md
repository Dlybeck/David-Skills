# David Skills

A collection of agent skills (slash commands and behaviors) loaded by Claude Code. Skills are organized into buckets and consumed by per-repo configuration emitted by `/setup`.

## Language

**Issue tracker**:
The tool that hosts a repo's issues — GitHub Issues, Linear, a local `.scratch/` markdown convention, or similar. Skills like `to-tickets`, `to-spec`, and `triage` read from and write to it.
_Avoid_: backlog manager, backlog backend, issue host

**Issue**:
A single tracked unit of work inside an **Issue tracker** — a bug, task, spec, or slice produced by `to-tickets`.
_Avoid_: ticket (use only when quoting external systems that call them tickets, or for a **Decision ticket** — see below)

**Decision ticket**:
A `wayfinder` unit — a child **Issue** of a `wayfinder:map` holding a *question* whose resolution is a decision, not a slice of a build to execute. The **decision** qualifier is what keeps it distinct from an implementation ticket; `wayfinder` introduces the term, then uses "ticket".

**Triage role**:
A canonical state-machine label applied to an **Issue** during triage (e.g. `needs-triage`, `ready-for-agent`). Each role maps to a real label string in the **Issue tracker** via `docs/agents/triage-labels.md`.

**Autopilot**:
An understanding-first authority wrapper for long-horizon autonomous work, entered by an explicit human handoff. A pre-departure grilling session locks a **Goal contract** before **Pursue Goal** adapts the plan from evidence. It may deliver into `dev` only when the contract authorizes that target and every gate passes.
_Avoid_: night mode, away mode (the trigger isn't time-of-day)

**Goal contract**:
The stable boundary for a long-horizon run: objective, observable proof, scope, authority, safety boundary, and delivery target. The plan may change freely inside it; changing the contract requires the human.

**Pursue Goal**:
The model-invoked autonomous engine under **Autopilot** and **Yolopilot**. It selects research, discovery, delivery, or optimization loops from the current uncertainty and stops only when proof passes, new human authority is required, or the evidence plateaus.
_Avoid_: pipeline (the loops adapt), pilot mode (authority belongs to the wrapper)

**Delegate**:
A bounded, on-call dispatch run over the **Issue tracker**'s frontier: `/delegate` claims ready **Issues** and hands each one whole to a worker subagent, and the run is over when the frontier is drained — on-call meaning invoked per frontier, with nothing persisting between runs. Pays off at any model tier; a light-model session is the flagship case.
_Avoid_: delegate mode (nothing stays on), orchestration mode, manager mode

**Router**:
The role the dispatching session plays during a **Delegate** run: classify a ticket and hand it off whole. A Router never decomposes work into subtasks it invented, never judges a worker's partial result, and never attempts to recover a stuck worker itself — duties withheld at every model tier, and exactly the failure modes that sink a cheap model given real orchestration duties.
_Avoid_: orchestrator, manager

**Confidence guideline**:
The shared safety principle behind unattended work: act freely inside the scope locked before departure, or on an existing strong confidence signal (e.g. `re-architect`'s `Strong` recommendation-strength); anything outside that scope, or hard to reverse, gets logged rather than acted on, left for human review.

**Yolopilot**:
The provisional-interpretation authority wrapper for long-horizon autonomous work, entered for a loose, last-second handoff with no grilling round. It states its assumptions, then **Pursue Goal** refines the plan from evidence. It may push a review branch but never merges into an integration branch on its own.
_Avoid_: yolo mode (the name is `yolopilot`, said in full)

## Relationships

- An **Issue tracker** holds many **Issues**
- An **Issue** carries one **Triage role** at a time
- A **Decision ticket** is an **Issue** (a child of a `wayfinder:map`)
- **Autopilot** and **Yolopilot** both delegate execution to **Pursue Goal** and answer to the **Confidence guideline**; **Delegate** doesn't need it — the human is present during a run, and anything beyond an issue's spec escalates to them
- **Autopilot** earns authority through a confirmed **Goal contract**; **Yolopilot** starts from a provisional one and therefore stops at a review branch

## Flagged ambiguities

- "backlog" was previously used to mean both the *tool* hosting issues and the *body of work* inside it — resolved: the tool is the **Issue tracker**; "backlog" is no longer used as a domain term.
- "backlog backend" / "backlog manager" — resolved: collapsed into **Issue tracker**.
