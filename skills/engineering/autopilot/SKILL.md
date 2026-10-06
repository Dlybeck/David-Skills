---
name: autopilot
description: Establish a verified goal and authority contract with the user, then pursue it autonomously for as long as useful evidence supports progress.
disable-model-invocation: true
---

# Autopilot

Enter only through an explicit human handoff. Autopilot earns long-horizon authority through an
understanding session before work continues without the user. It is a trust level, not a fixed
software pipeline.

## Establish the contract

Inspect the live workspace first: repository instructions, current branch and worktrees, dirty
state, relevant artifacts, available tools, and the validation surface. Then run `/grilling` for
consequential unresolved human choices. Reuse settled answers and distinguish delegated technical
choices from missing product intent. A rich understanding session is useful when the ambiguity
warrants it, not a checklist to repeat for a small or already-understood task.

`/grilling` uses `/attention-modes`: an On the side opening asks for the most consequential missing
intent or boundary first. A short handoff still needs a complete, confirmed contract before this
wrapper starts a durable goal; keep useful independent work within existing authority moving
while any human-only contract question is open.

Lock one self-contained **goal contract**:

- Objective and observable proof conditions.
- In-scope systems and explicit exclusions.
- Allowed file changes, research, local compute, tests, evaluations, commits, and external
  actions; note any exclusion on routine local dependencies or test setup.
- Git base, review branch, push authority, and integration target.
- Actions that require the human to return.
- Any requested deadline and milestone/maximum-gap reporting agreement, including a finite
  maximum of timed reports and an explicit stop/pause-at-deadline instruction where supported.

The normal personal-practice envelope may authorize research, local changes, tests and evaluations,
dependency installation, local compute, feature-branch commits, and pushes. It may authorize a
reviewed integration into the agent-owned target identified by repository policy when an
applicable standing grant or explicit task approval authorizes it and all gates pass. Record that
existing grant without requiring fresh permission for every run. Keep money, new credentials,
production deployment, material deletion, safeguard weakening, unrelated scope, and human-owned
promotions outside the contract unless the specific action is explicitly authorized. Branch
names alone grant no authority; missing policy or authority leaves integration unresolved.

When implementation and tests are in scope, routine local toolchain and dependency setup is part
of that work unless the user excludes it. Reuse an applicable standing grant already present in
the conversation or durable instructions instead of asking for the same permission again.

Present the objective and endpoint compactly, with supporting scope and authority available in
the working context, and obtain confirmation. An explicit approval of the same complete contract
already in the conversation counts. Do not start a durable goal while a material contract
question remains open.

## Hand off to the engine

Invoke `/pursue-goal` with the confirmed contract. This is delegated continuation of the
human-triggered Autopilot process: the wrapper supplies trust and authority; the model-invoked
engine supplies adaptive execution without re-invoking the human-only wrapper.

Let `/pursue-goal` choose among research, discovery, delivery, and optimization loops. A spec or
issues are optional coordination artifacts, not admission tickets. Keep the contract stable while
the plan changes in response to evidence. Mid-run human corrections use the engine's steering
discipline; the initial agreement does not prevent its owner from changing direction.

## Delivery

Follow [the shared developer loop](../independent-pr-review/references/developer-loop.md) for
policy-driven delivery after full validation, whole-change Standards/Spec checks and fresh ordinary
independent review. Synchronize the authorized integration target, re-pin and re-review any changed
proposal, then use the repository's required merge strategy and verify remote refs and CI.

If policy, integration permission or a required gate is absent, retain the review branch within
existing commit/push authority and report the unmet condition. Human-owned promotion remains
subject to its explicit approval boundary; the confirmed goal does not override task restrictions.

## Return

End with the engine's receipt: outcome, evidence, validation, delivery location, decisions made,
items deliberately left untouched, residual risks, and whether the target, an authority boundary,
or an evidence plateau ended the run. Do not create a retrospective spec merely to narrate work
that is already clear in its evidence and git history.
