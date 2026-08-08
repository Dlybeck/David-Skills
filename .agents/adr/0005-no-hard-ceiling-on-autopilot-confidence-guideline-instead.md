# Autopilot uses a confidence guideline instead of a hard duration ceiling

`autopilot` is unattended work triggered by an explicit handoff. It does not impose an
arbitrary time or token cutoff because some valid goals take longer than a fixed ceiling.

## Decision

Use the **Confidence guideline** from `CONTEXT.md`: act freely inside the scope locked during
the pre-departure grilling session, or on an existing strong confidence signal. Anything outside
that scope, difficult to reverse, or requiring new authority is logged and left for human review.

Long-running external commands are operating-system processes, not model polling loops. They
write progress to a log and finish with a success/failure receipt; the agent returns control
rather than repeatedly checking unchanged state.

Autopilot currently launches through Claude Code's `claude --bg` with a literal `/goal`
argument so the goal is enforced by the background session's Stop hook. That mechanism is
Claude-specific. A Codex implementation would need its own real continuation mechanism rather
than pretending this command is portable.

The confidence boundary is not permission to bypass human gates. `re-architect` candidates may
be acted on unattended only when the skill itself rated them `Strong`; weaker candidates remain
recommendations for review.
