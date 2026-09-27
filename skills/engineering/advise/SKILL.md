---
name: advise
description: Ask which skill or flow fits your situation. A router over the skills in this repo.
disable-model-invocation: true
---

# Advise

Help the human use this plugin. Recommend and stop; do not turn plugin advice into product
planning or start the recommended work, even when the suggested skill is model-invoked.

For everyday use, orient around understanding (`/grill-me` or `/grill-with-docs`), autonomous
handoff (`/autopilot` or `/yolopilot`), checking progress (`/status-report`), clarification
(`/wait-what`), and learning (`/teach`). Specialist skills remain available on their own terms.
`/to-spec`, `/to-tickets`, `/implement`, and `/handoff` are model- or user-reachable;
automatic selection never supplies missing authority for their effects.

A **flow** is one possible composition of skills, not a required sequence. Start from the user's
current situation and settled context. Recommend only the next useful practice; skip, revisit,
or combine stages when their inputs are already available. Internal discipline and genuine
prerequisites still apply. Read the relevant skill before making a load-bearing claim about it;
the sketches below are a map, not a substitute for the skill.

**Attention and tools are cross-cutting, not new workflow stages.** `/attention-modes` adapts
question depth and timing to Focused or On the side attention; it does not choose a different
skill or expand authority. `/tool-fit` selects useful capabilities available in the current
host for source access, visuals, and previews without making any one AI app a prerequisite.

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
3. **Branch — would durable requirements or decomposition help?**
   - **Requirements need a reference** → **`/to-spec`** synthesizes settled understanding.
   - **Independent work units help** → **`/to-tickets`** records tracer-bullet slices and blocking
     edges, directly from a conversation, plan, or spec. Publish only within tracker authority.
   - **Work is already coherent and understood** → **`/implement`** directly in the current context.

   These are independent choices, not a package deal. During authorized work the agent may select
   them and make delegated technical decisions without another approval round. Keep context while
   useful; neither tickets nor a new session are required merely because the work is long.

   **`/implement`** uses **`/tdd`** where appropriate and **`/code-review`** over the whole change.
   A request to implement or fix includes routine local toolchain, dependency, and test-environment
   preparation. Missing local prerequisites do not route through `/setup` or require renewed approval.
   Commits and ticket resolution require authority; without it, leave a tested local diff.
   **`/tdd`** and **`/code-review`** also work standalone. A conversation or current goal contract,
   including user corrections, can supply the requirements without a formal spec.

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

The human can question or correct a run in ordinary conversation. `/pursue-goal` reconciles clear
corrections with running work and its checkpoint; `/status-report` exposes current intent and
evidence without changing the goal. `/wait-what` repairs an explanation, not the goal itself.

## On-ramps

A starting situation that generates work, then merges onto the main flow.

- **Bugs and requests piling up** → **`/triage`**. It moves issues through triage roles and produces agent-ready issues, which **`/implement`** later picks up.

  Triage is only for issues **you didn't create** — bug reports, incoming feature requests, anything that arrives raw. Tickets that `/to-tickets` produced are already agent-ready, so **don't triage them**.

- **Something's broken** → **`/diagnosing-bugs`**. For unclear failures, intermittent flakes, or regressions, establish or reuse a **tight feedback loop**. Diagnosis-only ends with the cause and proposed fix; an authorized repair continues through a regression test and fix. Consider **`/re-architect`** when the finding is that there's no good seam to lock the bug down.

- **A huge, foggy effort — a greenfield project or a huge feature build, too big for one session** → **`/wayfinder`**, the most cognitively demanding flow here. When the way from here to the destination isn't visible yet, it charts a **shared map** of **decision tickets** on the issue tracker and resolves them one at a time — producing **decisions, not deliverables** — until the fog is pushed back and the way is clear. Where **`/grill-with-docs`** sharpens an idea you can hold in one session, wayfinder is for the idea you can't — and it's slower and denser, so save it for exactly that, never a well-scoped feature.

  When the map clears, **it hands off, it doesn't build**. Preserve its linked decisions in the
  implementation context. `/to-spec` can consolidate them when that would help; `/to-tickets`
  supplies decomposition when needed. None of these artifacts grants execution authority.

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

- **`/status-report`** — a model- or user-invoked progress snapshot connecting current evidence to milestones and long-term project outcomes. Use for a project overview or a substantial pilot review update: the report and useful visuals appear in chat by default; saved documents and webpages are opt-in. It reports existing state without changing plans or starting monitoring.
- **`/grill-me`** — a **stateless** interview: no local files or `CONTEXT.md`. Use it to sharpen
  a plan, design, or piece of writing whenever you want discussion without documentation.
- **`/grilling`** — the interview primitive itself: rounds, the frontier, facts are the agent's job and decisions are yours. `/grill-me` and `/grill-with-docs` are the two named ways in, and `/triage`, `/wayfinder` and `/re-architect` all run it internally. Reach for it directly only when you want the interview with no wrapper around it.
- **`/resolving-merge-conflicts`** — work an in-progress merge or rebase conflict hunk by hunk, resolving by **intent** traced to each side's primary source rather than by picking lines, then finish the operation. It never runs `--abort`. Standalone and off every flow: reach for it when you are already mid-conflict.
- **`/prototype`** — a throwaway program answering one design question. Keep its verdict and
  evidence as a **primary source**. It needs no issue or planning pipeline; production integration
  requires separate authority. Reach for it whenever a runnable answer is useful.
- **`/research`** — investigate **primary sources** and present cited findings. Small lookups run
  directly; substantial independent reading can use one background agent within the user's
  budget. Findings can settle the request directly or inform any later practice.
- **`/to-questionnaire`** — when the thing blocking you isn't in your head or the codebase but in **someone else's**, this writes them a questionnaire to fill in. It's the inverse of `/grill-me`: instead of interviewing you about the subject, it interviews you about the **send** — who it's going to, what you need back — and aims the questions at the gap. What comes back is material for `/grill-with-docs` or `/to-spec`.
- **`/wizard`** — for the steps only a **human** can take: provisioning infrastructure, setting up credentials or CI secrets, clicking through an unfamiliar third-party dashboard, running a one-off migration or cutover. It generates an interactive bash script that opens each URL, captures each value, and writes it into `.env` and GitHub secrets — so the procedure stops being something you re-explain to an agent every time. Model-invoked, so the agent reaches for it the moment it hits a wall only you can pass. If the agent could just do it itself, it should; this is for where a human is genuinely in the loop.
- **`/wait-what`** — the corrective for a message that didn't land. Use it mid-conversation, inside any other skill, and the agent re-pitches what it just said with the context you were missing, in plain English, using the `CONTEXT.md` vocabulary. It works after the fact; `/grill-with-docs` is the upfront cure, because a shared language agreed early is what stops the jargon arriving at all.
- **`/teach`** — learn a concept over multiple sessions, using the current directory as a stateful workspace.
- **`/writing-for-agents`** — reference for writing documents agents consume: skills, AGENTS.md, pointed-at docs.

## Configuration when needed

**`/setup`** — configure the issue tracker, triage labels, and doc layout when a selected skill
needs that configuration and it is missing. This is not development-environment setup; the agent
repairs local build and test prerequisites during the task that needs them. Standalone work does
not require `/setup` just because it is engineering work. Existing usable project conventions
count; custom trackers also work.
