# 01 — Design session: delegate runs over a wayfinder map's frontier

**What to build:** A decision, not code — run `/grill-with-docs` on composing `delegate` with
`wayfinder`: a delegate run over a wayfinder map's frontier would dispatch the AFK-able ticket
types (`research`, `prototype`) to worker subagents while `grilling` tickets surface to the
present human — potentially resolving a foggy map much faster with every decision still
human-made. The tracker vocabulary already supports it ("find the frontier" is deliberately
wayfinder-agnostic, and typed tickets exist). The session should settle: whether worker output
on a decision ticket (an `## Answer` + map update) fits the Router's never-judge constraint,
what the worker brief looks like for a research vs prototype ticket, and whether this is a
`delegate` extension, a `wayfinder` extension, or just documentation of a composition that
already works. Outcome lands as an ADR or a spec, per what the grilling finds.

**Blocked by:** None — but it needs David in the room; it's a grilling session, not agent work.

**Status:** ready-for-human

- [ ] A grilling session ran and its outcome is recorded (ADR, spec, or a documented "works as-is")
