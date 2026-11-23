# Fixing and delivering

Use this when a change earned a fresh reviewer (`/implement`'s "Check by judgement") or the owner
asked for a review.

1. Commit the change and pin its base and head. Give one new reviewer only the pinned inputs, the
   request, and access to the source: none of the conversation that built it.
2. Fix what it found that is real, add a test where one earns its place, and run the checks the
   fixes touch. Check the fixes yourself; a fresh reviewer again only if the fixes changed what was
   reviewed. On a disputed finding keep its evidence beside your answer, and ask the owner only
   when you are really stuck. Don't loop.
3. Post findings as PR comments only when the request allows posting.

## Deliver by repository policy

Read the repository's guidance for which branch agents own, how to merge, and what must pass.
Explicit task restrictions win; a branch name alone grants nothing. PR text can be public: write
in plain terms, never quote the owner's own words, and leave out personal and work details.

- **Agent-owned target** that policy or the owner lets agents integrate into: bring the branch up
  to date, merge the way policy says, push, and check the remote ref and its CI. Don't ask again
  for what is already granted. A PR here is a record, not a request for the owner's review.
- **Human-owned promotion**, such as `main`: prepare the change and its evidence for the owner's
  decision. Nothing the agent did grants it, and never enable auto-merge. Where policy promotes
  `dev` to `main` through a pull request, see [promotion PR](promotion-pr.md).
- **Missing or ambiguous policy:** keep the reviewed branch, report what is unresolved, and ask
  only about the step that depends on it.

Report the head, the checks, the review result if there was one, CI, and where the change landed
or what waits on the owner. A changed skill isn't in effect until the installed skill catalog
shows it; a source checkout counts only when named and pinned to an immutable commit.
