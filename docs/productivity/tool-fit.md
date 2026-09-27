## What it does

`tool-fit` makes the agent check which useful capabilities the current host actually offers.
It can inspect a connected original, open a current source, show a visual in chat, or preview a
file when that improves the result. It selects by the task rather than assuming a particular AI
app is present.

## When to reach for it

Type `/tool-fit`, or the agent reaches for it when source access, a visual explanation, an
artifact preview, or a workflow's fixed output format affects the quality of the answer. It is
most useful when the obvious text-only or file-only route would make evidence harder to inspect.

## Choose the useful capability

| Need | Useful route when available |
| --- | --- |
| Current external fact | Search, open the original, and cite what was inspected. |
| Relevant connected file or app | Search or read the original through an authorized connection. |
| Relationship or comparison | Show a fitting diagram, chart, or interactive view in chat. |
| Requested visual asset | Generate or edit an image when the host supports it and a bitmap is the useful form. |
| Reusable artifact | Create the file, preview it when possible, and link its source. |

## Common questions

**Will this make every answer use a tool or a visual?**
No. A simple fact or small update can stay text. The capability has to improve evidence or the
next decision.

**Will it connect a new account for me?**
No. It works with available, authorized access and keeps separate action boundaries intact.

## It's working if

- Current claims cite originals the agent actually opened.
- A connected file is inspected through the available connection instead of guessed from its name.
- Useful visuals and artifact previews are visible in chat, with a source file when one exists.
- A missing host capability is reported as a concrete limit without inventing its output.

## Where it fits

This is a cross-cutting tool choice practice for [research](../engineering/research.md),
[re-architect](../engineering/re-architect.md), [status-report](./status-report.md), and other
skills. [Advise](../engineering/advise.md) chooses a workflow; `tool-fit` helps that workflow
use the host well.
