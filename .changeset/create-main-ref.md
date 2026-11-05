---
"david-skills": patch
---

The branch guard now lets an agent create a `main` that does not exist yet, so a new repository can
get its first branch without David running the command by hand. Only one command shape passes: a
plain `gh api repos/OWNER/REPO/git/refs` POST with a `ref` of `refs/heads/main` (or `master`) and a
literal 40-character commit sha, on its own. GitHub refuses that call if the branch already exists,
so it cannot move or delete one. Pushes to `main`, merges, ref updates and deletions stay blocked.
The guard also now catches two ways of hiding a `gh api` write from it: a `gh -R owner/repo api`
flag ahead of the subcommand, and a shell substitution (`$(...)`, a backtick, `$'..'`) that supplies
or splits the endpoint or method. A `gh api` call is blocked when it has one anywhere but inside a
quoted `-f`/`-F` value, so a reply body built with `"$(cat file)"` still works.
