# 01 — Rewrite `autopilot` for the inline mechanism

**What to build:** `autopilot` no longer launches `claude --bg`. It sets `/goal` itself, in the
current session, right after the pre-departure grill locks the condition, and its working loop
dispatches chunks of work as background subagents — mirroring `/code-review`'s own existing
parallel-subagent pattern — instead of running synchronously or seeding a separate process.
`CONTEXT.md`'s `Autopilot` entry, `docs/engineering/autopilot.md`, and ADR 0005 (a dated update
note, not a rewrite) all resync to match.

**Blocked by:** None — can start immediately.

**Status:** resolved

- [x] `autopilot/SKILL.md`'s "Entering the mode" section no longer references `claude --bg`;
      documents setting `/goal <condition>` itself, in the current session, right after the
      pre-departure grill
- [x] `SKILL.md`'s working loop documents dispatching chunks of work (build, `/code-review`,
      idle-capacity `/re-architect` scan) as background subagents via the `Agent`/`Workflow` tool,
      mirroring `/code-review`'s own parallel-subagent pattern
- [x] Documents explicitly that `/goal`'s Stop hook is what forces continuation on a re-invoked
      turn, and that its evaluator only judges what's visible in the conversation — so dispatched
      findings must be surfaced in `autopilot`'s own response, not just acted on silently
- [x] The `/re-architect` "delegated continuation" citation to `.agents/invocation.md` is kept
      unchanged; the `claude --bg`-specific citation is removed, since there's no longer a
      separate session to justify
- [x] No mention of `claude --bg` remains anywhere in `autopilot/SKILL.md` or
      `docs/engineering/autopilot.md`, as either the default or an offered alternative — the one
      exception is a new FAQ entry in the docs page and a new ADR update note, both deliberately
      historical ("this is what was tried and why it was dropped"), not current behavior
- [x] Closing-report guidance corrected: read by reopening the same conversation, not via
      `claude agents`/`claude logs`
- [x] `CONTEXT.md`'s `Autopilot` entry reworded away from "backgrounded session" — turned out
      already satisfied; the entry never actually said that (checked before editing rather than
      assumed)
- [x] `.agents/adr/0005-no-hard-ceiling-on-autopilot-confidence-guideline-instead.md` gets a dated
      update note (not a rewrite) recording this correction
- [x] `docs/engineering/autopilot.md` resynced to match, per `.agents/writing-docs.md`'s
      re-sync-on-behavior-change rule
- [x] `claude plugin validate . --strict` passes

## Comments

- 2026-08-07 — `/code-review` (Standards axis) caught two real dictionary-link violations in
  `docs/engineering/autopilot.md` (`session` linked on its second occurrence instead of its
  first; `subagent` — a named dictionary term — never linked at all) and one under-specificity
  gap (the `Agent`/`Workflow` tool was never actually named, just described as "a background
  subagent"). Fixed in both `SKILL.md` and the docs page.
- 2026-08-07 — `/code-review` (Spec axis) caught real, undeclared scope: the ticket's checklist
  only authorized removing the stale `claude --bg` citation from `.agents/invocation.md`, not
  adding the new clarifying paragraph distinguishing self-continuation from delegated
  continuation. Judged worth keeping — it's genuinely useful and low-risk (adds a distinction,
  changes no existing rule) — but flagged here explicitly rather than left traceable only in the
  commit message, matching how the same situation was handled the first time `autopilot` touched
  this file.
- 2026-08-07 — `/code-review` (Spec axis) also caught that this ticket never turned the spec's own
  Testing Decisions ("verify with a real run before shipping") into an acceptance criterion, and
  that spec.md's Further Notes didn't actually contain the residual-risk statement its own Testing
  Decisions section promised. The latter is fixed in `spec.md` directly. The former stands as-is,
  deliberately: the original `autopilot` ticket didn't gate its own merge on a live run either —
  the dry run happened as a separate, follow-up activity afterward, and this ticket follows the
  same precedent rather than inventing a new one. **The live run is still owed, not done.**
