# Promotion PR

The one open pull request from the agent-owned `dev` into the owner's `main` (or `master`).
Merging it is how the owner makes a release official, so only the owner merges, approves, or
closes it, and the plugin hook enforces that. In a fork with an `upstream` remote, give every
`gh` command `--repo <owner>/<repo>` for `origin`.

## Open or update it

Open or update it when the owner asks for a release, directly or through whoever relays for
them; finishing a task is not that request. First check one pinned `dev` SHA: local `dev` equals
`origin/dev`, the repository's required tests pass on it, and its CI is green
(`gh run list --commit <sha>`). If any check fails, report it and open nothing.

Then `gh pr list --base main --head dev --state open`. One open: update its body, keeping the
other sections. None: `gh pr create --base main --head dev`. More than one: report them and
change neither.

The report accounts for all of `main..dev`: a short section per piece of work (what was asked,
what changed, how it was checked, what is left open) and anything else under **Also on dev**. It
ends with: merge with **Create a merge commit**, since a squash or rebase makes the release
refuse. The repository can be public, so write in plain terms, never quote the owner's own
words, and leave out personal and work details.

## Review comments

When the owner comments, fix through `dev` the usual way; the PR's head is `dev`, so pushing `dev`
updates it. Reply to each comment with `🤖 Agent: <what changed> in <sha>`, or the answer, and
skip comments that start `🤖 Agent:`, which are agents' own. Refresh the report. Resolving
threads is the owner's.

`dev` only moves forward: it is the PR's head, so never rewrite it.
