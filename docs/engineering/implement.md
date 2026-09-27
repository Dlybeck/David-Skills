## What it does

`implement` builds understood, authorized work with testing and whole-change review. The source can be a conversation, goal, [spec](https://www.aihero.dev/ai-coding-dictionary/spec), or tickets. A formal planning artifact is not required.

## When to reach for it

Type `/implement`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) selects it when behavior is understood and implementation is authorized. Advice and diagnosis-only requests do not trigger a repair.

## Evidence before delivery

Use [tdd](./tdd.md) where appropriate, with agreed or delegated testing seams. Review the entire change against the current request, including corrections, through [code-review](./code-review.md). When delegation is unavailable or unauthorized, perform the same review axes locally and disclose the lack of independence.

[Attention modes](../productivity/attention-modes.md) keeps consequential questions brief when you are On the side. [Tool fit](../productivity/tool-fit.md) brings in connected evidence or a useful UI preview when the host supports it; the tests and whole-change review still determine delivery readiness.

| Authority available | Delivery |
| --- | --- |
| Local edits and tests only | Tested, reviewable local diff |
| Commits authorized | Commit on the authorized branch |
| Ticket update authorized and acceptance passes | Resolve the originating ticket |

## Common questions

**Must I create a spec or tickets first?**

No. Clear requirements in the current conversation or goal are enough.

**Will it commit and close issues automatically?**

Only when those effects are authorized. Merely selecting the skill grants neither permission.

**Does review require more agents?**

Respect the active delegation budget. Local review is available when additional agents are not authorized; it is not described as independent review.

## It's working if

- The implementation matches the latest agreed behavior.
- Relevant tests pass and review findings are addressed.
- The result distinguishes tested, committed, and tracker-resolved states.
- No unrelated scope or extra approval ceremony appears.

## Where it fits

A delivery practice that can stand alone or follow [to-tickets](./to-tickets.md). [pursue-goal](./pursue-goal.md) may select it during an authorized run; [advise](./advise.md) explains its role.
