# Waiting policy: proposed amendment, not applied

The current account policy is `/home/dlybeck/.codex/AGENTS.md`. This document proposes a narrow
change for David's review; it does not override that policy or the host's instructions.

## Proposed replacement for the waiting boundary

Keep the prohibition on recurring AI polling, repeated unchanged-state reports, polling agents,
and unapproved recurring check-ins. Replace the imminent-only waiting clause and unconditional
return-after-launch fallback with this conditional rule:

> During an authorized task, use a verified, interruptible native wait or non-AI completion
> callback to continue the same task after a dependency finishes, within the host's supported
> limits. Register the wait or callback once; do not use repeated model turns or tool calls to
> check unchanged state. Keep an exact job handle, a progress log, and a terminal receipt.
> Useful independent work may continue within scope if it does not interfere with the job.
> After completion, verify identity and outcome, reconcile any user corrections, and continue
> useful work. Report material transitions only. If the host cannot provide this behavior,
> disclose the limitation before an unattended launch and leave an explicit next action; do
> not claim an ended conversation will resume itself.

Approval of this amendment would not permit recurring model checks, remove wait-duration limits,
authorize new services, or establish a universal polling schedule. Higher-priority host limits
still apply. The approved pivot allows a small local helper only if sufficient, not a persistent
agent supervisor or custom production chat client.

## What has actually been established

The subsequent [approved live batch](../evaluation/2026-09-07-approved-live-pivot-batch.md)
verified native in-flight correction and artifact-only transfer, plus short success/failure
completion followed by receipt inspection and an authorized next-action report. Its six runs
do not establish production long-job continuation, live stop handling, or timeout recovery.
The batch also records incomplete exported launch logging and parent supervision shortcomings;
neither is hidden by the successful bounded behaviors. This proposal remains unapplied.

- Native shell tools returned two-second success and failure jobs and this agent compared their
  results afterward. This proves bounded synchronous tool continuation, not an overnight callback.
- Official [app-server documentation](https://learn.chatgpt.com/docs/app-server), fetched
  2026-09-07, describes `turn/steer` and process/turn events. A process exit event delivered to a
  client is not proof that the current app chat resumes an AI turn after a long dependency.
- The current chat limits long blocking waits; repeated short model waits would violate account
  policy. A local log/receipt helper alone cannot resolve either limitation or wake an ended chat.
- No production helper or persistent service was added. Full long-job continuation, timeout,
  and live human interruption acceptance remain blocked pending a supported runtime and approval
  of any required policy amendment.

See the [pivot evaluation](../evaluation/2026-09-07-human-steered-autonomy.md) for source-test and
offline-test evidence. Do not treat this proposal or offline simulation as a live runtime pass.
