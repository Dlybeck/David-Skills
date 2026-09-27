## What it does

`attention-modes` adapts the conversation to the time and attention you have. **Focused** supports
deeper rounds of discussion. **On the side** starts with the highest-value broad question and
narrows only as your short replies allow. The mode changes the conversation, not what the agent
is allowed to do.

## When to reach for it

Type `/attention-modes`, or the agent reaches for it when you say you are busy, dictate a reply,
answer briefly, ask it to continue while you are away, or explicitly switch modes. A single
short answer is a cue to make the next turn easy to answer; you can always say "focused" or
"on the side" to settle the mode directly.

| Your attention | What happens |
| --- | --- |
| Focused | A sustained interview can use manageable rounds of independent questions. |
| On the side | The next prompt is short and starts with the most consequential unknown. Later prompts get finer. |

## Common questions

**Will "just go" approve everything that is still open?**
No. It can accept the specific proposal immediately before it. The agent can keep doing work
already within scope and authority, while leaving consequential decisions for you.

**Does the agent know I am using voice?**
Not reliably from dictated text alone. Saying that you are using voice or have little time makes
the preference clear; a pattern of brief replies also prompts the agent to simplify its next turn.

## It's working if

- You can answer the first On the side prompt in one or two sentences, and it still helps if you leave.
- Each later question depends on what your earlier answer settled.
- A brief "go" advances authorized work without silently deciding open product or release choices.
- Saying "focused" restores deeper discussion immediately.

## Where it fits

This is a cross-cutting conversation practice beneath [grilling](./grilling.md) and other skills
that need your input. [Advise](../engineering/advise.md) routes the work itself; attention mode
only changes how you collaborate on that work.
