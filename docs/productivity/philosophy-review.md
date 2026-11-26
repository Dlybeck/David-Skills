## What it does

`philosophy-review` keeps a project's **philosophy file**, `PHILOSOPHY.md` at the root: what the
project is for and what it believes, each idea with its reason. It **starts** the file from a
conversation about the project's story, never by asking for a philosophy. It **hardens** it over
time, held more firmly, never more detailed. And it **checks** a direction against it when asked.

A philosophy is a belief and its why, never a how: designs and decisions are evidence of it, not
entries in it. The file describes and never binds, and stays about a page.

## When to reach for it

Invoke `$philosophy-review` in Codex or `/philosophy-review` in Claude Code to start a project's
philosophy, or let the agent reach for it when you ask whether a project, plan or change still
fits what the project believes.

## Common questions

**Will it ask me what my philosophy is?**

No. Asking for a philosophy gets a wrong answer or a blank. It asks for the story, takes yes or no,
and welcomes rambling. What the repo and notes say shapes its questions but never replaces them.

**Is this a code review?**

No. [Code review](../engineering/code-review.md) checks a change against requirements and coding
standards. This checks whether the work still fits what the project believes.

**Does this add another development gate?**

No. It runs when asked, not as a stage before anything else.

## It's working if

- Starting it feels like talking about the project, not filling in a form.
- The draft reads like your own beliefs, with guesses marked, and none of its lines is a design rule.
- The file stays about a page as the project grows.
