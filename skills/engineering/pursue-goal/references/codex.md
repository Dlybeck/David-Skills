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

Use goal continuations for meaningful work, not status polling. Long-running external processes
must write their own log and receipt; return control until the user resumes the goal after that
receipt should exist.
