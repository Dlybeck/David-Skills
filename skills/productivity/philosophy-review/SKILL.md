---
name: philosophy-review
description: Start, harden, or check a project's philosophy file (PHILOSOPHY.md). Use when a project has no philosophy yet, when David's choices suggest the file should change, or when he asks whether a direction fits the project's founding principles. Not a routine development gate or general code-quality review.
---

# Philosophy

A project's philosophy is what it is for and what it believes, each idea with its reason. It
lives in `PHILOSOPHY.md` at the project root, so every chat that opens the project stands on the
same footing when weighing a request.

## What a philosophy is

A broad conviction with its why, which needn't be proven: "this app is context-based, which we
believe has real potential." It is never a how. Designs, decisions and rules are evidence of a
philosophy, not entries in it; when a line says what to do or not do, the belief behind it is
what belongs here, and only the owner can say what that is. "We don't know where this is going
yet" is a good entry.

It describes and never binds: a chat holds it up as a mirror, says why once, and follows the
owner's choice. Each idea is a bolded line and a few sentences, around sixty words, and the
file about a page. Going over that is the sign to merge or cut, since a philosophy that keeps
growing is turning into a rule book.

## Starting it

Starting is a conversation, every time. Never ask for a philosophy: someone still working out
what they are doing will answer it wrong or not know what to say. Ask for the story: what is
this, why do you want it, what's the background, who is it for. Yes or no is fine; rambling is
better, since the philosophy is in how they talk about it. What the repo and notes already say
shapes the questions ("your notes call it a self-portrait, not a resume; what's behind that?"),
never replaces them. Draft only after hearing them, keep their words, mark guesses, and write
the file once they've seen it.

## Hardening it

Over time the file hardens: ideas are held more firmly as the project proves them, never
narrowed into detail. When the owner's choices show something the file doesn't say, or go
against something it does, propose the change with what you saw and let them confirm. Hardening
is also cutting: what no longer holds, or has grown long, comes out.

## Checking a direction

When asked whether a project, plan or change still fits its philosophy, read `PHILOSOPHY.md` and
what the owner has said, then the smallest evidence that covers the question. For each belief,
say whether the work keeps it, strains it, or can't be told yet, and how. A bug, a cost or a
disliked design isn't a philosophy problem, and drift may mean the philosophy needs revisiting
rather than the work. Lead with the overall judgement, keep unrelated findings out, and end with
only what needs the owner. Report in chat; a check changes nothing.
