## What it does

`yolopilot` is `autopilot` minus the pre-departure grilling round: it takes a loose, one-line instruction, shows a short non-blocking warning naming the elevated risk, states its own best-guess interpretation, then launches immediately as a background [session](https://www.aihero.dev/ai-coding-dictionary/session) — no wait for a reply between any of those steps. It never merges into `dev` on its own; it completes its own git cycle only up through a pushed, reviewable feature branch, leaving the actual merge for a human decision.

## When to reach for it

You invoke this by typing `/yolopilot` — the agent won't reach for it on its own, and it ships with `disable-model-invocation: true`.

Reach for it when a handoff is genuinely last-second — no time even for [autopilot](./autopilot.md)'s grilling round, but you still want real, unattended progress rather than nothing. Reach for `/autopilot` instead whenever there's time for that round: a jointly-locked goal is the stronger guardrail, and `yolopilot` only exists for when that guardrail isn't affordable.

## Prerequisites

Same as `autopilot`: the repo has to run a `dev` integration branch (`main ← dev ← feature/**`, with `main` human-gated) — a house assumption stated rather than generalized away, per ADR 0006. A repo without a `dev` branch is outside its audience.

## The entry sequence

No grilling round happens here. Three steps run straight through, with no pause between them:

| Step | What happens |
| --- | --- |
| 1 | A short, 1–2 sentence non-blocking warning names the elevated risk directly — there's no locked goal, and the read on the instruction is the agent's own guess. |
| 2 | The agent states its own best-guess interpretation of the loose instruction, so there's a record of what got assumed. |
| 3 | It launches immediately via the same `claude --bg` + self-set `/goal` mechanism `autopilot` uses — the interpretation and the hard git rule stated directly in the `/goal` condition text, where the evaluator can judge them. |

## The one hard rule

Everything else about the working loop — the per-unit [code-review](https://aihero.dev/skills-code-review) gate, `Strong`-only [re-architect](./re-architect.md) idle-capacity work, the stopping logic — carries over from `autopilot` unchanged. The one rule that earns `yolopilot` its own identity: it never merges into `dev` automatically. It commits more often and at a finer grain than `autopilot` throughout the run — since there's no upfront-verified scope to lean on, the git history itself has to carry the audit trail — but the branch stops short of the merge. Once a human reviews and approves it, the AI can perform the actual `--no-ff` merge itself as a follow-up action, rather than the human needing to run the git commands by hand.

Before stopping, it runs one more whole-branch `/code-review` pass — on top of the per-unit passes already inherited from the working loop — using its own stated interpretation as the stand-in for a spec, since no formal one exists for a `yolopilot` run.

## Common questions

**Why doesn't this loosen the Confidence guideline the same way it loosens the grilling requirement?**

Because the two are separate concerns. The Confidence guideline — the same one `autopilot` answers to — anchors to *whatever the goal is*; here that anchor happens to be the agent's own best-guess interpretation instead of a jointly-grilled one, which naturally produces more assumption-driven behavior, but nothing about the guideline's own mechanics changed.

**Why does the closing message read so differently from `autopilot`'s?**

Because there's no jointly-set goal to report against — the closing message is doing more work here, explaining *why* key decisions were made and what's riskiest about them, not just stating which of the two stopping conditions ended the run. It also recommends running [to-spec](https://aihero.dev/skills-to-spec) retroactively, so work built without an upfront plan still gets a proper record, and offers [teach](https://aihero.dev/skills-teach) as an optional next step — never a default one.

## It's working if

- The warning and best-guess interpretation both show up before the branch appears, with no confirmation round in between.
- `dev` has no new commits from this run until a human has reviewed and approved the pushed branch — the merge, when it happens, is a distinct follow-up action.
- The pushed branch's history reads as a trail of small, individually-labeled commits, not one large diff.
- The closing message explains its reasoning and assumptions, not just what got done, and recommends `/to-spec` while only offering `/teach`.

## Where it fits

A lighter-entry sibling to [autopilot](./autopilot.md), not a chain step of its own — the same unattended mechanism, entered without the grilling round its safety property normally rests on, and structurally safer at the one point that matters (`dev`) to make up for it. [ask-claude](./ask-claude.md) is the router over the whole set when you're not sure which flow you're in.
