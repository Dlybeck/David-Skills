## What it does

`advise` is the harness-neutral router over the skills in this repo. You describe the situation you are in — an idea you cannot start, a pile of incoming bug reports, a [session](https://www.aihero.dev/ai-coding-dictionary/session) that has run long — and it names the skill or the sequence of skills that fits, plus where the human decisions in that sequence sit.

It recommends and stops. It may read a relevant skill to verify its advice, but it does not grill, write a [spec](https://www.aihero.dev/ai-coding-dictionary/spec), or fire the skill it just named. You choose what to invoke. Its map covers this collection, not every skill you have installed.

## When to reach for it

You invoke this by typing `/advise` — the agent won't reach for it on its own.

| Your situation | What the router gives back |
| --- | --- |
| An idea, and no idea where to start | The next useful practice, based on what is already understood |
| Bugs and requests arriving from other people | The [triage](./triage.md) on-ramp, and why [tickets](https://www.aihero.dev/ai-coding-dictionary/ticket) you generated yourself don't belong on it |
| Two skills that look interchangeable | Their different outputs: [grill-me](../productivity/grill-me.md) for stateless discussion, [grill-with-docs](./grill-with-docs.md) for domain documentation, [wayfinder](./wayfinder.md) for a large unresolved decision map |
| A long session and a decision about the [context](https://www.aihero.dev/ai-coding-dictionary/context) | The ordered tree over the five options at a phase boundary |
| A large objective you want pursued autonomously | Whether [autopilot](./autopilot.md) can earn a confirmed contract or [yolopilot](./yolopilot.md) must start provisionally |
| Current progress is hard to place in the larger project | [status-report](../productivity/status-report.md), which connects verified work to milestones and long-term outcomes directly in chat, with useful visuals |
| Work is ready for review but not committed | [code-review](./code-review.md), including relevant staged, unstaged, and new files; the request or goal contract can supply its requirements |
| A skill you have already picked | Nothing useful. Invoke that skill directly. |

## Prerequisites

The router names skills; it does not install them. Everything it points at has to be installed for the recommendation to be actionable, and it only knows the promoted skills in this repo.

Tracker-dependent work needs a known tracker convention. Existing usable instructions count; [setup](./setup.md) can establish missing configuration. Standalone review, implementation from conversation, research, and other no-tracker work do not require setup.

## Optional compositions

The everyday menu covers understanding, pilot handoff, status, clarification, and teaching.
The supporting skills [to-spec](./to-spec.md), [to-tickets](./to-tickets.md),
[implement](./implement.md), and [handoff](../productivity/handoff.md) can also be selected by the
agent during authorized work. This router still recommends and stops; its role is plugin guidance,
not general product planning. Ordinary corrections steer an active pilot without another command.

The word **flow** means one possible composition, not a required sequence. You can start from settled context, skip artifacts that add no value, or revisit a decision. A selected skill still has its own discipline and genuine inputs. The map describes several useful compositions:

- **Build compositions:** understanding, optional requirements capture or decomposition, and tested
  implementation. A prototype can settle a question at any point; artifact choices depend on their
  usefulness rather than session count alone.
- **On-ramps**, for a situation that generates work and then merges onto the main flow: incoming bug reports, something broken, or an effort too foggy and too large to hold in one session.
- **Autonomous entrances**, where Autopilot or Yolopilot grants an adaptive goal engine different authority based on how the handoff was established.
- **Standalones**, off every flow, reached for on their own terms — the prototype, the questionnaire, the merge conflict you are already sitting in.
- **A vocabulary layer underneath**, the two references the other skills pull in when the words rather than the process are the problem.

## The phase boundary

The other idea it hands you is the **phase boundary**: a useful moment to decide whether to continue, compact, or hand off. Preserve settled requirements across that choice. A compact checkpoint or self-contained ticket can support a restart; neither a fresh session nor a particular context-size threshold is mandatory for every task.

| Option | Take it when |
| --- | --- |
| **Continue** | The next phase wants this one verbatim, or you have [smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone) left. It is the only move that keeps the session as a [primary source](https://www.aihero.dev/ai-coding-dictionary/primary-source), so rule it out first |
| **`/clear`** | Everything behind you is disposable. Cheapest move on the board, and one-way if you were wrong |
| **[handoff](../productivity/handoff.md)** | Something has to travel: a new [harness](https://www.aihero.dev/ai-coding-dictionary/harness), a new directory, a colleague, a side task forked mid-phase |
| **Subagent** | The task is scoped tightly enough to run with you [away from the keyboard](https://www.aihero.dev/ai-coding-dictionary/afk) |
| **`/compact`** | None of the above. The default, and it lands here often |

Two of those are routinely got wrong, which is why the router carries the order rather than the list. `/handoff` reads like the general bridge between windows and is not: portability is the whole of what it buys. `/compact` is the bottom of the tree rather than the first reach, because the four questions above it are each cheaper or more precise.

## Common questions

**Isn't there just a list of the skills in the right order?**

People keep asking for one in the README. This skill is that list — it is what it exists for. A static table would say `wayfinder → to-spec → to-tickets → implement → code-review` and be wrong for most situations, because the interesting parts are the branches — is there a codebase, does the build span sessions, can this question be settled by talking. The honest cost is that the router is hand-maintained and lags the repo. `/grilling` and `/resolving-merge-conflicts` both shipped long before the router named them.

**It told me half the skills aren't installed.**

Human-only skills may be absent from the model's implicit-invocation list even when installed. That list alone cannot prove a skill is missing. Check the active harness's installed plugin catalog and explicit skill picker before changing the installation; the plugin manifest describes what the package intends to ship.

**It described a skill's behaviour, and the skill doesn't do that.**

The hand-maintained map can drift. The router now reads the relevant skill before making a load-bearing claim about its behavior. If the map and the skill disagree, the skill is authoritative. Advice beyond the map, such as a [plan mode](https://www.aihero.dev/ai-coding-dictionary/agent-mode) recommendation, should be identified as an inference rather than presented as a prerequisite.

**Why is it prose instead of a numbered checklist?**

A fair complaint, filed as an open issue arguing that most of the routing is deterministic and the narrative makes it hard to scan. Nothing stops you asking for the compressed form — "just give me the sequence" gets you the sequence. What the prose is carrying is the conditional half: the branches, where a human decision is expected, and where to clear or compact between steps. A flat checklist drops exactly that.

**Can it route over my own skills, or another author's?**

No. Three separate proposals have asked for a router that reads your local `skills/` directory and recommends from whatever is installed. `advise` is not that. It is a map of one set, maintained by hand, and it knows nothing about skills you wrote or installed from elsewhere.

**It told me to edit a SKILL.md.**

That advice is often correct and rarely durable. Someone asked it how to make [implement](./implement.md) close tickets, got told to add a line to the skill, and immediately spotted the problem: `npx skills update` overwrites the file, and the plugin install is read-only. Put standing behaviour in your own `CLAUDE.md` or `AGENTS.md`, or say it in the invocation. Prompt-level adaptations survive updates — pointing the flow at Linear instead of GitHub, or asking it which open tickets could run in parallel, are both things people do this way.

**It named a skill I don't have, or missed one I do.**

Check the changelog for a rename before assuming it is gone. `writing-great-skills` became [writing-for-agents](../productivity/writing-for-agents.md) with no alias, `to-prd` became [to-spec](./to-spec.md), and `pathfinder` became [wayfinder](./wayfinder.md). Four skills were retired outright into the skills that absorbed them: `ubiquitous-language`, `design-an-interface`, `qa` and `request-refactor-plan`. The reverse case is the router's own lag, above.

## It's working if

- It ends by naming what to type and stops there, instead of starting the work itself.
- The route it gives back mentions where to clear or compact context and where you are expected to review, not just a list of skill names.
- Where two skills are close, it explains the trade-off and leaves the choice with you.
- Any claim it makes about another skill's behaviour shows up in the trace as it reading that skill's `SKILL.md`.
- You recognise your own situation in what it hands back, rather than the nearest generic scenario.

## Where it fits

`advise` is a **standalone router** that sits over the whole set. It is never a step in a chain; it points into every chain, and it is the node the other docs pages link back to so none of them has to redraw the graph. From here you most often land on [grill-with-docs](./grill-with-docs.md), the head of the interactive flow, or [autopilot](./autopilot.md), the trust-building entrance to autonomous work.

It is a [secondary source](https://www.aihero.dev/ai-coding-dictionary/secondary-source) over the skills it describes. Where the router and a `SKILL.md` disagree, the `SKILL.md` is right.
