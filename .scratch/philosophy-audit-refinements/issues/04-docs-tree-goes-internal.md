# 04 — Docs tree goes internal

**What to build:** Every link in the docs tree resolves. Fork-added and renamed skills' docs
pages point their cross-links at repo-relative paths instead of `aihero.dev` URLs that don't
exist; the docs-writing conventions (`writing-docs.md`, the `CLAUDE.md` claim) describe the
internal convention this fork actually has, keeping the aihero.dev note only as the historical
origin of the page format. Links to Matt's genuinely published pages may stay where they refer to
his writing rather than to this fork's pages.

**Blocked by:** 01 — Record the decisions (implements the internal-only ruling ADR 0006 records).

**Status:** resolved

- [ ] A full-repo sweep finds no `aihero.dev/skills-` link targeting a renamed or fork-added skill
- [ ] Every docs-page cross-link touched resolves to a real file in the repo
- [ ] `writing-docs.md` and `CLAUDE.md` no longer describe a publishing pipeline the fork doesn't have
