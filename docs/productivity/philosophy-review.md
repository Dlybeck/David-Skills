## What it does

`philosophy-review` is the one skill for a project's **philosophy file**, `PHILOSOPHY.md` at the
project root: what the project is for, what it believes, and where it is going, each idea with its
reason. It does three jobs. It **starts** the file, asking for the story (what this is, why you
want it, the background, who it is for) and never for a philosophy, then drafts it for you to
react to. It **hardens** the file over time: ideas are held more firmly as the project proves
them, never narrowed into detail, and the agent proposes changes you confirm. And it does the
occasional deeper **check**, looking for actual drift from commitments the owner chose to
preserve rather than turning every bug or process preference into a breach.

The file describes and never binds: a chat shows it as a mirror and follows your choice. It has a
soft length limit, an idea and its why in about sixty words and the whole file about a page; going
over is the sign to merge or compress, not a refusal.

The check uses the owner's stated rules and relevant project or original-source evidence. It
keeps confirmed commitments separate from plausible interpretations. The result appears in chat;
the skill does not change the project or declare new permanent rules on its own.

## When to reach for it

Invoke `$philosophy-review` in Codex or `/philosophy-review` in Claude Code, or let the agent
reach for it when you ask whether a project, plan, or change still fits its founding philosophy.

| Situation | What the review checks |
| --- | --- |
| A new direction is being considered | Whether it preserves the principles that should survive every redesign |
| A project has grown over time | Whether its current structure and behavior still reflect those principles |
| A fork adapts another project | Which original principles the owner adopted, and where adaptations preserve or strain them |

## The boundary

A philosophy is a small set of durable commitments, not a checklist of preferred steps. A
recommended route through several skills can coexist with freedom to choose a different route.
Likewise, a selected skill can require a disciplined method without imposing it on every task.

The owner's current direction defines what this project must preserve. An original author's
writing helps establish what the source project meant; it does not silently make every original
recommendation binding on a fork.

## Common questions

**Will it ask me what my philosophy is?**

No. Asking for a philosophy gets a wrong answer or a blank. It asks for the story, accepts yes or
no, and welcomes rambling. It can also start from what the repo and past notes already say, and
ask only what is missing. "We don't know where this is going yet" is a fine entry.

**Is this a code review?**

No. [Code review](../engineering/code-review.md) checks a change against requirements and coding
standards. A philosophy review checks fidelity to the project's founding commitments. It may
cite code as evidence, but an ordinary defect is not automatically a philosophy violation.

**What if the principles have never been written down?**

The agent starts with what you have said must never change, reads available founding sources,
and asks one broad question if the central commitment remains unclear. It labels inferred
principles as candidates until you adopt them.

**Does this add another development gate?**

No. Reach for it when a direction needs checking. It does not become a required stage before
specification, implementation, or release.

## It's working if

- A new project's `PHILOSOPHY.md` reads like your own story, with guesses marked, and fits about a page.
- You can identify the exact principle behind each verdict and where it came from.
- A strict step inside an optional practice is not mistaken for a mandatory global workflow.
- You can see concrete evidence of fidelity or drift, with uncertainty labelled.
- The review leaves unrelated bug and style findings outside its philosophy judgment.

## Where it fits

This is a standalone check you can use whenever a project direction may be drifting. [Advise](../engineering/advise.md)
helps select practices; philosophy review checks the enduring constraints those choices must
respect. [Attention modes](./attention-modes.md) keeps its questions manageable when you are
working on the side.
