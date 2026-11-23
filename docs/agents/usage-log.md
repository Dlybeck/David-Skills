# Usage log

How David-Skills is actually used, kept so the skills can be revised from real use rather than
from feelings (Dev Plan decisions 29, 45 and 61). Logging started on 2026-11-22; the first build
also read back every chat kept since 2026-10-18.

## The idea

Claude Code already records each chat as it happens: every prompt, skill load and tool call, with
its time, folder and branch. Recording it a second time would add parts without adding
knowledge, so the log is built from those transcripts. What was missing, and what this adds:

- **One durable place.** A compact record per chat in the log folder, on a big disk, that
  outlives the transcripts wherever they end up.
- **How the work ended.** Filled in afterwards: from GitHub for a pull request, from git for a
  branch (merged into `dev` or `main`, still open, no commits yet, gone), and from David, whose
  word wins (accepted, abandoned, redone, ...).
- **Answers without digging.** One report: which skills were used, how often, in which projects,
  in what order within a piece of work, how long it took, where David stepped in, how many
  reviews or checks ran, and which skill sequences ended well.

Nothing in a chat behaves differently. The hook only starts a background read of the transcripts
when a chat opens, at most every 15 minutes, and is silent.

## Using it

The tool is [`hooks/usage-log.py`](../../hooks/usage-log.py). On David's machine the log folder is
`/srv/downloads/logs/david-skills` (set by `setup`, stored in
`~/.config/david-skills/usage-log.json`).

```bash
python3 hooks/usage-log.py report --since 2026-11-22
python3 hooks/usage-log.py outcome "Proj:feat/thing" redone --note "wrong approach"
python3 hooks/usage-log.py update
```

David's part is gathered into one moment: when he circles back to the skills, the chat reading
the log asks him about the pieces of work git can't settle ("abandoned or redone?") and records
his answers with `outcome`, naming the work as the report does (a PR link, `project:branch`, or
`project:session:<id>`). He can also just tell a chat in this repo at any time. Chats in other
projects don't know about the log, on purpose: nothing in a skill changed for it.

## Reading it honestly

- **A piece of work** is a pull request when the chat linked one, else its branch, else the chat.
- **"David stepped in"** counts prompts the harness marks as typed by a person in chats David
  started. A chat started by another chat or a background job has its opening brief counted as an
  agent's, not his. Messages relayed from his phone through another session are not counted.
- **Skill uses** are explicit loads (the model's Skill calls, David's slash commands, and loads
  inside subagents). A skill an agent follows from a reference without loading it is not seen.
- **Reviews or checks** are subagent dispatches whose description mentions review, verify or audit,
  plus review-skill loads.
- Codex chats are not read yet: none since 2026-10-12, and their files are compressed.
