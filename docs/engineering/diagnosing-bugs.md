## What it does

`diagnosing-bugs` investigates a hard bug or performance regression through a reproducible feedback loop. A diagnosis-only request ends with the verified cause and proposed fix; when repair is authorized, it continues through a regression test, fix, and cleanup.

It will not let the agent form a theory until a **tight** feedback loop exists — one named command, already run once, that goes red on *this* bug and green when it is fixed. The default behaviour of a coding agent handed a bug report is to read code and guess; this skill blocks that. If no red-capable command exists, there is no Phase 2. That single gate is what the skill is for. Everything after it — bisection, hypothesis-testing, instrumentation — is mechanical once the signal exists.

## When to reach for it

Type `/diagnosing-bugs`, or the agent reaches for it when asked to diagnose or debug an unclear failure or slowness. A straightforward known fix need not run the full investigation.

Reach for it on the hard ones: a bug that resists a first look, an intermittent flake, a regression that crept in between two known-good states. It is heavy by design, and the wrong tool for a question you want answered in one message.

| Your situation | Where to go |
| --- | --- |
| A specific defect whose cause remains unclear | This skill |
| A slow endpoint or a timing regression with a known before-and-after | This skill — it has a performance branch (measure a baseline, then bisect) |
| "Where are the bottlenecks in this codebase?" — no specific symptom | Not this skill. It diagnoses one known failure, it does not audit |
| A raw bug report from someone else, not yet confirmed or written up | [triage](./triage.md) first |
| Throwaway code to answer a design question, not chase a defect | [prototype](./prototype.md) |
| Building a planned behaviour test-first | [tdd](./tdd.md) |
| No good seam exists to lock the bug down | [re-architect](./re-architect.md) — this skill hands off there itself |

## The tight loop is the skill

Phase 1 gets disproportionate effort because it is the only phase that is hard. The skill gives a ladder of ways to construct the loop, roughly in order of preference:

1. A failing test at whatever seam reaches the bug.
2. A curl or HTTP script against a running dev server.
3. A CLI invocation with a fixture input, diffed against a known-good snapshot.
4. A headless browser script asserting on DOM, console, or network.
5. A replayed capture — a saved request, payload, or event log, run through the code path in isolation.
6. A throwaway harness: a minimal subset of the system, one function call.
7. A property or fuzz loop, for "sometimes wrong output".
8. A bisection harness you can hand to `git bisect run`.
9. A differential loop — same input, old version against new.
10. A [human-in-the-loop](https://www.aihero.dev/ai-coding-dictionary/human-in-the-loop) bash script, last resort. The skill ships `scripts/hitl-loop.template.sh` for this: the agent runs the script, you follow prompts in your terminal, and your answers come back as parseable output.

*A* loop is not the goal. **Tight** is: fast (seconds), deterministic (same verdict every run), sharp (asserts your exact symptom, not "didn't crash"), and agent-runnable unattended. A 30-second flaky loop is barely better than none. For a bug that only shows up sometimes, the target is not a clean repro but a **higher reproduction rate** — loop the trigger, parallelise, add stress, inject sleeps, until the flake rate is high enough to debug against.

When it genuinely cannot build one, it is instructed to stop and say so, list what it tried, and ask you for [environment](https://www.aihero.dev/ai-coding-dictionary/environment) access, a captured artifact, or permission to add temporary instrumentation. It should not proceed to hypothesise anyway.

## The gates between phases

The phases are gates, not a checklist. Each one refuses to open until something specific is true.

| Gate | What has to be true |
| --- | --- |
| Into Phase 2 | A named command, already run and pasted with its output, that can go red on this bug |
| Into Phase 3 | The repro is reproduced *and* minimised — every remaining element is load-bearing |
| Into Phase 4 | 3–5 ranked, falsifiable hypotheses exist, each stating its prediction, shown to you before any is tested |
| Into Phase 5 | Probes map to a specific prediction, one variable at a time, every debug log tagged `[DEBUG-a4f2]`-style so cleanup is one grep |
| Diagnosis done | Evidence supports the cause; proposed repair and uncertainty are explained without changing application code |
| Authorized repair done | Original repro no longer reproduces, instrumentation gone, and the confirmed hypothesis is recorded |

Phase 5 has an escape hatch worth knowing about. The regression test is written before the fix, but only if a **correct seam** exists for it — one where the test exercises the real bug pattern as it occurs at the call site. Where the only available seam is too shallow, the skill is told to say so rather than write a test that gives false confidence. That absence is itself the finding, and it is what routes the post-mortem to `re-architect`.

## Common questions

**It fires on quick questions where I just wanted a direct answer.**
Earlier versions activated on almost any failure description. The trigger now targets unclear failures, and existing reproductions or settled evidence are reused rather than rebuilt for ceremony. Say whether you want an explanation or a repair; the skill should not turn a straightforward known answer into a full investigation.

**Can I point it at a codebase and ask where the performance problems are?**
No. It diagnoses one failure you can already name. Its performance branch is for a regression with a symptom — establish a baseline measurement, then bisect, measure first and fix second — not for a proactive sweep. A skill for the proactive version was [proposed and closed](https://github.com/mattpocock/skills/issues/431); there is currently no skill for it.

**Does it stop and ask me before it writes the fix?**
It follows the authority you gave. Diagnosis-only work uses read-only checks or an isolated reproduction, explains the cause, and stops before application changes. If you already asked for the fix, it can continue without asking for the same permission again. New scope or external actions still need their own authority.

**I already ran `/triage` on this bug report. Is this the same work again?**
Partly, and neither skill admits it. As one reader put it: "Triage's step 3 is essentially a shallow, bounded instance of diagnosing-bugs Phase 1–2, but neither file mentions the other." Triage does a bounded "is this actually a bug, and what is the surface" pass; this skill does the thorough version. Running triage first is not wasted — its verification often gives you most of Phase 1's raw material — but expect to redo it properly here, and expect no cross-reference to tell you that.

**Will the repro output it pastes leak secrets?**
The skill explicitly requires redacting secrets from commands, outputs, and captured artifacts before showing them. Credentials belong in environment variables, and only signal-bearing artifact lines should be quoted. That instruction is not a guarantee: review anything destined for a public issue or PR, especially HAR files and logs containing authentication headers.

**My security scanner flagged this skill as high risk.**
A shipped shell template and instructions to run local commands can trigger capability-based warnings. Inspect the flagged script and intended actions; a scanner warning alone neither proves an exploit nor proves the operation safe. The human-in-the-loop template prompts for manual reproduction steps rather than granting permission to perform unrelated actions.

**What happened to `/diagnose`?**
Renamed to `/diagnosing-bugs` in v1.0.0. The old name no longer exists. Anything of yours that chains `/diagnose` — a wrapper skill, a saved prompt — needs updating.

## It's working if

- It shows you a command and its red output before it offers a single theory. If theory arrives first, the skill is not running.
- The failure it reproduces is the one you reported, not a nearby one it found on the way.
- It shrinks the repro before it starts guessing, and can tell you why each remaining piece is load-bearing.
- You are shown a ranked list of 3–5 hypotheses, each with a prediction you could falsify, before any of them is tested.
- Every debug log it adds carries a tag like `[DEBUG-a4f2]`, and a grep for that tag comes back empty when it declares done.
- A diagnosis-only request ends with the cause and no application-code changes; an authorized repair records which hypothesis was right.
- When it cannot lock the bug down with a test, it says so plainly instead of writing a shallow one.

## Where it fits

`diagnosing-bugs` is a reach-for-it-anytime standalone with no tracker prerequisite. It ends at a supported diagnosis or, when authorized, a verified repair. [advise](./advise.md) routes unclear failures here.

Two neighbours matter. [re-architect](./re-architect.md) takes the [handoff](https://www.aihero.dev/ai-coding-dictionary/handoff) when the real finding is that the code has no seam to lock the bug down — the recommendation is made after the fix is in, when there is more information. [triage](./triage.md) sits upstream of it for bugs that arrive as raw reports from other people, and does a shallower version of the same first two phases.
