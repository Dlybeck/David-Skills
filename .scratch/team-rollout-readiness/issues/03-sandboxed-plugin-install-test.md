# Sandboxed plugin install test (shared machine, David's user only)

Type: task
Status: resolved
Blocked by: 01

## Question

Prove the Claude Code plugin route end-to-end **from GitHub** (not the local-path marketplace
David currently uses), inside an isolated environment that cannot touch other users of this
shared machine or David's real config:

- Isolate via a temp config dir (per ticket 01's findings on what Claude Code respects — e.g.
  `CLAUDE_CONFIG_DIR` — never the real `~/.claude`).
- `/plugin marketplace add DenaliAI-Automation/Denali-DEV` + `/plugin install denali-dev@denali-dev`
  against the private repo over whichever protocol ticket 01 says is reliable here (HTTPS
  preferred — SSH to GitHub is flaky on this box).
- Verify: skills load (`/denali-dev:...` visible), the plugin-root hook fires (a push/PR to
  `main` is blocked), `setup`'s local-tracker template present.
- Exercise the update path per ticket 01: bump nothing — just run the documented update flow
  and confirm what does/doesn't refresh, so the runbook states it from observation.
- Record the exact command sequence — it becomes the runbook's install section and the
  teammate instructions.

## Answer

Ran 2026-08-08 in an isolated `CLAUDE_CONFIG_DIR` sandbox (scratchpad, David's user only,
deleted after), `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` throughout — HTTPS clone worked first try,
SSH never touched.

**The documented flow fails against `main`, works against `#dev`:**
- `claude plugin marketplace add DenaliAI-Automation/Denali-DEV` clones the **default branch
  (`main`)**, whose manifest is still upstream's — it registers marketplace **`mattpocock`**,
  and `plugin install denali-dev@denali-dev` then fails ("not found"). The install story is
  broken for teammates until `dev` is promoted to `main`.
- `claude plugin marketplace add 'DenaliAI-Automation/Denali-DEV#dev'` registers marketplace
  `denali-dev` correctly; `claude plugin install denali-dev@denali-dev` succeeds → v1.5.0,
  user scope, enabled.

**Verified in the snapshot:** all 29 promoted skills, both hooks (PreToolUse + SessionStart)
in the component inventory (`claude plugin details denali-dev@denali-dev`), ~1,241 always-on
tokens. Hook *firing* is proven by the real install: the plugin-root hook blocked a
`git branch -D` in this very session. A live `-p` session test wasn't possible — the sandbox
has no Anthropic auth and copying real credentials around a shared machine was ruled out.

**Update flow, observed:** `claude plugin marketplace update denali-dev` refreshes the catalog
only (per ticket 01); `claude plugin update denali-dev` fails with "not found" — the
**qualified name is required**: `claude plugin update denali-dev@denali-dev` → "already at
the latest version (1.5.0)". Runbook must use the qualified form.

**Surprise:** the content snapshot is **29M, of which 27M is `node_modules`** — something in
the marketplace/install pipeline materializes dev dependencies into every user's cache.
Graduated to ticket 08.

**Runbook command sequence (post-promotion):**
```
export CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1   # this org's SSH is unreliable
claude plugin marketplace add DenaliAI-Automation/Denali-DEV
claude plugin install denali-dev@denali-dev
# updates later:
claude plugin marketplace update denali-dev && claude plugin update denali-dev@denali-dev
```
(Until promotion: add the marketplace as `'DenaliAI-Automation/Denali-DEV#dev'` instead.)
