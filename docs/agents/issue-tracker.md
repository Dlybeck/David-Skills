# Issue tracker: Local Markdown

Issues and specs for this repo live as markdown files in `.scratch/`. Chosen deliberately over
GitHub Issues (2026-08-07) to keep day-to-day dev noise — rename debates, WIP thoughts, small
tracked decisions — out of the org repo's Issues tab entirely. These files are ordinary repo
files: commit them like anything else — and do it right away, not batched up for later. A write
that only exists in this checkout's working tree is invisible to anything that doesn't share it: a
`claude --bg` job and a `Workflow` agent's own worktree are both created from the last **commit**,
never from another checkout's uncommitted state. Confirmed the hard way — a claimed, then
resolved, ticket sat fully untracked through its entire lifecycle once; its dispatched worker's own
worktree never saw it at all. Push, too, if whatever you're handing off to won't share this
checkout at all (a genuinely separate clone or session, not just a worktree of it).

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The spec is `.scratch/<feature-slug>/spec.md`
- Implementation issues are one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` — never a single combined tickets file
- Triage state is recorded as a `Status:` line near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<feature-slug>/` (creating the directory if needed), then commit
it. An uncommitted ticket doesn't exist as far as anything dispatched into a separate worktree or
session is concerned — there's nothing there yet for it to read.

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

## When a skill says "claim the ticket"

Set the ticket's `Status:` line to `claimed`, save, and commit that change — the session's first
action, before any work, so a concurrent session dispatching in parallel skips it. Committing is
not optional: an uncommitted claim is invisible to anything that doesn't share this exact working
tree, including a `claude --bg` job or a `Workflow` agent's own worktree, both of which start from
the last commit regardless of how recent the uncommitted change is. An open ticket with no
**committed** `Status: claimed` is unclaimed.

## When a skill says "mark the ticket resolved"

Set the ticket's `Status:` line to `resolved`, save, and commit that change, for the same reason
committing the claim matters — the record needs to survive and be visible outside whichever
worktree happened to write it. This is a plain completion marker — it confirms the work was
committed, not that every acceptance criterion was independently re-verified. Leave the `- [ ]`
boxes as the implementer left them; ticking them is a separate, human judgement call.

## When a skill says "find the frontier"

Scan `.scratch/<feature-slug>/issues/` for ticket files that are open, unblocked (every ticket
listed in the file's `Blocked by:` line is `resolved`), and unclaimed (no `Status: claimed`);
first by number wins. This is the same scan whether the ticket set came from `/to-tickets` or is a
`wayfinder` map's children — nothing about it is wayfinder-exclusive.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a file with one **child** file per ticket.

- **Map**: `.scratch/<effort>/map.md` — the Notes / Decisions-so-far / Fog body.
- **Child ticket**: `.scratch/<effort>/issues/NN-<slug>.md`, numbered from `01`, with the question in the body. A `Type:` line records the ticket type (`research`/`prototype`/`grilling`/`task`); a `Status:` line records `claimed`/`resolved`.
- **Blocking**: a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is `resolved`.
- **Frontier**: the general "find the frontier" scan above — nothing wayfinder-specific about it.
- **Claim**: the general "claim the ticket" convention above.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: resolved`, then append a context pointer (gist + link) to the map's Decisions-so-far in `map.md`, then commit both files together.
