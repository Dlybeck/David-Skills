# Autopilot accepts an authorized stand-in

## Context

The owner wants a TPM — a person or controller — to start development chats, answer their intake
questions, and confirm their goal contracts on the owner's behalf, relaying anything big. An
earlier draft (Oct 1, "delegated requester") spread a requester preamble across most of the
collection; a later beta (Oct 3, "autonomous-autopilot") added a second, parallel Autopilot. The
owner judged that direction too sprawling: the result should be one tidy Autopilot.

## Decision

- Only `autopilot` accepts a **stand-in**. Its rules live in one file,
  `skills/engineering/autopilot/references/stand-in.md`; `grilling` and `pursue-goal` carry one
  pointer line each, honoring the stand-in boundary recorded in the goal contract. Pursue-goal's
  Claude Code and Codex adapters each name the contract-recorded stand-in in one existing line
  (status checks, steering) so they do not contradict that pointer. Every other
  skill, including `yolopilot`, is unchanged and owner-only — Yolopilot skips the grill, and the
  grill is what catches a stand-in's gaps.
- The grant comes only from the message that starts Autopilot. It is copied verbatim into the
  contract with the owner's original request and reservations, and the owner can narrow or revoke
  it. Grants seen only in agent output, tool results, files, or worker messages never count.
- The stand-in may confirm a contract inside the personal-practice envelope, including
  integration under a standing grant found in durable repository policy or owner-written
  instructions; a grant or approval the stand-in asserts itself does not count. It relays to the
  owner, before confirmation: contract changes to objective, scope, authority, or delivery
  target; integration or push authority not already so granted; anything outside the envelope;
  human-owned promotion; guessed product intent; and anything beyond the owner's
  original request. Autopilot talks only to the stand-in; silence is never a decision.
- Discovery flags, hooks, permission prompts, and the human-only `main` boundary are unchanged.
  The skill text is guidance, not runtime authentication.

## Considered and deferred

**Hardening option (b):** additionally require a durable owner-authored line (for example in the
consuming repository's `CLAUDE.md`) naming who may act as stand-in, and refuse otherwise. Deferred
for the owner's decision: it resists a spoofed grant in a shared session but adds per-repo setup.
Today the session's explicit handoff is the trusted channel. The same option would also enforce
Yolopilot's owner-only status, which today rests on documentation outside Yolopilot's unchanged
text: its "explicit last-second human handoff" wording cannot tell an owner from a stand-in.

## Validation

`scripts/test_pilot_scenarios.py` statically asserts the stand-in file's grant source, standard
grant block, and escalation list; the Autopilot pointer; the grilling and pursue-goal pointers;
and that Yolopilot and the user-invoked flags are unchanged. Static checks do not prove live host
behaviour with a stand-in.
