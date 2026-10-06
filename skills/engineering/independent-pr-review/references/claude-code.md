# Claude Code reviewer isolation

Read before dispatching an independent reviewer from a Claude Code developer context. Inspect the
exposed agent/session tool documentation and its context behavior before selecting a launch route.

Create a new isolated reviewer agent/session with an explicit brief containing only the pinned
repository, base/head, settled requirements/authority, source access, and this skill. Verify that
the selected route does not inherit the implementation transcript or earlier reviewer results;
a new tool invocation alone is not evidence of isolation. Do not resume an implementation agent
or reuse the preceding reviewer. Use supported host controls, without invented API names or flags.

When fresh context cannot be verified or dispatch is unavailable/outside budget, return the gate
unmet rather than relabel local self-review. Wait using the host's supported completion mechanism;
the developer retains the findings and owns subsequent repairs.
