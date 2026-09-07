## What it does

`to-spec` synthesizes settled requirements into a proportionate **[spec](https://www.aihero.dev/ai-coding-dictionary/spec)**. It captures the current understanding rather than starting another interview. Publishing to the configured tracker requires authority.

## When to reach for it

Type `/to-spec`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) selects it when authorized work needs a durable requirements reference.

| Situation | Useful next practice |
| --- | --- |
| Requirements are settled and need a reference | `to-spec` |
| Product intent is unresolved | [grill-with-docs](./grill-with-docs.md) |
| Understood work needs building, not another artifact | [implement](./implement.md) |
| Work needs decomposition | [to-tickets](./to-tickets.md), with or without a spec |

## Seams and scope

Reuse agreed testing seams or delegate their selection. Ask only about consequential unresolved choices outside that delegation. Capture distinct behaviors, important edge cases, implementation decisions, testing, and exclusions; do not invent user stories to make the document longer.

A known tracker convention and write authority are prerequisites to publishing, not to drafting. Without them, the result stays in chat or an authorized notes location. [setup](./setup.md) remains a human-selected configuration tool.

## Common questions

**Do I have to approve the same technical choices again?**

No. Existing agreements and explicitly delegated choices count. New product intent or broader authority still belongs to you.

**Does a spec authorize building or posting issues?**

No. The request or active contract supplies those permissions. A `ready-for-agent` label is applied only when both settled requirements and authority support it.

**Is an extensive user-story list required?**

No. Architectural work can emphasize interfaces and invariants. Detail should prevent ambiguity, not fill a template.

## It's working if

- The result reflects settled intent without another unnecessary interview.
- Its scope and length fit the actual problem.
- You can tell whether it is a draft or a published artifact.
- Selecting it does not start implementation.

## Where it fits

A requirements-capture practice, not an admission gate. [to-tickets](./to-tickets.md) can decompose its result; [implement](./implement.md) can also work directly from a conversation or goal. [advise](./advise.md) explains which plugin tool fits.
