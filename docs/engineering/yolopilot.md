## What it does

`yolopilot` starts a durable autonomous run immediately from the agent's stated best interpretation
of a loose handoff. It uses the same [pursue-goal](./pursue-goal.md) engine as Autopilot but replaces
upfront alignment with a provisional objective. Its default delivery is a review branch; existing
standing integration grants remain available under repository policy.

Its defining behavior is **refine afterward**. The run preserves what it initially assumed, learns
from research and experiments, and explains the difference at postflight.

## When to reach for it

You invoke this by typing `/yolopilot` — the agent will not reach for it on its own.

Reach for it when the handoff is genuinely last-second and a useful provisional interpretation is
better than waiting. Whenever you can stay for an understanding round, use
[autopilot](./autopilot.md); a jointly locked contract earns broader delivery authority.

## The delivery boundary

Yolopilot may research, modify local files, install dependencies, use local compute, run tests and
evaluations, and make small commits within your stated restrictions. It pushes its feature branch
only when your authority allows it and a remote is available; otherwise delivery stays local.
Repository guidance identifies branch ownership; the active request and applicable standing
grants determine authority. Missing policy or authority leaves integration unresolved. Money,
credentials, production, material deletion, safeguards and unrelated scope remain boundaries.
Human-owned promotion requires its explicit approval, and task restrictions override defaults.

## The learning digest

Postflight stays lightweight: initial assumptions, actions, evidence, changed understanding,
uncertainty, and what to inspect. The agent offers to explain a finding immediately. If you want to
retain the material across lessons, it offers the user-invoked `/teach` skill in a separate teaching
workspace.

A retrospective spec is exceptional rather than automatic. It pays only when the run exposes a
lasting product decision, unresolved requirement, or coordination need.

## Independent delivery review

A review branch completes [independent-pr-review](./independent-pr-review.md) before its settled
receipt. That loop routes settled work to an authorized agent-owned target or preserves a
reviewable branch at a missing-authority or human-owned approval boundary.

## Common questions

**Is this just Autopilot without questions?**

It shares the engine, but not the authority. Autopilot can earn a confirmed integration target;
Yolopilot starts provisionally. Both honor existing integration grants; neither creates new
authority simply by its name.

**What if its initial interpretation turns out wrong?**

It can refine the plan inside the provisional objective and scope. You can also correct it in
ordinary conversation: the engine retains the original interpretation as history and works from
the revised direction. Broader authority still requires your explicit instruction.

**Does it automatically start a teaching course afterward?**

No. It gives the short digest itself and merely offers `/teach`, whose stateful workspace would be
disproportionate after routine work.

**Can I include a deadline in a last-second handoff?**

Yes. It preserves your deadline and reporting agreement across continuations. It leaves timing
unset when you have not chosen it. At expiry, the end-of-run report distinguishes verified
results, unfinished work, attempted approaches, reasons, and any jobs still running.

## It's working if

- The warning and provisional interpretation appear before mutation, without waiting for a reply.
- Git history makes each material decision easy to inspect.
- The final result is validated, independently reviewed, and delivered only to an authorized target.
- The learning digest says what changed in the agent's understanding.

## Where it fits

`yolopilot` is the immediate autonomous entrance. [autopilot](./autopilot.md) is the stronger
understanding-first sibling, and [pursue-goal](./pursue-goal.md) is their shared engine.
[advise](./advise.md) routes across the whole set.
