# Productivity

General workflow tools, not code-specific.

## User-invoked

Reachable only when you type them (Claude Code: `disable-model-invocation: true`; Codex: `policy.allow_implicit_invocation: false` in `agents/openai.yaml`).

- **[grill-me](./grill-me/SKILL.md)** — Get relentlessly interviewed about a plan or design until every branch of the design tree is resolved.
- **[teach](./teach/SKILL.md)** — Teach the user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.
- **[to-questionnaire](./to-questionnaire/SKILL.md)** — Turn a decision you can't answer alone into a Markdown questionnaire for the one person who can — filled in async, or together over a meeting.
- **[wait-what](./wait-what/SKILL.md)** — Fire this the moment a message doesn't land. The agent re-pitches it with the context you're missing, in plain English, using your `CONTEXT.md` vocabulary.

## Model-invoked

- **[handoff](./handoff/SKILL.md)** — Export portable context for an actual authorized transfer without abandoning active work.

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[attention-modes](./attention-modes/SKILL.md)** — Adapt questions and handoffs to Focused or On the side attention, including brief or dictated replies.
- **[tool-fit](./tool-fit/SKILL.md)** — Choose useful host tools for sources, visuals, previews, and artifacts without tying the workflow to one AI app.
- **[grilling](./grilling/SKILL.md)** — Resolve material decisions through focused interview rounds, reusing settled context.
- **[writing-for-agents](./writing-for-agents/SKILL.md)** — Writing documents for agents: skills, AGENTS.md/CLAUDE.md, and any doc an agent reaches by a pointer.
- **[status-report](./status-report/SKILL.md)** — Connect verified progress to long-term project goals directly in chat with useful visuals; export a document or webpage on request.
