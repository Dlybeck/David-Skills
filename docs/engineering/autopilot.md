## What it does

`autopilot` enters unattended work mode: you lock a goal via a pre-departure grilling round, then it launches as a background [session](https://www.aihero.dev/ai-coding-dictionary/session) that sets `/goal` on itself and keeps working until that goal is met or it's genuinely stuck. It carries no time or token ceiling — a legitimately long-running task is meant to run its course, and the run is bounded by judgment instead: the shared Confidence guideline (`CONTEXT.md`), not a clock or a budget.

## When to reach for it

You invoke this by typing `/autopilot` — the agent won't reach for it on its own, and it ships with `disable-model-invocation: true`.

Reach for it when you're about to walk away and want real progress to keep happening while you're gone — not when the work is small enough to just finish before you go. It's the unattended counterpart to [delegate](./delegate.md): a `delegate` run dispatches tickets to workers while you're present to answer escalations; `autopilot` is for when you won't be there at all.

## Prerequisites

The pre-departure grilling round has to happen in an interactive foreground session, with you actually there to settle it — `autopilot` can't skip straight to unattended work without it. Beyond that, no persistent config file or prior setup is required — it locks what it needs fresh each time you invoke it — but the repo itself has to run a `dev` integration branch (`main ← dev ← feature/**`, with `main` human-gated): a personal workflow assumption `autopilot` states rather than generalizes away, per ADR 0006. A repo without a `dev` branch is outside its audience.

## The working loop

`autopilot` launches as a `claude --bg` job whose launch argument is itself a `/goal` invocation — the one mechanism that actually lets it set a real, Stop-hook-enforced goal without you typing anything, since an assistant can't set `/goal` from its own output. The whole launch string after `/goal ` becomes the enforced condition, so the checkable essentials — the git cycle, the review gate, the guardrails — are stated plainly as content inside the condition itself, where the evaluator can actually judge them. Nothing rides along as a pointer into this repo's checkout: that path resolves only here, not from a plugin-cache or `skills.sh` install (ADR 0006), so the launch argument carries everything self-contained instead. `claude --bg` auto-isolates into its own git worktree, which is also what keeps this run from being derailed by whatever you do in your own, separate conversation in the meantime.

Once active, each unit of work runs the same shape you'd drive by hand — branch, build, [code-review](https://aihero.dev/skills-code-review), fix real findings — then completes its own git cycle into `dev`, since `dev` is this agent's own branch throughout this repo's history; it never commits directly to it. Idle capacity runs [re-architect](./re-architect.md)'s exploration and scoring directly, acting only on its `Strong`-scored candidates and leaving the rest for you.

None of this is `autopilot` invoking `/re-architect`, or itself, as skill calls — both are user-invoked. It's a **delegated continuation**, in the sense `.agents/invocation.md` defines: your one deliberate act of running `/autopilot` is the trigger the rule requires, not a skill reaching for another skill on its own initiative.

## Common questions

**Why no time or token limit?**

Because a legitimately long-running task — an external job with its own logs and completion receipt, say — is sometimes the actual goal, and a blunt cutoff would kill it mid-flight for no reason. The Confidence guideline is the safety net instead: judgment about what's safe to act on, not a clock. The external job runs as an operating-system process; the agent does not poll it through repeated turns.

**Why does an unattended mode need a live grilling session first?**

Because "unattended" describes the run, not the setup. The destination has to be settled while a human is still there to settle it — reviewing scope drift after the fact, once you're already gone, is too late to correct it.

**Didn't this try running inline, in the same conversation, for a while?**

Briefly — the assumption was that `autopilot` could set `/goal` on itself from within the current session. It can't: `/goal` only fires on literal input to a session, either a human typing it or a fresh session's own launch argument, never on anything the assistant writes in its own output. Once that was confirmed, staying inline stopped being an option — `claude --bg`, with `/goal` passed as the launch argument itself, is the one mechanism that actually works hands-off.

**Doesn't a separate background process cost a network sandbox, or risk losing track of the run?**

Worth being honest about the first part: an earlier run did hit a `git push` timeout inside a `--bg` job, and for a while that was treated as a real, designed-in cost of backgrounding. A second run pushed fine over the same remote, and nothing in Claude Code's own documentation supports background sessions getting a different network posture — so that finding looks like it wasn't a reliable property to design around, not a reason to avoid `claude --bg`. Losing track of the run is, if anything, the opposite problem, and backgrounding is what actually solves it: a `--bg` job gets its own separate, `claude agents`-trackable identity, so it doesn't share a window with whatever you do next.

## It's working if

- The background job is still running after you close the terminal — that's the point of `claude --bg` over a scheduled loop.
- `dev` has new, real commits when you check back in, arrived at through a branch and a merge, never a direct commit — and `main` is untouched.
- Nothing outside what you locked in during grilling got acted on silently — it shows up logged in the closing message instead.
- The closing message, read via `claude agents`/`claude logs`, tells you plainly which of the two stopping conditions ended the run.

## Where it fits

A standing alternative to running the main chain (`grill-with-docs → to-spec → to-tickets → implement → code-review`) interactively, not a chain step of its own — the same work, just continued without you present. Its stopping mechanism is Claude Code's native `/goal`; its launch mechanism is `claude --bg`, with the goal invocation as the launch argument itself. [ask-claude](./ask-claude.md) is the router over the whole set when you're not sure which flow you're in.
