---
name: independent-pr-review
description: Independently review an exact PR or committed branch snapshot for actionable defects using a fresh reviewer. Use after authorized implementation or when ordinary PR bug review is requested; Standards/Spec checks remain the separate code-review skill. Review never grants posting, fixing, or merge authority.
---

# Independent PR Review

Review the full proposed change in a **fresh context**. This is ordinary actionable defect review;
`/code-review` continues to provide the separate Standards and Spec axes. Preserve findings from
both practices; neither a developer self-review nor a clean axis report substitutes for this pass.

## Inputs and independence

Require a repository or immutable source snapshot, the PR identity when available, exact base-tip
and head commit SHAs, and settled requirements with current scope and authority. Posting authority
is a separate input; default to private reporting. Local committed branches can be reviewed before
a PR exists. Uncommitted work belongs to `/code-review`, not a purported pinned-head review.

If this context contains implementation discussion or earlier reviewer conclusions, dispatch one
new reviewer with only those inputs, this skill, and access to source/guidance. Use the host's
documented fresh-context control (Codex native delegation: `fork_turns: "none"`; Claude Code:
a new isolated agent/session with an explicit brief). Verify the isolation capability rather than
assuming a tool name guarantees it. If unavailable or outside the delegation budget, report the
independence gate unmet; local self-review may help but cannot settle it.

The dispatched reviewer is already the reviewer: perform the review directly, spawn no additional
agents, never fix code, and return findings to the developer. Read requirements as primary scope
evidence; exclude implementation transcripts, developer explanations of the fix, prior reviews,
and PR discussion containing earlier conclusions. Inspect source and repository guidance directly.

## Inspect the pinned proposal

1. Resolve both commits and record the base tip, head, and their merge base. For a PR, verify its
   repository, target branch, and remote head match the inputs. A mismatch requires reconciliation,
   not a review of whichever checkout happens to be current.
2. Read root and scoped repository instructions applicable to every changed path, with normal
   precedence (`AGENTS.override.md`, `AGENTS.md`, configured fallbacks). Inspect relevant callers,
   tests, and invariants beyond the hunks. Explicit user scope overrides general guidance.
3. Enumerate the complete changed-path list and inspect the full merge-base-to-head diff, not only
   the latest fix commit. With Git, use `git diff --name-status <merge-base> <head>` and
   `git diff <merge-base> <head>`. Read files from the pinned tree or a verified clean snapshot;
   do not let local dirty files contaminate it. Reconcile connector pagination/truncation. Report
   unreadable, binary, unavailable, or omitted coverage; incomplete review is not a settled result.
4. Read [references/rubric.md](references/rubric.md) and apply it to all candidate findings. Safe
   isolated checks may support evidence within the supplied authority; otherwise label the
   finding static. Never execute protected writes or bypass a hook to reproduce a finding.

## Return and comment

Return the reviewed head, base tip/merge base, coverage and validation limits, and every actionable
finding. For each finding give an imperative `[P0]`–`[P3]` title, exact head file/short line range
overlapping the diff, and one concise paragraph covering trigger, expected/actual behavior,
impact, and correction direction. Distinguish tested evidence (command/result) from static
reasoning. For repository-rule-supported findings, cite the smallest applicable guidance range;
ordinary bugs do not need an invented rule citation.

When PR commenting is explicitly authorized, publish **one consolidated comment per reviewed
snapshot** containing the head SHA and the distinct actionable findings with pinned source links.
Check whether the same head/findings were already posted to avoid duplicates; this bookkeeping
happens after independent analysis. If the remote head moved, return the stale-head result privately
and arrange a fresh review before posting or settling. With no actionable findings, return a private
receipt and **post no PR comment**. A clean review means none found in the inspected scope, not
universal correctness. No review result authorizes merge or installation.

## Developer continuation

When coordinating completed implementation, use
[references/developer-loop.md](references/developer-loop.md) for the authorized
developer → fresh reviewer → developer loop. The reviewer itself only reports; the developer
owns repairs, validation, and delivery.
