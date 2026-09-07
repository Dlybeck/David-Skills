# Human-steered autonomy pivot: implementation and validation

As of 2026-09-07. Branch: `feature/human-steered-autonomy`, based on `19c526e`.
The first implementation commit, `650b643`, records the development profile and its research
before skill behavior changes. The repository guidance pointer is in `CLAUDE.md`, reached via
the tracked `AGENTS.md` symlink. All changes are local; no push, install, release, or promotion.

## Result

Source implementation is present, but the full pivot is **not complete or release-validated**.
Required live steering, fresh-context transfer, and long-job continuation remain unverified.
The reference for judging behavior is the
[development profile](../../docs/agents/david-development-profile.md), not a mandatory workflow.

- Exactly four skills become model- and user-reachable: requirements synthesis, decomposition,
  implementation, and portable handoff. All 30 promoted skills remain in both manifests.
- Pilots retain their distinct entrances and delivery authority. Shared steering preserves clear
  corrections and distinguishes questions, suggestions, and stop requests.
- Status reports expose current intent without changing it. Checkpoints and portable handoffs
  remain separate, and project-specific rules stay project-local.
- `advise` retains plugin guidance. Catalogs, human docs, invocation guidance, domain language,
  architectural decisions, and a minor Changeset are synchronized. Delegate's stale references
  to human-only implementation/advisory review were corrected without changing its dispatch role.

## Offline validation

| Check | Result |
| --- | --- |
| Repository validator | Pass: 30 promoted, 37 total skills |
| Hook suite | Pass: 148 checks |
| Pilot scenario structure | Pass: 7 fixtures; not behavioral proof |
| Evaluator tests | Pass: 19 tests, including real short process exits/timeouts and fake-RPC steering/transfer/timeout tests |
| Hermetic release suite | Pass: 6 tests |
| Local documentation links | Pass: 256 links after final docs synchronization |
| Skill quick validation | Pass for to-spec, to-tickets, implement, pursue-goal, status-report; handoff retains the pre-existing cross-harness `argument-hint` field rejected by this generic validator |
| `git diff --check` | Pass |
| `npm test` / Node version-sync tests | Environment gap: npm absent; no runnable Node on PATH. A non-executable Zed-managed Node file was found and left untouched |
| Claude plugin validation | Environment gap: Claude CLI absent |

## Live budget and observations

One of six authorized live runs was consumed (28.29 seconds, 120-second cap). Remaining five were
not launched after file-access evidence was missing. The allowed ceiling remains 300 seconds per
pivot case; offline tests verify rejection of a larger timeout. No recurring AI polling was used.

The first run, `pivot-router`, used source copied before the router wording update. It produced
a relevant optional menu and no project changes, but incorrectly generalized the router's own
role and reported inability to access local files. The trace contains **zero tool execution
events**. Native exit zero and `turn.completed` therefore do not establish the required skill
reads or a behavioral pass. The underlying access failure is not diagnosed by this trace alone.
A separate non-AI diagnostic using `codex sandbox --permission-profile :workspace` to run
`/bin/true` in that disposable directory failed with
`bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` (exit 1). This confirms a sandbox
startup restriction on the host; no namespace settings or sandbox protections were relaxed.
Do not use this run as coverage of the subsequently revised router.

Local raw evidence (outside the distribution):
`/tmp/david-eval-pivot-router-q95fsh9w/` — request, source hashes, trace, answer, Git snapshots,
and terminal receipt. Native thread: `01a0796f-6ce9-7cb0-979e-cdaf87583a1a`.
The evaluator's legacy `needs-review` status is intentionally not a pass. It now exposes missing
tool-event evidence as a warning and fingerprints account configuration before/after future runs,
invalidating the environment result if that configuration changes. The CLI also persisted one trust entry for this unique disposable
project; only that entry was removed, with no account-policy amendment or runtime relaxation.

The six reusable scenarios in `scripts/pivot_cases.py` cover routing, small delivery, artifact
composition, steering, status, and short waiting. `scripts/evaluate_steering.py` is a disposable
test transport: real `turn/steer`, followed by a new ephemeral thread receiving only artifact
context. It is not a production chat client or supervisor. Its protocol and timeout tests pass
offline; live support is unverified. It refuses unsupported approval/tool requests and does not
silently substitute a static replay for an in-flight correction.

## Native waiting boundary

Two root-chat native tool calls completed after a two-second wait:

- `pivot-native-success`, PID 3999789, terminal exit 0 / succeeded.
- `pivot-native-failure`, PID 3999816, terminal exit 7 / failed.

The agent compared both receipts afterward: success may advance; failure cannot satisfy
acceptance. This demonstrates short synchronous tool continuation only. The evaluator's offline
timeout and interrupted-turn tests do not prove live human interruption or an overnight resume.
No helper was added because process receipts alone cannot wake an ended chat.

## Remaining gates

1. Establish a working approved live test runtime; do not silently enable full-access execution
   to work around the confirmed sandbox startup restriction. Account trust side effects need
   explicit handling. Re-running all six scenarios after the invalid attempt requires a revised
   budget; the original six-run allowance has only five remaining.
2. Run the remaining scenarios within the remaining budget. Re-testing the updated router also
   consumes a run; do not silently exceed six total. Record any uncovered scenario honestly.
3. Provide Node/npm and Claude CLI through an approved existing environment where those checks
   are required, without changing another application's managed executable permissions.
4. Review the [waiting-policy proposal](../research/2026-09-07-waiting-policy-proposal.md), then
   verify actual permitted long-job continuation and interruption. If that requires a persistent
   agent service/custom production client, stop for redesign as agreed.

These are explicit limitations, not completed tests. Keep the branch unmerged until the desired
release gate is satisfied or David explicitly changes the acceptance scope.
