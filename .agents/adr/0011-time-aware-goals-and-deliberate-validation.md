# Optional deadlines, factual clocks, and deliberate validation

## Context

Long-horizon autonomy can consume days without useful progress. The owner requested optional hard
work-period limits, reports at milestones and no more than 45 minutes apart, and a final account
at expiry. The owner explicitly rejected coaching in clock reminders: the agent should interpret
remaining time from the conversation. Rapid AI job-status polling must remain prohibited.
The owner also requested: "Do not use the test suite casually."

## Decision

- Extend the existing goal contract; add no skill, trust mode, mandatory planning stage, or site.
- A user-selected deadline bounds the work period without weakening proof or expanding scope.
- Managed-plugin hooks supply only remaining time at existing tool boundaries, normally spaced
  five minutes apart. They stay inactive until a particular runtime session is opted in.
- Reuse status-report for milestone and explicitly agreed maximum-gap reports. Milestones reset
  the report clock, never the deadline. Unchanged progress gets a brief visible report.
- Keep timing state and the OS wait inside a small Python helper. The wait can return on an
  exact receipt, report time, or deadline without model calls; it supplies no chat-wakeup service.
- Exact delivery during waits and native goal stopping depend on verified host lifecycle support.
  Expiry never justifies marking an unmet goal complete or using blocked to suppress continuation.
- Choose tests by changed behavior, uncertainty, and delivery risk. Preserve relevant passing
  evidence; run mandatory checks at delivery and rerun only checks invalidated by new evidence.

## Boundaries

This refines ADR 0005's lack of an arbitrary default ceiling; open-ended goals remain available.
Account policies and host limits retain their authority. Reporting agreements need a finite bound
on recurring model wakeups. Existing account instructions are not automatically rewritten.
Hook output is advisory and time-only, not a hard interrupt. Python timing state uses POSIX locks;
Claude packaged behavior and long-duration continuation require their own runtime evidence.
