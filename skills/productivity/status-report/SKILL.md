---
name: status-report
description: Create an evidence-backed project status report connecting current work, milestones, and long-term goals. Use when the user asks for a progress overview, a project status document or webpage, or when an authorized workflow needs a milestone or final review report. Keep simple one-line status checks lightweight.
---

# Status Report

Produce a dated **snapshot** that answers: where are we, what changed, why does it matter to
the project, and what comes next? Make it understandable without reading the conversation.

## Ground the snapshot

Use the user's named project and reporting period; otherwise use the current project and a
snapshot as of now. Read repository instructions and follow their pointers to the authoritative
plan, roadmap, goal contract, domain vocabulary, and issue tracker. Use existing artifacts;
this skill requires neither a spec nor a ticket workflow.

Inspect the smallest relevant evidence set: current branch and changes, recent commits,
milestone records, research findings, test/evaluation receipts, and available delivery state.
Follow an explicitly linked cross-project plan when needed to understand the longer horizon.
Keep unrelated projects and private session archives outside the evidence search.

Treat plans as intended direction and artifacts as evidence of execution. Check dates and
revisions. Distinguish proposed, implemented locally, validated, committed, merged, and
released/deployed where those differences affect the reader's decision. A finished experiment
can be useful progress even when its hypothesis failed.

Resolve conflicting status claims against concrete evidence and surface unresolved conflicts.
Mark unavailable or stale evidence explicitly; neither conversation confidence nor an old
report proves current completion. Read existing receipts rather than launching builds,
experiments, or deployments just to produce a report. Use bounded read-only checks when needed.

If no authoritative long-term goal is available, state that gap and report the verified current
work. Label any inferred connection as tentative. Ask a focused question only when the missing
project or goal would materially change the report. Do not invent or rewrite the roadmap.

## Connect the horizons

Map meaningful current work to its immediate milestone and the longer-term outcome it supports.
For each material connection, explain the contribution: capability unlocked, uncertainty reduced,
dependency removed, or evidence still missing. Flag work with no clear connection as such.

Compare with the latest relevant snapshot if one exists, verifying the new state independently.
Without a prior snapshot, say this is the baseline rather than inventing a progress delta.
Use measured values with their baseline, evaluation scope, and date. Use percentages or delivery
dates only when a defined denominator or supported estimate exists; label estimates.

## Write for the reviewer

Lead with a two- or three-sentence assessment of the current situation. Keep the overview
readable in about a minute; move detailed evidence below it. Prefer these elements, combining
or omitting empty sections to suit the project:

- **Now:** active work, latest verified result, and immediate milestone.
- **Bigger picture:** longer-term outcome and how current work advances it. Use a small table
  such as `Project outcome | Milestone | Current evidence | Remaining gap` when it clarifies
  several relationships.
- **Since last time:** material deliveries, learning, setbacks, or changed assumptions.
- **Next:** the next useful action and what will prove it worked; distinguish agreed work
  from recommendations.
- **Needs attention:** actual blockers, risks, and decisions the user must make.
- **Evidence:** links to the relevant files, revisions, receipts, and sources, with an as-of
  timestamp and any verification limits.

Keep the long-term context brief enough that repeated reports emphasize what changed. Avoid
transcript recaps and activity counts that say nothing about outcomes. Choose status labels
from the evidence; reserve completion for satisfied proof conditions at the stated scope.

## Deliver once

Default to a concise overview directly in chat plus a Markdown snapshot in the project's
existing report location outside any commit-gated tracker directory. If none exists, use
`.reports/status/<timestamp>-<topic>.md`
with a collision-free timestamp. Honor chat-only requests. Without a writable workspace,
deliver in chat and state that no file was saved.

For a requested webpage, read [references/web-report.md](references/web-report.md).
Keep the same claims, dates, and evidence across formats. Link the saved report from chat;
the chat overview must remain useful on its own.

This is a reporting operation: write only report artifacts, leaving source plans, issue status,
code, and goal lifecycle unchanged. A report request does not start a goal, authorize delivery,
or schedule monitoring. Run once per invocation or authorized material checkpoint. For an
unchanged single-job status check, return one sentence without another report artifact.
