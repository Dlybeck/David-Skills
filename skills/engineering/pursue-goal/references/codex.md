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

Before an unattended dependency, establish whether this host provides a permitted interruptible
wait or non-AI completion callback that actually resumes this run. Test a short task through
completion and a subsequent agent action; CLI subprocess exit or app-server process events alone
do not prove that an existing chat resumes. Keep exact process/session identity and receipts.

Use goal continuations for meaningful work, not status polling.
Use the verified mechanism within current host wait limits. Do useful independent work when
available, without interfering with the running experiment. Never replace a native wait with
recurring goal turns, model status calls, or a polling agent. If the host or account policy
requires returning control and no completion callback is available, state the missing capability
and preserve the next action. Do not claim unattended continuation is supported in that case.
An account-policy amendment needs explicit user approval; plugin instructions cannot supply it.
