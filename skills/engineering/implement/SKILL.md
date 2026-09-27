---
name: implement
description: "Build understood, authorized work from a conversation, goal, spec, or tickets with testing and whole-change review. Use when behavior is ready to implement; not for advice, diagnosis-only, or unresolved product intent."
---

Implement the understood work authorized by the user in the conversation, current goal contract,
spec, or tickets. A formal spec or ticket is not required. Reuse settled requirements and the
current authorized workspace; ask only about consequential gaps outside delegated decisions.

Run `/attention-modes` for those questions and `/tool-fit` when connected evidence, a UI preview,
or an in-chat visual would materially improve implementation or review.

Use /tdd where possible, at agreed seams or with explicitly delegated seam selection.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use /code-review over the whole change, including relevant uncommitted and new files,
against the originating request and latest corrections. Respect the active delegation budget;
when subagents are not authorized, perform the same Standards and Spec axes locally and disclose
that the review was not independent. Fix real findings and rerun affected checks.

Commit only when the request or active contract authorizes it, on the authorized branch.
Otherwise leave a reviewable local diff. Invocation alone does not authorize Git delivery.

If a ticket supplied the work, its acceptance conditions pass, and tracker updates are authorized,
mark it resolved per the project's issue-tracker convention. Otherwise report the result without
changing its status. End with evidence, validation limits, and the actual delivery state.
