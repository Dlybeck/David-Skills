---
"david-skills": patch
---

Inspect supported inline Python process calls and executable shell positions in the Git guard.
Block literal subprocess pushes to main while allowing inert search and inspection text.
Preserve proposed PRs for human review and document the static guard's enforcement limits.
Preserve command boundaries after comments and multiline quoted text, and inspect substitutions
in unquoted heredoc bodies without treating body quote characters as shell quoting.
Distinguish here-strings from heredocs, read complete delimiter words, and preserve and
conservatively inspect remaining commands when a heredoc body boundary cannot be established.
Ignore parentheses inside word-initial shell comments while locating command substitutions,
preserving newline boundaries and quoted, escaped, or within-word literal hashes.
