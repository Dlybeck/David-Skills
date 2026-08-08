# This plugin encodes Denali's in-house practice — and an assumption must hold in every install, not just this checkout

A full audit of this fork against upstream (`mattpocock/skills`, 2026-08-08) surfaced one
question underneath most of its findings: is this repo a portable skills collection with a
Denali layer on top, or Denali's in-house practice that happens to be forked from one? The
README leaned toward the first; the unattended tier (`autopilot`, `yolopilot`) and the
plugin-root hooks quietly assumed the second. Every portability finding in the audit was a
symptom of that unmade decision.

## Decision

**In-house practice.** This plugin encodes how Denali's AI team works. That licenses, without
apology or generalization:

- Assuming the house branch model — `main ← dev ← feature/**`, with `main` human-gated — in
  skill bodies, launch instructions, and hooks. A repo without a `dev` integration branch is
  outside this plugin's audience, and the skills say so as a stated prerequisite rather than
  supporting it.
- Always-on plugin-root hooks (ADR 0003) enforcing house rules in every repo the plugin is
  enabled in. Opt-in-per-repo guardrails are upstream's model, deliberately not ours: our two
  hard rules exist because prose enforcement failed for real.
- Denali-specific skills (`soc2`) and integrations with no meaning outside the org.

What it does **not** license: assumptions that are false even *inside* Denali the moment the
plugin is installed normally. The rule that bounds everything: **an assumption must hold in
every install of this plugin** — installed from the plugin marketplace into any Denali repo —
not just in this development checkout. Concretely, at decision time, three standing violations
(all found by the audit; the spec that produced this ADR tickets their fixes):

- A launch argument that references a path inside this repo's checkout (`skills/engineering/…`)
  — resolves nowhere but here; instructions must travel as content.
- A skill body pointing at a `.scratch/` tracker file — `.scratch/` is dev noise for this repo,
  never shipped; guidance a skill needs must live in material every install carries.
- Docs links to `aihero.dev/skills-<name>` pages that don't exist for renamed or fork-added
  skills — the docs tree is internal; links point at repo files.

House assumptions get *declared* (a prerequisite line, a docs-page note); install lies get
*fixed*. That's the whole test for every future addition: "is this true in every install?" —
if yes and Denali-specific, state it; if no, it's a bug regardless of identity.

## Precedent riding along: hooks carry executable tests

The hooks are the mechanical backstop for rules that already failed as prose (ADR 0003). A
mechanical rule deserves a mechanical check: every hook lands with table-driven cases in the
hooks' test file, exercised at the hook's real contract — JSON on stdin, allow/block via exit
code, fail-open on malformed input — stdlib only, no framework. The first such file is
ticketed with the quoting-bypass fix in the same spec as this ADR; hooks added later add cases
to it.

## What this changes about the upstream relationship: nothing

Upstream remains the methodology source, merged regularly (`git fetch upstream && git merge
upstream/main`), and upstream-owned skill bodies stay untouched — the audit's headline finding
(shared-skill surface byte-identical at the core, no gate or STOP rule weakened) is a property
this decision explicitly preserves. In-house identity is about what *our additions* may assume,
not a license to fork the methodology itself.
