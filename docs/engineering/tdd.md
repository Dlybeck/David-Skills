## What it does

`tdd` builds a feature or fixes a bug test-first: one failing test, then just enough code to pass it, then the next behaviour. It carries the standards that make that loop produce tests worth keeping — what a good test is, where tests go, what mocks are for, and the three anti-patterns that quietly ruin a suite.

It settles the public boundaries under test before writing tests. Existing agreement in your request, spec, or goal contract counts. If you delegated implementation and test design, the agent names relevant existing public interfaces and proceeds; it asks when an unresolved choice changes behavior, scope, or authority. The skill supplies the loop's discipline, whether used directly or through [implement](./implement.md).

## When to reach for it

Type `/tdd`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) reaches for it automatically when a task fits — building a feature or fixing a bug test-first, or when you say "red-green-refactor".

Reach for it when there is a concrete behaviour to build, with an input and an observable output, and you want tests that survive a refactor.

| Your situation | Where to go |
| --- | --- |
| A behaviour with defined inputs and outputs — business logic, a request/response contract, a transformation, validation | `tdd` |
| The behaviour isn't pinned down yet | [to-spec](./to-spec.md), which also agrees the test seams before any code is written |
| The question is really the shape of the interface, not the tests | [codebase-design](./codebase-design.md) |
| You have a [spec](https://www.aihero.dev/ai-coding-dictionary/spec) or [tickets](https://www.aihero.dev/ai-coding-dictionary/ticket) and want the whole build run for you | [implement](./implement.md), which drives `tdd` per ticket |
| Config, wiring, glue, type annotations, straight CRUD delegation | Nothing here fits well — see the open gap below |

That last row is a real hole, not a stylistic preference. The skill decides *where* the seams go; nothing in it decides *whether* a change is worth the loop at all. Run it on a change with no independent source of truth to assert against and you get a test that restates the implementation — the tautological anti-pattern the skill itself warns about, arrived at from the other direction. It is [issue #746](https://github.com/mattpocock/skills/issues/746) and it is open. Until it closes, that judgement is yours or your `CLAUDE.md`'s.

## Prerequisites

[codebase-design](./codebase-design.md) needs to be installed. `tdd` used to carry its own deep-module and interface-design notes; in v1.0 those were deleted in favour of the shared skill, and `tdd` now leans on it for interface-design vocabulary. Nothing else — the skill is [stateless](https://www.aihero.dev/ai-coding-dictionary/stateless) and writes no files of its own.

## The loop, and the seam it runs at

Three words carry this skill.

**Red-green.** Write the failing test, then only enough code to pass it. No anticipating the test after next. There is no refactor phase: it was dropped in June 2026 because agents essentially never performed it, and because review and implementation work better as separate sessions. Refactoring belongs to [code-review](./code-review.md).

**Vertical slice.** One seam, one test, one minimal implementation, then repeat — the first cycle being a **tracer bullet** that proves a single path end to end. The opposite is horizontal slicing: all the tests first, then all the code. Bulk tests verify *imagined* behaviour, they check the shape of things rather than what a user does, and they commit you to a test structure before you understand the implementation.

**Agreed seam.** A seam is the public boundary you observe behavior at without reaching inside. Agreement can come from the conversation, a spec, or a goal contract; it does not require a particular earlier skill. Delegated test design permits choosing existing public interfaces within scope. New product or authority decisions still come back to you.

The three anti-patterns it is written to prevent:

| Anti-pattern | The tell |
| --- | --- |
| Implementation-coupled | The test breaks when you rename an internal function, though behaviour did not change. Mocked internal collaborators, asserted call counts, database queries used to verify instead of the interface. |
| Tautological | The expected value is computed the way the code computes it, so the test passes by construction. Expected values have to come from somewhere else — a known-good literal, a worked example, the spec. |
| Horizontal slicing | A batch of tests landed before any implementation. |

Mocks are for system boundaries only — external APIs, time, randomness, sometimes the filesystem or the database. Not your own modules.

## Common questions

**Why doesn't it refactor? The description says "red-green-refactor".**

Because the refactor step was removed and the description was not. The removal was deliberate: agents essentially never did it, and keeping implementation and review in separate sessions works better. Whether the result still counts as TDD by the book matters less than whether the loop produces better code. The mismatch between the trigger phrase and the body is filed as [issue #589](https://github.com/mattpocock/skills/issues/589) and is still open, so "red-green-refactor" continues to work as a phrase that fires the skill. What you get is red → green, and refactoring in [code-review](./code-review.md).

**It asked me to choose a test seam and I had no idea which to pick.**

You can delegate test design rather than choose from unfamiliar labels. The agent can use existing public interfaces and explain its choice without another approval round. When the decision affects product behavior, scope, or authority, ask what each proposed seam catches, misses, and costs before choosing.

**It wrote the implementation before the test, even though the skill says red first.**

It happens. One user pushed the [model](https://www.aihero.dev/ai-coding-dictionary/model) on it and got an unusually honest answer: "I knew the skill said 'one test at a time, watch it fail for the right reason' — I read it. I just defaulted to my normal habit." The skill is written to live with this. No instruction makes an agent comply 100% of the time, and forcing the point harder restricts the agent's creativity for little gain — the loop is worth running even when it is not followed strictly, because the results are still better overall. If strict adherence matters for a particular slice, watch the run rather than trusting the skill to enforce it.

**Should it write browser or end-to-end tests first?**

Usually not, and the skill will not stop it. A user reported the agent writing a Playwright test first, then burning a long loop re-running it and concluding the *test* was broken for a feature that did not exist yet. Configure this in your `CLAUDE.md`. Browser tests are slow enough that the red-green feedback loop stops paying for itself; declare in your repo's `CLAUDE.md` that they are written after the behaviour works.

**Does `/tdd` replace `/implement`, or the course's `/do-work`?**

No. `/tdd` documents the methodology; `/implement` is a very simple work→feedback→commit loop and is the direct stand-in for `/do-work`. The course's single `/do-work` step is now split across `/implement`, `/tdd` and `/code-review`. If you are asking which one to run against a ticket, the answer is almost always `/implement`.

**Where did the deep-modules and interface-design guidance go?**

Into [codebase-design](./codebase-design.md) in v1.0, generalised so several skills share one vocabulary. `refactoring.md` left at the same time; refactoring is now [code-review](./code-review.md)'s job, and that skill carries the Fowler smell baseline.

**Does it know about my other tickets?**

Not automatically. Supply the relevant scope and dependencies when they affect the behavior under test. The skill does not manage the issue graph, and test-first work is not permission to expand into sibling tickets.

## It's working if

- It names the seams before testing, reuses existing agreement, and asks only about consequential choices not already delegated.
- One test appears, goes red, gets just enough code to pass, and only then does the next test appear — not a batch of tests followed by a batch of code.
- Test names read as capabilities ("user can checkout with valid cart"), not as internals ("checkout calls paymentService.process").
- Expected values in assertions are literals you can trace to the spec, not values recomputed the way the code computes them.
- Renaming an internal function breaks nothing in the suite.
- Mocks appear only at external boundaries — the payment API, the clock — and never around your own modules.

## Where it fits

`tdd` is independently useful test-first discipline. One composition uses it inside implementation:

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

[to-spec](./to-spec.md) agrees the test seams up front, [implement](./implement.md) drives `tdd` per ticket, and [code-review](./code-review.md) checks afterwards that only the agreed seams were used — and owns the refactoring `tdd` no longer does. Its other neighbour is [codebase-design](./codebase-design.md), the shared source of the seam and deep-module vocabulary `tdd` speaks. You can also reach for it on its own, whenever there is a concrete behaviour to build and no full spec in play. When you are unsure which skill fits your situation, [advise](./advise.md) routes you.
