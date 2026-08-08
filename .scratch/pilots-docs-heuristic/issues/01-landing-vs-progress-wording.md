# 01 — Pilots' docs: the landing-vs-progress decision heuristic

**What to build:** `autopilot`'s and `yolopilot`'s docs pages answer "which one do I reach for?"
with the sharper heuristic settled in the 2026-08-08 design discussion, instead of only the
time-pressure framing: reach for **autopilot when the landing matters before you return**
(tomorrow's work depends on the merge, or the goal is subtle enough that a misread wastes the
whole run — the grilling is cheap insurance); reach for **yolopilot when you want progress and
reviewing a branch later is fine** (the cost of a misread is a discarded branch). Also worth a
line: the 2×2 that makes the pair coherent — merge rights are earned by the grilling, and the
best-guess-goal-plus-unattended-merge corner is deliberately impossible. Docs pages only;
neither SKILL.md changes. Re-sync `ask-claude`'s "Running unattended" section if its wording
would otherwise contradict the pages.

**Blocked by:** None — can start immediately.

**Status:** ready-for-agent

- [ ] Both docs pages carry the heuristic in their "When to reach for it" section
- [ ] No SKILL.md edits; `ask-claude` stays consistent with the pages
- [ ] `claude plugin validate . --strict` passes
