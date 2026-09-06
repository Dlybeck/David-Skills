---
name: advise
description: Ask which skill or flow fits your situation. A router over the skills in this repo.
disable-model-invocation: true
---

# Advise

You don't remember every skill, so ask.

A **flow** is one possible composition of skills, not a required sequence. Start from the user's
current situation and settled context. Recommend only the next useful practice; skip, revisit,
or combine stages when their inputs are already available. Internal discipline and genuine
prerequisites still apply. Read the relevant skill before making a load-bearing claim about it;
the sketches below are a map, not a substitute for the skill.

## The main flow: idea → ship

One useful route when an idea still needs shaping. It is not an entrance requirement for
implementation, research, review, or any standalone skill.

1. **`/grill-with-docs`** — sharpen an unresolved idea when domain decisions should be retained
   in `CONTEXT.md` and ADRs. Use `/grill-me` for a stateless discussion, including in a repo when
   no documentation is wanted. Both use `/grilling`; settled work need not repeat either interview.
2. **Branch — can you settle every question in conversation?** If a question needs a runnable answer (state, business logic, a UI you have to see), detour through a prototype, bridged by **`/handoff`** in both directions (a prototype lives in its own directory, which is exactly what `/handoff` is for — see Phase boundaries):
   - **`/handoff`** out, then open a fresh session against that file,
   - **`/prototype`** to answer the question with throwaway code,
   - **`/handoff`** back what you learned, and reference it from the original idea thread.
3. **Branch — is this a multi-session build?**
   - **Yes** → **`/to-spec`** (turn the thread into a spec), then **`/to-tickets`** to split it into tracer-bullet tickets, each declaring its **blocking edges**. On a local tracker that's one file per ticket under `.scratch/<feature>/issues/`, worked blockers-first by hand; on a real tracker the edges become native blocking links, so any ticket whose blockers are done can be grabbed — kick off **`/implement`** per ticket, **`/clear`ing context between each one**. Each ticket is self-contained, so the last one's context is disposable.
   - **No** → **`/implement`** right here, in the same context window.

   Either way, **`/implement`** builds each issue by driving **`/tdd`** internally — one red-green slice at a time — then closes out by running **`/code-review`**, a two-axis review (Standards + Spec) including relevant uncommitted and new files, before committing and marking the ticket resolved. Reach for **`/tdd`** on its own when you just want to build a concrete behaviour test-first without a full spec, and **`/code-review`** on its own whenever you want to review WIP, a branch, or a PR against a fixed point. The originating request or confirmed goal contract can supply the Spec axis without a formal spec document.

   **`/delegate`** dispatches this same step instead of you driving it: one bounded run claims each frontier ticket, hands it whole to a worker subagent, and tracks only whether it resolved — over when the frontier is drained. Reach for it when several tickets are ready and independent.

### Context hygiene

Preserve settled decisions between related practices. Continue in the same conversation while its
context remains useful; use a compact checkpoint or self-contained ticket when restarting would
otherwise lose requirements. A fresh implementation session is useful for an independent ticket,
not a mandatory boundary for every change.

Use the current harness's context controls when needed, preserving the primary evidence and open
decisions. Do not infer a universal safe context size from another model's token count.

## Running autonomously

**`/autopilot`** — long-horizon work whose authority is earned through a pre-departure `/grilling` session. It locks a goal contract, then `/pursue-goal` selects research, discovery, delivery, and optimization loops until the evidence proves the goal, new human authority is required, or the evidence plateaus. It may integrate into `dev` only when the locked contract authorizes that delivery target and every gate passes.

**`/yolopilot`** — the same long-horizon engine entered without grilling. It states a provisional interpretation and starts immediately, learning and refining inside that interpretation. It may push a review branch but never merges it. Its postflight gives a short account of assumptions, actions, evidence, and lessons, then offers an immediate explanation or the optional `/teach` path for durable learning.

**`/pursue-goal`** — the model-invoked engine under both pilots. It is not another trust mode and normally is not the human entry point. It keeps the goal contract stable while choosing whichever loop reduces the current uncertainty.

## On-ramps

A starting situation that generates work, then merges onto the main flow.

- **Bugs and requests piling up** → **`/triage`**. It moves issues through triage roles and produces agent-ready issues, which **`/implement`** later picks up.

  Triage is only for issues **you didn't create** — bug reports, incoming feature requests, anything that arrives raw. Tickets that `/to-tickets` produced are already agent-ready, so **don't triage them**.

- **Something's broken** → **`/diagnosing-bugs`**. For unclear failures, intermittent flakes, or regressions, establish or reuse a **tight feedback loop**. Diagnosis-only ends with the cause and proposed fix; an authorized repair continues through a regression test and fix. Consider **`/re-architect`** when the finding is that there's no good seam to lock the bug down.

- **A huge, foggy effort — a greenfield project or a huge feature build, too big for one session** → **`/wayfinder`**, the most cognitively demanding flow here. When the way from here to the destination isn't visible yet, it charts a **shared map** of **decision tickets** on the issue tracker and resolves them one at a time — producing **decisions, not deliverables** — until the fog is pushed back and the way is clear. Where **`/grill-with-docs`** sharpens an idea you can hold in one session, wayfinder is for the idea you can't — and it's slower and denser, so save it for exactly that, never a well-scoped feature.

  When the map clears, **it hands off, it doesn't build**: merge onto the main flow at **`/to-spec`**, which collapses the map's linked decisions into a buildable plan, then `/to-tickets` and `/implement` as usual. Looping the map straight into `/implement` skips that collapse and throws the linked detail away — go straight to `/implement` only when the effort turned out genuinely small.

## Codebase health

Not feature work — upkeep.

- **`/re-architect`** — run whenever you have a spare moment to keep the codebase good for agents to operate in. It surfaces **deepening opportunities**; picking one _generates an idea_ you can take into the main flow at `/grill-with-docs`. It's the survey that finds the candidates; **`/codebase-design`** (below) is the bench you design the chosen one on.

## Vocabulary underneath

Two model-invoked references that run *beneath* the other skills — each the single source of truth for its vocabulary. Reach for them directly when the **words**, not the process, are the problem; or let the skills above pull them in.

- **`/domain-modeling`** — sharpen the project's *domain* language: challenge a fuzzy term, resolve an overloaded word ("account" doing three jobs), record a hard-to-reverse decision as an ADR. It's the active discipline `/grill-with-docs` drives to keep `CONTEXT.md` a clean glossary.
- **`/codebase-design`** — the deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality) for designing a module's *shape*: a lot of behaviour behind a small interface at a clean seam. `/tdd` and `/re-architect` both speak it.

## Phase boundaries

A **phase** is a chunk of work inside a session — the grilling, the implementation, the QA. At the **boundary** between two of them you have five options, and picking between them is the fuzziest decision in this whole map:

- **Continue** — stay put. Costs nothing, loses nothing.
- **`/clear`** — empty the window, when nothing here matters to what's next.
- **`/handoff`** — write a portable markdown file. Narrow: only for a **new harness**, a **new directory**, a **colleague**, or forking a side task **mid-phase**. What it buys is portability.
- **Subagent** — send a tightly-scoped task to its own window and get a report back.
- **`/compact`** — compress this context and seed a fresh session with it. The **default**, at the bottom of the tree rather than the first reach.

Read [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) for the ordered tree — the five questions, the reasoning behind each branch, and why the primary-source cost makes **Continue** the one to rule out first. Make the decision **at** a boundary; mid-phase, continue or split the rest into subagents.

## Standalone

Off the main flow entirely.

- **`/status-report`** — a model- or user-invoked progress snapshot connecting current evidence to milestones and long-term project outcomes. Use for a project overview or a substantial pilot review update: concise conclusions in chat, a saved Markdown report, and a webpage when requested. It reports existing state without changing plans or starting monitoring.
- **`/grill-me`** — a **stateless** interview: no local files or `CONTEXT.md`. Use it to sharpen
  a plan, design, or piece of writing whenever you want discussion without documentation.
- **`/grilling`** — the interview primitive itself: rounds, the frontier, facts are the agent's job and decisions are yours. `/grill-me` and `/grill-with-docs` are the two named ways in, and `/triage`, `/wayfinder` and `/re-architect` all run it internally. Reach for it directly only when you want the interview with no wrapper around it.
- **`/resolving-merge-conflicts`** — work an in-progress merge or rebase conflict hunk by hunk, resolving by **intent** traced to each side's primary source rather than by picking lines, then finish the operation. It never runs `--abort`. Standalone and off every flow: reach for it when you are already mid-conflict.
- **`/prototype`** — a throwaway program answering one design question. Keep its verdict and
  evidence as a **primary source**. It needs no issue or planning pipeline; production integration
  requires separate authority. Reach for it whenever a runnable answer is useful.
- **`/research`** — investigate **primary sources** and save cited findings. Small lookups run
  directly; substantial independent reading can use one background agent within the user's
  budget. Findings can settle the request directly or inform any later practice.
- **`/to-questionnaire`** — when the thing blocking you isn't in your head or the codebase but in **someone else's**, this writes them a questionnaire to fill in. It's the inverse of `/grill-me`: instead of interviewing you about the subject, it interviews you about the **send** — who it's going to, what you need back — and aims the questions at the gap. What comes back is material for `/grill-with-docs` or `/to-spec`.
- **`/wizard`** — for the steps only a **human** can take: provisioning infrastructure, setting up credentials or CI secrets, clicking through an unfamiliar third-party dashboard, running a one-off migration or cutover. It generates an interactive bash script that opens each URL, captures each value, and writes it into `.env` and GitHub secrets — so the procedure stops being something you re-explain to an agent every time. Model-invoked, so the agent reaches for it the moment it hits a wall only you can pass. If the agent could just do it itself, it should; this is for where a human is genuinely in the loop.
- **`/wait-what`** — the corrective for a message that didn't land. Use it mid-conversation, inside any other skill, and the agent re-pitches what it just said with the context you were missing, in plain English, using the `CONTEXT.md` vocabulary. It works after the fact; `/grill-with-docs` is the upfront cure, because a shared language agreed early is what stops the jargon arriving at all.
- **`/teach`** — learn a concept over multiple sessions, using the current directory as a stateful workspace.
- **`/writing-for-agents`** — reference for writing documents agents consume: skills, AGENTS.md, pointed-at docs.

## Configuration when needed

**`/setup`** — configure the issue tracker, triage labels, and doc layout when a selected skill
needs that configuration and it is missing. Standalone work does not require setup just because
it is engineering work. Existing usable project conventions count; custom trackers also work.
