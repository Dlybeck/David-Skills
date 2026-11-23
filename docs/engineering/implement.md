## What it does

`implement` builds understood, authorized work and checks it by judgement. The source can be a conversation, goal, [spec](https://www.aihero.dev/ai-coding-dictionary/spec), or tickets. A formal planning artifact is not required.

An implementation request includes the routine local preparation needed to build and test it.
Missing dependencies are work to resolve, including when discovered partway through a task.

## When to reach for it

Type `/implement`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) selects it when behavior is understood and implementation is authorized. Advice and diagnosis-only requests do not trigger a repair.

## Evidence before delivery

Use [tdd](./tdd.md) where appropriate, with agreed or delegated testing seams. Before delivering,
the agent asks what the change could break and tests that. A small change may need only its tests;
one that could really hurt something (shared code, data, security, a release) gets one fresh
[independent-pr-review](./independent-pr-review.md). Fixes are checked, not re-reviewed in full.

Do not use the test suite casually. During development, run the tests for what changed plus a quick
smoke check; run a full check only when warranted (the PR to `main`, shared code, test setup or
dependencies, risk targeted tests cannot cover, or a check the repo requires). Tests should not be
a significant time blocker: run a slow full check in the background and keep working.

When a full check is warranted and the repo has a delivery gate (a local release script or
`make check`-style target; with only CI, its test command run locally), that gate is the full
check. The agent runs it once on the head it delivers, not the raw suite as well. A later
behavior change, such as a review fix, means one more run on the new head. Later steps such as a
deploy trust the gate's result instead of rerunning it.

Steps that need you, such as a sudo deploy or an approval, cost the most. Before a fix that needs
one, the agent reproduces every known live failure in that area and fixes them together. It says
up front how many such steps it will ask for. When it builds or changes a pipeline, it checks
which build tool the host really uses, builds only what ships with an explicit target, names one
authoritative check that later steps trust. For a release with slow steps it may also test that
the deploy does not rerun that check and write down each step's expected time.

[Attention modes](../productivity/attention-modes.md) keeps consequential questions brief when you are On the side. [Tool fit](../productivity/tool-fit.md) brings in connected evidence or a useful UI preview when the host supports it; the checks still determine delivery readiness.

| Authority available | Delivery |
| --- | --- |
| Local edits and tests only | Tested, reviewable local diff |
| Commits authorized | Commit on the authorized branch |
| Ticket update authorized and acceptance passes | Resolve the originating ticket |

## Delivery

Repository policy and applicable standing grants route delivery.

| Boundary | Settled delivery |
| --- | --- |
| Authorized agent-owned integration | Complete integration after every gate passes; a traceability PR needs no repeat human handoff |
| Human-owned promotion | Prepare the exact proposal for required approval |
| Missing policy or authority | Preserve the result within existing authority and report the unresolved decision |

## Common questions

**Must I create a spec or tickets first?**

No. Clear requirements in the current conversation or goal are enough.

**Will it commit and close issues automatically?**

Only when those effects are authorized. Merely selecting the skill grants neither permission.

**What if the toolchain or packages are missing?**

The agent checks project pins, installs or repairs compatible local prerequisites, sets up an
isolated test environment when useful, and continues. It does not ask again for routine setup.
A host permission denial, or something yours alone such as a new credential, still comes to you.

**Does every change get reviewed by another agent?**

No. Several reviewers on every change, redone after every fix, cost time and money and stand in for
judgement. The builder tests what could break; a fresh reviewer comes in only when the change could
really hurt something.

**What does it ask me about?**

Only what is yours alone: putting work on `main`, a new credential, spending, or deleting what
can't be made again. Everything else it decides by its own judgement, making its best guess on
anything that can be undone and telling you what it chose.

**Does every tiny edit trigger another test run?**

No. Another run needs a relevant behavior change, failure, unresolved concern, or delivery gate.
A comment or wording edit does not automatically invalidate a passing behavior check.

**Why doesn't it run the full suite before the release gate?**

The gate already runs it. Running both doubles the wait and proves nothing new. Targeted tests
catch mistakes while working; the gate is the one check delivery depends on.

**Why did it ask about several bugs before deploying?**

Each deploy that needs you costs your time at the keyboard. It finds every live failure it can
reproduce first, so one deploy covers all of them.

## It's working if

- The implementation matches the latest agreed behavior.
- What the change could break was tested; review was used where the change earned it.
- A missing local dependency triggers setup and a retry, rather than an authorization stop.
- The result distinguishes tested, committed, and tracker-resolved states.
- No unrelated scope or extra approval ceremony appears.
- When a full check is warranted and a delivery gate exists, the gate runs once on the delivered head, and the raw suite does not also run before it.
- Known live failures ship in one batch, with one request for each human step.

## Where it fits

A delivery practice that can stand alone or follow [to-tickets](./to-tickets.md). [pursue-goal](./pursue-goal.md) may select it during an authorized run; [advise](./advise.md) explains its role.
