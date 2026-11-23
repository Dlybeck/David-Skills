---
name: handoff
description: Pack up this chat's context in a file so another chat, folder, tool or person can carry on. Use when the user wants to pass the work to another chat, pick it up somewhere else, or hand it to someone; not for routine progress notes.
argument-hint: "What will the next session be used for?"
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save it outside the current workspace, in `${XDG_STATE_HOME:-~/.local/state}/handoffs/<project-folder-name>/<YYYY-MM-DD>-<short-topic>.md`, and give the user its full path. The OS temporary directory is cleared and nothing looks there later.

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
