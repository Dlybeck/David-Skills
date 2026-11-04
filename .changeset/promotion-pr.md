---
"david-skills": minor
---

Finished work now reaches David as one `dev` -> `main` promotion PR. Agents open or update it on a
pasted ready signal, after checking tests and CI on one pinned `dev` SHA. Its report covers what
was asked for, what changed, how it was tested, and what is left open. Review comments are fixed on
the same PR and answered with a `🤖 Agent:` reply. The hook allows opening that PR only from `dev`
and blocks every agent merge into `main`/`master`: `gh pr merge` and auto-merge, `gh api` merge
and ref writes, and force-pushes of `dev`. The release accepts GitHub's "Create a merge commit"
promotion and refuses squash or rebase with a clear message.
