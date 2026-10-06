# Codex-first pilots share an adaptive goal engine

The four targeted invocation changes and human-steering refinement are recorded in
[ADR 0010](./0010-human-steered-autonomy.md); the original decision below explains their starting point.

Delivery authority is refined by the current repository-policy routing in the shared independent
review loop: a provisional Yolopilot objective does not remove an applicable standing integration
grant. Human-owned promotion and explicit task restrictions remain boundaries. The review-only
statement in the original decision below records the initial default, not a prohibition on
already-authorized agent-owned integration.

## Context

The original pilots encoded one Claude-specific launch command and largely replayed the interactive
spec-to-implementation flow. David's Codex work includes ambitious AI research, experiments,
optimization, and product development whose next useful step often cannot be known upfront.

## Decision

Make Codex the canonical pilot design without forcing Claude Code to imitate Codex mechanics.

- `autopilot` and `yolopilot` remain human-invoked authority wrappers.
- `autopilot` earns trust through a confirmed understanding session; `yolopilot` starts from a
  provisional interpretation and can only push a review branch.
- `pursue-goal` is their model-invoked engine. It holds the goal contract stable while selecting
  research, discovery, delivery, and optimization loops from current evidence.
- Specs and issues are conditional coordination artifacts, not a mandatory entrance pipeline.
- A run stops when the proof passes, new human authority is required, or evidence plateaus; it has
  no arbitrary duration or token ceiling.
- Codex uses native durable goals and explicit linked-worktree isolation. Claude Code retains its
  background `/goal` adapter.
- `advise` replaces the harness-specific legacy name `ask-claude` and ships in both plugins.

Do not broadly reclassify the existing user-invoked skills in this change. Separate reusable
reasoning from publishing, dispatch, merge, deployment, and other capability-bearing effects first;
future invocation changes require scenario evidence that autonomous composition needs them.

Yolopilot closes with a quick learning digest and offers an immediate explanation. `/teach` remains
an optional human-invoked path for a durable teaching workspace rather than an automatic postflight
artifact.
