## What it does

`implement` builds understood, authorized work with testing and whole-change review. The source can be a conversation, goal, [spec](https://www.aihero.dev/ai-coding-dictionary/spec), or tickets. A formal planning artifact is not required.

An implementation request includes the routine local preparation needed to build and test it.
Missing dependencies are work to resolve, including when discovered partway through a task.

## When to reach for it

Type `/implement`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) selects it when behavior is understood and implementation is authorized. Advice and diagnosis-only requests do not trigger a repair.

## Evidence before delivery

Use [tdd](./tdd.md) where appropriate, with agreed or delegated testing seams. Review the entire change against the current request, including corrections, through [code-review](./code-review.md). When delegation is unavailable or unauthorized, perform the same review axes locally and disclose the lack of independence.

Do not use the test suite casually. Select checks for changed behavior and risk, preserve passing
evidence while it remains relevant, and run required full checks before delivery.

[Attention modes](../productivity/attention-modes.md) keeps consequential questions brief when you are On the side. [Tool fit](../productivity/tool-fit.md) brings in connected evidence or a useful UI preview when the host supports it; the tests and whole-change review still determine delivery readiness.

| Authority available | Delivery |
| --- | --- |
| Local edits and tests only | Tested, reviewable local diff |
| Commits authorized | Commit on the authorized branch |
| Ticket update authorized and acceptance passes | Resolve the originating ticket |

## Independent delivery review

Committed delivery also passes [independent-pr-review](./independent-pr-review.md) before the
settled result. Its repair loop supplements the separate Standards/Spec checks within existing
commenting and delivery authority. Repository policy and applicable standing grants route settled
work to agent-owned integration or a human-owned approval boundary; a dev-target traceability PR
does not itself require another human handoff.

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

## It's working if

- The implementation matches the latest agreed behavior.
- Relevant tests pass and review findings are addressed.
- A missing local dependency triggers setup and a retry, rather than an authorization stop.
- The result distinguishes tested, committed, and tracker-resolved states.
- No unrelated scope or extra approval ceremony appears.

## Where it fits

A delivery practice that can stand alone or follow [to-tickets](./to-tickets.md). [pursue-goal](./pursue-goal.md) may select it during an authorized run; [advise](./advise.md) explains its role.
