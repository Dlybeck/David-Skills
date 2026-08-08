# 01 — Clean up fork identity and stale branches

**What to build:** `README.md`, `CONTEXT.md`, and `.agents/install-block.md` describe this fork
(`denali-dev`) rather than Matt Pocock's personal repo — voice, install instructions, and title
all consistent with actually being Denali's own fork — while crediting Matt clearly and
generously (his repo linked, his site linked, this fork's `upstream` tracking relationship
stated). `origin`'s branch list on GitHub shows only branches that are this fork's own work.

**Blocked by:** None — can start immediately

**Status:** resolved

- [x] `README.md`'s opening pitch, install-command blocks, and picture/badge/newsletter CTA
      replaced with a description of this fork; a dedicated `## Credit` section added
- [x] `CONTEXT.md`'s title changed from "Matt Pocock Skills" to name this fork; its glossary
      body left untouched (unrelated content)
- [x] `.agents/install-block.md` rewritten so this fork's own single-plugin marketplace is the
      documented primary install route; Matt's official marketplace listing explicitly demoted
      to "not the install story"
- [x] `.agents/adr/0002` given a dated update note (not a rewrite) distinguishing which parts of
      its original text describe Matt's upstream shipping mechanics vs. this fork's actual one
- [x] All 86 `origin` branches other than `main`/`dev` verified byte-identical to their
      `upstream` counterpart, then deleted; `upstream` remote retained as the read-only path
      back to any of it
- [x] `claude plugin validate . --strict` passes after every change

## Comments
