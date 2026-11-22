## What it does

`implement` builds understood, authorized work with testing and whole-change review. The source can be a conversation, goal, [spec](https://www.aihero.dev/ai-coding-dictionary/spec), or tickets. A formal planning artifact is not required.

An implementation request includes the routine local preparation needed to build and test it.
Missing dependencies are work to resolve, including when discovered partway through a task.

## When to reach for it

Type `/implement`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) selects it when behavior is understood and implementation is authorized. Advice and diagnosis-only requests do not trigger a repair.

## Evidence before delivery

Use [tdd](./tdd.md) where appropriate, with agreed or delegated testing seams. Review the entire change against the current request, including corrections, through [code-review](./code-review.md). When delegation is unavailable or unauthorized, perform the same review axes locally and disclose the lack of independence.

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

[Attention modes](../productivity/attention-modes.md) keeps consequential questions brief when you are On the side. [Tool fit](../productivity/tool-fit.md) brings in connected evidence or a useful UI preview when the host supports it; the tests and whole-change review still determine delivery readiness.

| Authority available | Delivery |
| --- | --- |
| Local edits and tests only | Tested, reviewable local diff |
| Commits authorized | Commit on the authorized branch |
| Ticket update authorized and acceptance passes | Resolve the originating ticket |

## Independent delivery review

Committed delivery also passes [independent-pr-review](./independent-pr-review.md) before the
settled result. Its repair loop supplements the separate Standards/Spec checks within existing
commenting and delivery authority. Repository policy and applicable standing grants route delivery.

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
isolated test environment when useful, and continues. It reuses applicable standing grants rather
than asking again for routine setup. A real host permission denial, new account or credential,
spending, production change, or material deletion remains a separate boundary.

**Does review require more agents?**

Respect the active delegation budget. Local review is available when additional agents are not authorized; it is not described as independent review.

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
- Relevant tests pass and review findings are addressed.
- A missing local dependency triggers setup and a retry, rather than an authorization stop.
- The result distinguishes tested, committed, and tracker-resolved states.
- No unrelated scope or extra approval ceremony appears.
- When a full check is warranted and a delivery gate exists, the gate runs once on the delivered head, and the raw suite does not also run before it.
- Known live failures ship in one batch, with one request for each human step.

## Where it fits

A delivery practice that can stand alone or follow [to-tickets](./to-tickets.md). [pursue-goal](./pursue-goal.md) may select it during an authorized run; [advise](./advise.md) explains its role.
