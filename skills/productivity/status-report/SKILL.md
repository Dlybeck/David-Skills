---
name: status-report
description: Explain verified project progress in chat, with useful visuals connecting current work, milestones, and long-term goals. Use for progress overviews, milestone or final review reports, and requested status documents or webpages. Keep simple one-line status checks lightweight.
---

# Status Report

Produce a dated **snapshot** that answers: where are we, what changed, why does it matter to
the project, and what comes next? The report lives in the chat by default, understandable
without opening a file or rereading the conversation.

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
- **Direction:** the current working interpretation and why this approach was chosen, including
  consequential user corrections. Distinguish adopted direction from tentative suggestions;
  surface drift or stale goal metadata without rewriting it as part of the report.
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

Present the report directly in the response. Include an actual visual when it makes the state
or a relationship easier to understand: a diagram linking work to outcomes, a chart of measured
results, or a relevant image comparison. Choose what the evidence supports, not a fixed dashboard
template. Tables can clarify exact comparisons; status emojis and tables alone are not a
substitute when a graphical explanation would materially help. Simple updates can stay prose.

Use an available in-chat visualization capability according to its instructions; otherwise use
supported inline diagrams or image previews. Check generated visuals against the source evidence
and inspect rendering when tooling permits. If rendering is unavailable, keep the report useful
in text and disclose the limit. Illustrations are not evidence of implementation or delivery.

Save or export a report only when requested or explicitly required by the project's reporting
convention. For Markdown, use the existing report location outside commit-gated tracker
directories, falling back to `.reports/status/<timestamp>-<topic>.md` with a collision-free
timestamp. For a requested webpage, read [references/web-report.md](references/web-report.md).
An inline visual may need a backing file in the environment's response-output location; that
does not require a separate Markdown report, attachment, or hosted page. Keep claims, dates,
and evidence consistent across any requested formats; the chat response remains self-contained.

This is a reporting operation: write only report artifacts, leaving source plans, issue status,
code, and goal lifecycle unchanged. A report request does not start a goal, authorize delivery,
or schedule monitoring. Run once per invocation or authorized material checkpoint. For an
unchanged single-job status check, return one sentence without another report artifact.
