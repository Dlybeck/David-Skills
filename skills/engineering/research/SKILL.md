---
name: research
description: Investigate a question against high-trust primary sources and present cited findings, saving a durable note when the work needs one. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
---

If you are already running as a delegated, background, or subagent worker, do the research directly. Do not invoke `research` again and do not spawn another agent.

Otherwise, research directly for a small lookup or when there is no useful independent work to
continue locally. Use at most one **background agent** for substantial reading that can run
alongside other work, within the user's delegation budget. Tell that worker it is already
delegated and must not delegate again.

The researcher's job:

1. Run `/tool-fit` for source access. Investigate against **primary sources** — user-provided or connected originals, official docs, source code, specs, first-party APIs — rather than a secondary write-up. For current external facts, search when needed and open the actual source. Follow every material claim back to what was inspected.
2. Present the answer in chat with source links and any material uncertainty. A small lookup needs no extra file. For substantial research, delegated reading, requested documentation, or work that must survive a session, save one cited Markdown note in the repo's existing notes location when there is a repo. Otherwise use an available host artifact or a self-contained chat report. Link the durable output when the host supports it and say where it lives.
