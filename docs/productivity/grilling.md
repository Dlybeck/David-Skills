## What it does

`grilling` stress-tests a plan, decision, or idea before anyone acts on it. Its **design tree** covers the requested decision, not every possible decision about the product. Settled answers are reused; reversible assumptions and deferred choices are made visible.

Each **round** takes questions from the **frontier**: material decisions whose prerequisites are settled. [Attention modes](./attention-modes.md) sets the load. Focused discussion uses manageable batches; On the side starts with the most useful broad unknown and narrows as brief answers arrive. New answers reshape the remaining questions, so a narrow change need not become a whole-product interview.

## When to reach for it

Type `/grilling`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) reaches for it on its own when a task fits. It is the only [skill](https://www.aihero.dev/ai-coding-dictionary/skill) in the grilling family that is model-invoked, which is why you rarely type it: usually a skill you *did* type is running it for you.

Typing `/grilling` directly gets you the plain interview and nothing else. Where you want something more than that:

| What you have | Reach for |
| --- | --- |
| You want a stateless discussion, inside or outside a repo | [grill-me](./grill-me.md) — the same [session](https://www.aihero.dev/ai-coding-dictionary/session), with no document writes |
| You want domain vocabulary and decisions recorded in a repo | [grill-with-docs](../engineering/grill-with-docs.md) — the same session, with `CONTEXT.md` and qualifying ADRs |
| An effort too big to hold in one session | [wayfinder](../engineering/wayfinder.md) — it charts a map and runs grilling inside the decision tickets |
| A question that talking cannot settle — how something should look or feel | [prototype](../engineering/prototype.md) — build the throwaway version, then come back |
| A skill of your own that needs an interview | Invoke `/grilling` from it, rather than writing another interview |

## The round, the frontier, and who decides

Three ideas carry the whole skill.

The **design tree** is the model of the scoped decision and its dependencies. The **frontier** contains questions ready to ask. A **round** is a manageable selection from it, not a requirement to ask every available question at once.

For a specific choice, questions are numbered and titled behind a `❓`, with the agent's recommended answer on a separate `➡️` line. That lets you answer by number or accept a recommendation in a few words. An opening question about your intent or hard limits may have no recommendation: guessing your priorities would bias the answer. In an On the side exchange, the prompt stays short enough to answer aloud.

Facts are the agent's job: cheap [environment](https://www.aihero.dev/ai-coding-dictionary/environment) lookups happen directly. A [sub-agent](https://www.aihero.dev/ai-coding-dictionary/subagent) is reserved for substantial independent investigation within your budget. [Tool fit](./tool-fit.md) can bring an available source or visual into the conversation when it helps you decide. Material choices you have not delegated come back to you. The agent confirms a compact shared understanding before acting on a proposal from the interview; an explicit confirmation already given counts. If you leave first, work already within the task's authority can continue while open human choices remain visible.

The honest limit: the frontier is the agent's judgement, not a computed graph. It can put two questions in one round and only afterwards discover that one answer should have changed the other. There is no guard against that beyond telling it, which reopens the affected branch in the next round.

## What lives here and what lives in the wrappers

This page covers the mechanism. The things people most often want are documented one level up.

| Question | Where it is answered |
| --- | --- |
| The tree, the frontier, rounds, the question format, facts vs decisions | Here |
| How long a session should run, what to do with a question you can't answer by talking, how to avoid nodding along | [grill-me](./grill-me.md) |
| What gets written to `CONTEXT.md`, what becomes an ADR | [grill-with-docs](../engineering/grill-with-docs.md) |

## Common questions

**Can I go back to one question at a time?**
Yes. Say "on the side" when you have little attention or are dictating; the agent will lead with one short, high-value question and refine from there. You can also ask for one question at a time while staying Focused. For a standing preference, add this to your global `CLAUDE.md` or `AGENTS.md`:

```
When grilling, ask one question at a time.
```

The round-based default is genuinely contested. Practitioners who read slowly, work in a second language, or use the sequential format as focus scaffolding report that one-at-a-time is better for them. An explicit switch to Focused restores deeper rounds immediately.

**Where did `/batch-grill-me` go?**
Into this skill. Round-based questioning shipped briefly as a separate skill, then moved into `grilling` itself, so everything built on the primitive — `grill-me`, `grill-with-docs`, `triage`, `wayfinder` — got it at once. There is no `batch-grill-me` to install. On the side changes the question load without replacing the interview skill.

**Asking a whole round at once must lose the questions my earlier answers would have raised. Doesn't it?**
This is the most common objection to the round design, and the frontier is the answer to it: a round only ever contains questions that do not depend on each other, so no answer in a round can invalidate another question in that round. Answers still reshape everything downstream — the next round is recomputed, not pre-written. What you lose is smaller than "all questions at once" implies, and larger than nothing: see the frontier's limit above.

**It ran out of questions and started building.**
A confirmation gate exists for a new proposal from the interview: an empty frontier alone does not authorize acting on it. Weaker and faster [models](https://www.aihero.dev/ai-coding-dictionary/model) still break this — they may collapse the interview into a couple of questions and start building. The agent can continue work the active request already authorized while you are away, but it must leave unsettled human decisions open.

**It answered its own questions instead of asking me.**
That is a bug in the run, not the intended behaviour, and it was the reason facts and decisions were separated in the skill's text. It shows up most when another skill runs `grilling` inside a resolve-this-ticket frame, where the surrounding task reads as licence to keep moving. On the side is still a live exchange, even if you answer briefly or leave before every detail is settled. A grilling session that nobody answers has produced the agent's opinion rather than yours.

**Can I cap the number of questions?**
Yes: state your question budget or ask for only the highest-impact unresolved decisions. The default is scope-based, not a fixed count. If a cap leaves material uncertainty, the agent should name it rather than pretend the discussion is complete. You can narrow the scope, defer a choice, or authorize a reversible assumption.

**I installed `grill-me` on its own and nothing happens.**
`grill-me` is a one-line skill whose whole body is "run a `/grilling` session", so it needs this skill installed too. The same is true of `grill-with-docs`, which additionally needs [domain-modeling](../engineering/domain-modeling.md). The adaptive attention and host-tool guidance lives in [attention-modes](./attention-modes.md) and [tool-fit](./tool-fit.md). Installing the whole set includes them; with selective installs, include the supporting skills whose behavior you want.

**`grill-with-docs` ran, but it never loaded `grilling`.**
A real and unfixed rough edge, reported across [harnesses](https://www.aihero.dev/ai-coding-dictionary/harness) and models: a skill that names another skill does not reliably cause that skill to load, and `grill-with-docs` names two. The tell is a session that asks everything at once with no recommendations attached — that is the model improvising an interview rather than running this one. Asking the agent directly whether it loaded `grilling` and `domain-modeling` usually recovers it.

## It's working if

- Specific choices carry a recommendation you can accept or correct in a few words; open questions about your priorities do not invent one.
- An On the side opening asks the broadest useful missing question first, then gets finer as your answers allow.
- Nothing in a round needs another question in the same round answered first.
- Later rounds ask things the first round could not have asked.
- It looks up facts directly and uses delegated research only when the work and budget justify it.
- Research running in the background does not stall the round; only the questions that depend on it wait.
- It confirms the shared understanding before acting, without repeating approval you already gave.
- Questions resolve material uncertainty without reopening settled or unrelated decisions.

## Where it fits

`grilling` is a **primitive**, not a step you schedule: the single source of truth for the interview technique, kept in one place so every skill that needs an interview reaches for it instead of inventing one. [grill-me](./grill-me.md) and [grill-with-docs](../engineering/grill-with-docs.md) are its two user-invoked front doors, and `grill-with-docs` is where the main build chain begins, ahead of [to-spec](../engineering/to-spec.md). [wayfinder](../engineering/wayfinder.md) runs it to resolve decision tickets, [triage](../engineering/triage.md) to grill a vague report into a workable one, and [re-architect](../engineering/re-architect.md) to walk the tree once you have picked a candidate to deepen. When you are unsure which entry point fits, [advise](../engineering/advise.md) routes you.
