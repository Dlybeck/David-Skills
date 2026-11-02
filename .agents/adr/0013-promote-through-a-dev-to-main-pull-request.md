# Promote through a dev-to-main pull request

This amends [ADR 0003](./0003-plugin-root-hook-for-personal-git-workflow.md), whose hook blocked
every agent PR into `main`, and [ADR 0008](./0008-release-directly-after-human-main-promotion.md),
whose release required `main` and `dev` to be the same commit.

## Context

David promoted by pushing `dev` to `main` himself. He wants to review each finished task on GitHub
instead, or through a fresh cloud review session that posts PR comments. Then he wants to click
Merge. Agents keep integrating into `dev` on their own. The old hook blocked opening that PR but
did not block `gh pr merge`, `gh api` merges and ref writes, or force-pushes of `dev`. Every
GitHub merge method also leaves `main` on a commit that `dev` lacks, which the release refused.

## Decision

- One open **promotion PR**, head `dev` and base `main`. Agents open or update it only on a pasted
  ready signal from David or the TPM, recording that the dev chat, the TPM, and the chief of staff
  agree. Its checks, report template, cloud-review prompt, and review-fix loop live in
  `skills/engineering/independent-pr-review/references/promotion-pr.md`, reached from the
  developer loop's human-owned-promotion route and from Autopilot's Delivery section. There is no
  new skill, and Yolopilot is unchanged.
- Review comments come back as a pasted review fix. The dev chat fixes them through `dev`, which
  updates the same PR, and replies on each thread with a `🤖 Agent:` prefix. Agents use David's
  GitHub account, so that prefix is the only way to tell their comments from his, and agents
  skip comments that carry it.
- The hook allows `gh pr create` into `main`/`master` only from head `dev`, plus body edits,
  comments, and replies. A `gh pr create` with no `--base` targets the default branch, usually
  `main`, so it is held to the same head-`dev` rule; other PRs pass an explicit base. It blocks `gh pr edit --base main`, and `gh pr merge` (including `--auto`)
  when `gh pr view` reports a `main`/`master` base or cannot determine one. It also blocks
  `gh api` writes to PR merge, merges, merge-upstream, git refs, and contents endpoints; GraphQL
  merge and ref mutations; `gh repo sync` of a remote's `main`; pushes to `master`; and
  force-pushes or deletions of `dev`. Merges into `dev` and feature branches stay allowed: dev
  chats in David's other repositories merge their PRs with `gh pr merge`.
- The release accepts a merge commit on `main` whose second parent is exactly the `dev` tip with
  an unchanged tree. The release commit then fast-forwards both branches, and the lease on `dev`
  is that tip. A squash or rebase promotion fails with a message naming "Create a merge commit".
- The standing grant in `CLAUDE.md` takes effect when David merges the promotion PR that carries
  it. His merge counts as writing it. Until then, each promotion PR needs a relayed owner
  decision; the promotion-PR reference counts only a grant already on `main` as committed policy.

## Consequences

- `main` is one merge commit ahead of `dev` after a promotion with no Changeset. The next
  promotion's merge still has `dev` as its second parent and `dev`'s tree, so it releases normally.
- The hook's `gh pr merge` check makes one network call, and any failure blocks.
- Text inspection cannot see commands built at runtime, scripts, or other interpreters.
  Branch protection that allows only merge commits on `main` is a GitHub setting, which David
  configures himself.
