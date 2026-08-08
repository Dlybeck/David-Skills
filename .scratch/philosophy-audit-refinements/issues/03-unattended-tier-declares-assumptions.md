# 03 — Autopilot/yolopilot: declare the `dev` assumption, drop the checkout paths

**What to build:** An unattended run launched from a plugin install resolves everything it
references. Both `autopilot` and `yolopilot` state the `dev`-integration-branch assumption as an
explicit prerequisite (in the skill and on its docs page), citing ADR 0006's ruling rather than
leaving the assumption implicit in a launch string. The `claude --bg` launch argument is rebuilt
to carry the goal condition and guardrails inline as content, so nothing depends on where the
skill physically lives. The run's Out of Scope guidance moves out of the `.scratch/` spec pointer
into material every install ships.

**Blocked by:** 01 — Record the decisions (this ticket cites ADR 0006's declared assumption).

**Status:** resolved

- [ ] Both skills and both docs pages state the `dev` prerequisite plainly, before any launch step
- [ ] The launch argument contains no repo-relative path; goal and guardrails travel as content
- [ ] No skill body points at a `.scratch/` file; the Out of Scope guidance ships with the skill
- [ ] `claude plugin validate . --strict` passes; a grep sweep finds no checkout-relative launch paths
