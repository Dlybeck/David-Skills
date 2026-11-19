---
"david-skills": minor
---

Agents test less and ship in batches. `implement`, `diagnosing-bugs`, and `pursue-goal` now treat
a repo's local delivery gate (a release script or check target) as the one full check: targeted
tests while working, the gate once, and no raw-suite run before it or rerun after it. Before a fix
that needs a deploy or other human step, the agent reproduces every known live failure and fixes
them in one change, saying up front how many such steps it will ask for. A new `implement`
reference, pipeline checks, covers building pipelines: check the host's build tool, build only
the shipped stage with an explicit target, name one authoritative check, test the speed contract,
and write down the time budget. A new opt-in eval case, `gate-once`, checks the gate runs once.
