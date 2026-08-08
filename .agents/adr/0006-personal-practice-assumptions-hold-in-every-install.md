# This plugin encodes David's personal practice — and an assumption must hold in every install

An audit of this fork against upstream (`mattpocock/skills`, 2026-08-08) surfaced one question
underneath most of its findings: is this a fully portable skills collection, or David's personal
working practice built on a portable upstream? The README leaned toward the first; the unattended
tier (`autopilot`, `yolopilot`) and plugin-root hooks assumed the second.

## Decision

**Personal practice.** This plugin encodes how David works. That permits clearly stated
assumptions such as:

- The branch model `main ← dev ← feature/**`, with `main` human-gated.
- Always-on plugin-root hooks (ADR 0003) enforcing the two rules that prose alone failed to
  protect.
- Personal defaults for issue tracking, triage, and documentation.

It does not permit assumptions that are true only in this development checkout. The bounding
rule is: **an assumption must hold in every install of this plugin**, not just here. Examples of
violations include:

- A launch argument referencing a path inside this repository.
- A skill body depending on a `.scratch/` file that is not part of an installed skill.
- A docs link targeting a page that does not exist.
- A skill depending on a separate private work plugin.

Personal workflow assumptions are declared as prerequisites; installation lies and unavailable
dependencies are fixed or removed.

## Hooks carry executable tests

The hooks mechanically enforce rules that previously failed as prose (ADR 0003). Each hook
therefore carries table-driven cases in `hooks/test_hooks.py`, exercised at the hook's real
contract: JSON on stdin, allow/block through exit code, and fail-open behavior for malformed
input. The tests use only the Python standard library.

## Upstream relationship

Upstream remains the methodology source and is merged regularly with
`git fetch upstream && git merge upstream/main`. Upstream-owned skill bodies remain as close to
their source as practical. Personal identity governs this fork's additions and operational
defaults; it is not a reason to weaken the methodology.
