# Autopilot uses a confidence guideline instead of a hard duration ceiling

[ADR 0010](./0010-human-steered-autonomy.md) refines the continuation design: a verified permitted
non-AI callback/wait may continue the run; returning control remains the current policy fallback
when that capability is absent. Confidence never expands the current user-authorized scope.

`autopilot` is unattended work triggered by an explicit handoff. It does not impose an
arbitrary time or token cutoff because some valid goals take longer than a fixed ceiling.

## Decision

Use the **Confidence guideline** from `CONTEXT.md`: act freely inside the scope locked during
the pre-departure grilling session, or on an existing strong confidence signal. Anything outside
that scope, difficult to reverse, or requiring new authority is logged and left for human review.

Long-running external commands are operating-system processes, not model polling loops. They
write progress to a log and finish with a success/failure receipt; the agent returns control
rather than repeatedly checking unchanged state.

The shared `pursue-goal` engine preserves this boundary in both harnesses. Claude Code launches
through `claude --bg` with a literal `/goal` argument. Codex uses its native durable goal capability
and establishes linked-worktree isolation separately because goal continuation does not create it.
Neither adapter spends model turns polling an unchanged long-running process.

The confidence boundary is not permission to bypass human gates. `re-architect` candidates may
be acted on unattended only when the skill itself rated them `Strong`; weaker candidates remain
recommendations for review.
