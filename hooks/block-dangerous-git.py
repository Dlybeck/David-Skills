#!/usr/bin/env python3
"""
BLOCK DANGEROUS GIT: hard-block two categories of git command before they
run, mechanical backstops rather than written discipline the agent has to
remember correctly every time:

1. Anything that writes `main` (or `master`) without a human directly at the
   keyboard: `git push` targeting it (any form), `gh pr merge` and
   `--auto` for a PR based on it (or whose base cannot be determined),
   `gh api` writes that merge PRs or move refs or contents, and
   `gh repo sync` of its remote. Also force-pushes and deletions of the
   shared `dev` integration branch, which is the head of the dev -> main
   promotion PR. Opening that PR is allowed: `gh pr create` into a
   protected branch only from head `dev`; retargeting a PR there with
   `gh pr edit --base` is blocked. Pushing dev/feature branches and merging
   PRs into dev/feature branches stay fine for an agent to do on its own.
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
outside Claude Code -- not disabling this hook. The one network call is
`gh pr view` to learn a PR's base before `gh pr merge`; any failure there
blocks. Scripts, other interpreters, and variables that build a command at
runtime are outside what text inspection can see.
"""
import os
import re
import shlex
import subprocess
import sys

from _shared import read_hook_input

# `main` as the push target: preceded by start/whitespace/colon/plus (so it
# doesn't false-positive on a branch like "feature/main-page"), followed by
# whitespace/quote/shell-separator/end (so "main-ish" doesn't match either).
PUSH_TO_MAIN = re.compile(
    r'git\s+push\b[^|&;\n]*?(?:^|[\s:+])((?:refs/heads/)?(?:main|master))(?=[\s"\'&|;]|$)'
)
PROTECTED_BRANCHES = {"main", "master"}
# The agent-owned integration branch: the only head a PR into a protected
# branch may come from, and never force-pushed or deleted by an agent.
INTEGRATION_BRANCH = "dev"
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

# `gh api` endpoints whose writes merge a PR, move a ref, or commit content
# (the contents API commits to the default branch unless told otherwise).
API_WRITE_ENDPOINTS = re.compile(
    r'(?:^|/)(?:pulls/[^/]+/merge|merges|merge-upstream|git/refs(?:/.*)?|contents(?:/.*)?)$'
)
GRAPHQL_WRITE_MUTATIONS = re.compile(
    r'\b(mergePullRequest|enablePullRequestAutoMerge|enqueuePullRequest|mergeBranch'
    r'|updateRefs?|deleteRef|createCommitOnBranch)\b'
)
API_OPTIONS_WITH_VALUE = {
    "-X", "--method", "-f", "--raw-field", "-F", "--field", "--input",
    "-H", "--header", "-q", "--jq", "-t", "--template", "--cache",
    "--hostname", "-p", "--preview",
}
API_FIELD_OPTIONS = {"-f", "--raw-field", "-F", "--field"}
PR_MERGE_OPTIONS_WITH_VALUE = {
    "-A", "--author-email", "-b", "--body", "-F", "--body-file",
    "--match-head-commit", "-R", "--repo", "-t", "--subject",
}
SHELL_OPERATORS = set(";&|()")


def simple_commands(command):
    """Split shell text into token lists, one per simple command. Returns
    None when the text cannot be tokenized (unbalanced quotes and the like);
    callers treat that as unknown, never as safe."""
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return None
    commands, current = [], []
    for token in tokens:
        if token and set(token) <= SHELL_OPERATORS:
            if current:
                commands.append(current)
            current = []
        else:
            current.append(token)
    if current:
        commands.append(current)
    return commands


def gh_invocations(command, *subcommand):
    """Yield the argument list after each `gh <subcommand...>` in the command.
    Arguments stop at the next `gh`/`git` word, since a newline does not
    survive tokenizing. Yields None once if the command is not tokenizable
    but textually mentions the subcommand."""
    commands = simple_commands(command)
    if commands is None:
        if re.search(r'\bgh\s+' + r'\s+'.join(subcommand) + r'\b', command):
            yield None
        return
    width = len(subcommand)
    for tokens in commands:
        for index, token in enumerate(tokens):
            if os.path.basename(token) != "gh":
                continue
            if tuple(tokens[index + 1:index + 1 + width]) != subcommand:
                continue
            arguments = []
            for argument in tokens[index + 1 + width:]:
                if os.path.basename(argument) in {"gh", "git"}:
                    break
                arguments.append(argument)
            yield arguments


def option_values(arguments, long_name, short_name=None):
    """Every value given for an option, in `--x v`, `--x=v`, `-x v` and
    `-xv` forms."""
    values = []
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument in {long_name, short_name}:
            if index + 1 < len(arguments):
                values.append(arguments[index + 1])
            index += 2
            continue
        if argument.startswith(long_name + "="):
            values.append(argument[len(long_name) + 1:])
        elif short_name and argument.startswith(short_name) and len(argument) > 2 \
                and not argument.startswith("--"):
            values.append(argument[2:])
        index += 1
    return values


def positionals(arguments, options_with_value):
    found = []
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument == "--":
            found.extend(arguments[index + 1:])
            break
        if argument in options_with_value:
            index += 2
            continue
        if not argument.startswith("-"):
            found.append(argument)
        index += 1
    return found


def short_branch(ref):
    ref = ref.lstrip("+")
    return ref[len("refs/heads/"):] if ref.startswith("refs/heads/") else ref


def pr_create_problem(arguments, context_changed):
    """A PR into a protected branch (or into the repo default, when no
    --base is given) is allowed only from head `dev`."""
    if arguments is None:
        return "opens a PR whose base and head cannot be read from the command text."
    bases = option_values(arguments, "--base", "-B")
    if bases and all(short_branch(base) not in PROTECTED_BRANCHES for base in bases):
        return None
    heads = option_values(arguments, "--head", "-H")
    if heads:
        head = heads[-1]
    elif context_changed:
        return ("opens a PR into main/master (or the default branch) after changing "
                "directory, so its head is unknown. Pass --head dev explicitly.")
    else:
        head = current_branch()
    if head == INTEGRATION_BRANCH:
        return None
    target = "main/master" if bases else "the default branch (no --base given)"
    return (f"opens a PR into {target} from {head or 'an unknown head'!s}. Only the "
            f"dev -> main promotion PR may target a protected branch; pass --head dev, "
            f"or pass an explicit non-main --base for any other PR.")


def pr_edit_problem(arguments):
    if arguments is None:
        return "edits a PR in a way that cannot be read from the command text."
    if any(short_branch(base) in PROTECTED_BRANCHES
           for base in option_values(arguments, "--base", "-B")):
        return ("retargets a PR onto main/master. Only the dev -> main promotion PR may "
                "target it, and it is opened with gh pr create --head dev.")
    return None


def pr_merge_base(arguments, context_changed):
    """Look up the base branch of the PR `gh pr merge` would merge. Returns
    the branch name, or None when it cannot be determined."""
    selector = positionals(arguments, PR_MERGE_OPTIONS_WITH_VALUE)[:1]
    repo = option_values(arguments, "--repo", "-R")[-1:]
    if context_changed and not repo and not (selector and "://" in selector[0]):
        return None
    view = ["gh", "pr", "view", *selector, "--json", "baseRefName", "--jq", ".baseRefName"]
    if repo:
        view += ["--repo", repo[0]]
    try:
        out = subprocess.run(view, capture_output=True, text=True, timeout=20)
    except Exception:
        return None
    base = out.stdout.strip()
    return base if out.returncode == 0 and base else None


def pr_merge_problem(arguments, context_changed):
    if arguments is None:
        return "merges a PR in a way that cannot be read from the command text."
    base = pr_merge_base(arguments, context_changed)
    if base is None:
        return ("merges a PR (or enables auto-merge) whose base branch could not be "
                "determined with gh pr view. Merges into main/master are the owner's; "
                "name the PR explicitly so its base can be checked.")
    if base in PROTECTED_BRANCHES:
        return (f"merges a PR (or enables auto-merge) into {base}. Only the repository "
                f"owner merges into {base}.")
    return None


def graphql_text(arguments):
    """The GraphQL document(s) a `gh api graphql` call would send, or None
    when part of it comes from somewhere this hook cannot read."""
    texts = []
    for name, short in (("--raw-field", "-f"), ("--field", "-F")):
        for value in option_values(arguments, name, short):
            _, _, field = value.partition("=")
            if field.startswith("@"):
                try:
                    with open(field[1:], encoding="utf-8") as stream:
                        texts.append(stream.read())
                except Exception:
                    return None
            else:
                texts.append(field)
    for path in option_values(arguments, "--input"):
        try:
            with open(path, encoding="utf-8") as stream:
                texts.append(stream.read())
        except Exception:
            return None
    return "\n".join(texts)


def api_problem(arguments):
    if arguments is None:
        return "calls gh api in a way that cannot be read from the command text."
    endpoints = positionals(arguments, API_OPTIONS_WITH_VALUE)
    endpoint = endpoints[0].split("?", 1)[0].strip("/") if endpoints else ""
    if endpoint == "graphql":
        text = graphql_text(arguments)
        if text is None:
            return ("sends a GraphQL document from a file or stdin this hook cannot read. "
                    "Inline the query so it can be checked for merge and ref mutations.")
        match = GRAPHQL_WRITE_MUTATIONS.search(text)
        if match:
            return (f"runs the GraphQL mutation {match.group(1)}, which can merge a PR or "
                    f"move a branch, including main.")
        return None
    methods = [m.upper() for m in option_values(arguments, "--method", "-X")]
    has_fields = any(option_values(arguments, name, short) for name, short in
                     (("--raw-field", "-f"), ("--field", "-F"))) \
        or bool(option_values(arguments, "--input"))
    method = methods[-1] if methods else ("POST" if has_fields else "GET")
    if method != "GET" and API_WRITE_ENDPOINTS.search(endpoint):
        return (f"writes {endpoint} through gh api ({method}), which can merge a PR, move "
                f"a branch, or commit to main. Use git and gh pr commands for non-main "
                f"branches instead.")
    return None


def repo_sync_problem(arguments):
    if arguments is None:
        return "syncs a repository in a way that cannot be read from the command text."
    if not positionals(arguments, {"-b", "--branch", "-s", "--source"}):
        return None  # Syncs the local checkout only.
    branches = option_values(arguments, "--branch", "-b")
    if branches and all(short_branch(b) not in PROTECTED_BRANCHES for b in branches):
        return None
    return ("syncs a remote repository's main/master (or default) branch, which "
            "writes it. Name a non-main --branch instead.")


def push_flags_and_refspecs(arguments):
    """Split `git push` arguments into option flags and refspecs, using the
    same repository/refspec rule as push_uses_implicit_ref."""
    flags, found = [], []
    repository_from_option = False
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument == "--":
            found.extend(arguments[index + 1:])
            break
        if argument.startswith("--repo="):
            repository_from_option = True
        elif argument in PUSH_OPTIONS_WITH_VALUE:
            repository_from_option |= argument == "--repo"
            index += 2
            continue
        elif argument.startswith("-"):
            flags.append(argument)
        else:
            found.append(argument)
        index += 1
    return flags, (found if repository_from_option else found[1:])


def push_rewrites_dev(command):
    """Whether a push force-updates or deletes the shared `dev` branch."""
    for match in PUSH_COMMAND.finditer(command):
        try:
            arguments = shlex.split(match.group("arguments"))
        except ValueError:
            return INTEGRATION_BRANCH in match.group("arguments")
        flags, refspecs = push_flags_and_refspecs(arguments)
        short_flags = "".join(f[1:] for f in flags if not f.startswith("--"))
        force = "f" in short_flags or any(
            f == "--force" or f.startswith("--force-with-lease") for f in flags)
        delete = "d" in short_flags or "--delete" in flags
        if not refspecs:
            if force and current_branch() == INTEGRATION_BRANCH:
                return True
            continue
        for refspec in refspecs:
            source, colon, destination = refspec.partition(":")
            if not colon:
                destination = source
            if destination.lstrip("+") in {"HEAD", "@"}:
                destination = current_branch()
            if short_branch(destination) != INTEGRATION_BRANCH:
                continue
            if force or delete or refspec.startswith("+") or (colon and not source):
                return True
    return False


def normalize_git_options(command):
    """Expose Git subcommands behind global options to the existing guards.

    This is still a shell-text heuristic, not an authorization sandbox. When
    options or a shell cd can change ref resolution, require explicit push
    destinations rather than trusting the hook process's current branch.
    """
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return command, True
    output = []
    context_changed = "cd" in tokens
    index = 0
    value_options = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--config-env"}
    while index < len(tokens):
        token = tokens[index]
        output.append(token)
        index += 1
        if token != "git":
            continue
        while index < len(tokens) and tokens[index].startswith("-"):
            option = tokens[index]
            if option in value_options:
                context_changed = True
                index += 2
            elif option == "--":
                index += 1
                break
            else:
                if option not in {"--no-pager", "--paginate", "--no-optional-locks"}:
                    context_changed = True
                index += 1
    return " ".join(token if set(token) <= set(";&|()") else shlex.quote(token)
                    for token in output), context_changed


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


def push_problem(command, normalized, context_changed):
    if PUSH_TO_MAIN.search(normalized):
        return (
            "pushes directly to main/master. It is human-gated, full stop -- an agent "
            "never pushes to it or merges into it. Work reaches main only through the "
            "dev -> main promotion PR, which the repository owner merges."
        )
    if push_rewrites_dev(command):
        return (
            "force-pushes or deletes dev. dev is the shared integration branch and the "
            "head of the dev -> main promotion PR; add new commits instead of rewriting it."
        )
    if push_can_update_main_broadly(command):
        return (
            "uses a bulk or matching refspec that can update main without naming it. "
            "Push explicit non-main branches instead."
        )
    if context_changed and push_uses_implicit_ref(command):
        return ("leaves the push target implicit where it can resolve to main. Name an "
                "explicit non-main destination.")
    branch = current_branch()
    if branch in PROTECTED_BRANCHES and push_uses_implicit_ref(command):
        return f"pushes the current branch ({branch}) upstream. Same rule as a direct push to main."
    return None


def gh_problem(command, context_changed):
    """The first blocked `gh` call in the command. The merge check runs last
    because it is the only one that makes a network call."""
    checks = (
        (("pr", "create"), lambda arguments: pr_create_problem(arguments, context_changed)),
        (("pr", "edit"), pr_edit_problem),
        (("api",), api_problem),
        (("repo", "sync"), repo_sync_problem),
        (("pr", "merge"), lambda arguments: pr_merge_problem(arguments, context_changed)),
    )
    for subcommand, check in checks:
        for arguments in gh_invocations(command, *subcommand):
            problem = check(arguments)
            if problem:
                return problem
    return None


def destructive_problem(normalized):
    if RESET_HARD.search(normalized):
        return (
            "runs `git reset --hard`, which can silently discard commits with no undo. "
            "If this is genuinely wanted, run it manually outside Claude Code."
        )
    if CLEAN_FORCE.search(normalized):
        return (
            "runs a force `git clean`, which permanently deletes untracked files/directories. "
            "If this is genuinely wanted, run it manually outside Claude Code."
        )
    if BRANCH_FORCE_DELETE.search(normalized):
        return (
            "runs `git branch -D`, which force-deletes a branch even if it has unmerged "
            "commits. If this is genuinely wanted, run it manually outside Claude Code."
        )
    if DISCARD_ALL.search(normalized):
        return (
            "discards all uncommitted working-tree changes (`git checkout .` / "
            "`git restore .`). If this is genuinely wanted, run it manually outside "
            "Claude Code."
        )
    return None


def main():
    data = read_hook_input()
    if data is None:
        return 0

    if data.get("tool_name") != "Bash":
        return 0

    command = (data.get("tool_input") or {}).get("command") or ""
    command, context_changed = normalize_git_options(command)
    normalized = normalize_quoting(command)

    reason = (
        push_problem(command, normalized, context_changed)
        or gh_problem(command, context_changed)
        or destructive_problem(normalized)
    )
    if reason:
        sys.stderr.write(f"DANGEROUS GIT COMMAND blocked: this command {reason}\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
