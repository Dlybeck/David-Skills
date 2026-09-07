# Personal autonomy: first-pass conversation research

As of September 7, 2026. Plugin source inspected at `19c526e`. Research only: these are
findings and proposed tests, not new standing instructions, permissions, or implemented changes.

## Scope and method

Use David's own corrections as evidence of desired behavior, then compare those observations
with current skill instructions and documented host capabilities. Memory summaries supplied
navigation hints; the findings below were checked against original user messages or the current
conversation. Assistant explanations are not treated as David's preferences.

The advertised cross-chat listing tool returned an unavailable-tool error. A read-only metadata
pass over saved local Codex sessions found 19 candidate top-level records with relevant project
paths. Selected original messages were examined from Forge, Portfolio, two Arr tasks, and the
Mobile architecture discussion, alongside this David Skills conversation. This is a purposive
sample, not an exhaustive account-history review or a statistical estimate of failure frequency.
Some archived records had no matching user response items under the extraction used.

ScribblePocket is represented through the Forge/Mobile discussions, not a separately discovered
Pocket task. Arr/arr-mcp is treated as the likely RSuite reference; that naming is an inference.
Separate ChatGPT conversation history was not available. Official product documentation informs
capability claims, not claims about what happened in private ChatGPT conversations.

Only short, relevant excerpts and source pointers are retained here. Raw transcripts, pasted
terminal logs, account details, and authentication material are not copied into the repository.

## What the feedback actually supports

| Signal | Original evidence | Design implication and scope |
| --- | --- | --- |
| Autonomy means meaningful outcomes, not occupying time | Forge: an overnight proposal seemed like 15 minutes of work; later, a 20-minute run fixing one word was challenged as negligible. [F1] | Check that a proposed goal is substantial relative to the intended handoff, and judge progress against the real outcome. Do not require long runtimes or dismiss useful negative research results. |
| Questions belong where they unblock consequential decisions | Portfolio: finish independent work before returning with missing-image blockers. Later: ask while David is available, then work autonomously. [P1] | Reuse existing answers, distinguish decisions from agent-findable facts, and batch non-urgent blockers after safe independent work. This is not permission to cross an actual authority boundary. |
| The human goal can be short while the agent's working context is rich | Portfolio: “two to three sentences with a clear direction and clear endpoint, not specifics.” [P2] | Present a compact objective; recover constraints and acceptance evidence from authoritative context. Let the agent choose implementation details inside that scope. |
| Low ceremony does not mean poor documentation | Forge: “lets make sure we keep doucmenting”; requests to preserve a good restart point. This thread also criticized declining documentation during pilot runs. [F2, D1] | Keep one useful continuity record and evidence links. Chat-first presentation and durable working notes serve different purposes. |
| Quiet waiting must not become abandonment | Forge repeatedly objects both to many status messages and to stopping a goal while a job runs; Arr independently objects to costly polling. [F3, A1] | Treat execution, waiting, resumption, and notification as separate runtime concerns. Require a real supported continuation mechanism, not promises that an ended turn will return by itself. |
| Reviewer time is scarce | Arr: a week of setup attempts followed by another failed multi-stage wizard; Forge asks to stay out of routine labeling/approval work. [A1, A2, F4] | Validate agent-testable portions before owner handoff; keep unavoidable human actions small and resumable. Broad trust expressed in one task is not standing permission elsewhere. |
| Criticism is welcome, product substitution is not | Portfolio welcomes criticism and pushback, but rejects redesigning a personal exploratory site into a resume. Forge invites harsh feedback while restating its contextual mobile-OCR vision. [P3, F5] | Critique decisions against the user's intended product. Do not silently replace distinctive requirements with a generic best-practice target. |
| Some corrections must stay project-specific | Portfolio explicitly says its physical-believability review belongs only in that project and reiterates that theming must preserve navigation. [P2] | Preserve project-specific invariants and review criteria locally. Generalize the need to consult them, not the visual rules themselves. |
| Reports should reduce reconstruction work | This thread requests useful in-chat visuals, not file-first reports or icon-only tables. [D1] | The recent status-report correction fits the evidence; keep plain answers for small checks and retain explicit export options. |

These signals are strongest where they recur across projects or are repeated explicitly. A single
project-scoping instruction can still be decisive within that project. Quoted approvals are
historical evidence of interaction preferences, never authority for this research task.

## Where the current plugin fits, and where evidence suggests gaps

- **Already aligned:** `status-report` is chat-first; `grilling` reuses settled context;
  `pursue-goal` keeps an adaptive plan and one continuity checkpoint. Avoid inventing duplicates.
- **Preflight may still over-expand:** `autopilot` asks to close the whole decision frontier for
  unattended work and carries a detailed contract. Test whether it distinguishes indispensable
  user choices from implementation choices already delegated. A longer checklist is not proof
  of better understanding.
- **The waiting mismatch is partly policy/runtime, not merely a skill defect:** the current
  Codex adapter explicitly returns control until the user resumes after a receipt should exist.
  The account policy supplied to this task also requires returning after long-job launch without
  recurring AI checks. That does not match the experience described in F3. Current policy remains
  binding; historical requests cannot override it here. Resolving this needs a supported wait or
  completion mechanism and, where necessary, an explicit policy decision—not covert polling.
- **Owner handoff needs stronger behavioral evidence:** `wizard` currently calls for syntax and
  static tracing, avoiding live end-to-end execution because human interaction is involved.
  A useful candidate improvement is testing the noninteractive pieces and realistic failure/resume
  paths without live credentials before asking David to run the procedure. A1/A2 establish the
  pain; they do not prove that this skill alone caused every failure.
- **Evaluation is still too small for the autonomy ambition:** the previous bounded tests prove
  useful behaviors, not long-horizon reliability. Replaying corrections can expose misalignment
  without immediately paying for another overnight run.

## Fit with ChatGPT and Codex

Official documentation describes skills as progressively loaded: their names/descriptions are
available first, and their bodies are loaded on selection. It recommends focused skills and
scripts where deterministic behavior or external tools are needed. Therefore, a critical rule
inside an unselected skill is not an always-active guarantee. Keep small personal defaults,
project-specific context, and selected skill disciplines distinct. This placement recommendation
is an inference from the documented mechanism. [O1]

The app documents `/goal` as persistent work that can finish, pause, or need input, with `/plan`
available for shaping the objective. It also distinguishes app commands from CLI and ChatGPT web
commands. These sources do not prove that a particular host exposes reliable unattended
completion callbacks or identical tools. Verify the actual target surface before promising
continuation or reusing an adapter across ChatGPT and Codex. [O2, O3]

## Proposed next tests, not a mandatory workflow

1. **Short preflight:** offer a rich existing project context and a two-sentence goal. Observe
   whether the agent asks only consequential unanswered questions and preserves delegated choices.
2. **Partial blocker:** with one owner-only action blocked and independent work authorized, check
   that the agent completes useful independent work and returns one consolidated decision request.
3. **Material progress:** give a broad improvement goal plus an easy low-impact patch. Require an
   honest account of contribution without claiming the broad goal is complete or padding runtime.
4. **Continuity:** resume from stale prose and authoritative newer receipts; retain decisions,
   correct status, and avoid repeating expensive work.
5. **Quiet job lifecycle:** first establish host capabilities and authority, then test short
   process completion/failure with bounded non-AI waiting, no repeated model status turns, and an
   observable continuation or honest handoff. Do not start a multi-hour job to discover this gap.
6. **Project boundary:** offer Portfolio visual rules alongside an unrelated backend task; verify
   that the project-local aesthetic audit does not become a global requirement.
7. **Owner setup:** exercise simulated missing prerequisites and resume paths before owner-only
   interaction, without production changes or credentials.

Prefer small adjustments to existing skills, plus failure-based evaluations, over adding a new
named skill for each complaint. Review this profile with David before changing defaults or policy.

## Primary source registry

Conversation references use stable session identity plus recorded JSONL line numbers; files are
private local sources and may move if archived. User messages are historical observations.

- **D1:** This David Skills conversation, `019fe58f-52a3-7772-9b1e-17806bce3cd5`, user corrections
  about flexible composition, questions, documentation, autonomy, and chat-first reporting.
- **F1–F5:** [Forge conversation](/home/dlybeck/.codex/sessions/2026/08/23/rollout-2026-08-23T00-37-31-01a02c0d-1991-7900-90a9-6bc9f9f7aefa.jsonl).
  F1: Sep 5, lines 123027, 123707, 124008. F2: Aug 31, lines 82464, 82759.
  F3: Aug 30–Sep 6, lines 72449, 118493, 120532, 124409.
  F4: Sep 6, line 126680. F5: Sep 5, lines 122587, 122766.
- **P1–P3:** [Portfolio conversation](/home/dlybeck/.codex/sessions/2026/09/02/rollout-2026-09-02T01-21-14-01a05fb4-ba60-7851-930d-3377d46f116b.jsonl).
  P1: Sep 2/6, lines 823, 25346. P2: Sep 6, lines 25404, 25470, 25495.
  P3: Sep 2, lines 9, 247, 300.
- **A1:** [Arr setup conversation](/home/dlybeck/.codex/sessions/2026/08/29/rollout-2026-08-29T19-08-38-01a04eec-855d-7eb0-8b37-981237216412.jsonl),
  Aug 29–30, lines 156, 1134, 3481. Only the user's feedback, not pasted operational material,
  informs this report.
- **A2:** [Earlier Arr conversation](/home/dlybeck/.codex/sessions/2026/08/09/rollout-2026-08-09T02-22-21-019fe454-0c03-7093-bb27-a087cb815eb8.jsonl),
  Aug 25, lines 10411, 10904.
- **Mobile stage context:** [Mobile architecture conversation](/home/dlybeck/.codex/sessions/2026/08/22/rollout-2026-08-22T20-56-36-01a02b42-db43-7343-b958-ccdf5b85c0b9.jsonl),
  Aug 22, lines 796, 1134. Supports the historical Original/local/mobile distinction, not a
  separate claim that Pocket's implementation was inspected.
- **O1:** [Official skill authoring and discovery documentation](https://learn.chatgpt.com/docs/build-skills), fetched Sep 7.
- **O2:** [Official app goal commands](https://learn.chatgpt.com/docs/reference/slash-commands#set-or-manage-a-goal-with-goal), fetched Sep 7.
- **O3:** [Official developer commands by surface](https://learn.chatgpt.com/docs/developer-commands), fetched Sep 7.

## Follow-up synthesis: David's version, not a mandatory pipeline

David clarified that waiting must preserve autonomous continuation: do useful independent work
within scope, or genuinely wait without recurring model polling, then resume when the dependency
finishes. Ending the conversation and requiring David to restart it defeats the intended handoff.
This is design input, not an authorization to override the current account polling policy or
invent a monitoring schedule. The current policy and `pursue-goal` adapter need explicit
reconciliation during an authorized implementation, followed by a short real lifecycle test.

The proposed synthesis is composable engineering disciplines plus delegated process selection.
David retains ownership of intent, protected project constraints, authority, and acceptance; the
agent chooses and revises the research, design, implementation, and validation route inside them.

- Keep a small set of personal collaboration defaults, not a transcript-sized persona prompt.
  Clarify consequential unknowns while David is available, preserve his product intent, challenge
  weak assumptions, and report meaningful evidence with minimal unnecessary interruption.
- Keep project direction and invariants in existing project-local sources. Portfolio-specific
  aesthetic rules must not become account-wide requirements.
- Refine existing pilots and shared execution disciplines before adding new slash commands.
  Autopilot aligns first; Yolopilot proceeds from a stated provisional interpretation within
  granted authority. Both retain evidence, continuity, and validation obligations.
- Separate a short human-facing objective from agent-maintained operational context. Specs and
  tickets remain optional; a durable checkpoint should retain current proof, decisions, rejected
  approaches, and the next useful action without duplicating every artifact.
- Put deterministic job receipts and verified wait/resume mechanics behind tools or adapters.
  A stronger instruction alone cannot guarantee host-level continuation.
- Convert repeated corrections into bounded behavioral evaluations. Distinguish durable
  preferences from project rules and one-task choices; do not silently accumulate new defaults.

Rechecked upstream sources on Sep 7: [Matt's README](https://github.com/mattpocock/skills)
explicitly favors small, adaptable, composable skills and user control, while
[his engineering article](https://www.aihero.dev/5-agent-skills-i-use-every-day) also emphasizes
disciplined internal processes. Thus composition is flexible, not an exemption from validation.
[OpenAI's skill documentation](https://learn.chatgpt.com/docs/build-skills) confirms selective
loading, explicit/implicit invocation, focused skills, and scripts when deterministic behavior
is needed. These support the proposed packaging, not a guarantee of unattended runtime behavior.

## Corrected skill split after source review

David's latest clarification is active authorship: heavy initial involvement, autonomous work
with sporadic human corrections, and an end review that may launch another stage. A correction
must update the working understanding and survive context changes; a status question must not
be mistaken for a new objective. He also explicitly corrected the proposed use of `advise`:
it advises how to use this plugin, not how to plan a product in general.

Re-read actual source instructions rather than relying on catalog summaries:

- [advise](../../skills/engineering/advise/SKILL.md) is a plugin router. Preserve that purpose.
- [grill-me](../../skills/productivity/grill-me/SKILL.md) and
  [grill-with-docs](../../skills/engineering/grill-with-docs/SKILL.md) already provide deliberate
  understanding sessions, stateless or with domain documentation. No new general planning
  front door is justified by the evidence.
- [wayfinder](../../skills/engineering/wayfinder/SKILL.md) is a shared decision map, planning
  by default, with explicit live-human ticket types. Do not relabel it an autonomous build loop.
- [to-spec](../../skills/engineering/to-spec/SKILL.md),
  [to-tickets](../../skills/engineering/to-tickets/SKILL.md), and
  [implement](../../skills/engineering/implement/SKILL.md) are the strongest initial candidates
  for model reachability, but retain their actual jobs. Replace routine human gates only for
  already-delegated decisions, scale artifacts to the task, and separate invocation from authority
  to publish, commit, or resolve tracker items. Do not make their sequence compulsory.
- [handoff](../../skills/productivity/handoff/SKILL.md) is a portable context export, not routine
  ongoing documentation. It could become model-reachable for an actual transfer without giving
  the agent permission to abandon a live goal or spawn a replacement session.
- [pursue-goal](../../skills/engineering/pursue-goal/SKILL.md) already owns adaptive execution
  and continuity. Strengthen steering reconciliation and verified waiting there before creating
  a new interruption command or another orchestration engine.

Recommended presentation split: an everyday human set (plugin help, deliberate understanding,
pilot handoff, status, clarification, teaching); AI-selectable engineering practices plus the
specific conversion candidates above; and an optional specialist shelf retaining shared mapping,
architecture workshops, triage, setup, questionnaires, and explicit delegation. These are usage
groups, not a new third invocation flag or a promise that the host hides picker entries.

No plugin, project policy, installed bundle, account memory, remote ref, or live service was changed.
