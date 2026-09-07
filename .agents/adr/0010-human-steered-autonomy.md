# Composable practices support human-steered autonomy

## Context

The [development profile](../../docs/agents/david-development-profile.md) establishes substantial
initial collaboration, autonomous execution with intermittent human steering, and reviewer-led
completion. Less human command management must not reduce engineering discipline or erase a
skill's original purpose. The existing engine already supports optional artifacts and adaptive work.

## Decision

- Preserve every promoted skill and name. `advise` remains a plugin router, not general planning.
- Make exactly `to-spec`, `to-tickets`, `implement`, and `handoff` model- and user-reachable in both
  harnesses. Their descriptions identify real triggers; their side effects require authority.
- Accept delegated seam and decomposition decisions without repeated approval. Keep product
  changes, external writes, commits, issue closure, and worker dispatch separately authorized.
- Keep `pursue-goal` as the shared engine. Persist clear corrections, reconcile affected work,
  distinguish questions/suggestions from instructions, and preserve the current direction across
  context transfers. A stable contract is stable against model drift, not against its owner.
- Keep status reporting read-only with respect to the goal and plan, exposing current intent and
  evidence in chat. Keep routine continuity distinct from a portable handoff.
- Prefer native non-AI waiting, within account policy and host limits. A small helper is justified
  only if it actually supplies missing execution/receipt/wait functionality; it must not pretend
  to wake a chat. A persistent agent service or custom production client requires redesign.

## Validation and remaining boundary

Six opt-in pivot scenarios cover plugin routing, small delivery, artifact composition, real
in-flight steering plus fresh-context transfer, status-only reporting, and native short waiting.
Offline protocol tests and process receipts are not live behavioral passes. Production long-job
continuation remains unproven until the current host demonstrates completion followed by useful
agent work, including failure and interruption handling. Account-policy changes require separate
explicit approval; this ADR cannot grant it. See the dated evaluation report for actual coverage.
