## What it does

`status-report` explains current progress in the context of the project's longer-term goals.
Every report is a dated **snapshot**, grounded in available evidence; a plan to do something
does not count as proof that it is finished.

It connects active work to milestones and project outcomes, identifies what changed, and gives
you the next useful action with the evidence you should expect from it.

## When to reach for it

Invoke `$status-report` in Codex or `/status-report` in Claude Code, or let the agent reach for
it when a task calls for a project progress report.

| Situation | Result |
| --- | --- |
| Returning to a project or reviewing a milestone | Current state, recent changes, and next actions connected to project goals |
| Reviewing a long autonomous run | Verified outcomes, remaining gaps, and their significance to the project |
| Requesting a document | A concise chat overview and saved Markdown snapshot |
| Requesting a webpage | The same evidence presented as a readable webpage |
| Checking whether one running job has changed | A short status answer; no full report needed |

## Prerequisites

Provide access to the project and any long-term plan outside it that the report should use.
Existing planning and tracking conventions are sufficient. Saved reports use the project's
report location outside commit-gated tracker directories, falling back to `.reports/status/`;
chat-only reports need no folder. Report snapshots do not require tracker commits before later
agent dispatch.

## Common questions

**Can it show both what is happening now and where the project is going?**

Yes. It connects each meaningful piece of current work to a milestone and longer-term outcome.
If the project direction is missing or the connection is uncertain, the report says so.

**Do I have to open a document or webpage to understand it?**

No. The key conclusions appear directly in chat. The saved report holds the fuller evidence.
You can also request chat only.

**Does a webpage mean it gets published or updates itself?**

No. A webpage can be a local HTML file. Hosting uses an authorized destination, and every
report remains a dated snapshot. It does not start background monitoring.

**Do I need specs, tickets, or a pilot running first?**

No. It uses whatever evidence and project direction already exist. Research findings and
failed experiments can count as useful progress when they settle a project question.

## It's working if

- You can understand current progress and its purpose without rereading the conversation.
- You can tell which work is proposed, tested, and actually delivered.
- Important claims link to evidence, and unknowns remain visible.
- You know what happens next and which decisions need your attention.

## Where it fits

This is a reach-for-it-anytime standalone reporting skill. [Pursue Goal](../engineering/pursue-goal.md)
can use it for a substantial reviewer update; [handoff](./handoff.md) instead prepares continuity
for another worker. [Advise](../engineering/advise.md) routes you across the collection.
