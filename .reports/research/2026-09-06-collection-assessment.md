# David Skills collection coherence assessment

As of 2026-09-06; pre-fix snapshot `f887ac9a63bdab4f824fa0f4d246147e7de1d950`, `feature/status-report`. Read-only assessment of all 30 promoted skill bodies, their 30 human docs pages, and 30 `agents/openai.yaml` files, plus relevant composition references. This report is the only artifact authored by this reviewer. Later corrections do not retroactively change these observations.

## Verdict

Retain the collection and its selectable practices. The [primary-source philosophy research](./2026-09-06-skills-philosophy.md) supports **user-owned composition, not a universal mandatory pipeline**; selected practices can still have demanding internal contracts. Most skills have distinct, useful purposes. The substantive defects are concentrated in routing, authority handoffs, and stale documentation, not evidence that the collection needs replacing with a framework.

`autopilot` and `yolopilot` already select adaptive loops through `pursue-goal`; specs/tickets are conditional there. A new `prepare-goal` architecture remains a proposal, not existing behavior or a requirement of this assessment. Testing should assess useful outcomes and boundaries at different entry points, not demand any fixed sequence.

## Consequential findings

1. **P1 — Merge resolution can sweep unrelated work into a commit.** `skills/engineering/resolving-merge-conflicts/SKILL.md:14` says “Stage everything and commit.” An interrupted merge may coexist with unrelated edits or an already-populated index. Resolve and stage only intended merge/rebase changes; inspect staged contents and preserve unrelated work before completing. Test a real conflict with an unrelated dirty file.

2. **P1 — Diagnosis silently includes implementation.** `skills/engineering/diagnosing-bugs/SKILL.md:3` activates on plain broken/failing/slow reports; `:114-138` requires fixing and a completion commit/PR narrative, with no diagnosis-only exit. A user asking why something failed has not necessarily requested a fix. Preserve reproduction discipline for genuinely hard bugs, narrow automatic activation, and distinguish diagnosis authority from repair authority. Test a diagnosis-only request and a simple already-explained failure.

3. **P1 — Wayfinder can authorize itself through its own Notes.** `skills/engineering/wayfinder/SKILL.md:13` allows execution via map Notes, while `:111-114` has the agent create those Notes. `docs/engineering/wayfinder.md:69` explicitly describes this failure. Require a human-authorized execution exception; an agent-authored map is evidence of planning, not a grant of authority. Test resuming a map whose Notes assert permission absent from the actual request.

4. **P1 — Prototype completion exceeds a decision-only request.** `skills/engineering/prototype/SKILL.md:26` unconditionally folds validated decisions into production code and commits a branch with an implementation-issue pointer. This breaks standalone exploratory use without an issue and can turn “show alternatives” into implementation. Capture the answer and evidence; integrate production only within actual authorization. Apply the same boundary to `LOGIC.md:63` and `UI.md:99` close-out guidance.

5. **P2 — Router adds dependencies the skills do not require.** `skills/engineering/advise/SKILL.md:17,88,101` prefers documented grilling merely because a directory exists and imposes setup before engineering. In contrast, `implement:17`, `code-review:13-14`, and `domain-modeling:40` explicitly support standalone/no-tracker use. `setup:3` repeats the universal prerequisite. Recommend based on missing inputs and desired artifacts; a working directory does not make stateless conversation inferior. `to-spec:9`, `to-tickets:11`, `triage:43`, and `wayfinder:25` say “run /setup,” although `.agents/invocation.md:8` prohibits skills invoking human-only skills. Suggest that the human invoke setup only when necessary; accept existing conventions without requiring its provenance.

6. **P2 — TDD reopens a human gate inside autonomous delivery.** `pursue-goal:48-50` may select TDD, but `tdd:22-24` requires human-confirmed seams before any test. The pilot contract does not require seam agreement. Preserve the discipline while recognizing already-agreed seams and explicitly delegated seam selection; clarify consequential uncertainty instead of always asking again. Independently test interactive TDD and delegated autonomous delivery.

7. **P2 — Human docs contradict the fork and route readers upstream.** `docs/engineering/implement.md:58,66` says batch dispatch does not exist and WIP review remains broken, despite `delegate` and the current `code-review`. `docs/engineering/diagnosing-bugs.md:71` says redaction is unimplemented despite its skill's `:12-16`. `docs/engineering/re-architect.md:84` claims a hard-coded Claude Agent call that the current skill no longer contains. Numerous sibling links point to AIHero instead of this fork's pages, violating repo docs conventions and exposing users to different behavior. Localize known sibling links and correct demonstrably stale operational claims, retaining clearly labeled historical evidence rather than rewriting history.

8. **P2 — Cost behavior deserves explicit tests.** `grilling:20` delegates every factual lookup, `research:8` always spawns a worker, and `delegate:78` watches ticket status without a completion-event rule. The first two can inflate tiny tasks; the third conflicts with account-wide no-AI-polling policy if interpreted as repeated checks. Preserve worthwhile isolation and parallelism, but verify bounded delegation and event-driven continuation. Do not infer that every optional parallel practice should be removed.

## Complete promoted coverage

Paths below use `E = skills/engineering`, `P = skills/productivity`; each `name:line` identifies its `SKILL.md`. H means human-only, M means model/user reachable. All inspected YAML invocation policies agree with frontmatter; this proves metadata consistency, not live picker behavior. Each row also covers the same-named `docs/<bucket>/<name>.md`.

| Skill | Independent purpose and genuine inputs | Assessment |
| --- | --- | --- |
| E/advise (H) | Recommend a relevant practice from the user's situation | Correct F5/F7; maps are advice, not admission gates (`:11-26`). |
| E/autopilot (H) | Establish authority and delegate an outcome | Retain understanding-first contract (`:13-46`); test F6 and proportional questioning. |
| E/code-review (M) | Review a pinned change against standards and intent | Retain two independent axes; request/goal suffices without tracker (`:13-53`). |
| E/codebase-design (M) | Shared vocabulary for an existing design question | Retain focused reference (`:8-12`); alternatives optional, not a redesign trigger. |
| E/delegate (H) | Dispatch ready independent tickets | Tracker/claim/config are genuine inputs (`:28-62`); test F8. |
| E/diagnosing-bugs (M) | Determine cause from reproducible failure | Fix F2 and stale docs; retain evidence-first hard-bug discipline (`:18-66`). |
| E/domain-modeling (M) | Resolve terminology and durable decisions | Retain lazy glossary and three-condition ADR bar (`:40,66-74`); no mandatory setup. |
| E/grill-with-docs (H) | Interview while recording domain decisions | Genuine grilling/domain-modeling composition (`:7`); optional paperwork choice. |
| E/implement (H) | Build already-decided work | Conversation, spec, or ticket acceptable (`:7-17`); clarify opening and F7 docs. |
| E/prototype (M) | Answer one design question with runnable evidence | Retain two artifact branches (`:12-17`); fix F4 close-out. |
| E/pursue-goal (M) | Adapt execution within explicit outcome/authority | Retain optional artifacts and evidence checkpoints (`:48-72`); fix F6 seam interaction. |
| E/re-architect (H) | Survey architectural friction, then discuss selection | Genuine candidate/user-choice boundary (`:60-71`); F7 docs and offline HTML remain risks. |
| E/research (M) | Answer a question from cited primary sources | Retain source/artifact discipline (`:10-14`); test proportionality F8. |
| E/resolving-merge-conflicts (M) | Resolve interrupted operation by intent | In-progress conflict is genuine input (`:6-12`); fix F1. |
| E/setup (H) | Record tracker, labels, and domain conventions | Configuration choice is useful (`:9-15`); narrow false universal prerequisite F5. |
| E/tdd (M) | Build behavior via red-green slices at public seams | Retain anti-tautology/vertical slicing (`:28-38`); repair F6 delegated boundary. |
| E/to-spec (H) | Synthesize known decisions into tracker artifact | Existing conversation and destination needed (`:7-19`), not a required prior grill; F5. |
| E/to-tickets (H) | Decompose agreed work into verifiable slices | Explicitly accepts conversation (`:9,17`); breakdown approval genuine; F5. |
| E/triage (H) | Evaluate incoming issues and apply directed outcome | Tracker and maintainer decisions genuine (`:70-90`); fix setup reachability F5. |
| E/wayfinder (H) | Map unresolved decisions across sessions | Retain sparse map, revisitability, and no-fog exit (`:84-116`); fix F3/F5. |
| E/wizard (M) | Build human-operated procedure script | Known stages, destinations, confirmation genuine (`:18-43`); retain no self-execution. |
| E/yolopilot (H) | Begin provisionally, refine within narrower authority | Retain shared engine and digest (`:18-30,43-54`); explicit user restrictions override defaults. |
| P/grill-me (H) | Stateless interview anywhere | Retain minimal wrapper (`:7`); router must not deny repo use. |
| P/grilling (M) | Stress-test a human decision tree | Preserve human decisions and confirmation (`:6-22`); test bounded scope and F8. |
| P/handoff (H) | Portable continuity for another agent | Existing conversation; pointers avoid duplicated state (`:8-16`); disclose temp lifetime. |
| P/status-report (M) | Relate verified progress to larger outcomes | No spec/ticket prerequisite (`:13-35`); retain snapshot and reporting-only authority (`:81-84`). |
| P/teach (H) | Accumulate mission-grounded learning | Dedicated learning workspace and sources (`:10-30`); not default postflight ceremony. |
| P/to-questionnaire (H) | Draft questions for someone holding missing knowledge | Recipient and desired answer are genuine inputs (`:9-15`); reuse supplied answers. |
| P/wait-what (H) | Repair understanding in the current conversation | Retain tiny interruption primitive (`:7`); missing glossary is not a gate. |
| P/writing-for-agents (M) | Shape agent-readable instructions | Retain reference, pruning and behavioral no-op test; no workflow prerequisite. |

## Limits and next evidence

This is source-level assessment, not a claim that all 30 skills were behaviorally executed. Root review owns hooks, executable templates, installed-plugin loading, technical regressions, and bounded behavioral trials. Existing primary evidence supports targeted corrections; broader simplification should depend on observed failures. No recommendation here requires adding a new entry-point skill, changing human/model invocation classes wholesale, or deleting useful skills.
