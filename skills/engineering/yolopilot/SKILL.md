---
name: yolopilot
description: Skip the grilling round for a last-second handoff, then work unattended without merging into dev on its own.
disable-model-invocation: true
---

# Yolopilot

Manually triggered only — "I have to leave right now, no time for a grilling round, just go." Reuses `autopilot`'s entire mechanism (self-set `/goal` via a `claude --bg` launch argument, the same working loop, the same Confidence guideline — see `CONTEXT.md`) and skips only its pre-departure grilling round. `autopilot` earns unattended trust by grilling a precise goal before it starts; `yolopilot` skips that and earns the equivalent trust structurally instead, by never letting its own less-scoped judgment reach `dev` without a human decision first.

**Prerequisite:** like `autopilot`, this assumes a `dev` integration branch (`main ← dev ←
feature/**`, with `main` human-gated) — a house assumption stated rather than generalized away,
per ADR 0006. A repo without a `dev` branch is outside this skill's audience.

## Entering the mode

No grilling round happens here. The entry sequence runs straight through, with no wait for a reply between any step:

1. **Show a short, non-blocking warning.** One to two sentences naming the elevated risk directly — there is no locked goal behind this run, and the interpretation of the instruction is the agent's own guess rather than a jointly-grilled one. Invite an immediate objection, then continue right away.
2. **State its own best-guess interpretation** of the loose instruction, plainly, so there is a record of what got assumed even though no one was there to correct it in the moment.
3. **Launch immediately**, with `/goal` as the literal launch argument: `claude --bg --name "<descriptive name>" "/goal <condition>, landed on a feature branch off dev, committed in small frequent steps, pushed, and left there for review — never merged into dev automatically, never a direct commit to dev. Guardrails: run /code-review after each unit of work and fix any real finding before continuing, then one more whole-branch /code-review pass before stopping; use idle capacity only on Strong-scored /re-architect candidates, leaving Worth exploring and Speculative ones logged for review instead of acted on; log anything outside the stated interpretation, or hard to reverse, instead of acting on it."` This is a **delegated continuation**, per `.agents/invocation.md`, of `yolopilot`'s own process — not the assistant emitting `/goal` from its own output, which does nothing. It is the same mechanism `autopilot` uses: the CLI parses a fresh session's launch argument as real input, the same way it parses a human's own first message, and sets an actively-enforced Stop hook from it.

   The whole string after `/goal ` becomes the enforced condition — confirmed directly, not
   assumed. State every checkable essential — the interpretation from step 2, the hard git rule,
   the guardrails above — as content inside the condition text itself, in plain language the
   evaluator can judge on its own. Carry nothing by pointer: a path into this repo's checkout
   resolves only here, not from a plugin-cache or `skills.sh` install (ADR 0006), so the launch
   argument has to be self-contained rather than deferring to a file the background session might
   not be able to reach.
4. **`claude --bg` auto-isolates into its own git worktree** — the same property `autopilot` relies on, not something `yolopilot` sets up itself. It answers the same risk `autopilot` answers this way: a `--bg` job has its own separate, `claude agents`-trackable identity, independent of whatever this conversation does next.

## The working loop

Once the background session's own `/goal` is active, the loop is inherited unchanged from `autopilot` with two exceptions: commit grain, and the git-cycle stopping point.

1. Branch, build, run `/code-review` (fully autonomous — no human needed to run it), and fix any real finding before continuing. This is the one per-unit review gate this run gets, same as `autopilot`.
2. When there's no locked work left to do this instant, use the idle capacity for tech debt the same way `autopilot` does: follow `/re-architect`'s own exploration and candidate-scoring steps directly — a **delegated continuation**, per `.agents/invocation.md`, of its process — skipping its pick-and-grill steps entirely, since those need a human this mode doesn't have. Act only on `Strong`-scored candidates; leave `Worth exploring` and `Speculative` candidates in the closing report instead of touching them.
3. **Commit more often, and at a finer grain, than `autopilot` would.** There is no upfront-verified scope to lean on here — the anchor is the agent's own best-guess interpretation, not a jointly-grilled goal — so the git history itself has to carry the audit trail instead: small, clearly-labeled commits at each step, rather than batching toward the end. If the best-guess interpretation drifts, the history is where that shows up and gets caught.
4. **Never merge into `dev` automatically.** Complete the git cycle only up through a pushed, reviewable feature branch: commit, push, and leave the branch there for review. This is the one hard rule that earns `yolopilot` its own identity, distinct from `autopilot` — merging happens only once a human reviews and approves the branch, at which point the AI can perform the actual merge (`--no-ff` into `dev`) itself, as a follow-up action, rather than the human needing to run the git commands by hand. `dev` is otherwise this agent's own branch throughout this repo's history, but this mode never crosses that line unattended. Only `main` is human-gated, and that's already covered unconditionally by the existing `hooks/block-dangerous-git.py`; this skill makes no changes to it.

## The Confidence guideline

Inherited unchanged from `autopilot`, per `CONTEXT.md` — only its anchor changes, to the agent's own stated best-guess interpretation from step 2 of Entering the mode rather than a jointly-grilled goal.

Before the run ends, apply it once more, holistically, across everything the run actually did: is there anything here a reviewer would likely push back on? Log it rather than let a pattern of small, individually-fine actions add up to something surprising once the branch is reviewed.

## Before stopping

Run one additional `/code-review` pass across the *whole branch* — on top of the per-unit passes already run throughout the working loop — passing its own stated best-guess interpretation as the stand-in for a spec, since no formal spec exists for this run. Fix any real finding it surfaces before closing out; this is the last check before the branch is left for review, so it earns the same treatment a per-unit finding gets.

## Ending

Stop when:

- `/goal`'s evaluator confirms the locked condition is met — the branch is pushed and left for review, never merged into `dev` — or
- Progress genuinely stalls: a full turn with no forward movement, or something surfaces that only a human can decide.

Close with a deliberately explanatory message in the background session itself — not a terse status line. State why the key decisions were made the way they were, what was assumed at each step, and what's riskiest about the result, so the reader can actually understand and trust the work before extending it. Recommend running `/to-spec` retroactively — the work was built without an upfront plan, so it earns a proper spec/ticket record after the fact instead of never getting one. Offer `/teach` as an optional next step for going deeper into the domain — always genuinely optional, since spinning up its full stateful workspace after every run would be disproportionate. Both stay recommendations for the user to act on themselves: `/to-spec` and `/teach` are user-invoked skills, so this run states them and leaves them there. Read the message via `claude agents`/`claude logs` when checking in — there's no separate saved report file; git history — the commits, the pushed branch — is already the durable record of what happened, and the message is the human-readable summary of it.
