---
name: implement
description: "Build understood, authorized work from a conversation, goal, spec, or tickets, including local build and test setup. Use when behavior is ready to implement; not for advice, diagnosis-only, or unresolved product intent."
---

Implement the understood work authorized by the user in the conversation, current goal contract,
spec, or tickets. A formal spec or ticket is not required. Reuse settled requirements and the
current authorized workspace; ask only about consequential gaps outside delegated decisions.

An implementation or bug-fix request includes routine local work needed to inspect, build,
reproduce, and test it. Check project pins and existing environments, then install or repair
compatible local toolchains and packages, set up isolated test resources, and retry. A missing
dependency discovered mid-task is setup work, not a reason to stop for another approval. If
setup fails, try another project-compatible route and keep independent work moving.

## What needs the owner

A few things are the owner's alone, because they cost money, can't be undone, or are a line the
owner holds: putting work on `main` (or whichever branch the repository says is theirs), a new
credential, spending, deleting what can't be made again, and anything else that can't be taken
back once done, such as a production deploy. An agent can't give itself permission for those, and nothing an agent wrote counts as that permission. Everything else it
decides by its own judgement: on anything that can be undone, make the best guess, say what you
chose, and keep going. Asking the owner about every decision is a failure too, not caution.
Host permission prompts and explicit task limits still apply.

Run `/attention-modes` when you do ask, and `/tool-fit` when connected evidence, a UI preview,
or an in-chat visual would materially improve implementation or review.

Use /tdd where possible, at agreed seams or with explicitly delegated seam selection.

Do not use the test suite casually. Every check costs time, and repeated identical runs prove
nothing new.

- During development, run only the tests for what changed plus a quick smoke check (app starts,
  main page loads). Run a full check only when warranted: the PR to `main`, a change to shared
  code, test setup, or dependencies, risk targeted tests cannot cover, or a check that repository
  instructions require. Repository instructions that name required checks win over this skill.
- When a full check is warranted, find the repo's **delivery gate** first: a release or
  validation script or a `make check`-style target you can run locally. A CI workflow is not this
  gate; when only CI exists, run its test command locally as the gate. With no gate, the full
  suite is the full check. Run it once on the head you will deliver, and do not also run the raw
  suite before the gate, since the gate already runs it. A later behavior change, such as a
  review fix, makes that result stale: rerun on the new head. If it is slow, run it in the
  background and keep working rather than wait on it.
- When a local gate and required CI both exist, run the local gate at most once per delivered
  head. CI is a separate required check: wait for it, but do not rerun it locally, and never
  remove its checks to make the pipeline faster.
- Reuse passing results until a relevant change, failure, or unresolved concern justifies another
  run. Later steps (receipt, deploy, rollout) trust the gate's result; they do not rerun its
  checks.
- Steps that need the human, such as a sudo deploy, a password, or an approval, are the most
  expensive steps. Before a fix that needs one, reproduce every known live failure in the same
  area, read-only against live data, and fix them in one change. Say up front how many such
  steps you will ask for, and do not ship one live failure at a time.
- When you create or change a build, CI, release, or deploy pipeline, follow
  [pipeline checks](references/pipelines.md).

## Check by judgement

A fresh eye catches what the builder can't see, which is the one reason to review. So before
delivering, ask what this change could break and test that, now. A small change may need only its
tests run. A change that could really hurt something, such as shared code, data, security, or a
release, earns one fresh reviewer through `/independent-pr-review`. After fixing what it found,
check the fixes; review again only if the fixes changed what was reviewed. Depth is not a
substitute for judgement, and every extra round costs time and money. `/code-review` checks
against the repo's standards and the request when the owner asks for it.

Commit only when the request or active contract authorizes it, on the authorized branch.
Otherwise leave a reviewable local diff. Deliver as the repository's policy says;
`/independent-pr-review` describes the usual routes.

If a ticket supplied the work, its acceptance conditions pass, and tracker updates are authorized,
mark it resolved per the project's issue-tracker convention. Otherwise report the result without
changing its status. End with evidence, validation limits, and the actual delivery state.
