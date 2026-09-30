# Optional run timing

Use the user's agreed absolute deadline; convert a duration once at handoff and keep that endpoint
across context changes. Timed reporting is a separate agreement: milestones plus a maximum gap
(normally 45 minutes), destination, and a finite maximum of timed reports. For a deadline-bounded
run, propose the maximum as `ceil(run duration / report interval)` in the contract. Reporting-only
runs need an explicit maximum. Account policy still governs recurring AI calls.

## Managed-plugin helper

Resolve `hooks/run-timing.py` from the active plugin root, not a development checkout. The root
is three parents above this skill's directory. The helper uses Python's standard library and
POSIX file locks. Editable skill copies may lack it; use the host's clock and supported wait
instead, and state the unavailable hook coverage. Ordinary un-timed work needs no helper.

After worktree isolation, run the helper from the run's workspace:

```bash
python3 <plugin-root>/hooks/run-timing.py start --deadline <ISO-8601-with-timezone>
```

Session identity comes from `CODEX_THREAD_ID` or `CLAUDE_CODE_SESSION_ID`; when unavailable or
ambiguous, supply `--session` from the actual runtime. Never guess an ID or reuse another chat's.
The helper stores per-session state under `.reports/.run-timing/`; keep this runtime directory out
of Git in consuming projects using their existing local-ignore convention.

The `PostToolUse` hook supplies only `Time remaining: N minutes.`, normally at five-minute
spacing; `SessionStart` restores the current fact to a refreshed context. `--cue-seconds` changes
that spacing. The agent chooses its approach from the conversation; the hook adds no planning
advice and starts no model turn. It is advisory, not a process interrupt or native goal timer.

`status` reads the deadline and next report time. After delivering a milestone or scheduled
report, call `report` to reset only the reporting clock. `--report-seconds` defaults to 2700;
zero disables timed reports. Call `finish` after the end-of-run report to silence the timer.
These actions change only runtime timing state, never the native goal lifecycle.

## Waiting and reporting

For an exact job receipt, the helper can wait inside an OS process:

```bash
python3 <plugin-root>/hooks/run-timing.py wait --receipt <exact-job-receipt>
```

It returns at receipt availability, the report time, deadline, or timer closure. Receipt
availability is not a success verdict: inspect job identity, attempt, and exit status afterward.
`wait` without a receipt waits for the next reporting/deadline boundary. The process uses no AI
calls, scheduler, or persistent service. Retain the active run through a host-supported blocking
wait or verified callback; a yielded shell session or helper exit cannot wake an ended chat.

When a report is due during a long job, inspect its existing evidence once, report briefly even
if unchanged, reset the reporting clock, and continue waiting. This is an explicitly authorized
run report, not permission for additional job-status checks. Bound these wakeups by the contract's
maximum; do not create recurring automation or another agent to check the process.

Exact delivery during uninterrupted tool calls and stopping native goal continuations require
verified runtime support. Establish that path before promising a maximum gap or hard stop. If
the host cannot supply it, disclose the exact limitation rather than claiming hooks enforce it.

## Deadline

At the endpoint, end substantive work and deliver `/status-report`'s end-of-run report from
existing evidence, disclosing unfinished validation. Account
for exact running jobs; cancellation needs its own authority. Preserve their logs and receipts.
Use only the host's exposed lifecycle controls with explicit user authority. An agreed request
to pause the goal at the deadline can supply that authority where the host allows it. Otherwise
disclose the missing control; completion and blocking must never substitute for expiry.
