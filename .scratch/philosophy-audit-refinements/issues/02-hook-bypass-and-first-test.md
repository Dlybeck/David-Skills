# 02 — Close the hook quoting bypass, add the first executable test

**What to build:** The `main` guard can no longer be sidestepped by re-quoting: `git push origin
"main"` (and other quoted or equivalent spellings, for both the push and PR patterns) is blocked
exactly like the unquoted form, while feature-branch pushes and near-miss lookalikes such as
`feature/main-page` still pass. The fix is proven by the repo's first executable test: a Python
standard-library-only test file (no framework, no new dependencies — the hooks' own discipline)
that drives the hook as a subprocess through its existing contract — JSON on stdin, allow/block
via exit code — over a table of cases, including malformed stdin failing open (exit 0, silent).
Runnable directly with `python3`.

**Blocked by:** None — can start immediately.

**Status:** resolved

- [ ] Quoted spellings of push-to-main and PR-to-main block, for both patterns
- [ ] Feature-branch pushes and `feature/main-page`-style lookalikes pass; the four destructive-op patterns still block, their safe lookalikes still pass
- [ ] Malformed stdin exits 0 silently (fail-open contract covered by a test case)
- [ ] Test file runs green via plain `python3`, stdlib only, exercising the subprocess seam — never internals
