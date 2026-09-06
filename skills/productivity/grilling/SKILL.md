---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user rigorously until the requested decision is understood. Bound the **design
tree** to that decision: reuse settled answers and existing context; do not expand a small change
into an interview about the whole product. Each material decision branches into those that depend
on it.

Work the tree in **rounds**. The **frontier** is the material decisions whose prerequisites are
settled. Ask a manageable batch, highest-impact first, with numbered questions and a recommended
answer. Keep remaining questions for later; skip those answered by new context. Then wait for
the user's answers before the next round.

Each question should be formatted like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree — settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job: inspect the environment directly for cheap lookups. Delegate only
substantial independent investigation within the user's budget; ask other settled-frontier
questions while it runs. Material choices not already delegated are the user's — ask and wait.

The session is done when no material decision in the agreed scope remains unresolved. State any
reversible assumptions and deferred choices instead of silently deciding them. Obtain confirmation
of the compact shared understanding before acting; an explicit confirmation already given counts.
