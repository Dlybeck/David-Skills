Status: resolved

# `yolopilot`: `autopilot` minus the rigorous planning, for last-second hand-offs

## Problem Statement

the user sometimes needs to hand off a task at the last second — about to leave, no time for
`autopilot`'s careful pre-departure grilling — but still wants real, unattended progress rather
than either doing nothing or accepting the higher risk of an ungoverned, ungated background job.
`autopilot` itself requires a grilling round to lock a precise goal before it will background
itself, which is exactly the ceremony this situation doesn't have time for.

## Solution

A new user-invoked mode, **`yolopilot`**, that reuses `autopilot`'s entire mechanism (self-set
`/goal` via a `claude --bg` launch argument, the same working loop, the same Confidence
guideline) but skips the pre-departure grilling round entirely: it takes a loose, one-line
instruction, shows a short non-blocking warning naming the elevated risk, states its own
best-guess interpretation, then launches immediately with no wait for confirmation. The
Confidence guideline is inherited unchanged — no mechanical loosening — but naturally produces
more assumption-driven behavior since its anchor is the agent's own read of a loose instruction
rather than a jointly-grilled one. The one hard rule that earns this mode its own identity,
distinct from `autopilot`: it never merges into `dev` on its own. The `/goal` condition states
this explicitly — the task, on a feature branch, pushed, ready for review — and merging happens
only once the user reviews and approves, at which point the AI can perform the merge itself rather
than the user needing to run it by hand. Because there's no upfront-verified scope the way `autopilot`
has, git tracking is deliberately heavier here, not lighter: commits land more frequently and at
finer grain throughout the run, so the history itself is a self-documenting trail of what was
assumed and done at each step. Before stopping, it runs one more `/code-review` pass across the
whole branch — using its own stated interpretation as the stand-in for a spec, since no formal one
exists — and closes with a deliberately explanatory summary (why the key decisions were made, what
was assumed, what's riskiest) rather than a terse status line, recommending `/to-spec` be run
retroactively and offering `/teach` as an optional next step if the user wants to go deeper.

## User Stories

1. As a team member, I want to hand off a loose, last-second instruction and have real work start
   immediately, so that walking away doesn't mean nothing gets done just because I didn't have
   time for a careful grilling round.
2. As a team member, I want this mode to reuse `autopilot`'s exact mechanism (self-set `/goal` via
   `claude --bg`), so that a second, separately-maintained backgrounding approach doesn't have to
   be built and re-verified from scratch.
3. As a team member, I want a short, direct warning shown once, at the start, naming the elevated risk of
   skipping the grilling round, so that I have a clear, honest signal about what I'm actually
   getting before I walk away.
4. As a team member, I want that warning to never block or wait for a reply, so that "last second, need
   to leave" stays true rather than becoming another confirmation round.
5. As a team member, I want the agent to state its own best-guess interpretation of my instruction as it
   starts, so that there's a record of what it assumed even though I'm not there to correct it in
   the moment.
6. As a team member, I want the Confidence guideline to apply exactly as it does in `autopilot`, unchanged,
   so that the one proven safety mechanism this session has relied on all along isn't quietly
   weakened just because entering this mode is faster.
7. As a team member, I want it understood that more assumptions will naturally happen here than in
   `autopilot`, purely because the anchor is the agent's own reading rather than a jointly-grilled
   one — not because any guideline threshold was loosened.
8. As a team member, I want this mode to never merge into `dev` on its own, so that the one thing
   distinguishing it from `autopilot` is a real, meaningful safety property, not just a shorter
   setup step.
9. As a team member, I want the `/goal` condition to state that hard rule explicitly — landed on a feature
   branch, pushed, ready for review, never auto-merged — so that the rule lives somewhere the
   evaluator can actually check, not just in a pointer it can't resolve.
10. As a team member, I want to be able to approve the branch and have the AI perform the actual merge
    itself, so that approving doesn't mean I also have to go run git commands by hand.
11. As a team member, I want the rest of the working loop — the `/code-review` gate, `Strong`-only
    `/re-architect` idle-capacity work, the stopping logic — to carry over from `autopilot`
    unchanged, so that this mode isn't a lesser-quality version of the same work, just a
    faster-entry one.
12. As a team member, I want `main` to stay exactly as untouchable as it is everywhere else in this repo,
    so that no new mode ever gets to treat that boundary as negotiable.
13. As a future contributor reading this skill's `SKILL.md`, I want it to clearly name what's
    different from `autopilot` and what's inherited unchanged, so that the two don't read as
    unrelated designs that happen to share a mechanism.
14. As a team member, I want `CONTEXT.md`'s existing Confidence-guideline relationship (which already
    anticipated "a future unattended skill should too") to be fulfilled by this mode's entry, so
    that the glossary's own forward-looking note doesn't sit unfulfilled indefinitely.
15. As a team member, I want this mode's own docs page and registry entries to exist wherever
    `autopilot`'s and `delegate`'s do, so that it's discoverable the same way, not a hidden or
    half-shipped addition.
16. As a teammate on the AI Innovation team, I want the name `yolopilot` to do double duty —
    instantly clear about the risk being accepted, and instantly clear about its relationship to
    `autopilot` — so that the name itself teaches the design, the way `autopilot` and `delegate`
    already do.
17. As a team member, I want this spec's resulting ticket(s) to be real material `/delegate` can dispatch,
    so that testing one backlog item can also retire the other still-open gap from this session
    (delegate's own live dry run) rather than requiring a second, unrelated task later.
18. As a team member, I want `yolopilot`'s git history to be finer-grained and more frequently committed
    than `autopilot`'s, so that if its best-guess interpretation drifts, I can actually see where
    and recover cleanly rather than facing one big undifferentiated diff.
19. As a team member, I want one final `/code-review` pass across the whole branch before it stops, not
    just the per-unit passes already inherited from `autopilot`'s working loop, so that anything
    that fell between the cracks of individual reviews still gets caught.
20. As a team member, I want the closing message to explain its reasoning and key assumptions, not just
    list what got done, so that I can actually understand and trust the work before extending it.
21. As a team member, I want the closing message to recommend running `/to-spec` retroactively, so that
    work built without an upfront plan still gets a proper record afterward — the same move this
    session's own first spec already made for already-completed work.
22. As a team member, I want `/teach` offered as an optional next step, not a default one, so that going
    deeper on the domain is available without every run spinning up a full teaching workspace
    whether I want it or not.

## Implementation Decisions

- New user-invoked skill `yolopilot` at `skills/engineering/yolopilot/`, following the same
  `disable-model-invocation: true` / `agents/openai.yaml` pattern as every other user-invoked
  skill.
- Reuses `autopilot`'s exact backgrounding mechanism: `claude --bg --name "<name>" "/goal
  <condition>"` as the launch argument, with the condition stating the checkable essentials
  directly (the task interpretation, plus the hard git rule) rather than relying on a `SKILL.md`
  pointer alone — the same fix `autopilot`'s own combined dry run already proved necessary.
- No pre-departure grilling round. The skill's entry sequence: (1) show a short, 1-2 sentence,
  non-blocking warning naming the elevated risk and inviting an immediate objection; (2) state its
  own best-guess interpretation of the loose instruction; (3) launch immediately — no wait for a
  reply between any of these steps.
- Confidence guideline inherited unchanged from `autopilot` — anchored to the agent's own stated
  interpretation rather than a jointly-grilled one. No new mechanical threshold; the increase in
  assumption-driven behavior is a natural consequence of the looser anchor, not a designed
  loosening of the guideline itself.
- The one hard rule distinguishing this mode from `autopilot`: it completes its own git cycle up
  through a pushed, reviewable branch, but never merges into `dev` automatically. The `/goal`
  condition states this explicitly as part of the checkable condition text.
- Once the user reviews and approves the branch, the AI performs the actual merge (`--no-ff` into
  `dev`) itself in a follow-up action — approval is a human decision, not necessarily a
  human-run git command.
- The rest of the working loop is inherited unchanged from `autopilot`: the `/code-review` gate
  before considering any unit of work clean, `Strong`-only `/re-architect` idle-capacity handling,
  and the same stopping logic (goal met per the evaluator, or genuine stall).
- `main` remains covered unconditionally by the existing `hooks/block-dangerous-git.py`; this
  skill makes no changes to it.
- Registry integration follows the same shape as `autopilot`/`delegate`:
  `.claude-plugin/plugin.json`, both `README.md`s, `docs/engineering/yolopilot.md`, and an
  `ask-claude` entry noting this as a lighter-entry sibling to `/autopilot` in the "Running
  unattended" section.
- `CONTEXT.md` gains an entry for `yolopilot`, and its Relationships section's existing
  forward-looking note ("a future unattended skill should [answer to the Confidence guideline]
  too") is fulfilled by pointing to it.
- Commits land more frequently and at finer grain throughout the working loop than `autopilot`'s
  do — small, clearly-labeled commits at each step rather than batching toward the end — since
  there's no upfront-verified scope to lean on, and the git history itself needs to carry that
  audit trail instead.
- Before stopping, runs one additional `/code-review` pass across the whole branch (on top of the
  per-unit passes already inherited from `autopilot`'s working loop), passing its own stated
  best-guess interpretation as the stand-in for a spec, since no formal spec exists for this run.
- The closing message is deliberately more explanatory than `autopilot`'s terse status report: it
  states why key decisions were made the way they were, what was assumed, and what's riskiest
  about it — enough for the user to actually understand the work before trusting or extending it.
- The closing message recommends running `/to-spec` retroactively — the same move this session's
  own first spec (`plugin-cleanup-and-integrations`) made for already-completed work — so the
  yolo'd work gets a proper spec/ticket record after the fact instead of never getting one.
- The closing message also offers `/teach` as an optional next step, not a default recommendation
  — spinning up `/teach`'s full stateful workspace by default after every run would be
  disproportionate; it's there for when the user specifically wants to go deeper.

## Testing Decisions

- No automated test suite exists for this repo (prose/config, not application code) — same
  precedent as every prior spec this session.
- Structural: `claude plugin validate . --strict`.
- Scenario-based dry run: invoke `yolopilot` for real against a small, genuine task, confirming
  (a) the warning displays and doesn't block, (b) it states a reasonable interpretation, (c) it
  launches via the same `claude --bg` + `/goal` mechanism already proven for `autopilot`, (d) it
  completes a branch and push but does not merge into `dev`, (e) once approved, a follow-up merge
  (by the AI or by the user) lands it cleanly, (f) commits along the way are finer-grained than a
  typical `autopilot` run's, (g) a final whole-branch `/code-review` pass actually runs before it
  stops, (h) the closing message reads as genuinely explanatory rather than a terse status list,
  and recommends `/to-spec` while offering (not defaulting into) `/teach`.
- This spec's resulting ticket(s) are also the intended live test material for `/delegate`'s own
  still-outstanding dry run (a separately tracked gap from earlier this session) — `/delegate`,
  not `/implement`, should be the one dispatching them. If `/to-tickets` produces only a single
  ticket (matching the pattern every prior skill-build ticket this session has followed), that's
  accepted as a valid, if narrower, first test of `/delegate` — real parallel dispatch across
  independent tickets would need a second, separately-sourced ticket alongside it, decided at
  that point, not manufactured here.

## Out of Scope

- A mechanically different Confidence-guideline threshold — considered and explicitly rejected;
  only the interpretation anchor differs, not the guideline's own mechanics.
- Any change to `autopilot`'s own mechanism, working loop, or git-cycle rules — this is a sibling
  mode built on top of what already exists, not a revision to it.
- Manufacturing a second, unrelated ticket purely to guarantee `/delegate` gets a multi-ticket
  parallel-dispatch test — deferred to a real decision once the actual `/to-tickets` breakdown is
  known.
- Actually running `/teach` or `/to-spec` as part of the autonomous run itself — both are
  user-invoked and both stay genuine recommendations in the closing message, never something
  `yolopilot` triggers on the user's behalf.

## Further Notes

- This is the "third idea" parked early in this session's original two-idea grilling round, picked
  up now on its own terms rather than folded retroactively into that earlier design.
- Distinguishing this mode from `autopilot` in one line, for anyone who reads only this:
  `autopilot` earns unattended trust by grilling a precise goal before it starts; `yolopilot` skips
  that and earns the equivalent trust structurally instead, by never letting its own less-scoped
  judgment reach `dev` without a human decision first.
- The name went through one real revision during grilling: an earlier working name, `freehand`,
  was rejected on the grounds that it needed a metaphor decoded (drawing → no ruler → no rigid
  plan) rather than being instantly clear the way `autopilot`/`delegate` are. `yolopilot` replaced
  it specifically because it does two things at once — names the risk being accepted, and names
  the relationship to `autopilot` — the way a good name in this plugin is expected to.

## Comments
