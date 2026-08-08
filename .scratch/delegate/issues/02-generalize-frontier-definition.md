# 02 — Generalize the `Frontier` definition in `docs/agents/issue-tracker.md`

**What to build:** The existing `Frontier` bullet (open, unblocked, unclaimed tickets under
`.scratch/<feature>/issues/`) currently sits under a "Wayfinding operations" heading as if it only
applies to a `wayfinder` map. It doesn't — the same scan applies identically to a plain
`/to-tickets` ticket set. Move it out from under that heading, or add a line making clear it isn't
wayfinder-exclusive, so a future skill (starting with `delegate`, ticket 03) can point at this one
definition instead of re-deriving the same scan logic under a different name.

**Blocked by:** None — can start immediately.

**Status:** resolved

- [x] The `Frontier` definition reads correctly for both a `wayfinder` map and a plain
      `/to-tickets` ticket set
- [x] `wayfinder`'s own `SKILL.md` still reads correctly against the updated doc — no broken
      cross-reference or duplicated definition
- [x] The wording is generic enough that `delegate` can cite it directly in ticket 03

## Comments

- 2026-08-07 — `/code-review` (Spec axis) caught a real bug in the first pass: the generalized
  definition asserted "unclaimed" as a universal criterion, but `claimed` is a wayfinder-only
  concept — plain `/to-tickets` tickets carry no claim status at all. Fixed by splitting the
  general convention (open + unblocked only, true for both) from wayfinder's own additional
  filter (drops `claimed`/assigned tickets), documented separately in "Wayfinding operations."
  This also surfaced a real gap for `delegate/03`: there is currently no claim mechanism for plain
  tickets, which its parallel dispatch will need — noted on that ticket rather than invented here.
  `/code-review` (Standards axis) separately caught that `to-tickets/SKILL.md`'s own inline
  frontier line wasn't wired to the new shared convention — fixed in the same pass.
- 2026-08-07 — Ticket 03 closed the claim gap this ticket flagged: added a general "claim the
  ticket" convention (mirroring `wayfinder`'s own claim step exactly) to `docs/agents/issue-
  tracker.md` and both seed templates. "Find the frontier" now includes "unclaimed" as a
  universal criterion again, since it's actually true this time.
