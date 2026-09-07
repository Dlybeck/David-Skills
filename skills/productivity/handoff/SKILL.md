---
name: handoff
description: Export portable context for a real transfer to another session, directory, harness, or collaborator. Use when a transfer is requested or already authorized; not for routine progress notes or ending an active goal.
argument-hint: "What will the next session be used for?"
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include a "suggested skills" section in the document, which suggests skills that the agent should invoke.

Preserve the current objective, authority boundaries, consequential user corrections (and what
they supersede), evidence, unresolved questions, and next action. Distinguish the current user
direction from proposals and unverified status. Derive branch/revision facts from commands when
relevant. Instruct the recipient to reconcile the handoff with live state before continuing.

Creating this export does not transfer execution, start another session or subagent, pause or
complete a goal, or grant the recipient new authority. Continue the active task unless the user
requested a stop or the actual authorized transfer requires one.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
