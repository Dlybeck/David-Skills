## What it does

`research` answers a question by inspecting the **[primary sources](https://www.aihero.dev/ai-coding-dictionary/primary-source)** that own the answer: user-provided or connected originals, official docs, source code, specs, and first-party APIs. For current external facts, it searches when needed and opens the actual source. Material claims point back to what was inspected rather than repeating a secondary account.

The answer appears in chat with source links and meaningful uncertainty. A small lookup needs no extra file. Substantial or delegated reading, requested documentation, and findings needed beyond the [session](https://www.aihero.dev/ai-coding-dictionary/session) get one cited Markdown note in the repo's notes location when a repo exists. Without a checkout, the agent uses an available host artifact or a self-contained chat report.

## When to reach for it

Type `/research`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) reaches for it automatically when a task turns into reading legwork.

Reach for it when the next step is *finding something out* — how a third-party API behaves, what a connected original says, whether a version claim holds. [Tool fit](../productivity/tool-fit.md) chooses available authorized access to the source, without requiring a particular app or connector. What you need decides which skill:

| What you need | Reach for |
| --- | --- |
| An external fact a decision is waiting on | `research` |
| A decision made *with* you, by interview | [grilling](../productivity/grilling.md) |
| A durable architecture decision, written into `CONTEXT.md` and ADRs | [grill-with-docs](./grill-with-docs.md) |
| To find out whether an approach works in your codebase | [prototype](./prototype.md) |
| A plan too big to hold in one session | [wayfinder](./wayfinder.md) |

The line between `research` and `grill-with-docs` is the **shelf life of what comes back**. Research produces short-lived assets — what this library's auth mechanism does as of this week. An ADR records a decision you keep. If what you are producing is a decision rather than a fact, you are [grilling](https://www.aihero.dev/ai-coding-dictionary/grilling), not researching.

## Delegated legwork

Small lookups run directly and return in chat. Substantial reading can use one **background agent** when useful independent work remains in the main session and the user's delegation budget allows it. Source quality and a useful answer matter more than whether the reading ran in another context.

Delegation is at most one level deep. An already-delegated worker researches directly and must not invoke `research` again or spawn another worker.

When a durable note is warranted, its location follows the repo's existing notes convention. If there is none, the agent picks a sensible location and tells you where. The note is one file with citations, linked from the chat answer.

## Common questions

**It spawned a second research agent — is that meant to happen?**

No. Upstream [issue #530](https://github.com/mattpocock/skills/issues/530) documented recursive fan-out, including one run measured at roughly 450k [tokens](https://www.aihero.dev/ai-coding-dictionary/token). David Skills carries the instruction-level fix: an agent that is already a [subagent](https://www.aihero.dev/ai-coding-dictionary/subagent) must research directly and must not delegate again. If you still see more than one worker, stop the duplicate and report the harness and model so the guard can be tightened.

**Where should the file live — and should I commit it?**

Small lookups do not create one. For substantial or delegated work in a repo, follow its existing notes convention and your retention policy. Without a repo, use a host artifact when available or keep the complete cited report in chat. A dated file can preserve valuable evidence, but later work should recheck facts that may have changed. The skill does not require either committing or deleting it.

**What counts as a "high-trust" primary source, and who decides?**

The [model](https://www.aihero.dev/ai-coding-dictionary/model) judges which original owns the claim; there is no fixed domain allowlist. Connected originals, official docs, source code, specs, and first-party APIs can qualify. The safeguard is inspecting the source itself and citing what was actually read. Follow a couple of links: if they land on a summary of the thing rather than the thing, the run failed at its one job.

**Does a later session reuse what an earlier run found?**

Not automatically. A durable note becomes useful later when a human or another skill points at it: attach it to a spec, bring it into a grilling session, or link it from a [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket). A small lookup answered only in chat has no separate note to reload.

**Why not just ask the agent to go read the docs?**

You can. The skill adds primary-source discipline and makes a durable cited note when the work warrants one, with bounded background reading available when that separation earns its cost. A short direct answer can stay entirely in chat.

**When does it stop reading?**

There is no stopping criterion in the skill, and this shows up as two complaints that look opposite but are the same gap: agents that go far too deep, and agents that cover a topic broadly while missing the one specific detail that mattered. One practitioner put it as "deep-research skills are a bit too deep sometimes. And telling an agent to research usually results in missing crucial details." Scoping is on you. A narrow, answerable question — one API, one behaviour, one version claim — comes back far better than "research X".

**`/wayfinder` created research tickets — do I resolve those myself?**

Wayfinder can resolve ready research directly or through one bounded worker. Extra tickets remain pending rather than causing one worker per ticket. Findings are linked from their tickets; a separate branch is optional when isolation and Git authority justify it. Preserve linked evidence while the map still depends on it.

## It's working if

- Small lookups stay direct; substantial independent reading may use one background task.
- No research worker creates another research worker.
- The answer appears in chat with links to originals actually inspected, plus material uncertainty.
- Substantial or delegated work leaves one cited note in the repo when there is a repo, or a complete cited artifact or chat report when there is not.
- The cited answer or note lets you make the decision you were stuck on without reconstructing the research.

## Where it fits

A reach-for-it-anytime standalone: its findings can answer the request directly or inform [grilling](../productivity/grilling.md), [wayfinder](./wayfinder.md), or an autonomous [pursue-goal](./pursue-goal.md) run. For the whole map, see [advise](./advise.md).
