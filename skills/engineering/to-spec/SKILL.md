---
name: to-spec
description: Synthesize settled requirements into a proportionate spec. Use when the user requests a spec or authorized work needs a durable requirements reference; not a prerequisite for every implementation.
---

This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user — just synthesize what you already know.

Use existing issue-tracker and triage-label conventions when publishing. If a required convention
is missing, ask for it or recommend that the human invoke `/setup`; never invoke that human-only
skill automatically. Drafting in chat does not require tracker setup.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

Reuse agreed seams or choose them when test design is delegated. Ask only about consequential
unresolved behavior or interface choices outside that delegation; do not repeat the interview.

3. Write a proportionate spec using the template below. Publish to the configured tracker only
when the request or active contract authorizes that write; apply `ready-for-agent` only when the
requirements are settled and the label change is authorized. Otherwise return a draft in chat or
an already-authorized notes location and state what remains unpublished. Selecting this skill
does not grant tracker authority or authorize implementing the spec.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A concise numbered list covering distinct user-visible behaviors and important edge cases.
Use this form when helpful:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

Scale detail to the actual feature. Do not invent actors, scope, or duplicate stories to fill a
template. Preserve decisions already captured elsewhere with a reference rather than repetition.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
