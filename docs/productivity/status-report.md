## What it does

`status-report` explains current progress in the context of the project's longer-term goals.
Every report is a dated **snapshot**, grounded in available evidence; a plan to do something
does not count as proof that it is finished.

The report appears directly in chat, with useful visuals connecting active work to milestones
and project outcomes. It identifies what changed and gives you the next useful action with the
evidence you should expect from it. Saving a separate report is opt-in.

## When to reach for it

Invoke `$status-report` in Codex or `/status-report` in Claude Code, or let the agent reach for
it when a task calls for a project progress report.

| Situation | Result |
| --- | --- |
| Returning to a project or reviewing a milestone | An in-chat report with current state, useful visuals, and next actions connected to project goals |
| Reviewing a long autonomous run | Verified outcomes, remaining gaps, and their significance to the project |
| Requesting a document | A concise chat overview and saved Markdown snapshot |
| Requesting a webpage | The same evidence presented as a readable webpage |
| Checking whether one running job has changed | A short status answer; no full report needed |

It uses available project evidence and any linked long-term plan. Existing planning and tracking
conventions are sufficient; the default chat report needs no report folder or document tool.

## Common questions

**Can I see whether the agent has misunderstood the goal?**

Yes. A substantial report exposes the current interpretation, approach, consequential corrections,
and evidence, separating adopted direction from suggestions. Reporting a mismatch does not itself
rewrite the plan or mutate the goal.

**Can it show both what is happening now and where the project is going?**

Yes. It connects each meaningful piece of current work to a milestone and longer-term outcome.
If the project direction is missing or the connection is uncertain, the report says so.

**Do I have to open a document or webpage to understand it?**

No. The report itself is in chat, including its useful visuals and evidence links. A separate
Markdown snapshot or webpage is created only when you request it or your project explicitly
requires a saved report.

**By visuals, do you mean just a table with status icons?**

No. When useful, it includes a diagram, a chart of measured results, or relevant images directly
in the conversation. The choice follows the evidence rather than a fixed template. A brief update
can still be plain text. [Tool fit](./tool-fit.md) selects a visual or preview the current host
can display; unavailable rendering is disclosed rather than blocking the report.

**Does a webpage mean it gets published or updates itself?**

No. A webpage can be a local HTML file. Hosting uses an authorized destination, and every
report remains a dated snapshot. It does not start background monitoring.

**Do I need specs, tickets, or a pilot running first?**

No. It uses whatever evidence and project direction already exist. Research findings and
failed experiments can count as useful progress when they settle a project question.

## It's working if

- You can understand current progress and its purpose directly in chat without opening a file.
- Visuals explain a meaningful relationship or result rather than just decorating status labels.
- You can tell which work is proposed, tested, and actually delivered.
- Important claims link to evidence, and unknowns remain visible.
- You know what happens next and which decisions need your attention.

## Where it fits

This is a reach-for-it-anytime standalone reporting skill. [Pursue Goal](../engineering/pursue-goal.md)
can use it for a substantial reviewer update; [handoff](./handoff.md) instead prepares continuity
for another worker. [Advise](../engineering/advise.md) routes you across the collection.
