# 05 — Writing pass: single source of truth, negation/justification, mechanical sweep

**What to build:** The fork-added skills read like upstream wrote them, per the repo's own
`writing-for-agents` discipline. The Confidence guideline has exactly one full definition (in
`CONTEXT.md`); every other mention is a pointer plus at most a one-clause gloss. The
worktree-from-last-commit fact is owned by the tracker doc convention; the local seed template
keeps the generic git truth without naming any harness mechanism. `delegate` and `yolopilot`
prohibitions are rephrased positively wherever a positive phrasing exists — the true hard
guardrails (Router never decomposes/judges/rescues; yolopilot never merges into `dev` unattended)
stay, paired with their positive counterpart. In-body design justification is cut where an ADR or
changeset already carries it, moved into a dated ADR note where it isn't. Mechanical sweep rides
along: `delegate`'s in-skill Common-questions section deleted (its docs page owns the material),
`soc2` docs H1 recased to match siblings, the engineering bucket README's stray blank line
removed, and `autopilot`/`yolopilot` frontmatter descriptions trimmed toward one line with the
trimmed string propagated everywhere it's pasted.

**Blocked by:** 03 — Unattended tier declares assumptions; 04 — Docs tree goes internal. (File
contention, not logic: this pass edits the same skill bodies as 03 and the same docs pages as 04.)

**Status:** resolved

- [ ] Grep sweep: exactly one full Confidence-guideline definition repo-wide; all other mentions are pointers
- [ ] Grep sweep: no harness-mechanism names in seed templates; no Common-questions heading inside any SKILL.md
- [ ] Prohibitions in fork-added skills are either positively phrased or genuine hard guardrails paired with the positive target
- [ ] No in-body design-justification prose that duplicates an existing ADR/changeset; new rationale landed as dated ADR notes
- [ ] Frontmatter descriptions trimmed and identical in every surface that pastes them
