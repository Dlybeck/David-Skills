#!/usr/bin/env python3
"""
REQUIRE COMMITTED CLAIM: block dispatch into an isolated worktree or background
session -- a `claude --bg` launch, or a call to the `Workflow` tool -- while
the local markdown tracker (anything under `.scratch/`) has uncommitted
changes.

Why this exists: dispatched work starts from the last *commit*, not from this
checkout's working tree -- see `docs/agents/issue-tracker.md`'s "claim the
ticket" / "mark the ticket resolved" conventions for the full story, including
the incident that first surfaced the gap. Those conventions already say to
commit, in prose -- prose alone already missed it once, so this is the
mechanized backstop, same philosophy as `block-dangerous-git.py` applied to
git branch safety: a hook that can't forget beats an agent that has to
remember correctly every single time.

Scoped to the two dispatch mechanisms this plugin's skills actually use:
a Bash command that looks like a `claude --bg` launch, and any call of the
`Workflow` tool. Only fires when this repo's tracker is local markdown
(`.scratch/` exists) -- a real tracker (GitHub, Linear) claims via an API
call that's already visible everywhere the moment it's made, so this class of
bug can't happen there.

Heuristic on command text and a plain `git status`, not a real dispatch-
mechanism parser. Slight over-blocking (refusing a Workflow call that never
actually touches the tracker) is the acceptable failure mode here, not the
reverse -- matching block-dangerous-git.py's own stated policy. If this ever
blocks something legitimate, commit (or discard) the uncommitted tracker
change and retry -- don't disable this hook.
"""
import re
import subprocess
import sys
from pathlib import Path

from _shared import read_hook_input

BG_LAUNCH = re.compile(r'claude\b[^|&;\n]*--bg\b')
TRACKER_ROOT = Path(".scratch")


def dirty_tracker_files():
    """Uncommitted (staged, unstaged, or untracked) changes anywhere under
    .scratch/ -- tickets, but also spec.md and wayfinder's map.md, which the
    tracker convention's "commit both files together" Resolve step depends
    on just as much as a ticket file does. Narrowing this to */issues/*.md
    would silently miss map.md edits -- not a hypothetical, caught in review
    on this hook's own first pass."""
    try:
        out = subprocess.run(
            # --untracked-files=all: without it, a brand-new untracked directory
            # collapses to one line (the directory itself), not one line per file
            # inside it -- which silently hid exactly the case this hook exists to
            # catch (a freshly published, never-committed ticket file).
            ["git", "status", "--porcelain", "--untracked-files=all", "--", str(TRACKER_ROOT)],
            capture_output=True, text=True, timeout=5,
        )
    except Exception:
        return []
    if out.returncode != 0:
        return []
    return [line[3:].strip() for line in out.stdout.splitlines()]


def main():
    data = read_hook_input()
    if data is None:
        return 0

    tool_name = data.get("tool_name")
    tool_input = data.get("tool_input") or {}

    if tool_name == "Bash":
        command = tool_input.get("command") or ""
        if not BG_LAUNCH.search(command):
            return 0
    elif tool_name == "Workflow":
        pass  # any Workflow call can dispatch into an isolated worktree
    else:
        return 0

    if not TRACKER_ROOT.is_dir():
        return 0  # not this repo's tracker shape (e.g. GitHub issues) -- no gap to catch

    dirty = dirty_tracker_files()
    if not dirty:
        return 0

    sys.stderr.write(
        "BLOCKED: about to dispatch into a separate worktree/session "
        f"({tool_name}) while these tracker files have uncommitted changes:\n"
        + "\n".join(f"  {f}" for f in dirty)
        + "\n\nA claude --bg job and a Workflow agent's own worktree are both created "
        "from the last commit, not from this checkout's working tree -- an uncommitted "
        "'Status: claimed' (or 'resolved') is invisible to whatever you're about to "
        "dispatch, no matter how recent the change is. Commit (and push, if the worker "
        "won't share this checkout) the tracker change first, then retry.\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
