# Codex goal adapter

Use Codex's native goal capability for durable continuation. Inspect the current goal first. Reuse
it only when it is the same objective; never replace an unfinished, unrelated goal implicitly.

Create one goal whose objective embeds the complete goal contract and instructs the run to follow
`/pursue-goal`. Keep the goal stable while plans and loops evolve. Mark it complete only after all
proof conditions and the authorized delivery target pass. Report an authority boundary or evidence
plateau through the goal mechanism only as its current tool contract permits.

Goal continuation does not create Git isolation. Establish or reuse the linked worktree described
by `/pursue-goal` before the first mutation, and include its absolute path in the goal objective so
every continuation operates in the same checkout.

Treat incoming human messages as steering of the current run, not implicit requests to replace
the goal. Use only goal controls actually exposed by this host. When a correction cannot be
written into native goal metadata, keep the updated contract in the existing checkpoint, identify
the stale metadata, and reconcile both at each continuation.

Before an unattended dependency, inspect this host's tools for a permitted blocking wait or
non-AI completion callback that resumes this run. Prefer an interruptible wait so human steering
remains available. Where exposed, a dedicated sleep tool can keep the current run pending without
recurring model calls; use its actual duration and interruption contract. A shell `sleep` command
is insufficient if the shell tool yields early and leaves only a background process.

Verify the selected mechanism with a short task and a subsequent agent action. Keep exact
process/session identity and receipts. That proves the short lifecycle only; record any untested
long-duration, timeout, or interruption behavior without treating it as proven failure. CLI
subprocess exit or app-server events alone do not prove that an ended chat resumes.

Use goal continuations for meaningful work, not status polling.
For an explicitly timed run, use [run timing](timing.md); the helper's clock and wait process
do not pause or complete the native goal. Verify the permitted deadline lifecycle control and
report-time continuation separately from process completion before promising exact timing.
Use the verified mechanism within current host wait limits. Do useful independent work when
available, without interfering with the running experiment. Never replace a native wait with
recurring goal turns, model status calls, or a polling agent. Keep the goal active while a
dependency runs; do not mark it blocked to suppress continuation turns or require a user restart
merely because the wait is long. Missing callbacks do not prevent a supported blocking wait.

If neither mechanism can preserve or resume the run under host instructions, state the exact
missing capability or binding restriction and preserve the next action. Disclose that unattended
continuation remains unmet; never invent a pause API or misuse goal completion/blocking to end a
wait. An account-policy amendment needs explicit user approval; plugin instructions cannot
supply it.
