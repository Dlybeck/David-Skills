# Actionable defect rubric

Adapted from the [public Codex review rubric at commit
402f5b6](https://github.com/openai/codex/blob/402f5b6fdf28a7a72c153dbe6fe01e252205d7d6/codex-rs/prompts/templates/review/rubric.md).
The local adaptation uses one consolidated PR comment rather than inline comments or Codex's
JSON verdict. Specific user and applicable repository guidance take precedence.

Flag a discrete defect introduced by this proposal when it materially affects correctness,
performance, security, or maintainability and the author would likely repair it. Establish a
concrete affected input, caller, invariant, or environment from evidence. Exclude pre-existing
problems, intentional behavior, speculative breakage, unstated requirements, and trivial style.
Match the repository's level of rigor. Report all qualifying issues, deduplicating by defect and
remedy while retaining applicable rule support; do not manufacture findings to fill a quota.

| Priority | Meaning |
| --- | --- |
| P0 | Immediate blocker to release, operations, or broad usage; reserve for unconditional failures. |
| P1 | Urgent defect for the next repair cycle. |
| P2 | Normal actionable defect to address. |
| P3 | Lower-impact actionable improvement. |

Use short imperative titles (at most 80 characters including priority), narrow changed-line
locations (normally no more than 5–10 lines), and matter-of-fact, concise paragraphs. Explain
the triggering conditions before their impact. Suggest a correction direction without generating
a fix; a code fragment, if essential, stays at most three lines. Cite an applicable repository
rule only when it contributes a specific invariant, scope, remedy, or confirmation requirement.
Ordinary correctness findings remain eligible without rule support.

The private receipt records coverage, evidence, and uncertainty rather than asserting that a
clean pass guarantees correctness. The external comment adapts each finding to this shape:

> Reviewed commit: `<full head SHA>`; comparison: `<merge base>` → `<head>`.
>
> **[P1] Preserve the command boundary** — `path/to/file.py:42–44` (pinned link).
> Under `<trigger>`, `<expected>` becomes `<actual>`, causing `<impact>`. Adjust `<direction>`.
> Evidence: `<isolated test command/result, or static reasoning and runtime limitation>`.

Repeat the finding block for each distinct actionable issue inside the single comment. Keep clean
receipts private; no empty comment, generic praise, or implied merge approval.
