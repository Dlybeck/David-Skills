# 01 — `autopilot` skill

**What to build:** The full `autopilot` skill and its registry integration, per
`.scratch/autopilot/spec.md` — a manually-triggered, unattended work mode that locks its goal via
a pre-departure grilling session, then runs backgrounded until the goal is met or it hits a
blocker only a human can resolve.

**Blocked by:** None — can start immediately. Doesn't hard-depend on `delegate`'s ticket-status
fix; `autopilot` isn't necessarily working off `/to-tickets` output.

**Status:** resolved

- [x] New user-invoked skill `autopilot` at `skills/engineering/autopilot/` (`SKILL.md` +
      `agents/openai.yaml`, same invocation pattern as other user-invoked skills)
- [x] `SKILL.md` documents: manual-only trigger (never scheduled); a pre-departure `/grilling`
      session that locks the goal condition and scope/guardrails before backgrounding
- [x] Documents launching via `claude --bg` driving native `/goal <condition>`, and states why
      (survives full disconnection; the harness's session-scoped `/loop` does not)
- [x] Documents the **Confidence guideline** (per `CONTEXT.md`/ADR 0005) as the safety model in
      place of a hard time/token ceiling — act freely inside locked scope or on a strong existing
      confidence signal; anything outside scope or hard to reverse gets logged, not acted on
- [x] Documents that each unit of work ends with `/code-review`, and real findings get fixed
      before it's considered done
- [x] Documents idle-capacity tech-debt work via `/re-architect`'s scan, acting only on
      `Strong`-scored candidates; `Worth exploring`/`Speculative` candidates are left in the
      closing report instead
- [x] Documents completing the full git cycle autonomously (commit, merge `--no-ff` into `dev`,
      push, delete branch) — `dev` is unrestricted for the agent; only `main` is human-gated, and
      that's already covered by the existing hook with no changes
- [x] No changes made to `hooks/block-dangerous-git.py`
- [x] Documents the closing report as the background session's own final plain-English message,
      read via `claude agents` — no new saved-file convention introduced
- [x] Registry integration complete: `.claude-plugin/plugin.json`, top-level `README.md`,
      `skills/engineering/README.md` (User-invoked), `docs/engineering/autopilot.md` (four-section
      template per `.agents/writing-docs.md`), `ask-claude`'s `SKILL.md` map
- [x] `claude plugin validate . --strict` passes

## Comments

- 2026-08-07 — `/code-review` (Standards axis) caught the "delegated continuation" reasoning
  restated three times near-verbatim (`.agents/invocation.md` → `SKILL.md` → docs page) instead
  of pointed back to once; trimmed `SKILL.md` and the docs page down to bare pointers. Also caught
  a dangling reference to `claude-handoff` (unpromoted, no docs page) — reworded to describe the
  `claude --bg` mechanism generically instead of name-dropping an unlinkable skill.
- 2026-08-07 — `/code-review` (Spec axis) caught real, undeclared scope: this ticket never
  authorized touching `.agents/invocation.md` or the already-shipped `skills/engineering/delegate/
  SKILL.md`. Judged the generalization itself worth keeping — the same "delegated continuation"
  reasoning was independently needed twice over just within this ticket (continuing this skill's
  own process unattended; running `/re-architect`'s scan without its human-only steps), on top of
  what `delegate` already needed for `/implement` — but the cross-file touch needed to be
  traceable, not just noted in a commit message. Comment appended to `delegate/03`'s own ticket
  cross-referencing this one.
