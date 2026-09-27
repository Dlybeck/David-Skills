---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user rigorously until the requested decision is understood. Bound the **design
tree** to that decision: reuse settled answers and existing context; do not expand a small change
into an interview about the whole product. Each material decision branches into those that depend
on it.

Work the tree in **rounds**. The **frontier** is the material decisions whose prerequisites are
settled. Run `/attention-modes` to match the question load to the user's attention. In Focused
mode, ask a manageable batch, highest-impact first. On the side, start with the most useful broad
unknown and ask narrower questions as answers arrive. Keep remaining questions for later; skip
those answered by new context. Wait for the user's answer before the next dependent round.

Format a specific choice like so, with a recommendation the user can accept in a short reply:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

For an opening question about intent or a hard limit, omit the recommendation when any answer
would be a guess about the user's priorities. Keep the prompt short and answerable aloud.

Each round the user answers reshapes the tree — settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job: inspect the environment directly for cheap lookups. Delegate only
substantial independent investigation within the user's budget; ask other settled-frontier
questions while it runs. Material choices not already delegated are the user's — ask and wait.
Use `/tool-fit` when an available source or visual would make a question easier to answer.

The session is done when no material decision in the agreed scope remains unresolved. State any
reversible assumptions and deferred choices instead of silently deciding them. Obtain confirmation
of the compact shared understanding before acting on a proposal from the interview; an explicit
confirmation already given counts. If the user leaves before then, continue work already within
the active task's authority and preserve the open human decisions.
