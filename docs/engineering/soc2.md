## What it does

`soc2` applies Denali's existing SOC2 compliance policy to whatever you point it at — a diff, a spec, a ticket, or a wizard script — and reports back with a policy ID and a compliant alternative for anything that violates it. It carries no policy of its own; every rule lives in the separate `denali-soc2-compliance` skill, and this one is only the seam that calls it from inside a `denali-dev` flow.

## When to reach for it

You invoke this by typing `/soc2` — the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) won't reach for it on its own, and no other skill fires it for you either.

Reach for it right before something ships and actually touches customer data, credentials, or a production write path — a diff about to be reviewed, a wizard script about to walk someone through provisioning access, a ticket about to be published. Most work this plugin produces never needs it; running it on every diff or every ticket would be a false-positive-heavy habit, not a safety net.

## Prerequisites

Needs `denali-soc2-compliance` installed (it ships with the `denali-platform` plugin). If it isn't installed, `soc2` says so and stops rather than inventing a substitute policy.

## The seam, not the source

`soc2` deliberately owns zero policy content. Every other check-style skill in this set that could plausibly duplicate a ruleset instead points at the one place that ruleset actually lives — this is that pattern applied here. If the policy ever needs updating, there's exactly one file to change, and it isn't this one.

## Common questions

**Why isn't this just a third axis on `code-review`?**

It could be, later — that's a deliberate follow-up decision, not a default. Not every repo this plugin runs in is a Denali project handling regulated data, so folding a compliance check into every `code-review` run would fire it far more often than it's wanted. Staying a separate, manually-invoked skill keeps the common case (a review with no compliance angle) free of noise — and it matches shape this plugin already uses elsewhere, not a one-off: `code-review` itself keeps Standards and Spec as genuinely separate axes so one can't pollute the other's judgment, the same reasoning applied one level up here; `research` defers to primary sources rather than reimplementing knowledge, the same way `soc2` defers to `denali-soc2-compliance` rather than reimplementing policy; and `wait-what` stays strictly on-demand rather than firing automatically mid-flow, the same posture `soc2` takes toward `code-review` and `to-tickets`.

## It's working if

- It names a policy ID for every violation it reports, never a vague "this might be a problem."
- A clean pass gets stated plainly, not hedged.
- If `denali-soc2-compliance` isn't installed, it says so outright instead of guessing at a policy.

## Where it fits

A **reach-for-it-anytime standalone**, like [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) or [prototype](https://aihero.dev/skills-prototype) — not a step any chain assumes. Its one real neighbour is [code-review](https://aihero.dev/skills-code-review), which it deliberately does not merge into (see the question above). For which skill to reach for next, [ask-claude](./ask-claude.md) routes the whole set.
