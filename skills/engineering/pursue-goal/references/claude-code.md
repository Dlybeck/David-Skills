# Claude Code goal adapter

Use Claude Code's background session plus a literal `/goal` launch argument. Launch one
self-contained background session with `claude --bg --name "<goal-slug>" "/goal <goal contract and
proof conditions>. Follow the pursue-goal process until a stopping boundary is reached."`.

Treat this as delegated continuation of the human-invoked pilot wrapper. The launch argument must
contain the whole contract; never depend on a path inside the David Skills development checkout
because an installed plugin may live elsewhere.

Claude's background mechanism supplies its own worktree. Confirm the background job's worktree and
branch in its first update, then apply the same isolation, authority, checkpoint, and receipt rules
as `/pursue-goal`. Do not create a second worktree around it.

Use `claude agents` or `claude logs` only for a human-requested status check. The background run
records meaningful progress itself and does not require an AI polling loop.
