## What it does

`handoff` exports portable [context](https://www.aihero.dev/ai-coding-dictionary/context) for another session, directory, harness, or collaborator. Writing the export does not itself transfer execution or end an active goal.

## When to reach for it

Type `/handoff`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) selects it for a requested or already-authorized transfer. Routine progress belongs in the existing checkpoint, not repeated handoff documents.

## Preserve the current understanding

The document retains the objective, authority, consequential corrections, superseded assumptions, evidence, open questions, and next action. Existing plans, decisions, commits, and receipts are linked rather than copied. Sensitive information is redacted.

By default the file goes into the operating system's temporary directory, not the project. Supply an intended recipient or next task to focus it. The recipient must reconcile the export with live state before acting.

## Common questions

**Does creating a handoff stop the current work?**

No. It does not pause or complete a goal, start a session, or spawn a worker. Those are separate actions governed by the user's request.

**Will my mid-run corrections survive?**

The export records the current direction and what each consequential correction superseded, keeping unadopted suggestions distinct.

**Is this the same as a status report?**

No. [status-report](./status-report.md) informs you about verified progress. Handoff equips a recipient to continue work.

## It's working if

- The recipient knows the current intent without reconstructing the conversation.
- Corrections are not lost behind an obsolete original plan.
- Evidence is linked and rechecked rather than repeated as unquestioned fact.
- Exporting context does not silently abandon the ongoing task.

## Where it fits

A standalone transfer tool. [pursue-goal](../engineering/pursue-goal.md) owns ongoing continuity; [advise](../engineering/advise.md) helps distinguish the two.
