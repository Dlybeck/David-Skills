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
An unattended work mode, entered by an explicit, manual "I'm leaving, keep working without me" handoff — never scheduled. A pre-departure grilling session locks the goal condition and guardrails first; the run itself is bounded by the **Confidence guideline**, not a fixed time or token ceiling.
_Avoid_: night mode, away mode (the trigger isn't time-of-day)

**Delegate**:
A bounded, on-call dispatch run over the **Issue tracker**'s frontier: `/delegate` claims ready **Issues** and hands each one whole to a worker subagent, and the run is over when the frontier is drained — on-call meaning invoked per frontier, with nothing persisting between runs. Pays off at any model tier; a light-model session is the flagship case.
_Avoid_: delegate mode (nothing stays on), orchestration mode, manager mode

**Router**:
The role the dispatching session plays during a **Delegate** run: classify a ticket and hand it off whole. A Router never decomposes work into subtasks it invented, never judges a worker's partial result, and never attempts to recover a stuck worker itself — duties withheld at every model tier, and exactly the failure modes that sink a cheap model given real orchestration duties.
_Avoid_: orchestrator, manager

**Confidence guideline**:
The shared safety principle behind unattended work: act freely inside the scope locked before departure, or on an existing strong confidence signal (e.g. `re-architect`'s `Strong` recommendation-strength); anything outside that scope, or hard to reverse, gets logged rather than acted on, left for human review.

**Yolopilot**:
An unattended work mode, sibling to **Autopilot**, entered for a loose, last-second handoff with no time for a pre-departure grilling round: a short non-blocking warning plus the agent's own best-guess interpretation stand in for the locked goal, then it launches immediately via the same `claude --bg` + self-set `/goal` mechanism. Answers to the same **Confidence guideline**, unchanged, anchored to that best-guess interpretation instead of a jointly-grilled one. The one hard rule that earns it a distinct identity: it completes its own git cycle up through a pushed, reviewable feature branch, but never merges into `dev` on its own — that happens only once a human reviews and approves.
_Avoid_: yolo mode (the name is `yolopilot`, said in full)

## Relationships

- An **Issue tracker** holds many **Issues**
- An **Issue** carries one **Triage role** at a time
- A **Decision ticket** is an **Issue** (a child of a `wayfinder:map`)
- **Autopilot** and **Yolopilot** both answer to the **Confidence guideline**; **Delegate** doesn't need it — the human is present during a run, and anything beyond a ticket's spec escalates to them
- **Yolopilot** reuses **Autopilot**'s entire mechanism, diverging only in skipping the grilling round and never merging into `dev` unattended

## Flagged ambiguities

- "backlog" was previously used to mean both the *tool* hosting issues and the *body of work* inside it — resolved: the tool is the **Issue tracker**; "backlog" is no longer used as a domain term.
- "backlog backend" / "backlog manager" — resolved: collapsed into **Issue tracker**.
