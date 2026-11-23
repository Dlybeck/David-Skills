---
name: autopilot
description: Establish a verified goal and authority contract with the user, then pursue it autonomously for as long as useful evidence supports progress.
disable-model-invocation: true
---

# Autopilot

Enter only through an explicit handoff from the human owner. Autopilot earns long-horizon
authority through an understanding session before work continues without the user. It is a trust
level, not a fixed software pipeline.

## Establish the contract

Inspect the live workspace first: repository instructions, current branch and worktrees, dirty
state, relevant artifacts, available tools, and the validation surface. Then run `/grilling` for
consequential unresolved human choices. Reuse settled answers and distinguish delegated technical
choices from missing product intent. A rich understanding session is useful when the ambiguity
warrants it, not a checklist to repeat for a small or already-understood task.

`/grilling` uses `/attention-modes`: an On the side opening asks for the most consequential missing
intent or boundary first. A short handoff still needs a complete, confirmed contract before this
wrapper starts a durable goal; keep useful independent work moving while a contract question
is open.

Lock one self-contained **goal contract**:

- Objective and observable proof conditions.
- In-scope systems and explicit exclusions.
- Allowed file changes, research, local compute, tests, evaluations, commits, and external
  actions; note any exclusion on routine local dependencies or test setup.
- Git base, review branch, push authority, and integration target.
- Anything the owner wants to be asked about beyond what is theirs alone (see `/implement`).
- Any requested deadline and milestone/maximum-gap reporting agreement, including a finite
  maximum of timed reports and an explicit stop/pause-at-deadline instruction where supported.

Inside the contract the run decides by judgement and doesn't ask again for what is already
granted, here or in the repository's instructions. What is the owner's alone (`/implement`'s
"What needs the owner") stays outside it unless the owner names the specific action.

Present the objective and endpoint compactly, with supporting scope and authority available in
the working context, and obtain the owner's confirmation. An explicit approval of the same
complete contract already in the conversation counts. Do not start a durable goal while a material contract
question remains open.

## Hand off to the engine

Invoke `/pursue-goal` with the confirmed contract. This is delegated continuation of the
explicitly triggered Autopilot process: the wrapper supplies trust and authority; the
model-invoked engine supplies adaptive execution without re-invoking the user-invoked wrapper.

Let `/pursue-goal` choose among research, discovery, delivery, and optimization loops. A spec or
issues are optional coordination artifacts, not admission tickets. Keep the contract stable while
the plan changes in response to evidence. Mid-run human corrections use the engine's steering
discipline; the initial agreement does not prevent its owner from changing direction.

## Delivery

Check and deliver as `/pursue-goal` says: test what the change could break, bring in a fresh
reviewer only when it could really hurt something, and route the result by repository policy.
Without the authority or a passing check, keep the review branch and report what is missing.
Promotion to the owner's branch stays the owner's.

## Return

End with the engine's receipt: outcome, evidence, validation, delivery location, decisions made,
items deliberately left untouched, residual risks, and whether the target, an authority boundary,
or an evidence plateau ended the run. Do not create a retrospective spec merely to narrate work
that is already clear in its evidence and git history.
