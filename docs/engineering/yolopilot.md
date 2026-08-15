## What it does

`yolopilot` starts a durable autonomous run immediately from the agent's stated best interpretation
of a loose handoff. It uses the same [pursue-goal](./pursue-goal.md) engine as Autopilot but replaces
upfront alignment with a stricter delivery boundary: it leaves a pushed review branch and never
merges it.

Its defining behavior is **refine afterward**. The run preserves what it initially assumed, learns
from research and experiments, and explains the difference at postflight.

## When to reach for it

You invoke this by typing `/yolopilot` — the agent will not reach for it on its own.

Reach for it when the handoff is genuinely last-second and a useful provisional interpretation is
better than waiting. Whenever you can stay for an understanding round, use
[autopilot](./autopilot.md); a jointly locked contract earns broader delivery authority.

## The review-branch boundary

Yolopilot may research, modify local files, install dependencies, use local compute, run tests and
evaluations, make small commits, and push its feature branch. It cannot merge into `dev` or another
integration branch. Money, credentials, production, material deletion, safeguards, unrelated scope,
and `main` remain human boundaries.

## The learning digest

Postflight stays lightweight: initial assumptions, actions, evidence, changed understanding,
uncertainty, and what to inspect. The agent offers to explain a finding immediately. If you want to
retain the material across lessons, it offers the user-invoked `/teach` skill in a separate teaching
workspace.

A retrospective spec is exceptional rather than automatic. It pays only when the run exposes a
lasting product decision, unresolved requirement, or coordination need.

## Common questions

**Is this just Autopilot without questions?**

It shares the engine, but not the authority. Autopilot can earn a confirmed integration target;
Yolopilot always stops at a review branch.

**What if its initial interpretation turns out wrong?**

It can refine the plan inside the provisional objective and scope. A new objective or broader
authority stops the run for a human.

**Does it automatically start a teaching course afterward?**

No. It gives the short digest itself and merely offers `/teach`, whose stateful workspace would be
disproportionate after routine work.

## It's working if

- The warning and provisional interpretation appear before mutation, without waiting for a reply.
- Git history makes each material decision easy to inspect.
- The final branch is validated, reviewed, pushed, and unmerged.
- The learning digest says what changed in the agent's understanding.

## Where it fits

`yolopilot` is the immediate autonomous entrance. [autopilot](./autopilot.md) is the stronger
understanding-first sibling, and [pursue-goal](./pursue-goal.md) is their shared engine.
[advise](./advise.md) routes across the whole set.
