# David's development profile

Confirmed direction as of 2026-09-07. This is a design reference for developing David Skills,
not a personality assessment, a new skill, or standing authority to act in other projects.
The [conversation research](../../.reports/research/2026-09-07-personal-autonomy-feedback.md)
records the evidence and its limits. Its source keys below refer to that note; raw conversations
and operational logs are not part of this profile.

## Confirmed cross-project preferences

| Area | Preference and observable consequence |
| --- | --- |
| Collaboration | Understand the ambition together at the beginning, then let the AI work autonomously. David checks in intermittently to judge and correct direction, reviews the result, and may kick off another stage. His availability is an opportunity for steering, not a prerequisite for each next step. [D1, P1] |
| Decision ownership | David owns product intent, consequential tradeoffs, scope, and authority. The AI chooses and revises implementation details inside delegated boundaries. Welcome criticism without substituting a generic product for the one David wants. [D1, P3, F5] |
| Steering | A correction must change subsequent work and survive context changes. Distinguish questions and tentative suggestions from instructions; do not silently promote every comment into a requirement or restart the interview after each correction. [D1, latest clarification] |
| Planning | Inspect existing evidence and reuse settled answers. Ask about consequential decisions, not agent-findable facts or already-delegated choices. A human-facing goal can be two or three sentences while the AI keeps richer working context. [D1, P1, P2] |
| Composability | Keep the engineering practices available in any useful combination. Specs, tickets, prototypes, and research are tools, not a mandatory global sequence. Preserve the discipline inside each selected practice. [D1] |
| Engineering | Judge progress against meaningful outcomes and uncertainty reduced, not activity, token use, or hours occupied. Validate actual behavior before reporting success or handing manual steps to David. A small patch can be useful without fulfilling a broad goal. [F1, A1, A2] |
| Continuity | Keep decisions, evidence, failed approaches, current stages, and a next action recoverable. Prefer one useful checkpoint and links to existing artifacts over duplicate reports or repeated expensive work. Waiting must preserve the active goal and autonomous continuation; job duration alone must not force a manual restart. [F2, D1; explicit correction, 2026-09-07] |
| Cost | Avoid unnecessary delegation and repeated AI status checks. Use useful independent work within scope or supported non-AI waiting; do not invent busywork or disturb an experiment merely to fill time. [F3, A1, D1] |
| Communication | Keep chat concise and understandable. Reports belong in chat by default, with visuals when they clarify the evidence. Distinguish local, tested, committed, pushed, and deployed results. Offer teaching rather than forcing a lesson into every handoff. [D1, P3, A2] |
| Boundaries | Preserve protected originals and project invariants. Autonomy preferences do not authorize spending, deployment, deletion, new account access, external writes, or expanding the task. Specific current instructions determine authority. [D1, F5, P2] |

## Project-specific examples, not global defaults

- **ScribbleScan / Forge:** protect the designated Original and frozen evaluation baselines;
  assess changes against the actual OCR objective, not a convenient tiny improvement. Preserve
  research and experiment stages so long work can resume. [F1, F2, F5]
- **Portfolio:** preserve its exploratory self-portrait intent and established navigation.
  Physical-believability and theme-grounding rules were explicitly restricted to that project;
  they are not universal backend or UI requirements. [P2, P3]
- **Arr / RSuite-related setup:** minimize owner-only steps and validate agent-testable portions
  before handoff. The research note labels the RSuite-to-Arr mapping as an inference. [A1, A2]

No general language, framework, editor, naming, or code-format preference is established here.
Follow each project's actual conventions rather than inferring them from this sample.

## Unresolved tensions and capability limits

- **Waiting versus host capability:** David explicitly reaffirmed on 2026-09-07 that wait times
  must not pause the goal. A supported blocking wait satisfies the no-AI-polling requirement
  without a separate callback. Verify the host's actual wait and continuation behavior; name
  binding host restrictions rather than adding a policy that requires manual resumption.
- **Broad ambition versus scope:** substantial overnight work is a desired use case, not a minimum
  duration, unlimited compute budget, or permission to invent additional objectives.
- **Desired steering versus measured behavior:** continuous availability of human steering is the
  target; the existing research is not proof that every installed runtime reliably handles it.
- **Evidence coverage:** the research samples local saved conversations, not all chats. Pocket is
  represented through related discussions; separate private ChatGPT history was unavailable.

## How this profile should evolve

Use explicit new feedback to correct this document. Separate a repeated general preference from
a project rule or one-task choice, preserve important disagreements as unresolved, and connect
material changes to behavioral tests. Do not silently promote model suggestions into preferences.
Plugin skills should encode only the relevant reusable discipline; this whole profile is not
copied into project instructions, installed as a skill, or written to account memory.
