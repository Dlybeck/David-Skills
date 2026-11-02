# Promotion PR

A **promotion PR** is the one open pull request from the agent-owned integration branch (`dev`)
into the human-owned branch (`main` or `master`). Agents open it, keep its report current, and fix
review comments on it; only the owner merges it, and the plugin hook enforces that. Use this
reference when repository policy routes human-owned promotion through that PR. Commands below say
`main`; use `master` where that is the human-owned branch.

Two pasted handoffs drive it: a **ready signal** opens or updates the PR, and a **review fix**
returns the owner's comments. They come from the owner or from the TPM relaying for them. Act on the
PR only from one of them; finishing a task is not a ready signal.

## Ready signal: open or update the PR

```text
Ready for <owner>: <task>
Agreed: dev chat, TPM, chief of staff (<date>)
Owner's original request (verbatim): <what the owner asked for>
Owner decision for this PR: <committed repository policy | relayed by <who> on <date>>
```

"Committed repository policy" means a grant already on `main`, where only the owner puts it. A
grant that exists only on `dev` or a feature branch needs the relayed decision.

Run every readiness check on one pinned `dev` SHA and record its result. Any failure ends the step:
report the failing check with its evidence and open nothing.

1. `git fetch origin`; local `dev` equals `origin/dev`. Pin that SHA. If `dev` is unpushed, push it
   only within this run's push authority; otherwise report it.
2. The repository's required tests pass on the pinned SHA (this repository: `npm test`).
3. Every CI run for the pinned SHA has completed successfully:
   `gh run list --commit <sha> --json name,status,conclusion,url`. None found is a failure.
4. The task's integration is on `dev`: `git merge-base --is-ancestor <task merge> <sha>`.
5. The task's final head has no unresolved actionable review findings.

Then find the PR: `gh pr list --base main --head dev --state open --json number,url,body`.

- **One open:** update it. Read its current body, keep every other task's section, add or refresh
  this task's section, and apply with `gh pr edit <n> --body-file <report>`.
- **None open:** `gh pr create --base main --head dev --title "Promote dev to main: <task>"
  --body-file <report>`. With more than one task in the report, title it
  `Promote dev to main (<count> tasks)`.
- **More than one open:** report them and change neither.

Done when `gh pr view <n> --json headRefOid,body` shows the pinned SHA and the report, and the PR
URL has gone back to whoever sent the signal.

## Report template

The PR always shows all of `main..dev`, so the report accounts for every commit: one section per
ready task, and everything else under **Also on dev**
(`git log --first-parent --oneline origin/main..origin/dev`).

````markdown
Head: `dev` @ <sha> · Tests: `<command>` passed · CI: <run url> green

## <task>
- **Asked for:** <owner's original request, verbatim>
- **Changed:** <what changed, in the owner's terms; key files>
- **Tested:** <commands and results, CI, independent review receipt>
- **Left open:** <known gaps, deferred items, or "nothing">

## Also on dev
<commits in main..dev that belong to no task above, or "none">

## Reviewing
Merge with **Create a merge commit**. A squash or rebase merge makes the release refuse.

For a fresh cloud review, paste into a new Claude session with access to this repository:

```text
Review PR <url> (base main, head dev @ <sha>) for actionable defects. Read the full main...dev
diff and the repository guidance, using /independent-pr-review if it is installed. Post each
finding as a PR review comment on the line it concerns, in one review submitted as a comment.
Report only; do not push, merge, approve, or change code.
```
````

## Review fix: comments back to the same PR

```text
Review fix: PR #<n>
Comments: <comment url>, <comment url>
Relayed via chief of staff (<date>); owner's call for each: <fix | answer | won't fix>
```

1. Read each listed comment, and only those. The URL anchor names its kind:
   `#discussion_r<id>` → `gh api repos/<o>/<r>/pulls/comments/<id>`;
   `#issuecomment-<id>` → `gh api repos/<o>/<r>/issues/comments/<id>`;
   `#pullrequestreview-<id>` → `gh api repos/<o>/<r>/pulls/<n>/reviews/<id>`.
   Agents post with the owner's GitHub account, so a body starting `🤖 Agent:` is an agent's own
   reply: skip it. A comment that asks for more than the task's scope goes back to the TPM with a
   recommendation instead of a fix.
2. Fix through the developer loop: a feature branch from `dev`, the repository's tests, a fresh
   independent review, integration into `dev`, and a push of `dev`. The PR's head is `dev`, so the
   push updates it. Check `headRefOid` equals the new `dev` SHA and CI is green on it.
3. Reply to each comment with `🤖 Agent: <what changed> in <sha>; <tests run>.` — or the answer,
   for an answer or won't-fix call. An inline comment gets a threaded reply:
   `gh api repos/<o>/<r>/pulls/<n>/comments/<id>/replies -f body=<reply>`. Any other comment
   gets `gh pr comment <n> --body <reply>` that links the comment. Thread resolution is the
   owner's.
4. Refresh the report: the head SHA, and the task's **Changed** and **Tested** lines with an
   **After review** note.

Done when every listed comment has a reply naming its commit or answer, the PR head equals the
`dev` tip, CI is green, and that summary has gone back to the TPM.

## Boundaries

Merging, approving, enabling auto-merge, and closing the promotion PR belong to the owner.
`dev` only moves forward: new commits, never a rewrite, since it is the PR's head.
