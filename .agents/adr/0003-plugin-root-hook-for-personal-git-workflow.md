# Plugin-root hooks enforce David's personal Git workflow

## Context

Prose rules were not enough to prevent two recurring mistakes: agents attempting destructive Git
operations, and agents pushing or opening pull requests directly against the human-gated
`main` branch.

## Decision

Ship the guardrails as plugin-root hooks under `hooks/`, so they apply wherever David enables
the plugin:

- `block-dangerous-git.py` blocks destructive commands and agent pushes or pull requests to
  `main`.
- `require-committed-claim.py` ensures local-markdown work is claimed in a committed state
  before delegate dispatch.
- `delegate-recommend.py` may recommend the delegate workflow for a matching router model.

Claude Code and Codex auto-discover `hooks/hooks.json` at the plugin root. Do not also declare the
same hooks file in either plugin manifest; doing both can load it twice. Codex requires the user
to review and trust plugin hooks before they run.

These are intentionally global personal defaults. A project that should not inherit them should
not enable the plugin wholesale; use skills.sh to install selected skills instead. A skills-only
copy deliberately carries no hooks.

Every hook change must add or update table-driven coverage in `hooks/test_hooks.py`.
