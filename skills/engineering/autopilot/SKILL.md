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
state, relevant artifacts, available tools, and the validation surface. Then run `/grilling` in
this conversation until the whole decision frontier needed for unattended work is closed.

Lock one self-contained **goal contract**:

- Objective and observable proof conditions.
- In-scope systems and explicit exclusions.
- Allowed file changes, research, dependencies, local compute, tests, evaluations, commits, and
  external actions.
- Git base, review branch, push authority, and integration target.
- Actions that require the human to return.

The normal personal-practice envelope may authorize research, local changes, tests and evaluations,
dependency installation, local compute, feature-branch commits, and pushes. It may authorize a
reviewed `--no-ff` merge into `dev` only when the user confirms that delivery target during this
session and repository gates pass. Keep money, new credentials, production deployment, material
deletion, safeguard weakening, unrelated scope, and `main` outside the contract unless the user
grants the specific action explicitly.

Present the final contract compactly and obtain confirmation. Do not start a durable goal while a
material contract question remains open.

## Hand off to the engine

Invoke `/pursue-goal` with the confirmed contract. This is delegated continuation of the
human-triggered Autopilot process: the wrapper supplies trust and authority; the model-invoked
engine supplies adaptive execution without re-invoking the human-only wrapper.

Let `/pursue-goal` choose among research, discovery, delivery, and optimization loops. A spec or
issues are optional coordination artifacts, not admission tickets. Keep the contract stable while
the plan changes in response to evidence.

## Delivery

Before any authorized integration into `dev`:

1. Rebase or merge the current `dev` state according to repository policy.
2. Run the contract's full validation surface and a whole-change `/code-review`.
3. Fix every real finding and rerun affected gates.
4. Merge `--no-ff` from the feature branch, push only the authorized refs, and verify the remote.

If any integration permission or gate is absent, leave the work on its review branch and report
the unmet condition. Push that branch only when the contract explicitly authorizes the push;
otherwise leave it local. `main` remains human-gated.

## Return

End with the engine's receipt: outcome, evidence, validation, delivery location, decisions made,
items deliberately left untouched, residual risks, and whether the target, an authority boundary,
or an evidence plateau ended the run. Do not create a retrospective spec merely to narrate work
that is already clear in its evidence and git history.
