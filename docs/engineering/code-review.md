## What it does

`code-review` reviews changes since a pinned baseline along two axes, including relevant uncommitted work when reviewing work in progress. **Standards** asks whether the code follows how this repo writes code. **Spec** asks whether the code does what the originating request, goal contract, issue, or [spec](https://www.aihero.dev/ai-coding-dictionary/spec) asked for. Each axis runs in its own [sub-agent](https://www.aihero.dev/ai-coding-dictionary/subagent) so neither sees the other's reasoning.

The two axes are never merged and never re-ranked. The report ends with a worst issue *per axis* and refuses to name a single winner across them, because a change can pass one axis and fail the other: code that follows every convention while implementing the wrong thing passes Standards and fails Spec; code that does exactly what the [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket) asked while breaking the repo's conventions does the reverse. A blended verdict lets the passing axis hide the failing one.

## When to reach for it

Type `/code-review`, or the agent reaches for it automatically when you ask to review a branch, a PR, work in progress, or anything "since X".

| Your situation | Reach for |
| --- | --- |
| A diff exists and you want to know if it is built right *and* is the right thing | `code-review` |
| You want bugs hunted in the diff — null paths, races, off-by-one | Claude Code's own built-in review, not this one (see the name clash below) |
| Nothing is written yet and you want it written test-first | [tdd](./tdd.md) |
| A whole spec needs building, review included | [implement](./implement.md), which calls this skill itself |
| The whole codebase has drifted, not one diff | [re-architect](./re-architect.md) |
| Something is broken and you do not know why | [diagnosing-bugs](./diagnosing-bugs.md) |

The baseline comes from you or the calling workflow; an uncommitted-only review uses `HEAD`.
It asks when the baseline remains ambiguous and validates it before spawning reviewers.
Committed-only reviews stay confined to their range; pre-commit and WIP reviews also cover
relevant staged, unstaged, and new files without pulling in unrelated edits.

## Prerequisites

The Standards axis needs nothing. It reads whatever the repo documents (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, and the like) and falls back on a built-in baseline when the repo documents nothing.

The Spec axis needs a requirements source, not necessarily a formal document. It looks in this order:

1. Your supplied spec, explicit request, or confirmed goal contract, including current corrections.
2. Issue references in the commit messages (`#123`, `Closes #45`, a GitLab `!67`), fetched through the configured tracker.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch or feature name.
4. Asking you.

Tracker lookup uses `docs/agents/issue-tracker.md` when available. A supplied request or document
does not require [setup](./setup.md). With no requirements source at all, the Spec sub-agent is
skipped and the report says "no spec available" rather than inventing requirements.

## The two axes

| | Standards | Spec |
| --- | --- | --- |
| Question | Is it built right? | Is it the right thing? |
| Reads | The repo's documented standards, plus the smell baseline | The originating request, goal contract, issue, or spec |
| Reports | Documented breaches (can be hard), and smells (always judgement calls) | Missing or partial requirements, scope creep, requirements implemented wrongly |
| Every finding cites | The standards file and the rule, or the named smell plus the hunk | The requirement in its source |

A generic review skill that does not know your standards is the thing this design is trying to avoid — it flags what is deliberate in your codebase and misses the invariants your codebase actually depends on. So the repo's own documentation is the [primary source](https://www.aihero.dev/ai-coding-dictionary/primary-source) on the Standards axis, and **the repo always overrides**.

The **smell baseline** is the floor underneath it: twelve Fowler code smells from _Refactoring_ ch.3 — Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest. Each is a labelled heuristic ("possible Feature Envy"), never a hard violation, and each is stated as *what it is* → *how to fix*, so a finding arrives with a move attached rather than a complaint. Anything your linter already enforces is skipped by both axes.

## Common questions

**It collides with Claude Code's own `/code-review`. What do I do?**

This is the most reported problem with the skill, and it is not fixed. Claude Code ships its own `/code-review`, which does something different — it hunts bugs in the diff, where this one checks spec compliance and repo standards. Installing this library means one of them wins, and which one wins depends on how you installed. Via the plugin marketplace, everything is aliased under a `david-skills:` prefix and the built-in becomes hard to reach at the unqualified name; via a plain skills install, the local file wins and this skill shadows the built-in. One clean answer is to remove Claude Code's built-in skills entirely: a large [context](https://www.aihero.dev/ai-coding-dictionary/context) saving, and the collision stops mattering. The shadowing itself is arguably a Claude Code [harness](https://www.aihero.dev/ai-coding-dictionary/harness) bug — a skill author should be free to name a skill anything — so the other answer is to rename the local copy. Editing the frontmatter or renaming the directory gets undone by `npx skills update`; the durable workaround reported by users is to fork the skill to a new name and drop `code-review` from the managed set, keeping a note of the commit you forked from so you can re-sync by hand.

**Its sub-agents keep invoking `/code-review` again and spawn more agents.**

That was an upstream bug reproduced in more than one harness, with one report reaching 50-plus agents. David Skills adds the same hard constraint to both reviewer briefs: the Standards and Spec workers are already the reviewers, must not invoke `code-review`, and must not spawn more agents. A normal run therefore creates at most those two first-level reviewers.

**Should I run it in the same [session](https://www.aihero.dev/ai-coding-dictionary/session) that wrote the code?**

Prefer a fresh one. As one reader put it: "Same context reviewing itself isn't review, it's confirmation bias with a slash command." The reviewing agent in the authoring session holds every assumption that shaped the code, which is exactly the context an independent reviewer would not have. This is also why people ask for [implement](./implement.md) without its built-in review step — it runs the review inside the session that just wrote the diff. Invoking `/code-review` yourself from a clean session is the honest version.

**After every ticket, or once at the end?**

Both work, and the skill does not decide for you. Per-ticket keeps each diff small enough that the Spec axis has one clear spec to check against, which is the mode `implement` uses. Batching to the end of a branch catches interactions between tickets that the per-ticket passes each miss. If you are unsure, review per ticket and run one final pass against the branch point.

**Can I trust the findings?**

Not without checking. Sub-agent output is a hypothesis, not evidence — one team reported a dozen breaking changes that prose-based reviews had waved through. The skill aggregates the two reports verbatim or lightly cleaned rather than re-verifying each claim against the files, so a finding can cite the wrong location or overstate an impact. Read the citation on each finding before acting on it. That every finding is required to carry one — a standards rule, a smell plus its hunk, or a spec line — is what makes this checkable at all.

**Why does it find new problems every single time I run it?**

Because fixes create new surface, and because the judgement-call half of the Standards axis is not deterministic between runs. One reader described the loop plainly: "/code-review and /improve-code-architecture always find new stuff every time. I implement fixes, rerun these skills, and again and again." There is no convergence guarantee. Treat a pass as a list of leads, act on the ones with a cited rule behind them, and stop — do not run it in a loop until it comes back clean, because it will not.

**Does it review my uncommitted work?**

Yes, for WIP and pre-commit reviews. It includes tracked edits in the index and working tree,
plus the contents of relevant untracked files. Both reviewers receive the same scope and evidence,
even if they run in isolated worktrees. It does not commit or stash your work to make it visible.
A committed-only PR review does not silently include local edits.

## It's working if

- It refuses a bad ref before dispatch and reports no changes only after checking every in-scope layer.
- New files and uncommitted changes appear in a WIP review; unrelated edits remain outside its scope.
- The report arrives as two separate blocks under `## Standards` and `## Spec`, not one merged list.
- Every Standards finding names either a rule in one of your repo's files or one of the twelve smells, with the hunk quoted; every Spec finding quotes the originating requirement.
- The closing summary gives a worst issue per axis and declines to pick an overall winner.
- With no spec available, the Spec block says so instead of listing requirements it inferred from the code.

## Where it fits

`code-review` is the review step at the tail of the build chain — `grill-with-docs → to-spec → to-tickets → implement → code-review` — and also stands alone on any branch or PR you point it at.

- [implement](./implement.md) is the closest neighbour: it drives the build and calls this skill as its own closing review before committing.
- [to-spec](./to-spec.md) and [to-tickets](./to-tickets.md) produce the document the Spec axis checks against; a vague spec makes that axis vague.
- [re-architect](./re-architect.md) is the whole-codebase counterpart — this skill only ever looks at one diff.

[advise](./advise.md) routes across the whole set when you are unsure which skill the situation wants.
