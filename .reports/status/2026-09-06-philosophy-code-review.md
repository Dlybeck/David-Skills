# Philosophy and code review

As of 2026-09-06 01:11 UTC. Baseline: `v1.6.0` / `d8549ed`; reviewed local work on
`feature/status-report`, including new files. Changes remain uncommitted and unreleased.

The status-report addition fits the collection's small, composable-skill philosophy. Three
high-priority issues were found and corrected: two existing workflow defects and one report-path
integration problem. Source review and local validation are complete; live harness behavior and
long autonomous runs were not exercised.

## Bigger picture

| Project outcome | Immediate milestone | Current evidence | Remaining gap |
| --- | --- | --- | --- |
| Autonomous work stays understandable to a human reviewer | Evidence-backed status snapshots | New skill connects current work, milestones, and longer-term goals; chat + Markdown, optional webpage | Release and real-project use |
| Autonomy respects the user's authority | Safe delivery fallback | Autopilot keeps a review branch local without explicit push permission | Instruction-level review, not a live pilot exercise |
| Reviews cover what will actually ship | Pre-commit review coverage | Code-review now includes staged, unstaged, and relevant new files | No live end-to-end reviewer evaluation |

This is the baseline review snapshot, not a measured improvement against an earlier report.
The proposed pre-goal preparation redesign remains a separate, unimplemented proposal.

## Standards

- **P1, fixed — WIP omitted from review.** The old `git diff <base>...HEAD` excluded local
  changes even though implement invokes review before committing. The skill now pins the scope,
  checks tracked/index/untracked layers, and supplies both reviewers the same evidence, including
  snapshots for isolated worktrees. Docs and advise routing were synchronized.
- **P1, fixed — absent authority caused a push.** Autopilot's old fallback required a pushed
  branch whenever any delivery permission was missing. It now leaves work local unless the
  contract explicitly permits that push. The independent reviewer rechecked both P1 fixes.
- **P1, fixed — reports blocked worker dispatch.** The proposed `.scratch/status-reports/`
  default collided with the hook guarding uncommitted tracker state. A real-Git regression test
  reproduced this. The default is now `.reports/status/`, outside the tracker. The hook itself
  is unchanged; all `.scratch` claims, specs, maps, and even a feature named `status-reports`
  remain protected.
- **P2, deferred — delegate completion protocol.** Its instruction to watch ticket status lacks
  an explicit event-driven completion path and can invite repeated AI polling. Account policy
  still prohibits such polling. A follow-up should specify worker completion notifications and
  a single inspection at the returned commit, yielding when no callback exists.
- **P2, deferred — prototype promotion authority.** Its unconditional instruction to fold a
  validated decision into real code is too broad for exploratory-only requests. A follow-up
  should separate recording the answer from authorized production implementation.

Standards: three high-priority findings fixed; two lower-priority concerns remain.

## Spec

The independent intent review found no discrepancies in the status-report addition. It is
human- and model-reachable, connects immediate evidence to long-term outcomes, delivers a useful
chat summary and saved Markdown, and supports an explicitly requested webpage. It does not
require specs/tickets, mutate plans or goals, invent progress percentages, or start monitoring.
It handles stale evidence, missing roadmaps, and unchanged single-job checks explicitly.

Spec: zero findings; no outstanding high-priority issue within the reviewed scope.

## Philosophy

The design follows the repository's recorded philosophy in ADR 0004 and ADR 0009: one focused
reusable discipline, with optional presentation detail in a reference file. It adds observability
to autonomous work without creating another mandatory planning pipeline. Research progress can
be reduced uncertainty rather than shipped code. Plans describe intent; receipts establish
execution. Reporting does not become a second roadmap authority.

## Validation and limits

- `npm test`: passed with an isolated temporary Node 22 runtime; no machine-wide installation.
- Repository validator: 30 promoted skills, 37 total; manifests and version surfaces aligned.
- Hook suite: 113 checks passed, including seven added real-Git report/tracker checks.
- Pilot fixture validation: seven structural scenarios passed. These check scenario structure
  and instruction fragments, not actual autonomous agent performance.
- Version synchronization: three tests passed.
- `npm run test:release`: six hermetic tests passed; no real release or external branch writes.
- Skill quick validator: status-report and code-review passed. The generic validator rejects
  the existing Claude-specific `disable-model-invocation` key in autopilot; the repository's
  dual-harness validator accepts and checks this intentional metadata.
- Shell syntax and `git diff --check`: passed.
- Claude CLI unavailable, so `claude plugin validate . --strict` was not run.
- No webpage was requested for this review, built, or published. No live install/release check.

## Next

Agreed review and high-priority corrections are complete locally. Recommended next action is
human review, then the repository's feature-to-dev validation and human-approved main promotion.
Release machinery can consume the pending Changesets; this review did not commit, push, merge,
install, or change the installed plugin. The two P2 concerns are follow-ups, not implemented work.

## Evidence

- [Status-report skill](../../skills/productivity/status-report/SKILL.md) and
  [web reference](../../skills/productivity/status-report/references/web-report.md)
- [Code-review scope](../../skills/engineering/code-review/SKILL.md)
- [Autopilot delivery boundary](../../skills/engineering/autopilot/SKILL.md)
- [Report/tracker regression checks](../../hooks/test_hooks.py)
- [Unchanged tracker safeguard](../../hooks/require-committed-claim.py)
- [Delegate completion protocol](../../skills/engineering/delegate/SKILL.md)
- [Prototype capture rule](../../skills/engineering/prototype/SKILL.md)
- [Existing philosophy](../../.agents/adr/0004-analyze-existing-philosophy-before-adding-not-stacking.md)
  and [adaptive pilots](../../.agents/adr/0009-codex-first-adaptive-pilot-engine.md)
