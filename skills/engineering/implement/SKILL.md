---
name: implement
description: "Build understood, authorized work from a conversation, goal, spec, or tickets, including local build and test setup. Use when behavior is ready to implement; not for advice, diagnosis-only, or unresolved product intent."
---

Implement the understood work authorized by the user in the conversation, current goal contract,
spec, or tickets. A formal spec or ticket is not required. Reuse settled requirements and the
current authorized workspace; ask only about consequential gaps outside delegated decisions.

An implementation or bug-fix request includes routine local work needed to inspect, build,
reproduce, and test it. Check project pins and existing environments, then install or repair
compatible local toolchains and packages, set up isolated test resources, and retry. A missing
dependency discovered mid-task is setup work, not a reason to stop for another approval. Reuse
applicable standing user grants from the conversation or durable instructions across tasks; a new
task does not revoke them. Do not invent a grant from an inaccessible prior conversation.

If setup fails, try another project-compatible local route and continue independent work. Ask
only when the specific next step needs a human decision, a denied host/tool permission, new
credentials or account access, spending, production changes, material deletion, or scope beyond
the request. Skill instructions never override a host permission gate or an explicit task limit.

Run `/attention-modes` for those questions and `/tool-fit` when connected evidence, a UI preview,
or an in-chat visual would materially improve implementation or review.

Use /tdd where possible, at agreed seams or with explicitly delegated seam selection.

Do not use the test suite casually. Choose checks for the behavior changed and the risks involved;
run the required full suite before delivery. Reuse passing results until a relevant change,
failure, or unresolved concern justifies another run.

Once done, use /code-review over the whole change, including relevant uncommitted and new files,
against the originating request and latest corrections. Respect the active delegation budget;
when subagents are not authorized, perform the same Standards and Spec axes locally and disclose
that the review was not independent. Fix real findings and rerun affected checks.

Commit only when the request or active contract authorizes it, on the authorized branch.
Otherwise leave a reviewable local diff. Invocation alone does not authorize Git delivery.

For a committed proposal, invoke /independent-pr-review and follow its developer continuation
loop before presenting the settled result. Preserve the separate Standards/Spec findings above.
Use a fresh reviewer with only pinned source, guidance, and settled requirements; ordinary findings
are additional evidence, not developer self-review. Missing commit or independent-review authority
leaves that gate explicitly unmet. Posting, pushing, and PR creation remain separately authorized.

If a ticket supplied the work, its acceptance conditions pass, and tracker updates are authorized,
mark it resolved per the project's issue-tracker convention. Otherwise report the result without
changing its status. End with evidence, validation limits, and the actual delivery state.
