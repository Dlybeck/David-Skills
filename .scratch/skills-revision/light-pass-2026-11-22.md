# Light pass, 2026-11-22 (Dev Plan sprint 0.3)

Status: ready-for-human

David-Skills is on the right track (Dev Plan decision 29), so this pass fixed only what was plainly
wrong or stale. Anything bigger is written down below with its reason and left for when David
circles back to the skills (decision 61), so the revision comes from the usage log, not feelings.

## Small fixes made (the complete list of behaviour changes)

1. **handoff** saved its file in the OS temporary folder, which is cleared and where nothing
   looks later. It now saves to `~/.local/state/handoffs/<project>/<date>-<topic>.md`, still
   outside the workspace, and gives the user the full path.
2. **`gh` in forks.** In a checkout with an `upstream` remote, plain `gh` resolved to the upstream
   repository (seen in David-Skills on 2026-11-02: a CI wait polled another repo's runs forever).
   The GitHub issue-tracker template said `gh` infers the repo automatically, which is wrong in a
   fork; it and the promotion-PR reference now say to pass `--repo` for `origin`. On this machine
   the David-Skills checkout itself still needs `gh repo set-default Dlybeck/David-Skills`, run by
   David: the agent's attempt was refused by its permission check.
3. **wait-what docs page** lacked the Common questions section every promoted docs page carries.
4. **Development profile.** Another agent's report sat in `docs/agents/david-development-profile.md`
   as David's own feedback. That line existed only on PR #10's branch and was taken out there.

The two pull requests that were open into `dev` also change behaviour, by David's decision on
2026-11-22:

5. **PR #10, run the gate once** (merged with changes). `implement`, `diagnosing-bugs` and
   `pursue-goal` treat a repo's delivery gate as the one full check and batch every known live
   failure before a step that needs David. Its pipeline checklist's speed test and time-budget
   table were made optional, and the profile line was removed.
6. **PR #9, reports reach David where he is** (merged as is). `pursue-goal` counts a report as
   delivered only when it reaches him through the channel he's on, not only its own chat.

Not a behaviour change: the usage log ([docs/agents/usage-log.md](../../docs/agents/usage-log.md))
adds a silent hook that only reads transcripts.

## Bigger changes for the revision (not made)

What the first month of use shows (2026-10-18 to 2026-11-22, 377 chats; explicit skill loads
only, so a skill followed without being loaded is not counted):

- **16 of the 34 promoted skills were never loaded:** attention-modes, codebase-design, delegate,
  diagnosing-bugs, grill-me, handoff, prototype, re-architect, resolving-merge-conflicts, tdd,
  to-questionnaire, to-spec, to-tickets, tool-fit, triage, wizard. Reason to look: a promoted
  skill nobody reaches for is weight on every chat's skill list and on `advise`. Some may be
  followed through references or just not needed yet; the log will tell over more use.
- **Use concentrates in a few skills:** independent-pr-review 46, autopilot 28, pursue-goal 26,
  wait-what 14, status-report 12. Reason: the revision should start where the work actually goes.
- **wait-what was typed 14 times.** Reason: each time David said a message didn't land. That is a
  measure of how often the agents' writing loses him, worth tracking down as a cause rather than
  patched per message.

Seen while reading the skills:

- **The autonomy skills overlap** (autopilot, yolopilot, pursue-goal, delegate, and ADRs 0005 and
  0009 to 0012), each with its own references, stand-in, timing and receipt rules. Reason: it's
  hard to tell which to pick, `advise` has to arbitrate, and it's the most rule-heavy part of the
  collection, against decision 8 (philosophy over rules).
- **Three names for grilling** (grill-me, grilling, grill-with-docs). Reason: one behaviour, three
  entry points.
- **handoff and in-progress/claude-handoff do nearly the same job.** Reason: the in-progress one
  looks like a leftover from before handoff was generalised.
- **advise, attention-modes and tool-fit are routers or meta skills.** Reason: `advise` reads more
  like a set of caveats than a map; attention-modes and tool-fit were never loaded.
- **The review loop over-checks.** The developer loop asks for a fresh full review after every
  fix; PR #10 went through six review rounds. Reason: it pulls against "avoid unnecessary
  delegation", and the log now counts reviews per piece of work, so the cost can be measured.
- **The documentation load is heavy for a private fork:** 34 docs pages, 13 ADRs, upstream-era
  history in FAQs (issue numbers, renames), a `mattpocock/skills` label column in the setup
  triage template, and `docs/agents/delegate.md` as the one skill-specific page in a config folder.
  Reason: simplification is David's main philosophy.
- **`require-committed-claim.py` runs under two matchers** (Bash, and Workflow|Agent). Reason: the
  kind of rule stacking to revisit.

From building the log:

- **Codex chats are not in the log.** None since 2026-10-12, and their files are compressed.
  Reason: the plugin is meant to work in both harnesses (decision 21); read them if Codex comes
  back into use.
- **Who sent a prompt is inferred.** Background and agent-started chats label every prompt as a
  person's; the log counts only David's own chats' prompts. Reason: if the step-in counts look
  wrong in use, a harness-owned label would be better than the inference.
