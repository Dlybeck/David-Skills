# Engineering

Skills I use daily for code work.

## User-invoked

Reachable only when you type them (Claude Code: `disable-model-invocation: true`; Codex: `policy.allow_implicit_invocation: false` in `agents/openai.yaml`).

- **[advise](./advise/SKILL.md)** — Ask which skill or flow fits your situation. A router over the user-invoked skills in this repo.
- **[grill-with-docs](./grill-with-docs/SKILL.md)** — Grilling session that also builds your project's domain model, sharpening terminology and updating `CONTEXT.md` and ADRs inline.
- **[triage](./triage/SKILL.md)** — Move issues through a state machine of triage roles.
- **[re-architect](./re-architect/SKILL.md)** — Scan a codebase for deepening opportunities, present a visual review in chat or a useful page, then grill through whichever one you pick.
- **[setup](./setup/SKILL.md)** — Configure tracker, labels, and domain docs when selected skills need missing project conventions.
- **[delegate](./delegate/SKILL.md)** — Dispatch ready tickets whole to worker subagents until the frontier is drained.
- **[autopilot](./autopilot/SKILL.md)** — Enter unattended work mode — lock a goal before you leave, then keep working without you until it's met.
- **[yolopilot](./yolopilot/SKILL.md)** — Skip the grilling round for a last-second handoff, then work unattended within existing authority and repository integration policy.
- **[wayfinder](./wayfinder/SKILL.md)** — Plan a huge chunk of work — more than one agent session can hold — as a shared map of decision tickets on the issue tracker, resolved one at a time until the way to the destination is clear.

## Model-invoked

- **[to-spec](./to-spec/SKILL.md)** — Synthesize settled requirements into a proportionate spec; publish only with authority.
- **[to-tickets](./to-tickets/SKILL.md)** — Decompose understood work into verifiable tracer-bullet tickets with blocking edges when useful.
- **[implement](./implement/SKILL.md)** — Build understood work from a conversation, goal, spec, or tickets with tests and whole-change review.

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[prototype](./prototype/SKILL.md)** — Build a throwaway prototype to answer a design question: a single shareable HTML file for state/logic, or several toggleable UI variations.
- **[diagnosing-bugs](./diagnosing-bugs/SKILL.md)** — Disciplined diagnosis loop for hard bugs and performance regressions: build a feedback loop that goes red on this bug → minimise → hypothesise → instrument → fix → regression-test.
- **[research](./research/SKILL.md)** — Investigate primary sources and present cited findings; save a durable note when useful.
- **[tdd](./tdd/SKILL.md)** — Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time.
- **[domain-modeling](./domain-modeling/SKILL.md)** — Actively build and sharpen a project's domain model — challenge terms, stress-test with scenarios, update `CONTEXT.md` and ADRs inline.
- **[codebase-design](./codebase-design/SKILL.md)** — Shared discipline and vocabulary for designing deep modules: small interfaces, clean seams, testable through the interface.
- **[code-review](./code-review/SKILL.md)** — Two-axis review of the diff since a fixed point: **Standards** (does it follow the repo's coding standards, plus a Fowler smell baseline?) and **Spec** (does it faithfully implement the originating issue/spec?), run as parallel sub-agents.
- **[independent-pr-review](./independent-pr-review/SKILL.md)** — Fresh actionable defect review of an exact committed head and full base diff, with an authorized developer repair/re-review loop and quiet clean results.
- **[resolving-merge-conflicts](./resolving-merge-conflicts/SKILL.md)** — Work through an in-progress git merge or rebase conflict hunk by hunk, resolving by intent traced to each side's primary source, then finish the operation — never `--abort`.
- **[wizard](./wizard/SKILL.md)** — Generate an interactive bash wizard that walks a human through steps only they can perform: provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover.
- **[pursue-goal](./pursue-goal/SKILL.md)** — Drive an authorized long-horizon objective through adaptive research, discovery, delivery, and optimization loops until the evidence reaches a real stopping boundary.
