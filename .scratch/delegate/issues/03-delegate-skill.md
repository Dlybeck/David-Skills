# 03 — `delegate` skill

**What to build:** The full `delegate` skill and its registry integration, per
`.scratch/delegate/spec.md` — a light model acting strictly as a **router** (classify and hand off
whole tickets, never decompose work or judge a worker's partial result) over Sonnet/Opus subagent
workers, in a live mode where the user stays present.

**Blocked by:** 01 (`/implement` marks its ticket resolved), 02 (generalized `Frontier`
definition) — the router's core mechanism reads ticket status from 01 and dispatches from the
frontier defined in 02.

**Status:** resolved

- [x] New user-invoked skill `delegate` at `skills/engineering/delegate/` (`SKILL.md` +
      `agents/openai.yaml`, `disable-model-invocation: true` / `policy.allow_implicit_invocation:
      false`, per `.agents/invocation.md`)
- [x] `SKILL.md` documents the router role explicitly: classify + hand off whole tickets pulled
      from the frontier (per `docs/agents/issue-tracker.md`); never decompose work into invented
      subtasks; never judge a worker's partial result — quality judgment stays with each worker's
      own `/implement` → `/code-review` gate
- [x] Live/present framing documented: a worker stuck beyond its ticket's spec surfaces directly
      to the user in conversation; no automatic stronger-model fallback
- [x] Generalizes past Fable to any cheap/expensive model pair; Fable documented as the flagship,
      motivating case, not a hard requirement
- [x] Always manually invocable regardless of active model; additionally *recommended* — never
      auto-enabled — via a best-effort `SessionStart` model check
- [x] Documents that entering the mode satisfies the `Workflow` tool's own required multi-agent
      opt-in for the rest of the session
- [x] Dispatch mechanism (raw subagent calls vs. the `Workflow` tool; if `Workflow`, average
      agents per phase and a preferred delegation model) is asked of the user at setup time, not
      hardcoded
- [x] `CONTEXT.md`'s `Router` / `_Avoid_: orchestrator, manager` vocabulary used consistently
      throughout the skill's own text
- [x] Registry integration complete: `.claude-plugin/plugin.json`, top-level `README.md`,
      `skills/engineering/README.md` (User-invoked), `docs/engineering/delegate.md` (four-section
      template per `.agents/writing-docs.md`), `ask-claude`'s `SKILL.md` map
- [x] `claude plugin validate . --strict` passes
- [x] The router has its own claim convention for dispatching plain `/to-tickets` tickets in
      parallel — resolved by adding a general "claim the ticket" convention to
      `docs/agents/issue-tracker.md` and both seed templates (mirroring `wayfinder`'s own claim
      step exactly) rather than inventing a delegate-specific mechanism

## Comments

- 2026-08-07 — `/code-review` (Standards axis) caught a real, load-bearing tension left implicit
  in the first pass: dispatching a worker to run `/implement` is exactly the reach
  `.agents/invocation.md` forbids — `/implement` is user-invoked, and no other skill (including
  `delegate`) can reach a user-invoked skill. Resolved explicitly in the Dispatch section: workers
  follow `/implement`'s process directly rather than invoking it as a skill call, on the reasoning
  that turning `delegate` on is itself the one deliberate human trigger the rule requires — it
  substitutes for typing `/implement` per ticket, not a way around who's allowed to trigger it.
  Also caught: "Workflow" used with no grounding (clarified as Claude Code's own orchestration
  tool) and two Setup questions (average agents per phase, preferred delegation model) collected
  but never used in Dispatch — both now wired in.
- 2026-08-07 — `/code-review` (Spec axis) caught that the SessionStart best-effort recommendation
  was documented in prose only, with no actual mechanism behind it, despite its checkbox already
  being marked done. Fixed properly: added `hooks/delegate-recommend.py` (verified against Claude
  Code's actual hook docs for the exact input/output contract, not guessed) and wired it into
  `hooks/hooks.json`. Manually tested against four scenarios (no `model` field; matching model, no
  config; matching model, with config; non-matching model, with config) — all behaved correctly.
- 2026-08-07 — Out-of-band note from building `autopilot` (`.scratch/autopilot/issues/01-
  autopilot-skill.md`): this file's Dispatch-step reasoning about `/implement` being a delegated
  continuation, not an invocation, was trimmed to a bare pointer at `.agents/invocation.md`'s new
  "Delegated continuation of a user-invoked skill's own process" section — the same reasoning
  `autopilot` needed twice over, promoted to shared doctrine rather than re-derived a third time.
  Not authorized by this ticket's own scope; flagged as a deliberate, traceable deviation rather
  than a silent one. No behavioral change to `delegate` itself, wording only.
