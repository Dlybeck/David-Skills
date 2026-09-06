---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
---

If you are already running as a delegated, background, or subagent worker, do the research directly. Do not invoke `research` again and do not spawn another agent.

Otherwise, research directly for a small lookup or when there is no useful independent work to
continue locally. Use at most one **background agent** for substantial reading that can run
alongside other work, within the user's delegation budget. Tell that worker it is already
delegated and must not delegate again.

The researcher's job:

1. Investigate the question against **primary sources** — official docs, source code, specs, first-party APIs — not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.
