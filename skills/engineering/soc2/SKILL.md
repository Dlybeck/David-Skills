---
name: soc2
description: Run Denali's SOC2 compliance filter against a diff, spec, ticket, or wizard script before it ships. Deliberately manual — it never fires on its own.
disable-model-invocation: true
---

# SOC2

A thin, on-demand gate: apply Denali's existing SOC2 compliance policy to whatever's in front
of you right now. This skill owns no policy of its own — every rule, policy ID, and compliant
alternative lives in `denali-platform:denali-soc2-compliance`; this one is just the seam that
calls it from inside a `denali-dev` flow, in this plugin's own house style.

## Why separate, not automatic

Not every repo or task here needs a SOC2 pass — most of what `denali-dev` produces (this
plugin's own docs, a solo side project, a non-Denali repo) never touches customer data,
credentials, or a production write path. Wiring this into `code-review` or `to-tickets` so it
fires on every run would be noise most of the time, for the cases that don't need it. This
stays a deliberate, one-command gate: reach for it when the artifact in front of you actually
warrants it, not by default.

## What it checks

Point it at whatever's current — ask if it's not obvious which:

- **A diff** — the changes on the current branch since a fixed point (the same scope
  `code-review` reviews).
- **A spec or ticket** — the output `to-spec`/`to-tickets` is about to publish.
- **A wizard script** — what `wizard` is about to walk someone through, especially anything
  provisioning credentials, secrets, or access.
- **The current conversation** — if none of the above apply, whatever's been decided so far.

## Process

1. Confirm what's being checked. If more than one candidate is in scope (a diff *and* a ticket
   describing it), ask which, or check both explicitly named as separate passes.
2. Run the `denali-platform:denali-soc2-compliance` skill against it. If that skill isn't
   installed, say so plainly and stop — don't improvise a substitute policy from memory.
3. Report findings exactly as that skill reports them: the policy ID and the compliant
   alternative for every violation. Don't summarize away the policy ID.
4. If nothing violates policy, say so plainly — a clean pass is a real answer, not a
   non-answer to soften.

## Where else this gets used

Nowhere automatically — that's the point of keeping it separate. If a later, deliberate
decision wires it into `code-review` as a third axis alongside Standards/Spec, or into `wizard`
whenever secrets are involved, that's its own follow-up call, not something this skill does on
its own initiative.
