# Phase 2 rename/terminology review

Working document, not a skill or docs page — a checklist for the systematic review pass
described in the bootstrap plan (de-brand + align terminology to Denali's own usage). One
entry per promoted skill (Engineering + Productivity only — `misc/`, `in-progress/`, and
`deprecated/` aren't promoted, so they're out of scope for this pass; see the note at the
bottom if you want them covered too).

For each skill: its current name, current one-line description (as it reads in the top-level
`README.md` today), and a blank **Notes/corrections** field — add "keep as-is," a new name, a
terminology swap, or whatever's relevant. Nothing here gets touched until we go through this
together.

---

## Engineering

### User-invoked

#### `ask-matt`
Ask which skill or flow fits your situation. A router over the user-invoked skills in this repo.

**Notes/corrections:**
>ask-claude

#### `grill-with-docs`
Grilling session that also builds your project's domain model, sharpening terminology and updating `CONTEXT.md` and ADRs inline.

**Notes/corrections:**
>keep as-is (2026-08-07). Explored swapping the short `grill-me` name onto this skill's
>behavior (it's the common case whenever a repo exists) and giving the current `grill-me` a
>new name. Got stuck finding a name for the stateless variant that was actually situational
>rather than mechanical — "fresh project" turned out to be the wrong trigger entirely (an empty
>repo still counts as a working directory); the real trigger is "no repo decided/available to
>write into at all," which never produced a name better than what already exists. Dropped.

#### `triage`
Move issues through a state machine of triage roles.

**Notes/corrections:**
>

#### `improve-codebase-architecture`
Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.

**Notes/corrections:**
>re-architect

#### `setup-matt-pocock-skills`
Configure this repo for the engineering skills (issue tracker, triage labels, domain doc layout). Run once per repo before using the other engineering skills.

**Notes/corrections:**
>setup (renamed twice: setup-matt-pocock-skills -> setup-denali-skills -> setup, once the plugin identity itself shortened to denali-dev)

#### `to-spec`
Turn the current conversation into a spec and publish it to the issue tracker. No interview — just synthesizes what you've already discussed.

**Notes/corrections:**
>

#### `to-tickets`
Break any plan, spec, or conversation into a set of tracer-bullet tickets, each declaring its blocking edges — written as text in a local file, or as native blocking links on a real tracker.

**Notes/corrections:**
>

#### `implement`
Build the work described by a spec or set of tickets, driving `/tdd` at pre-agreed seams and closing out with `/code-review` before committing.

**Notes/corrections:**
>

#### `wayfinder`
Plan a huge chunk of work, more than one agent session can hold, as a shared map of decision tickets on the issue tracker — resolve them one at a time until the way to the destination is clear.

**Notes/corrections:**
>

### Model-invoked

#### `prototype`
Build a throwaway prototype to answer a design question — a single shareable HTML file for state/logic questions, or several radically different UI variations toggleable from one route.

**Notes/corrections:**
>

#### `diagnosing-bugs`
Disciplined diagnosis loop for hard bugs and performance regressions: build a feedback loop that goes red on this bug → minimise → hypothesise → instrument → fix → regression-test.

**Notes/corrections:**
>

#### `research`
Investigate a question against high-trust primary sources and capture the findings as a cited Markdown file in the repo, run as a background agent.

**Notes/corrections:**
>

#### `tdd`
Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time.

**Notes/corrections:**
>

#### `domain-modeling`
Actively build and sharpen a project's domain model — challenge terms against the glossary, stress-test with edge-case scenarios, and update `CONTEXT.md` and ADRs inline.

**Notes/corrections:**
>

#### `codebase-design`
Shared discipline and vocabulary for designing deep modules: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface.

**Notes/corrections:**
>

#### `code-review`
Two-axis review of the diff since a fixed point: **Standards** (does it follow the repo's coding standards, plus a Fowler smell baseline?) and **Spec** (does it faithfully implement the originating issue/spec?), run as parallel sub-agents so neither pollutes the other.

**Notes/corrections:**
>

#### `resolving-merge-conflicts`
Work through an in-progress git merge or rebase conflict hunk by hunk, resolving by intent traced to each side's primary source, then finish the operation — never `--abort`.

**Notes/corrections:**
>

#### `wizard`
Generate an interactive bash wizard that walks a human through steps only they can perform: provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover.

**Notes/corrections:**
>

#### `personal-git-workflow` — REMOVED 2026-08-07
*(Added this session, not from upstream; removed the same day this worksheet review resumed.)* Was a `main ← dev ← feature/**` branching model for solo/dev-quality repos. David judged the teaching prose unnecessary — the mechanical enforcement (the plugin-root hook blocking any push/PR into `main`, plus four branch-agnostic destructive-op blocks) is what actually mattered, and it doesn't depend on the skill existing. See ADR 0003's update note.

**Notes/corrections:**
>removed, not renamed — no entry needed going forward

---

## Productivity

### User-invoked

#### `grill-me`
Get relentlessly interviewed about a plan or design until every branch of the design tree is resolved.

**Notes/corrections:**
>

#### `handoff`
Compact the current conversation into a handoff document so another agent can continue the work.

**Notes/corrections:**
>

#### `teach`
Teach the user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.

**Notes/corrections:**
>

#### `to-questionnaire`
Turn a decision you can't answer alone into a Markdown questionnaire for the one person who can — filled in async, or together over a meeting. It grills you about the send (who it's for, what you need back), not the subject.

**Notes/corrections:**
>keep as-is (2026-08-07). `to-survey` was floated and held up fine on its own (keeps the `to-*`
>family shape, same meaning, shorter) — called off along with the whole short-names pass when
>the paired `grill-with-docs`/`grill-me` rename got stuck, not because of a problem with this
>one specifically. Fine to pick back up on its own later if wanted.

#### `wait-what`
Fire this the moment a message doesn't land. The agent re-pitches it with the context you're missing, in plain English, using your `CONTEXT.md` vocabulary.

**Notes/corrections:**
>

### Model-invoked

#### `grilling`
Interview the user relentlessly about a plan, decision, or idea until every branch of the design tree is resolved. The reusable interview primitive behind `grill-me`, `grill-with-docs`, `triage`, `wayfinder` and `re-architect`.

**Notes/corrections:**
>

#### `writing-for-agents`
Writing documents for agents: skills, AGENTS.md/CLAUDE.md, and any doc an agent reaches by a pointer.

**Notes/corrections:**
>

---

## Not covered here

`skills/misc/` (`migrate-to-shoehorn`, `scaffold-exercises`, `setup-pre-commit`), `skills/in-progress/`
(`loop-me`, `claude-handoff`, `setup-ts-deep-modules`, `writing-beats`, `writing-fragments`,
`writing-shape`), and `skills/deprecated/` (currently empty) aren't promoted, so they're out of
scope for this pass. Say if you want a matching worksheet for those too.
