---
name: philosophy-review
description: Check a project, plan, or proposed change against its founding principles. Use when the user asks for a philosophy review or explicitly asks whether a direction violates the project's original intent. This is not a routine development gate or general code-quality review.
---

# Philosophy Review

Assess whether the project still honors the principles its owner chose to preserve. Review the
whole project or the named proposal, change, or decision. Report in chat by default; reviewing
does not authorize edits to the project or its principles.
Run this check when requested, not as a prerequisite for other skills or ordinary development.

## Establish the principles

Start with what the user has already said must never change. Read the project's own philosophy,
mission, founding notes, decisions, and relevant instructions. If the project adopts an earlier
work's philosophy, check that work's primary sources when available. An author's description is
evidence of their intent, not automatic authority over the owner's current project.

Separate **confirmed commitments** from source-backed candidates, recommended methods,
historical examples, and ordinary preferences. Do not turn a common workflow, one past decision,
or your idea of good practice into a permanent rule. If sources conflict, identify the conflict;
the owner's explicit current direction controls the review. If no principle is clear, ask one
high-level question about what the project must never sacrifice. Use `/attention-modes` when
the user is busy or replying briefly: front-load that question, then inspect available evidence
while they are away. Never treat silence as confirmation of a candidate principle.

## Check for drift

Inspect the smallest evidence set that covers the review target: project behavior and structure
for a whole-project review, or the actual proposal, diff, and affected interfaces for a narrower
one. For each confirmed principle, show concrete evidence that it is preserved, at risk, broken,
or not yet verifiable. Explain the mechanism: how does the choice preserve or undermine the
principle? A disliked implementation, bug, cost, or stylistic preference is not automatically a
philosophy violation.

Distinguish a required step *inside a chosen practice* from a workflow imposed on every task.
Distinguish an optional recommendation from a gate. When the boundary depends on the owner's
interpretation, present the choice rather than declaring a breach. Suggest the smallest change
that would restore a confirmed principle without discarding useful project-specific adaptations.

## Report

Lead with the overall fidelity judgment. Name each principle, its source and confidence, the
relevant project evidence, and the verdict. Put actual violations ahead of plausible risks;
keep unrelated quality findings out of the philosophy verdict. End with only the consequential
interpretations that need the owner. Cite inspected sources and state important coverage gaps.
Use `/tool-fit` when a visual comparison would materially clarify the relationships; a short
review can remain plain text.

If the owner asks to preserve the resulting principles for future reviews, propose concise
wording in the project's chosen location and write it only within the task's authority. A
review alone does not create a new constitution, workflow stage, or implementation task.
