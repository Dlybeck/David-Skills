---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use /code-review to review the work.

Commit your work to the current branch.

If the work came from a ticket on the issue tracker, mark it resolved — per `docs/agents/issue-tracker.md`'s "When a skill says 'mark the ticket resolved'" convention. Skip this when there was no ticket (working directly from a spec, or from the conversation).
