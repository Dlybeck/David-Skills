---
name: autopilot
description: Enter unattended work mode — lock a goal before you leave, then keep working without you until it's met.
disable-model-invocation: true
---

# Autopilot

Manually triggered only — "I'm leaving, keep working without me" — never scheduled. Once
entered, work continues in a background session, bounded by the **Confidence guideline** (see
`CONTEXT.md`) rather than a fixed time or token ceiling: a legitimately long-running task (a
long-running external job, say) is meant to run its course, not get killed by an arbitrary
cutoff.

**Prerequisite:** this repo runs a `dev` integration branch (`main ← dev ← feature/**`, with
`main` human-gated) — a personal workflow assumption stated rather than generalized away, per ADR 0006. A
repo without a `dev` branch is outside this skill's audience.

## Entering the mode

1. **Lock the goal, right here.** Run a `/grilling` session in this same conversation to settle
   the goal condition (what `/goal` gets set to) and any scope or guardrail questions. An
   unattended run needs its destination settled while a human is still there to settle it —
   reviewing scope drift after the fact is too late.
2. **Launch the background session with `/goal` as the literal launch argument**:
   `claude --bg --name "<descriptive name>" "/goal <condition>, landed on dev via a feature
   branch merged --no-ff — never a direct commit — with any real /code-review finding fixed
   first. Guardrails: never commit directly to dev; run /code-review after each unit of work and
   fix any real finding before continuing; use idle capacity only on Strong-scored /re-architect
   candidates, leaving Worth exploring and Speculative ones logged for review instead of acted
   on; log anything outside locked scope, or hard to reverse, instead of acting on it; stop when
   the condition is met or progress genuinely stalls."` This is a **delegated continuation**, per
   `.agents/invocation.md`, of `autopilot`'s own process — not the assistant emitting `/goal` from
   its own output, which does nothing. The CLI parses a fresh session's launch argument as real
   input, the same way it parses a human's own first message, and sets an actively-enforced Stop
   hook from it.

   The whole string after `/goal ` becomes the enforced condition — confirmed directly, not
   assumed. State every checkable essential (the git cycle, the review gate, the guardrails
   above) as content inside the condition text itself, in plain language the evaluator can judge
   on its own. Carry nothing by pointer: a path into this repo's checkout resolves only here, not
   from a plugin-cache or `skills.sh` install (ADR 0006), so the launch argument has to be
   self-contained rather than deferring to a file the background session might not be able to
   reach.
3. **`claude --bg` auto-isolates into its own git worktree** — a property of the mechanism, not
   something `autopilot` sets up. It's also what actually answers the risk of continuing to chat
   in the same window and losing track of the run: a `--bg` job has its own separate, `claude
   agents`-trackable identity, independent of whatever this conversation does next. Whatever's
   already keeping *that* background session durable against disconnection (a terminal
   multiplexer, typically) is `--bg`'s own concern from here — it survives closing the terminal
   outright, so `autopilot` doesn't need to provide that itself.

## The working loop

Once the background session's own `/goal` is active:

1. Branch, build, run `/code-review` (fully autonomous — no human needed to run it), and fix any
   real finding before continuing. This is the one review gate this run gets; there's no one else
   to catch what it misses.
2. When there's no locked work left to do this instant, use the idle capacity for tech debt:
   follow `/re-architect`'s own exploration and candidate-scoring steps directly — a **delegated
   continuation**, per `.agents/invocation.md`, of its process rather than an invocation of it
   (`/re-architect` is user-invoked) — but skip its pick-and-grill steps entirely, since those need
   a human this mode doesn't have. Act only on `Strong`-scored candidates; leave `Worth exploring`
   and `Speculative` candidates in the closing report instead of touching them.
3. **Never commit directly to `dev`.** Once a unit of work is clean, complete the full git cycle:
   branch, commit, merge `--no-ff` into `dev`, push, delete the feature branch. `dev` is this
   agent's own branch throughout this repo's history — nothing here waits for a human — but the
   branch-then-merge shape is not optional, even hands-off. Only `main` is human-gated, and that's
   already covered unconditionally by the existing `hooks/block-dangerous-git.py`; this skill
   makes no changes to it.

## The Confidence guideline

Applied continuously, per `CONTEXT.md`: act on the scope locked in step 1, or an existing strong
confidence signal; log anything else for review instead.

Before the run ends, apply it once more, holistically, across everything the run actually did: is
there anything here the user would likely push back on? Log it rather than let a pattern of small,
individually-fine actions add up to something surprising on return.

## Ending

Stop when:

- `/goal`'s evaluator confirms the locked condition is met, or
- Progress genuinely stalls — a full turn with no forward movement, or something surfaces that
  only the user can decide. Sharper stuck/no-progress heuristics (what exactly counts as
  "stuck," how many turns) are deliberately left undefined: `/goal`'s evaluator only judges the
  locked condition and has no native give-up exit, and a stall is itself a special case of the
  Confidence guideline — low confidence you're headed anywhere good — not a separate problem to
  solve.

Close with a plain, high-level message in the background session itself — what got done, what got
logged and left for review, and which of the two conditions above ended the run. Read it via
`claude agents`/`claude logs` when you check in. There's no separate saved report file: git
history — the commits, the merged branches — is already the durable record of what happened; the
message is just the human-readable summary of it.
