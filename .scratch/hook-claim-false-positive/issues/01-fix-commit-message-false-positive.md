# 01 — require-committed-claim: stop matching prose in commit messages

**What to build:** The `require-committed-claim` hook blocks on actual uncommitted ticket
claims, never on words. During the philosophy-audit-refinements run (2026-08-08, recorded in
that spec's closing comment) it blocked a worker's commit because the commit *message* contained
the literal string `claude --bg` — the heuristic matched text it should never have looked at.
Fix test-first: add a failing case to the hooks' test file (a payload whose command is a commit
whose message mentions the trigger words but whose working tree has no unclaimed ticket, which
must pass), then fix the heuristic so it inspects state, not prose. All existing cases stay
green.

**Blocked by:** None — can start immediately.

**Status:** ready-for-agent

- [ ] New test case: commit with trigger words only in its message, no uncommitted claim → allowed
- [ ] The real protection is untouched: an actually-uncommitted claim before a dispatch still blocks
- [ ] Full hook test suite green via plain `python3`
