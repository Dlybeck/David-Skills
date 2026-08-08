# Analyze the existing skill's philosophy before adding to it — don't stack on top

When adding anything new to this plugin — a skill, a tracker backend, a gate — understand
*why* the existing pattern it resembles is shaped the way it is before building against it, and
either genuinely fit that shape or explicitly justify diverging from it. Copying a neighboring
skill's surface structure without checking the reasoning underneath it is stacking, not
integrating.

## Why this is a rule now, not just advice

The Jira issue-tracker template was built once, then rebuilt, because the first pass copied the
GitHub/GitLab templates' surface shape (a seed file `setup` fills in) without first
understanding *why* those two work well with almost no per-project variance: GitHub and GitLab
issues have one stable structure everywhere, so a single template genuinely covers every repo.
Jira doesn't have that property — issue-type schemes and workflows vary per project (verified
directly: two real Denali Jira projects use different subtask-type naming for the same concept)
— a fact that would have surfaced immediately from asking "why doesn't the GitHub template need
to discover anything live?" *before* writing the Jira one. Instead it surfaced after the fact,
on a second pass, alongside an unrelated stale-tool-name bug caught the same way.

## Consequence

A new addition that turns out not to fit an existing pattern's actual reasoning isn't
automatically wrong to build — Jira support was still worth adding, on its own terms. But the
analysis has to happen *before* building starts, not get discovered by a rebuild after
`/code-review` (or a user) catches it.
