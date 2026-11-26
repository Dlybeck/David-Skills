---
name: philosophy-review
description: Start, harden, or check a project's philosophy file (PHILOSOPHY.md). Use when a project has no philosophy yet, when David's choices suggest the file should change, or when he asks whether a direction fits the project's founding principles. Not a routine development gate or general code-quality review.
---

# Philosophy

A project's philosophy is what it is for, what it believes, and where it is going, each idea with
its reason. It lives in the project, in `PHILOSOPHY.md` at the root, so every chat that opens the
project stands on the same footing when weighing a request. That shared footing is the point:
without it, answers about the same project vary from chat to chat.

This skill does three jobs on that one file: **start** it, **harden** it over time, and **check**
a direction against it.

## What a philosophy is

A broad conviction with its reasons, which needn't be proven. "This app is context-based, which we
believe has real potential, and its approaches follow from that" is a philosophy; a list of
required steps is not. "We don't know where this is going yet" is a good entry, and honest.

It **describes and never binds**. A chat holds it up as a mirror ("this looks different from what
the project says it believes, still want to?"), says why once, then follows the owner's choice.
If a philosophy ever blocks work, it is being held as a rulebook.

Each idea gets a bolded line, then a few sentences of why, around sixty words, with the owner's
own quotes and sources not counted. The whole file stays about a page. This soft limit is the one
deliberate push against the file turning into a rule book. Going over is not refused; it is the
sign to merge ideas, compress, or move an example out. What changes week to week (status,
plans, tasks) is context and belongs elsewhere.

## Starting it

Never ask the owner for a philosophy. Someone who is still working out what they are doing will
answer it wrong or not know what to say, and the file would record a guess as a belief. Ask for
the story instead: what is this, why do you want it, what is the background, who is it for. Short
answers and yes or no are fine; rambling is better, because there is no right answer and the
philosophy is in the way they talk about it.

Begin from what already exists (the repo, README, notes, past chats, any library or planning
notes) and ask only what is missing. Draft the file for the owner to react to, since reacting is
easier than composing. Loose is fine. Mark anything inferred as a guess, and keep the owner's
own words where they gave them. Write it only once they have seen the draft.

## Hardening it

Over time the file **hardens**, not sharpens: ideas are held more firmly as the project proves
them, and are never narrowed into detail. A good philosophy stays broad. When the owner's choices
show something the file does not say, or contradict something it does, propose the change with
what you saw and let them confirm. A pattern of acting against an idea means the idea has
changed or never held; either way the file follows the owner, not the other way round. Hardening
is also pruning: when the file grows past its page, compress.

## Checking a direction

The deeper check asks whether a project, plan, or proposed change still honors the principles its
owner chose to preserve. It runs when asked, not as a prerequisite for other skills. Report in
chat; reviewing does not authorize edits.

**Establish the principles.** Start with `PHILOSOPHY.md` and what the user says must never
change; then the project's mission, founding notes, decisions, and instructions. If the project
adopts an earlier work's philosophy, check that work's primary sources. An author's description is
evidence of intent, not authority over the owner's current project. Separate **confirmed
commitments** from source-backed candidates, recommended methods, historical examples, and
ordinary preferences; a common workflow or one past decision is not a permanent rule. If sources
conflict, name the conflict; the owner's explicit current direction controls. If no principle is
clear, ask one high-level question about what the project must never sacrifice, using
`/attention-modes` when they are busy. Silence never confirms a candidate.

**Check for drift.** Inspect the smallest evidence set that covers the target. For each confirmed
principle, show concrete evidence that it is preserved, at risk, broken, or not yet verifiable,
and the mechanism: how the choice preserves or undermines it. A disliked implementation, bug, or
cost is not automatically a philosophy violation. A required step inside a chosen practice is not
a workflow imposed on every task, and a recommendation is not a gate. When the boundary depends
on the owner's interpretation, present the choice rather than declaring a breach.

**Report.** Lead with the overall judgment. Name each principle, its source and confidence, the
evidence, and the verdict; actual violations before plausible risks; unrelated quality findings
left out. End with only the interpretations that need the owner, and state coverage gaps. Use
`/tool-fit` when a visual would clarify; a short review can stay plain text.
