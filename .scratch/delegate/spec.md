Status: resolved

# `delegate`: light-model router over subagent workers

## Problem Statement

Denali's AI team has real, underused Fable capacity, and today every session — including the
parts that are pure classification and dispatch, not reasoning — pays the price of whichever
model is doing the talking. David wants a mode where a light model handles the conversation and
routing while Sonnet/Opus subagents do the actual work, specifically as a cost-saving delegation
pattern rather than a heavier "orchestration" role that the evidence says a light model shouldn't
be given.

## Solution

A new user-invoked skill/mode, `delegate`. A light model acts strictly as a **router**:
classifies and hands off whole tickets to Sonnet/Opus subagent workers, never decomposing work
into subtasks it invented and never judging a worker's partial result. This is a deliberate,
research-backed narrowing — prior art (Anthropic's own multi-agent engineering writeup, a
planner-capacity scaling study, Cognition's "Don't Build Multi-Agents") is consistent that a weak
model given real decomposition/synthesis/recovery duties is the specific failure mode to avoid,
while a cheap model doing classification-and-handoff only is well-precedented and safe.

David stays present — `delegate` is a live mode, not an unattended one. He's talking directly to
the light model while workers run delegated, which resolves escalation almost for free: a worker
stuck on something beyond its ticket's spec surfaces straight to David, no automatic
stronger-model fallback attempted.

The router dispatches from the same **frontier** concept `docs/agents/issue-tracker.md` already
defines for `wayfinder` (open, unblocked, unclaimed tickets under `.scratch/<feature>/issues/`) —
generalized in that doc, since the mechanism is identical for a plain `/to-tickets` ticket set and
was previously filed as if it were wayfinder-exclusive. Quality judgment never sits with the
router; each dispatched `/implement` subagent already self-validates via its own `/code-review`
gate, so the router's only job is reading a ticket's `Status:` line to know when to dispatch next.

The mode generalizes past Fable to any cheap/expensive model pair — Fable is the flagship,
motivating case (the actual underused capacity), not a hard requirement. It's always available as
a manual, explicit toggle regardless of active model, and additionally *recommended* — never
auto-enabled — at session start when the best-effort `SessionStart` hook happens to report the
active model as a light one (Claude Code has no reliable way to detect a mid-session model
switch, so this recommendation is best-effort by nature, not a guarantee).

## User Stories

1. As David, I want a mode where a light model handles the conversation while heavier models do
   the actual work, so that I'm not paying full-price attention for pure routing.
2. As David, I want that light model's job strictly limited to classify-and-hand-off, so that it's
   never put in the position of making a judgment call it isn't strong enough to make well.
3. As David, I want the unit of delegation to be a whole ticket, not a finer-grained sub-step, so
   that the router never has to evaluate a partial result.
4. As David, I want the router to pull from the same unblocked/unclaimed ticket concept
   `wayfinder` already uses, so that this doesn't invent a second, parallel notion of "what's
   next."
5. As David, I want each dispatched ticket to go through the same `/implement` → `/code-review`
   cycle it would in a normal session, so that quality assurance doesn't get weaker just because
   delegation is involved.
6. As David, I want the router to only need to check a ticket's completion status, not judge the
   work itself, so that its own low context stays legitimately low, not a fiction.
7. As David, I want to stay present and be the one a stuck worker escalates to, so that no
   automatic fallback is quietly making judgment calls on my behalf while I'm right there.
8. As David, I want this mode to work with any cheap/expensive model pair, not just Fable
   specifically, so that the discipline is reusable even when Fable isn't the model in question.
9. As David, I want Fable named as the flagship use case in documentation, so that the mode's
   original motivation (underused capacity, real cost savings) stays visible even though the
   mechanism is general.
10. As David, I want turning the mode on to double as my one confirmation for the `Workflow`
    tool's multi-agent gate, so that I'm not re-confirming the same intent on every dispatch.
11. As David, I want the mode recommended to me automatically when Fable happens to be detected at
    session start, so that I don't have to remember it exists every time it would actually help.
12. As David, I want that recommendation to never silently auto-enable the mode, so that I always
    get a say even when the detection happens to fire.
13. As David, I want the exact dispatch mechanism (raw subagent calls vs. the `Workflow` tool, and
    if `Workflow`, limits like average agents per phase and a preferred delegation model) asked of
    me at setup time rather than hardcoded, so that it fits how I actually want to run it.
14. As a teammate reading `CONTEXT.md`, I want "router" used consistently instead of
    "orchestrator" or "manager," so that the vocabulary doesn't imply duties this mode explicitly
    avoids giving the light model.
15. As a future contributor to this plugin, I want the reasoning behind "router, not orchestrator"
    documented somewhere discoverable, so that a future change doesn't casually hand the light
    model decomposition/synthesis duties without knowing why that was avoided.
16. As David, I want `delegate` and `autopilot` to share the same Confidence-guideline vocabulary
    where their concerns overlap, so that the plugin has one safety principle instead of two
    similar ones that quietly drift apart.

## Implementation Decisions

- New user-invoked skill `delegate` at `skills/engineering/delegate/` — `disable-model-invocation:
  true`, matching `agents/openai.yaml`'s `policy.allow_implicit_invocation: false`.
- Registry integration: same shape as `autopilot`'s — `.claude-plugin/plugin.json`, top-level
  `README.md` and `skills/engineering/README.md` (User-invoked), `docs/engineering/delegate.md`,
  and an `ask-claude` entry, most naturally noted alongside `/implement` in the main flow since
  it changes how ticket execution happens, not what the tickets are.
- Vocabulary: **router** (not orchestrator/manager) for the light model's role — formalized in
  `CONTEXT.md`. `_Avoid_` list carries both rejected terms so future contributors don't reach for
  them by habit.
- `docs/agents/issue-tracker.md`'s **Frontier** definition is generalized out from under its
  "Wayfinding operations"-only heading (or given a note that it applies beyond `wayfinder`) so
  `delegate` can point at the existing definition directly instead of re-deriving the same scan
  logic under a different name.
- `/implement` gets the same small addition noted in `autopilot`'s spec: mark its ticket's
  `Status:` line `resolved` after `/code-review` and commit. `delegate`'s status-tracking depends
  on this; it is fixed once, at the source, not duplicated as delegate-specific logic.
- Trigger: always manually available regardless of active model; additionally recommended
  (never auto-enabled) via a best-effort `SessionStart`-hook model check.
- Entering the mode satisfies the `Workflow` tool's own required opt-in for multi-agent
  orchestration for the remainder of the session — no per-call re-confirmation needed once active.
- Escalation: a stuck worker surfaces directly to David in the live conversation. No automatic
  stronger-model fallback is attempted — deliberately, per the same research this spec is built
  on.
- Dispatch mechanics (raw subagent calls vs. the `Workflow` tool; if `Workflow`, average agents
  per phase and a preferred delegation model) are asked of the user at setup time, not fixed by
  this spec.

## Testing Decisions

- No automated test suite exists for this repo — same precedent as `autopilot`'s spec.
- Structural: `claude plugin validate . --strict`.
- Scenario-based dry run: invoke `delegate` against a small, real ticket set that includes at
  least one intentionally-blocked ticket. Confirm it (a) dispatches only frontier tickets, (b)
  correctly reads each ticket's resolution status rather than judging the work itself, (c)
  correctly surfaces a stuck worker to David instead of attempting to resolve it automatically,
  and (d) never begins acting on the `Workflow` tool without the mode having been explicitly
  turned on first.
- Standard `/code-review` (two-axis) against the merge-base, on `delegate`'s own implementation
  branch, before it merges into `dev`.

## Out of Scope

- Reliable mid-session active-model detection — not possible per Claude Code's own documentation
  (no `$CLAUDE_MODEL` env var, `SessionStart`'s `model` field not guaranteed present, doesn't
  update on a `/model` switch). Explicitly not attempted; the best-effort session-start check is
  the ceiling here.
- Automatic stronger-model fallback on a stuck worker — considered and explicitly rejected in
  favor of surfacing to David directly, since he's present by design in this mode.
- A fixed, hardcoded dispatch mechanism (`Agent` tool vs. `Workflow` tool) — deferred to a
  setup-time question per repo/user preference.
- Any decomposition, synthesis, or partial-result judgment performed by the router itself — the
  specific failure mode this spec's research base exists to avoid; not a gap, a deliberate limit.
- A lighter "spontaneous" mode — raised during the same grilling session but as a separate,
  parked addition (see `autopilot`'s Out of Scope); not part of this spec.

## Further Notes

- Backed directly by research run during grilling into cheap-orchestrator/expensive-worker
  delegation patterns. The consistent finding across sources: a weak "planner" given real
  decomposition/synthesis/recovery duties is a documented failure mode (one scaling study found a
  weak-planner configuration losing roughly 40% relative performance versus a weak-actor
  configuration with the same total capacity); a cheap model doing classification-and-handoff only
  is the well-precedented, safe version. This spec commits to the latter shape throughout.
- Shares the Confidence guideline concept with `autopilot`, though `delegate`'s live, human-present
  framing makes its escalation path simpler — "ask David" is just the conversation continuing,
  not a special mechanism.
