## What it does

`to-tickets` decomposes understood work into **[tracer bullets](https://www.aihero.dev/ai-coding-dictionary/tracer-bullet)**: verifiable vertical slices with explicit blocking edges. It accepts a conversation, plan, or spec; it does not require all three.

## When to reach for it

Type `/to-tickets`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) selects it when authorized work benefits from coordination or restartable slices. Small coherent changes can go directly to [implement](./implement.md).

## Decomposition and delivery

Each slice delivers a complete narrow behavior. Wide mechanical refactors retain the expand–contract exception rather than pretending every migration batch is independently shippable.

| Decision | Who handles it |
| --- | --- |
| Granularity and dependencies already delegated | The agent checks them against the outcome |
| Consequential unresolved choice | You resolve the missing decision |
| Publishing or changing tracker state | Requires authority in the request or current contract |

Reuse the project's tracker conventions; [setup](./setup.md) is optional when different configuration is needed. Without publishing authority, return a draft rather than posting issues. Decomposition itself neither launches workers nor authorizes implementation.

## Common questions

**Do I need a spec first?**

No. A conversation or plan can provide the same settled requirements. Use [to-spec](./to-spec.md) only when a separate requirements reference earns its cost.

**Will it stop for approval of every slice?**

Not when you delegated those decisions. You can still correct the breakdown while work proceeds.

**Does it close the parent issue?**

No. The parent is not modified by this skill. Downstream resolution requires its own acceptance evidence and authority.

## It's working if

- Each slice can be verified and its dependencies are real.
- No settled choices are repeatedly put back to you.
- The tracker changes only within the requested authority.
- The breakdown covers the outcome without inventing extra work.

## Where it fits

An optional decomposition practice alongside [to-spec](./to-spec.md) and [implement](./implement.md). [advise](./advise.md) helps choose the relevant practice rather than requiring a sequence.
