# 01 — `/implement` marks its ticket resolved

**What to build:** `/implement`'s process gains a closing step: immediately after `/code-review`
and commit, it marks the ticket it just built `Status: resolved` (local tracker) or closes the
corresponding issue (a real tracker) — so a ticket's completion is visible in the tracker itself,
without a human updating it by hand afterward.

**Blocked by:** None — can start immediately.

**Status:** resolved

- [x] `/implement`'s `SKILL.md` documents the closing step, placed after `/code-review` and commit
- [x] Running `/implement` against an existing `ready-for-agent` local-tracker ticket flips its
      `Status:` line to `resolved` once the work is committed
- [x] The real-tracker path (closing the issue) is documented alongside the local-tracker path
- [x] No other part of `/implement`'s existing process changes

## Comments

- 2026-08-07 — `/code-review` (Standards axis) caught two stale references to `/implement`'s old
  five-beat description in `ask-claude/SKILL.md` and `skills/engineering/README.md` (the
  top-level `README.md` had the same staleness, caught by inspection) — fixed in the same commit.
  The Spec axis caught that this very ticket hadn't actually been flipped to `resolved` yet,
  despite the mechanism being fully documented — the dogfooding step you're reading right now.
