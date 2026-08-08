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
import shlex
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
PUSH_COMMAND = re.compile(r'git\s+push\b(?P<arguments>[^|&;\n]*)')

# Options whose following token is an option value rather than a repository or
# refspec. Long `--option=value` forms are handled separately below.
PUSH_OPTIONS_WITH_VALUE = {
    "--exec",
    "--push-option",
    "--receive-pack",
    "--recurse-submodules",
    "--repo",
    "-o",
}
UNBOUNDED_PUSH_OPTIONS = {"--all", "--branches", "--mirror"}

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


def push_uses_implicit_ref(command):
    """Whether a `git push` command leaves Git to select the ref to push.

    On `main`, `git push` and `git push origin` must be blocked because both
    can push the current branch. An explicit non-main refspec such as
    `git push origin feature/auth` is safe even when the checkout currently
    happens to be on `main`; the command does not target `main`.

    This remains deliberately conservative. If shell tokenization fails, or
    the command supplies no explicit refspec, treat it as implicit.
    """
    for match in PUSH_COMMAND.finditer(command):
        try:
            arguments = shlex.split(match.group("arguments"))
        except ValueError:
            return True

        positionals = []
        repository_from_option = False
        index = 0
        while index < len(arguments):
            argument = arguments[index]

            if argument == "--":
                positionals.extend(arguments[index + 1:])
                break

            if argument.startswith("--repo="):
                repository_from_option = True
                index += 1
                continue

            if argument in PUSH_OPTIONS_WITH_VALUE:
                if argument == "--repo":
                    repository_from_option = True
                index += 2
                continue

            if argument.startswith("-"):
                index += 1
                continue

            positionals.append(argument)
            index += 1

        # Without --repo, Git's first positional is the repository and any
        # later positional is a refspec. With --repo, every positional is a
        # refspec.
        refspecs = positionals if repository_from_option else positionals[1:]
        if not refspecs:
            return True

        # A source-only HEAD/@ refspec still resolves to the current branch.
        # A destination (`HEAD:feature/x`) makes the non-main target explicit.
        for refspec in refspecs:
            source_only = refspec.lstrip("+")
            if ":" not in source_only and source_only in {"HEAD", "@"}:
                return True

    return False


def push_can_update_main_broadly(command):
    """Whether a push can update main without naming it literally.

    Bulk branch options, matching refspecs (`:`), and wildcard refspecs can
    all include `main` from a checkout on some other branch. Block them
    unconditionally; there is no reliable textual proof that main is absent.
    """
    for match in PUSH_COMMAND.finditer(command):
        try:
            arguments = shlex.split(match.group("arguments"))
        except ValueError:
            return True

        for argument in arguments:
            if (
                len(argument) > 2
                and argument.startswith("--")
                and any(option.startswith(argument) for option in UNBOUNDED_PUSH_OPTIONS)
            ):
                return True

            refspec = argument.lstrip("+")
            if refspec == ":" or (":" in refspec and "*" in refspec):
                return True

    return False


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
    elif push_can_update_main_broadly(command):
        reason = (
            "uses a bulk or matching refspec that can update main without naming it. "
            "Push explicit non-main branches instead."
        )
    elif current_branch() == "main" and push_uses_implicit_ref(command):
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
