# David Skills

David's private, personal fork of [mattpocock/skills](https://github.com/mattpocock/skills) — agent skills for real engineering, adapted to David's git practices and issue-tracking conventions. This collection encodes a personal working environment: some skills assume a `dev` integration branch with `main` human-gated, and the managed plugins carry Git guardrail hooks. Those assumptions are declared rather than hidden (see [.agents/adr/0006](./.agents/adr/0006-personal-practice-assumptions-hold-in-every-install.md)).

Developing real applications is hard. Approaches like GSD, BMAD, and Spec-Kit try to help by owning the process. But while doing so, they take away your control and make bugs in the process hard to resolve.

These skills are designed to be small, easy to adapt, and composable. They work with any model. They're based on decades of engineering experience. Hack around with them. Make them your own.

## Credit

David Skills began as a fork of [Matt Pocock's skills](https://github.com/mattpocock/skills). The original methodology and many of the skills are Matt's; see [aihero.dev](https://www.aihero.dev) for his writing, courses, and newsletter on AI-assisted engineering. This fork layers David's personal workflows on top and tracks Matt's `main` through the read-only `upstream` remote (`git fetch upstream && git merge upstream/main`).

## Installation

The normal route is a managed plugin fetched from this private GitHub repository. It does not link to a local checkout. Authenticate GitHub once on each machine before installing:

```bash
gh auth login
gh auth setup-git
```

Pick the plugin for the agent you use. Installing an editable file copy as well creates duplicate skills.

### 1. Get the skills

<details>
<summary><strong>Claude Code</strong></summary>

```
/plugin marketplace add Dlybeck/David-Skills
/plugin install david-skills@david-skills
```

Not in Claude Code's official marketplace — that listing (`mattpocock-skills`) is Matt's unmodified original. This is a private single-plugin marketplace baked into this repo; add it once, then install from it.

To update later:

```
/plugin marketplace update david-skills
/plugin update david-skills@david-skills
```

</details>

<details>
<summary><strong>Codex</strong></summary>

```bash
codex plugin marketplace add Dlybeck/David-Skills --ref main
codex plugin add david-skills@david-skills
```

Codex clones a marketplace snapshot from GitHub into its own managed cache. Review and trust the plugin hooks when Codex prompts you; `/hooks` shows their commands and status. Start a new task after installation so the skills are loaded.

To update later:

```bash
codex plugin marketplace upgrade david-skills
```

The upgrade command refreshes the Git snapshot and reinstalls the configured plugin from it.

</details>

<details>
<summary><strong>Editable files for other agents or tinkerers</strong></summary>

If you intentionally want ordinary skill files you can edit, use [skills.sh](https://skills.sh):

```bash
npx skills@latest add Dlybeck/David-Skills
```

Pick the target agent and skills in its prompts. Include `setup` when your selected skills need missing project configuration. Nothing updates behind your back; pull an updated skill when you want it with `npx skills@latest update <name>`. This file-copy route does not install the plugin hooks.

</details>

### 2. Configure only what you need

When selected skills need missing tracker or domain configuration, run `/setup` in Claude Code
or `$setup` in Codex. Standalone work can start directly; an existing usable convention counts.
Setup will:

- Ask you which issue tracker you want to use (GitHub or local files)
- Ask you what labels you apply to tickets when you triage them (`/triage` uses labels)
- Select the instruction file for the active agent and propose a domain-doc layout

### 3. You are ready to go

The README uses `/name` as shorthand in the sections below. In Codex, invoke an installed skill as `$name`.

### Harness coverage

| Route | Skills | Git guardrail hooks |
| --- | --- | --- |
| Claude Code plugin | All promoted skills listed below | Included automatically |
| Codex plugin | All promoted skills listed below | Included after you review and trust them |
| Editable skills.sh copy | Whichever skills you select | Not included |

Codex is the canonical autonomous-development surface. `advise`, `autopilot`, and `yolopilot` now ship there alongside the model-invoked `pursue-goal` engine; Claude Code uses its own background-goal adapter without constraining the Codex design.

For everyday use, keep a small menu: `advise` for using this plugin, the grilling tools for
understanding, the pilots for autonomous handoff, `philosophy-review` for checks against founding
principles, `status-report` for progress, and `wait-what` or `teach` for explanation. Correct a
running task in ordinary conversation. The full collection
below remains available; model-invoked skills are still human-reachable and do not imply new
permissions. Long-job continuation depends on verified host support and account policy, not the
plugin's presence alone. The [development profile](./docs/agents/david-development-profile.md)
records this fork's design intent without imposing project-specific rules on every installation.

The model-invoked `attention-modes` skill adapts interviews when you have time to focus or can
only answer briefly on the side. `tool-fit` checks the current host's useful capabilities for
sources and presentation; neither mode nor tool availability grants new action authority.

## Why These Skills Exist

This collection targets common failure modes in Claude Code, Codex, and other coding agents.

### #1: The Agent Doesn't Do What You Want

> "No-one knows exactly what they want"
>
> David Thomas & Andrew Hunt, [The Pragmatic Programmer](https://www.amazon.co.uk/Pragmatic-Programmer-Anniversary-Journey-Mastery/dp/B0833F1T3V)

**The Problem**. The most common failure mode in software development is misalignment. You think the dev knows what you want. Then you see what they've built - and you realize it didn't understand you at all.

This is just the same in the AI age. There is a communication gap between you and the agent. The fix for this is a **grilling session** - getting the agent to ask you detailed questions about what you're building.

**The Fix** is to use:

- [`/grill-me`](./skills/productivity/grill-me/SKILL.md) - for non-code uses
- [`/grill-with-docs`](./skills/engineering/grill-with-docs/SKILL.md) - same as [`/grill-me`](./skills/productivity/grill-me/SKILL.md), but adds more goodies (see below)

These skills help you align with the agent before work starts and think deeply about the change
you are making. Use them whenever a change needs careful framing.

### #2: The Agent Is Way Too Verbose

> With a ubiquitous language, conversations among developers and expressions of the code are all derived from the same domain model.
>
> Eric Evans, [Domain-Driven-Design](https://www.amazon.co.uk/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)

**The Problem**: At the start of a project, devs and the people they're building the software for (the domain experts) are usually speaking different languages.

Agents are usually dropped into a project and asked to infer its jargon as they go. The result
is often 20 words where one domain term would do.

**The Fix** for this is a shared language. It's a document that helps agents decode the jargon used in the project.

<details>
<summary>
Example
</summary>

Here is an example [`CONTEXT.md`](https://github.com/mattpocock/course-video-manager/blob/076a5a7a182db0fe1e62971dd7a68bcadf010f1c/CONTEXT.md)
from Matt Pocock's `course-video-manager` repository. Which one is easier to read?

- **BEFORE**: "There's a problem when a lesson inside a section of a course is made 'real' (i.e. given a spot in the file system)"
- **AFTER**: "There's a problem with the materialization cascade"

This concision pays off session after session.

</details>

This is built into [`/grill-with-docs`](./skills/engineering/grill-with-docs/SKILL.md). It's a grilling session, but that helps you build a shared language with the AI, and document hard-to-explain decisions in ADR's.

It's hard to explain how powerful this is. It might be the single coolest technique in this repo. Try it, and see.

> [!TIP]
> A shared language has many other benefits than reducing verbosity:
>
> - **Variables, functions and files are named consistently**, using the shared language
> - As a result, the **codebase is easier to navigate** for the agent
> - The agent also **spends fewer tokens on thinking**, because it has access to a more concise language

### #3: The Code Doesn't Work

> "Always take small, deliberate steps. The rate of feedback is your speed limit. Never take on a task that’s too big."
>
> David Thomas & Andrew Hunt, [The Pragmatic Programmer](https://www.amazon.co.uk/Pragmatic-Programmer-Anniversary-Journey-Mastery/dp/B0833F1T3V)

**The Problem**: Let's say that you and the agent are aligned on what to build. What happens when the agent _still_ produces crap?

It's time to look at your feedback loops. Without feedback on how the code it produces actually runs, the agent will be flying blind.

**The Fix**: You need the usual tranche of feedback loops: static types, browser access, and automated tests.

For automated tests, a red-green-refactor loop is critical. This is where the agent writes a failing test first, then fixes the test. This helps give the agent a consistent level of feedback that results in far better code.

The **[`/tdd`](./skills/engineering/tdd/SKILL.md) skill** slots into any project. It encourages
red-green-refactor and gives the agent guidance on what makes good and bad tests.

For debugging, **[`/diagnosing-bugs`](./skills/engineering/diagnosing-bugs/SKILL.md)** wraps
best practices into a disciplined loop, gated phase by phase.

### #4: We Built A Ball Of Mud

> "Invest in the design of the system _every day_."
>
> Kent Beck, [Extreme Programming Explained](https://www.amazon.co.uk/Extreme-Programming-Explained-Embrace-Change/dp/0321278658)

> "The best modules are deep. They allow a lot of functionality to be accessed through a simple interface."
>
> John Ousterhout, [A Philosophy Of Software Design](https://www.amazon.co.uk/Philosophy-Software-Design-2nd/dp/173210221X)

**The Problem**: Most apps built with agents are complex and hard to change. Because agents can radically speed up coding, they also accelerate software entropy. Codebases get more complex at an unprecedented rate.

**The Fix** for this is a radical new approach to AI-powered development: caring about the design of the code.

This is built in to every layer of these skills:

- [`/to-spec`](./skills/engineering/to-spec/SKILL.md) quizzes you about which modules you're touching before creating a spec

And crucially, [`/re-architect`](./skills/engineering/re-architect/SKILL.md) surveys a codebase
for deepening opportunities and hands you the candidates. Run it every few days on an active
codebase. It is a survey, not a rescue: on a genuinely old codebase it will find real candidates,
but it will not untangle the mud for you.

### Summary

Software engineering fundamentals matter more than ever. These skills condense those fundamentals
into repeatable practices for shipping better applications.

## Reference

These split on one axis — who can invoke them. **User-invoked** skills are reachable only when you type them (e.g. `/grill-me`); their job is to orchestrate. **Model-invoked** skills can be invoked by you _or_ reached for automatically by the agent when the task fits; they hold the reusable discipline. A user-invoked skill may invoke model-invoked skills, but never another user-invoked one.

### Engineering

Skills for daily code work.

**User-invoked**

- **[advise](./skills/engineering/advise/SKILL.md)** — Ask which skill or flow fits your situation. A router over the user-invoked skills in this repo.
- **[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)** — Grilling session that also builds your project's domain model, sharpening terminology and updating `CONTEXT.md` and ADRs inline.
- **[triage](./skills/engineering/triage/SKILL.md)** — Move issues through a state machine of triage roles.
- **[re-architect](./skills/engineering/re-architect/SKILL.md)** — Scan a codebase for deepening opportunities, present a visual review in chat or a useful page, then grill through whichever one you pick.
- **[setup](./skills/engineering/setup/SKILL.md)** — Configure tracker, labels, and domain docs when selected skills need missing project conventions.
- **[delegate](./skills/engineering/delegate/SKILL.md)** — Dispatch ready tickets whole to worker subagents until the frontier is drained.
- **[autopilot](./skills/engineering/autopilot/SKILL.md)** — Enter unattended work mode — lock a goal before you leave, then keep working without you until it's met.
- **[yolopilot](./skills/engineering/yolopilot/SKILL.md)** — Skip the grilling round for a last-second handoff, then work unattended without merging into `dev` on its own.
- **[wayfinder](./skills/engineering/wayfinder/SKILL.md)** — Plan a huge chunk of work, more than one agent session can hold, as a shared map of decision tickets on the issue tracker — resolve them one at a time until the way to the destination is clear.

**Model-invoked**

- **[to-spec](./skills/engineering/to-spec/SKILL.md)** — Synthesize settled requirements into a proportionate spec; publish only with authority.
- **[to-tickets](./skills/engineering/to-tickets/SKILL.md)** — Decompose understood work into verifiable tracer-bullet tickets with blocking edges when useful.
- **[implement](./skills/engineering/implement/SKILL.md)** — Build understood work from a conversation, goal, spec, or tickets with tests and whole-change review.

- **[prototype](./skills/engineering/prototype/SKILL.md)** — Build a throwaway prototype to answer a design question — a single shareable HTML file for state/logic questions, or several radically different UI variations toggleable from one route.
- **[diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md)** — Disciplined diagnosis loop for hard bugs and performance regressions: build a feedback loop that goes red on this bug → minimise → hypothesise → instrument → fix → regression-test.
- **[research](./skills/engineering/research/SKILL.md)** — Investigate primary sources and present cited findings; save a durable note when useful.
- **[tdd](./skills/engineering/tdd/SKILL.md)** — Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time.
- **[domain-modeling](./skills/engineering/domain-modeling/SKILL.md)** — Actively build and sharpen a project's domain model — challenge terms against the glossary, stress-test with edge-case scenarios, and update `CONTEXT.md` and ADRs inline.
- **[codebase-design](./skills/engineering/codebase-design/SKILL.md)** — Shared discipline and vocabulary for designing deep modules: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface.
- **[code-review](./skills/engineering/code-review/SKILL.md)** — Two-axis review of the diff since a fixed point: **Standards** (does it follow the repo's coding standards, plus a Fowler smell baseline?) and **Spec** (does it faithfully implement the originating issue/spec?), run as parallel sub-agents so neither pollutes the other.
- **[resolving-merge-conflicts](./skills/engineering/resolving-merge-conflicts/SKILL.md)** — Work through an in-progress git merge or rebase conflict hunk by hunk, resolving by intent traced to each side's primary source, then finish the operation — never `--abort`.
- **[wizard](./skills/engineering/wizard/SKILL.md)** — Generate an interactive bash wizard that walks a human through steps only they can perform: provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover.
- **[pursue-goal](./skills/engineering/pursue-goal/SKILL.md)** — Drive an authorized long-horizon objective through adaptive research, discovery, delivery, and optimization loops until the evidence reaches a real stopping boundary.

### Productivity

General workflow tools, not code-specific.

**User-invoked**

- **[grill-me](./skills/productivity/grill-me/SKILL.md)** — Get relentlessly interviewed about a plan or design until every branch of the design tree is resolved.
- **[teach](./skills/productivity/teach/SKILL.md)** — Teach the user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.
- **[to-questionnaire](./skills/productivity/to-questionnaire/SKILL.md)** — Turn a decision you can't answer alone into a Markdown questionnaire for the one person who can — filled in async, or together over a meeting. It grills you about the send (who it's for, what you need back), not the subject.
- **[wait-what](./skills/productivity/wait-what/SKILL.md)** — Fire this the moment a message doesn't land. The agent re-pitches it with the context you're missing, in plain English, using your `CONTEXT.md` vocabulary.

**Model-invoked**

- **[handoff](./skills/productivity/handoff/SKILL.md)** — Export portable context for an actual authorized transfer without abandoning active work.

- **[attention-modes](./skills/productivity/attention-modes/SKILL.md)** — Adapt collaboration to Focused or On the side attention, including brief or dictated replies.
- **[tool-fit](./skills/productivity/tool-fit/SKILL.md)** — Use fitting host tools for evidence, visuals, previews, and artifacts.
- **[philosophy-review](./skills/productivity/philosophy-review/SKILL.md)** — Check a project or proposed change against its owner-adopted founding principles.
- **[grilling](./skills/productivity/grilling/SKILL.md)** — Resolve material decisions through focused interview rounds, reusing settled context.
- **[writing-for-agents](./skills/productivity/writing-for-agents/SKILL.md)** — Writing documents for agents: skills, AGENTS.md/CLAUDE.md, and any doc an agent reaches by a pointer.
- **[status-report](./skills/productivity/status-report/SKILL.md)** — Connect verified progress to long-term project goals directly in chat with useful visuals; export a document or webpage on request.
