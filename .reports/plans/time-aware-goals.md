# Time-aware goals

## Contract

Add optional user-chosen deadlines and milestone/maximum-gap reports to the existing goal
engine. Timing context contains only time remaining, normally at five-minute spacing during
existing tool activity. The agent chooses its approach from the conversation. Reporting defaults
to chat with evidence-led visuals; unchanged progress gets a brief report. A milestone report
resets the 45-minute maximum gap. Deadline expiry ends substantive work with an honest report,
not a success claim. Preserve the prohibition on recurring AI job-status polling.
Do not use the test suite casually: select checks for changed behavior and risk, preserve passing
evidence, and run required full checks before delivery.

Implementation was local on `codex/time-aware-goals`, based on `7657c57`. The owner's subsequent
request authorizes committing and pushing to `dev`, with installation investigated separately.
Promotion to `main` remains the owner's release action. No hosting or account-instruction changes
are part of this feature.

## Plan

1. Build and test a session-scoped timing helper and silent-by-default hook through their real
   CLI/stdin interfaces. Cover spacing, independent sessions, restart, expiry, and report reset.
2. Add an OS-managed wait that returns on an identified receipt, report time, or deadline;
   verify that it does not make model calls or create a scheduler/service.
3. Integrate the small contract changes into both pilots, the engine, reports, adapters, router,
   human docs, and ADRs. Document event-boundary limits and actual lifecycle requirements.
4. Run repository validation and whole-change Standards/Spec review. Run at most two bounded
   native behavioral trials (120 seconds each) in disposable projects, with receipts and no
   user-configuration writes. A short trial does not prove a 45-minute or overnight lifecycle.

## Evidence

Local implementation and functional verification are complete. The owner authorized delivery to
`dev` after these checks; production installation and release remain separate delivery states.

| Area | Result |
| --- | --- |
| Minimal clock | Opt-in per-session helper; hook output is only remaining time, normally five minutes apart at existing tool boundaries. Native delivery verified below. |
| Reporting | Existing status-report skill handles milestones, the agreed maximum gap, brief unchanged progress, and the deadline report. Milestones reset the report clock, not the deadline. |
| Usage safety | OS-managed waiting contains no model calls. It does not create a service or wake an ended chat. |
| Testing discipline | Implement and pursue-goal say “Do not use the test suite casually”; preserve relevant passing evidence and complete required checks within the work period. |
| Repository checks | Required `npm test` passed, including 173 hook-contract checks, repository/catalog validation, pilot scenarios, version sync, and evaluator tests. Claude Code is unavailable, so its native validation remains unverified. |
| Whole-change review | Standards review found no actionable issues. Spec review caught validation starting after deadline expiry; fixed to report existing evidence and unfinished checks. |
| Native functional smoke checks | Passed in isolated Codex state: time cue delivery, report boundary, packaged hooks, report reset, deadline expiry, end-of-run report, and timer closure. |

## Earlier native trials

Two short disposable development trials passed independent correctness checks (five normalization
cases and 341 sequence cases); each invoked tests once. The timed trial emitted no native hook
cues, so this is **not** evidence of timing-driven speed, cost, report cadence, or deadline
compliance. Both trials used the new testing guidance; they are not an evaluation of its effect
against the previous guidance either.

The baseline CLI unexpectedly persisted a temporary project-trust entry despite ignoring user
configuration. Only that exact entry was removed, restoring the original account-config hash.
Subsequent checks isolated CLI state and left account configuration unchanged. Original receipts:

- `/tmp/david-timing-baseline-5x518qf3/receipt.json`
- `/tmp/david-timing-timed-4wp9jcsl/receipt.json`
- `/tmp/david-hook-delivery-p8kt5zlt/receipt.json`

A bounded hook-delivery probe also supplied no cue. Read-only, non-inference runtime inspection
confirmed hook discovery and matching session identity, but did not establish delivery. The owner
identified the investigation as drift, then clarified the acceptance criterion: verify hooks and
overall functionality; leave practical speed and cost assessment to personal use.

## Functional verification

The minimal check used isolated user-level hook configuration with an invocation recorder rather
than the earlier project-local trial setup. It recorded four native invocations: inactive
SessionStart was silent, both active PostToolUse events emitted only `Time remaining: 1 minutes.`,
and PostToolUse after timer closure was silent. The agent reported the exact cue and `report_due`
wait reason. Receipt: `/tmp/david-functional-hooks-n4gw1z7b/receipt.json`.

The packaged check installed a snapshot of the candidate through the local marketplace into
disposable Codex state. Its installed helper and hooks.json matched source byte-for-byte. The
native packaged hook updated its cue timestamp and emitted expiry; the report reset preserved
the fixed deadline; OS waiting returned at the report and deadline boundaries; the agent delivered
both reports and finished the timer. Receipt: `/tmp/david-packaged-hooks-4y6pgzvm/receipt.json`.
Both checks completed successfully and left account configuration unchanged. They used vetted
temporary hook definitions with invocation-scoped hook-trust bypass, not persisted account trust.
No production plugin installation or release occurred.

## Reevaluation and remaining boundary

Keep this as a small extension of existing workflows: no new skill, site, scheduler, or clock
coaching. The hook is advisory; the agent interprets the time fact. The policy, helper, and packaged
Codex hook path are functionally verified. Long-duration native goal continuation and hard process
interruption are not established by these checks; exact lifecycle support retains its documented
boundary. Claude Code native validation is unavailable on this host. Practical usefulness will be
assessed by the owner in use. No speed/cost experiment is required. Installation and release remain
separate from this local implementation.
