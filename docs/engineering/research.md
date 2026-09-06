## What it does

`research` answers a question by reading the sources that own the answer, then leaves a cited Markdown file in the repo. It works only from **[primary sources](https://www.aihero.dev/ai-coding-dictionary/primary-source)** — official docs, source code, specs, first-party APIs — and follows every claim back to the source that owns it, so it will not repeat a blog post's account of an API when the API's own docs are reachable.

The durable output is a file, written where the repo already keeps such notes, with a link on each claim. A concise answer in chat can accompany it. The artifact is something you can react to or hand to another agent after the [session](https://www.aihero.dev/ai-coding-dictionary/session) ends.

## When to reach for it

Type `/research`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) reaches for it automatically when a task turns into reading legwork.

Reach for it when the next step is *finding something out* from outside the working directory — how a third-party API behaves, what a spec actually says, whether a version claim holds — and you'd rather not stall your own thread doing the reading. What you need decides which skill:

| What you need | Reach for |
| --- | --- |
| An external fact a decision is waiting on | `research` |
| A decision made *with* you, by interview | [grilling](../productivity/grilling.md) |
| A durable architecture decision, written into `CONTEXT.md` and ADRs | [grill-with-docs](./grill-with-docs.md) |
| To find out whether an approach works in your codebase | [prototype](./prototype.md) |
| A plan too big to hold in one session | [wayfinder](./wayfinder.md) |

The line between `research` and `grill-with-docs` is the **shelf life of what comes back**. Research produces short-lived assets — what this library's auth mechanism does as of this week. An ADR records a decision you keep. If what you are producing is a decision rather than a fact, you are [grilling](https://www.aihero.dev/ai-coding-dictionary/grilling), not researching.

## Delegated legwork

Small lookups run directly. Substantial reading can use one **background agent** when useful independent work remains in the main session and the user's delegation budget allows it. Source quality and a useful answer matter more than whether the reading ran in another context.

Delegation is at most one level deep. An already-delegated worker researches directly and must not invoke `research` again or spawn another worker.

Where the file lands is decided by the repo, not by the skill: it matches whatever convention already exists for notes, and if there is none it picks somewhere sensible and tells you where. It writes one file per run.

## Common questions

**It spawned a second research agent — is that meant to happen?**

No. Upstream [issue #530](https://github.com/mattpocock/skills/issues/530) documented recursive fan-out, including one run measured at roughly 450k [tokens](https://www.aihero.dev/ai-coding-dictionary/token). David Skills carries the instruction-level fix: an agent that is already a [subagent](https://www.aihero.dev/ai-coding-dictionary/subagent) must research directly and must not delegate again. If you still see more than one worker, stop the duplicate and report the harness and model so the guard can be tightened.

**Where should the file live — and should I commit it?**

Follow the repo's existing notes convention and your retention policy. A dated research file can preserve valuable evidence, but later work should recheck facts that may have changed. The skill does not require either committing or deleting it.

**What counts as a "high-trust" primary source, and who decides?**

The [model](https://www.aihero.dev/ai-coding-dictionary/model) does. The skill names the *kinds* of source that qualify — official docs, source code, specs, first-party APIs — and there is no allowlist, no domain gate, and no verification pass. This was the loudest objection when the skill was first proposed and it has never been answered publicly: "Five research subagents pointed at junk just gives you five confident wrong answers faster. How are you gating what counts as high-trust sources?" The mitigation you actually have is the citation on each claim. Follow two or three of them. If they land on a summary of the thing rather than the thing, the run failed at its one job.

**Does a later session reuse what an earlier run found?**

No. Nothing auto-loads a past research file; it is a document sitting in the repo until a human or a skill points at it. This was raised early as the strongest challenge to the design — "the value's the markdown becoming context the agent re-reads later, not the fetch itself. A write-once dead file is just a fancy search" — and the shipped skill does not solve it. In practice the file earns its keep by being fed into the next step deliberately: attach it to a spec, quote it into a grilling session, point a [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket) at it.

**Why not just ask the agent to go read the docs?**

You can. The skill adds primary-source discipline and a cited artifact, with background reading available when that separation earns its cost. If a short direct answer is all you need, ordinary conversation may be sufficient.

**When does it stop reading?**

There is no stopping criterion in the skill, and this shows up as two complaints that look opposite but are the same gap: agents that go far too deep, and agents that cover a topic broadly while missing the one specific detail that mattered. One practitioner put it as "deep-research skills are a bit too deep sometimes. And telling an agent to research usually results in missing crucial details." Scoping is on you. A narrow, answerable question — one API, one behaviour, one version claim — comes back far better than "research X".

**`/wayfinder` created research tickets — do I resolve those myself?**

Wayfinder can resolve ready research directly or through one bounded worker. Extra tickets remain pending rather than causing one worker per ticket. Findings are linked from their tickets; a separate branch is optional when isolation and Git authority justify it. Preserve linked evidence while the map still depends on it.

## It's working if

- Small lookups stay direct; substantial independent reading may use one background task.
- No research worker creates another research worker.
- One new Markdown file shows up, in the folder the repo already uses for notes, and the agent tells you the path.
- Every claim in it carries a link, and following two at random lands you on an official doc, a spec, or the actual source file — not on someone's write-up of it.
- You can make the decision you were stuck on from the file alone, without going back to the sources yourself.

## Where it fits

A reach-for-it-anytime standalone: its findings can answer the request directly or inform [grilling](../productivity/grilling.md), [wayfinder](./wayfinder.md), or an autonomous [pursue-goal](./pursue-goal.md) run. For the whole map, see [advise](./advise.md).
