# 01 — Record the decisions: ADR 0006, ADR notes, README framing

**What to build:** The identity call from the audit session exists on paper, citable by every
downstream ticket. A new ADR 0006 declares this plugin encodes Denali's in-house practice —
naming what that licenses (the `dev ← feature/**` integration assumption with `main` human-gated,
always-on plugin-root hooks, Denali-specific skills) and the rule that bounds it (an assumption
must be true in *every install of this plugin*, not just in this checkout — checkout-relative
paths, pointers to unshipped files, and dead URLs are lies, not assumptions). It also records the
new precedent that hooks carry executable tests. ADR 0003 gains a dated update covering the third
hook (`delegate-recommend.py`: informational-only, fail-silent, previously undocumented). ADR
0005 gains a dated note recording autopilot's fenced bypass of `re-architect`'s human-gated steps
as deliberate (`Strong`-scored candidates only, everything else logged) — behavior unchanged, now
on the record. The README's framing updated to match the in-house identity, with the Credit
section untouched.

**Blocked by:** None — can start immediately.

**Status:** resolved

- [ ] ADR 0006 exists, states the in-house ruling, the every-install rule, and the hook-test precedent
- [ ] ADR 0003 has a dated update naming `delegate-recommend.py`; original decision text untouched
- [ ] ADR 0005 has a dated note recording the fenced `re-architect` bypass; original decision text untouched
- [ ] README framing no longer claims portability the unattended tier doesn't deliver; Credit section byte-identical
