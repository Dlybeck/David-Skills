# Developer and independent reviewer loop

Use this after completing authorized implementation and required validation. Keep `/code-review`'s
Standards and Spec checks and their findings separate; resolve those gates as the calling workflow
requires. This additional loop preserves ordinary defect findings independent of developer self-review.

1. Prepare a reviewable commit only within commit authority. Pin the target base tip, head, merge
   base, repository/PR, and requirements. If commit authority is absent, leave a local diff and
   report this pinned-commit gate unmet instead of committing merely to enable review. For an
   existing PR, synchronize its feature head within push authority before each PR review and
   verify it matches the pinned commit. Without that authority, review the local committed branch
   privately and disclose that the current remote PR is not covered. A draft PR may be opened
   within delivery authority before the loop settles; creating it is not presenting it as settled.
2. Invoke `/independent-pr-review` by dispatching one **new reviewer per cycle**, with no inherited
   implementation conversation or prior reviewer conclusions. Supply only the pinned inputs,
   settled requirements/authority, source access, and the skill. Use documented fresh-context
   controls; compacting or clearing the developer conversation is not an independent reviewer.
3. Preserve the returned ordinary findings separately from the developer's own assessment and
   Standards/Spec reports. When the active request authorizes intermediate review comments, let
   the workflow publish one consolidated actionable comment for that head without asking the
   user to approve its wording first. Review alone grants no posting authority; absent it, keep
   findings private and continue authorized local repairs. No actionable findings means no comment.
4. The **developer** addresses actionable findings inside the settled scope, adds justified
   regressions, runs affected and required full checks, and commits within authority. Then repeat
   the full-base review with a fresh reviewer on the new exact head; no incremental-only review
   or reuse of a previous clean result. Reconcile other required review gates if fixes affect them.
5. Escalate material scope, security, permission, or approval blockers as soon as they arise. If a
   finding is disputed or unchanged unsupported advice recurs, preserve its evidence and the
   developer's response separately. Seek a decision on genuine deadlock; do not silently dismiss
   ordinary findings or run an endless identical review loop. User interruption takes effect
   immediately under the calling workflow's stop/steering rules.
6. Settle only when the exact final head has complete fresh coverage, no unresolved actionable
   findings, and the required checks pass. Push the feature branch and create/update its PR only
   within delivery authority; verify the remote head and exact-head CI before presenting the settled
   PR. If a push or base update changes the proposal, re-pin and re-review. If CI is unavailable,
   disclose the unmet gate instead of claiming it passed.

Present the settled PR with its exact head, tests, independent review receipt, residual limitations,
and actual delivery state. Blockers and material progress can be reported earlier; suppressing an
unfinished PR presentation does not prevent human steering. **Every merge into `main` requires
David's explicit final approval for that particular merge**; prior feature work, loop approval,
clean reviews, and CI never imply it. Follow any stricter repo/dev merge, release, installation,
or publication gates. Never enable auto-merge on the strength of this loop.
