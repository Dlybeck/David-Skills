## What it does

`grilling` stress-tests a plan, decision, or idea before anyone acts on it. Its **design tree** covers the requested decision, not every possible decision about the product. Settled answers are reused; reversible assumptions and deferred choices are made visible.

Each **round** takes a manageable batch from the **frontier**: material decisions whose prerequisites are settled, highest-impact first. Dependent questions wait for a later round. New answers reshape the remaining questions, so a narrow change need not become a whole-product interview.

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

Inside a round every question arrives in a fixed shape: numbered and titled behind a `❓`, then the body, then the agent's recommended answer alone on a `➡️` line. That is what makes a round answerable by number — "1 yes, 2 the second option, 3 no, here's why" — instead of by quoting questions back. The format has one known rough edge: the recommendation sometimes argues *against* the question as it was worded, so agreeing with the recommendation means answering "no" to the question. When that happens, answer the recommendation and say so.

Facts are the agent's job: cheap [environment](https://www.aihero.dev/ai-coding-dictionary/environment) lookups happen directly. A [sub-agent](https://www.aihero.dev/ai-coding-dictionary/subagent) is reserved for substantial independent investigation within your budget. Material choices you have not delegated come back to you. Before acting, the agent confirms a compact shared understanding; an explicit confirmation already given counts.

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
Yes, and a large part of the audience does. Add this to your global `CLAUDE.md`:

```
When grilling, ask one question at a time.
```

The round-based default is genuinely contested. Practitioners who read slowly, who work in a second language, or who use the sequential format as focus scaffolding all report the one-at-a-time rhythm is better for them, and the opt-out is supported rather than tolerated.

**Where did `/batch-grill-me` go?**
Into this skill. Round-based questioning shipped briefly as a separate skill, then moved into `grilling` itself, so everything built on the primitive — `grill-me`, `grill-with-docs`, `triage`, `wayfinder` — got it at once. There is no `batch-grill-me` to install, and no separate sequential skill either; the `CLAUDE.md` line above is the way back to one-at-a-time.

**Asking a whole round at once must lose the questions my earlier answers would have raised. Doesn't it?**
This is the most common objection to the round design, and the frontier is the answer to it: a round only ever contains questions that do not depend on each other, so no answer in a round can invalidate another question in that round. Answers still reshape everything downstream — the next round is recomputed, not pre-written. What you lose is smaller than "all questions at once" implies, and larger than nothing: see the frontier's limit above.

**It ran out of questions and started building.**
A confirmation gate exists precisely for this: the skill is not finished when the frontier empties, it is finished when you say the understanding is shared. Weaker and faster [models](https://www.aihero.dev/ai-coding-dictionary/model) still break it — this is reported most often on lower-effort or non-frontier models, which collapse "interview until shared understanding" into a couple of questions and an outline. If yours does it, the reliable fix is a line in your own `AGENTS.md` or `CLAUDE.md` telling the agent not to implement without permission.

**It answered its own questions instead of asking me.**
That is a bug in the run, not the intended behaviour, and it was the reason facts and decisions were separated in the skill's text. It shows up most when another skill runs `grilling` inside a resolve-this-ticket frame, where the surrounding task reads as licence to keep moving. The same constraint is why there is no async mode: people have asked for a variant that reads a GitHub issue and posts one consolidated decision memo, and that is a different skill, because a grilling session that nobody answers has produced the agent's opinion rather than yours.

**Can I cap the number of questions?**
Yes: state your question budget or ask for only the highest-impact unresolved decisions. The default is scope-based, not a fixed count. If a cap leaves material uncertainty, the agent should name it rather than pretend the discussion is complete. You can narrow the scope, defer a choice, or authorize a reversible assumption.

**I installed `grill-me` on its own and nothing happens.**
`grill-me` is a one-line skill whose whole body is "run a `/grilling` session", so it needs this skill installed too. The same is true of `grill-with-docs`, which additionally needs [domain-modeling](../engineering/domain-modeling.md). Installing the whole set avoids the problem; installing selectively means installing the primitives as well.

**`grill-with-docs` ran, but it never loaded `grilling`.**
A real and unfixed rough edge, reported across [harnesses](https://www.aihero.dev/ai-coding-dictionary/harness) and models: a skill that names another skill does not reliably cause that skill to load, and `grill-with-docs` names two. The tell is a session that asks everything at once with no recommendations attached — that is the model improvising an interview rather than running this one. Asking the agent directly whether it loaded `grilling` and `domain-modeling` usually recovers it.

## It's working if

- A round arrives as a numbered list, each question with its recommendation on a separate `➡️` line, and you can answer the whole round by number.
- Nothing in a round needs another question in the same round answered first.
- Later rounds ask things the first round could not have asked.
- It looks up facts directly and uses delegated research only when the work and budget justify it.
- Research running in the background does not stall the round; only the questions that depend on it wait.
- It confirms the shared understanding before acting, without repeating approval you already gave.
- Questions resolve material uncertainty without reopening settled or unrelated decisions.

## Where it fits

`grilling` is a **primitive**, not a step you schedule: the single source of truth for the interview technique, kept in one place so every skill that needs an interview reaches for it instead of inventing one. [grill-me](./grill-me.md) and [grill-with-docs](../engineering/grill-with-docs.md) are its two user-invoked front doors, and `grill-with-docs` is where the main build chain begins, ahead of [to-spec](../engineering/to-spec.md). [wayfinder](../engineering/wayfinder.md) runs it to resolve decision tickets, [triage](../engineering/triage.md) to grill a vague report into a workable one, and [re-architect](../engineering/re-architect.md) to walk the tree once you have picked a candidate to deepen. When you are unsure which entry point fits, [advise](../engineering/advise.md) routes you.
