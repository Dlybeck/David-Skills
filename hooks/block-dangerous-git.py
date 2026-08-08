#!/usr/bin/env python3
"""
BLOCK DANGEROUS GIT: hard-block two categories of git command before they
run, mechanical backstops rather than written discipline the agent has to
remember correctly every time:

1. Anything that touches `main` without a human directly at the keyboard --
   `git push` targeting `main` (any form) and `gh pr create`/`gh pr edit`
   with `--base main`. Scoped to `main` only: this repo's own policy is
   that pushing dev/feature branches is fine for an agent to do on its
   own, so this does NOT block those.
2. Local-destructive git operations that can silently lose uncommitted
   work or commits, regardless of which branch you're on: `git reset
   --hard`, `git clean -f`/`-fd`, `git branch -D`, `git checkout .` /
   `git restore .`. These aren't a branch-policy question the way #1 is --
   there's no "it's fine on a feature branch" case for discarding
   uncommitted changes or force-deleting a branch, so they're blocked
   unconditionally.

This supersedes the old misc/git-guardrails-claude-code skill, matching its
full blocked-pattern list but scoped more precisely on the push/PR side
(main only, not every push) and without depending on `jq`.

Heuristic on command text, not a real shell/git parser. Slight over-
blocking (refusing something that wasn't actually dangerous) is the
acceptable failure mode here, not the reverse. If this ever blocks
something legitimate, the escape hatch is running the command manually
outside Claude Code -- not disabling this hook.
"""
import re
import subprocess
import sys

from _shared import read_hook_input

# `main` as the push target: preceded by start/whitespace/colon/plus (so it
# doesn't false-positive on a branch like "feature/main-page"), followed by
# whitespace/quote/shell-separator/end (so "main-ish" doesn't match either).
PUSH_TO_MAIN = re.compile(
    r'git\s+push\b[^|&;\n]*?(?:^|[\s:+])(main|refs/heads/main)(?=[\s"\'&|;]|$)'
)
PR_BASE_MAIN = re.compile(r'gh\s+pr\s+(create|edit)\b[^|&;\n]*--base[= ]main\b')
BARE_PUSH = re.compile(r'git\s+push\b')

# Local-destructive patterns -- branch-agnostic, ported from
# git-guardrails-claude-code's DANGEROUS_PATTERNS with the same scope.
RESET_HARD = re.compile(r'git\s+reset\s+--hard\b')
CLEAN_FORCE = re.compile(r'git\s+clean\s+(-\w*f\w*|--force)\b')
BRANCH_FORCE_DELETE = re.compile(r'git\s+branch\s+-D\b')
DISCARD_ALL = re.compile(r'git\s+(checkout|restore)\s+\.(?:\s|$)')


def normalize_quoting(command):
    """Strip shell quote characters (`"` and `'`) from the command text
    before pattern matching, so `git push origin "main"` (or an
    interpolation-adjacent spelling like `"ma"in`, which a real shell
    concatenates to `main` the same way) matches exactly like the unquoted
    form. Purely textual, not shell-aware -- matching this hook's own
    heuristic, over-blocking-not-under-blocking policy: the boundary
    characters the patterns below check for (whitespace, `:`, `+`, `&`,
    `|`, `;`, end of string) are all still present after quotes are
    removed, so `feature/main-page` and similar stay unaffected."""
    return command.replace('"', '').replace("'", '')


def current_branch():
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except Exception:
        return ""


def main():
    data = read_hook_input()
    if data is None:
        return 0

    if data.get("tool_name") != "Bash":
        return 0

    command = (data.get("tool_input") or {}).get("command") or ""
    normalized = normalize_quoting(command)

    reason = None
    if PUSH_TO_MAIN.search(normalized):
        reason = (
            "pushes directly to main. main is human-gated, full stop -- an agent never "
            "pushes to it and never opens a PR into it, not even to hand a human a button "
            "to click. If the repo owner wants to promote dev -> main right now, that's a "
            "command they run themselves, not one this tool executes on their behalf."
        )
    elif PR_BASE_MAIN.search(normalized):
        reason = "opens a PR into main. Same rule as a direct push into main."
    elif BARE_PUSH.search(normalized) and current_branch() == "main":
        reason = "pushes the current branch (main) upstream. Same rule as a direct push."
    elif RESET_HARD.search(normalized):
        reason = (
            "runs `git reset --hard`, which can silently discard commits with no undo. "
            "If this is genuinely wanted, run it manually outside Claude Code."
        )
    elif CLEAN_FORCE.search(normalized):
        reason = (
            "runs a force `git clean`, which permanently deletes untracked files/directories. "
            "If this is genuinely wanted, run it manually outside Claude Code."
        )
    elif BRANCH_FORCE_DELETE.search(normalized):
        reason = (
            "runs `git branch -D`, which force-deletes a branch even if it has unmerged "
            "commits. If this is genuinely wanted, run it manually outside Claude Code."
        )
    elif DISCARD_ALL.search(normalized):
        reason = (
            "discards all uncommitted working-tree changes (`git checkout .` / "
            "`git restore .`). If this is genuinely wanted, run it manually outside "
            "Claude Code."
        )

    if reason:
        sys.stderr.write(f"DANGEROUS GIT COMMAND blocked: this command {reason}\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
