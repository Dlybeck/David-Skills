#!/usr/bin/env python3
"""
BLOCK DANGEROUS GIT: hard-block two categories of git command before they
run, mechanical backstops rather than written discipline the agent has to
remember correctly every time:

1. Anything that writes `main` (or `master`) without a human directly at the
   keyboard: `git push` targeting it (any form), `gh pr merge` and
   `--auto` for a PR based on it (or whose base cannot be determined),
   `gh api` writes that merge PRs or move refs or contents,
   `gh repo sync` of its remote, and gh aliases, which could hide any of these. Also force-pushes and deletions of the
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
SHELL_OPERATORS = set(";&|()\n")
DIRECTORY_CHANGERS = {"cd", "pushd", "popd"}
GH_FLAGS_WITH_VALUE = {"-R", "--repo"}
GH_SINGLE_WORD_COMMANDS = {"api", "browse", "status", "completion", "help"}
# gh's own top-level commands. Any other first word is an alias or an
# extension; aliases can hide `pr merge` or `api`, so they are looked up.
GH_COMMANDS = {
    "agent-task", "alias", "api", "attestation", "auth", "browse", "cache", "codespace",
    "completion", "config", "copilot", "extension", "gist", "gpg-key", "help", "issue",
    "label", "org", "pr", "preview", "project", "release", "repo", "ruleset", "run",
    "search", "secret", "ssh-key", "status", "variable", "workflow",
}
# Variables that point gh at another repository or host than the hook's own.
GH_TARGET_VARIABLES = re.compile(r'\bGH_REPO\b')
GH_HOST_VARIABLE = re.compile(r'\bGH_HOST\b')


def is_option_prefix(flag, *options, minimum=3):
    """Whether a long flag is an abbreviation of one of `options`; Git
    accepts any unambiguous prefix of a long option."""
    return len(flag) >= minimum and any(option.startswith(flag) for option in options)


# A heredoc operator and its delimiter word: quoted ('END', "END"),
# backslash-escaped (\END) or bare, including hyphens (END-OF-BODY).
HEREDOC_AT = re.compile(
    r"""<<(-?)[ \t]*(?:'([^'\n]+)'|"([^"\n]+)"|\\?([A-Za-z_][^\s;&|()<>'"]*))"""
)


def heredoc_delimiter(match):
    return next(group for group in match.groups()[1:] if group is not None)
SHELLS = {"bash", "sh", "zsh", "dash", "ksh", "mksh", "ash", "fish"}
# Words that run a `-c` script argument: the shells, and script(1).
SCRIPT_RUNNERS = SHELLS | {"script"}
# A shell reading stdin, by bare name or path (/bin/bash, /usr/bin/env bash).
SHELL_READER = re.compile(r"(?:^|[\s;&|(/])(?:" + "|".join(sorted(SHELLS)) + r")(?=\s|$)")


def skip_heredoc_bodies(command, index, pending, keep=None):
    """Consume the bodies of `pending` heredocs starting at `index` (the line
    after their operators). Appends kept lines to `keep` when given. Returns
    the index after the last delimiter line."""
    length = len(command)
    for strip_tabs, delimiter in pending:
        while index < length:
            end = command.find("\n", index)
            end = length if end < 0 else end
            body_line = command[index:end]
            index = end + 1
            if (body_line.lstrip("\t") if strip_tabs else body_line) == delimiter:
                break
            if keep is not None:
                keep.append(body_line + "\n")
    return index


def substitution_end(command, start, closer):
    """Index of the `)` or backtick closing a command substitution whose text
    starts at `start`, or -1 when it is not closed. Quotes, nested parentheses
    and heredoc bodies inside it are skipped."""
    depth, quote, pending = 1, None, []
    index, length = start, len(command)
    while index < length:
        char = command[index]
        if quote:
            if char == quote:
                quote = None
            elif char == "\\" and quote == '"':
                index += 1
            index += 1
            continue
        if char == "\\":
            index += 2
            continue
        if closer == "`":
            if char == "`":
                return index
        elif char in "'\"":
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
        elif command.startswith("<<", index) and not command.startswith("<<<", index):
            match = HEREDOC_AT.match(command, index)
            if match:
                pending.append((match.group(1) == "-", heredoc_delimiter(match)))
                index = match.end()
                continue
        elif char == "\n" and pending:
            index = skip_heredoc_bodies(command, index + 1, pending)
            pending = []
            continue
        index += 1
    return -1


def without_heredoc_bodies_and_comments(command):
    """Rewrite shell text into what its commands are, for tokenizing:

    - heredoc bodies are dropped as data (report text often holds an
      unbalanced apostrophe), unless a shell reads them;
    - comments are dropped; a mid-word `#` (fixes#3) is not one;
    - backslash-newline is joined where the shell joins it, outside single
      quotes, comments and quoted heredoc bodies;
    - a command substitution inside double quotes ("$(...)" or "`...`") is
      lifted out as its own lines, rewritten the same way, so the commands
      it runs are seen.

    One quote-aware scan does all of it, so `<<EOF` or `#` inside a quoted
    string counts for nothing. Text it cannot follow (an unclosed
    substitution) is returned unchanged rather than guessed at."""
    out, line = [], []
    pending = []
    quote = None
    index, length = 0, len(command)

    def emit(text):
        out.append(text)
        line.append(text)

    while index < length:
        char = command[index]
        if quote == "'":
            emit(char)
            if char == "'":
                quote = None
            index += 1
            continue
        if char == "\\" and index + 1 < length:
            if command[index + 1] == "\n":
                index += 2
            else:
                emit(command[index:index + 2])
                index += 2
            continue
        if quote == '"':
            if char == "`" or command.startswith("$(", index):
                opener, closer = (1, "`") if char == "`" else (2, ")")
                end = substitution_end(command, index + opener, closer)
                if end < 0:
                    return command
                inner = without_heredoc_bodies_and_comments(command[index + opener:end])
                emit('"\n' + inner + '\n"')
                index = end + 1
                continue
            emit(char)
            if char == '"':
                quote = None
            index += 1
            continue
        if char == "`":
            # An unquoted backtick substitution sticks to its neighbours as
            # one word; lift it out as its own lines, like a quoted one.
            end = substitution_end(command, index + 1, "`")
            if end < 0:
                return command
            emit("\n" + without_heredoc_bodies_and_comments(command[index + 1:end]) + "\n")
            index = end + 1
            continue
        if char in "'\"":
            quote = char
            emit(char)
            index += 1
            continue
        if char == "#" and (not line or "".join(line)[-1:].isspace()
                            or "".join(line)[-1:] in SHELL_OPERATORS):
            while index < length and command[index] != "\n":
                index += 1
            continue
        if command.startswith("<<", index) and not command.startswith("<<<", index):
            match = HEREDOC_AT.match(command, index)
            if match:
                pending.append((match.group(1) == "-", heredoc_delimiter(match)))
                emit(match.group(0))
                index = match.end()
                continue
        if char == "\n":
            emit(char)
            keep = [] if SHELL_READER.search("".join(line)) else None
            line = []
            index = skip_heredoc_bodies(command, index + 1, pending, keep)
            out.extend(keep or [])
            pending = []
            continue
        emit(char)
        index += 1
    return "".join(out)


def shell_tokens(command):
    """Tokenize shell text, keeping unquoted newlines as operator tokens.
    Heredoc bodies and comments are removed first; shlex's own comment rule
    would also start one at a mid-word `#`. Returns None when the text cannot
    be tokenized (unbalanced quotes and the like); callers treat that as
    unknown, never as safe."""
    command = without_heredoc_bodies_and_comments(command)
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()\n")
        lexer.whitespace = " \t\r"
        lexer.whitespace_split = True
        lexer.commenters = ""
        return list(lexer)
    except ValueError:
        return None


def branch_switched(command):
    """Whether the command changes the checked-out branch, so the hook's own
    current branch and current-branch PR may not describe all of it."""
    for tokens in simple_commands(command) or []:
        for index, token in enumerate(tokens[:-1]):
            following = tokens[index + 1]
            if os.path.basename(token) == "git" and following in {"checkout", "switch", "worktree"}:
                return True
            if os.path.basename(token) == "gh" and tokens[index + 1:index + 3] == ["pr", "checkout"]:
                return True
    return False


def switch_target(arguments):
    """The branch a `git checkout`/`git switch` lands on, or None when it
    cannot be read: a new branch from -b/-c, else an existing local branch.
    A path checkout (`--`, or a name that is not a local branch) is unknown."""
    for option in ("-b", "-B", "-c", "-C"):
        values = option_values(arguments, option)
        if values:
            return values[-1]
    if "--" in arguments:
        return None
    names = [argument for argument in arguments if not argument.startswith("-")]
    if len(names) != 1:
        return None
    try:
        known = subprocess.run(
            ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{names[0]}"],
            capture_output=True, timeout=5,
        ).returncode == 0
    except Exception:
        return None
    return names[0] if known else None


NOT_A_SWITCH = object()


def uses_current_branch(tokens):
    """Whether a simple command acts on the current branch: a push, or a gh
    PR create/merge that may default to it, including inside a script it
    runs (`sh -c`, `eval`)."""
    for index, token in enumerate(tokens):
        for script in embedded_scripts(tokens, index):
            inner = simple_commands(script)
            if inner is None or any(uses_current_branch(part) for part in inner):
                return True
        if index == len(tokens) - 1:
            break
        name = os.path.basename(token)
        if name == "git" and tokens[index + 1] == "push":
            return True
        if name == "gh" and tokens[index + 1:index + 3] in (["pr", "create"], ["pr", "merge"]):
            return True
    return False


def possible_branches(command, switched):
    """The branches the command's pushes and PR commands may run on, with
    None for a switch that cannot be read (gh pr checkout, git worktree, a
    path).

    When every operator from the first switch to the last command that acts
    on the current branch is `&&`, a failed switch stops the chain, so each
    such command runs on the branch of the last switch before it (or the
    starting branch, before any switch): only those branches count. Any
    other shape counts the starting branch and every switch target."""
    start = current_branch()
    if not switched:
        return {start}
    segments, current = [], []
    for token in shell_tokens(command) or []:
        if token and set(token) <= SHELL_OPERATORS:
            segments.append((current, token))
            current = []
        else:
            current.append(token)
    segments.append((current, ""))

    every, used = {start}, set()
    branch = start
    first_switch = last_user = None
    for position, (tokens, _) in enumerate(segments):
        for index, token in enumerate(tokens[:-1]):
            target = NOT_A_SWITCH
            if os.path.basename(token) == "gh" and tokens[index + 1:index + 3] == ["pr", "checkout"]:
                target = None
            elif os.path.basename(token) == "git" and tokens[index + 1] == "worktree":
                target = None
            elif os.path.basename(token) == "git" and tokens[index + 1] in {"checkout", "switch"}:
                target = switch_target(tokens[index + 2:])
            if target is not NOT_A_SWITCH:
                every.add(target)
                branch = target
                if first_switch is None:
                    first_switch = position
        if uses_current_branch(tokens):
            used.add(branch)
            last_user = position
    if first_switch is None or last_user is None:
        return every
    chained = all(operator == "&&" for _, operator in segments[first_switch:last_user])
    return used if chained else every


def simple_commands(command):
    """Split shell text into token lists, one per simple command, at shell
    operators and unquoted newlines. Returns None when the text cannot be
    tokenized."""
    tokens = shell_tokens(command)
    if tokens is None:
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


def gh_calls(command):
    """Yield (words, flags) for each `gh` call: its subcommand words in order,
    and the flags given between them (gh accepts `gh pr -R x merge`). Flags
    that take a value carry it. Yields None once if the command cannot be
    tokenized but mentions gh."""
    commands = simple_commands(command)
    if commands is None:
        if re.search(r'\bgh\b', command):
            yield None
        return
    for tokens in commands:
        for index, token in enumerate(tokens):
            scripts = embedded_scripts(tokens, index)
            for script in scripts:
                yield from gh_calls(script)
            if scripts:
                continue
            if os.path.basename(token) != "gh":
                continue
            words, flags = [], []
            rest = tokens[index + 1:]
            position = 0
            while position < len(rest):
                argument = rest[position]
                if argument in GH_FLAGS_WITH_VALUE:
                    flags.extend(rest[position:position + 2])
                    position += 2
                elif argument.startswith("-"):
                    flags.append(argument)
                    position += 1
                else:
                    words.append(argument)
                    position += 1
                    if len(words) == 2 or words[0] in GH_SINGLE_WORD_COMMANDS:
                        break
            yield words, flags, rest[position:]


def gh_invocations(command, *subcommand):
    """Yield the argument list of each `gh <subcommand...>` call, with any
    flags given before the subcommand included. Yields None once if the
    command is not tokenizable but mentions gh."""
    for call in gh_calls(command):
        if call is None:
            yield None
            return
        words, flags, arguments = call
        if tuple(words[:len(subcommand)]) == subcommand:
            yield flags + list(words[len(subcommand):]) + arguments


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
    """The branch a ref names; Git resolves both `refs/heads/x` and `heads/x`."""
    ref = ref.lstrip("+")
    for prefix in ("refs/heads/", "heads/"):
        if ref.startswith(prefix):
            return ref[len(prefix):]
    return ref


def gh_aliases():
    """Names of the user's gh aliases, or None when they cannot be listed."""
    try:
        out = subprocess.run(["gh", "alias", "list"], capture_output=True, text=True, timeout=10)
    except Exception:
        return None
    if out.returncode != 0:
        # gh exits non-zero with "no aliases configured" on an empty list.
        return set() if "no aliases" in (out.stdout + out.stderr).lower() else None
    return {line.split(":", 1)[0].strip() for line in out.stdout.splitlines() if ":" in line}


def gh_alias_problem(calls):
    """gh aliases can expand to any command, so defining one is blocked and
    using one is blocked; the full command is always available instead."""
    unknown = set()
    for words, _, _ in calls:
        if words[:1] == ["alias"] and words[1:2] and words[1] in {"set", "import"}:
            return ("defines a gh alias. An alias can hide a merge into main from this "
                    "check; run the full gh command instead.")
        if words and words[0] not in GH_COMMANDS:
            unknown.add(words[0])
    if not unknown:
        return None
    aliases = gh_aliases()
    if aliases is None:
        return (f"runs gh {sorted(unknown)[0]}, which is not a gh command, and gh aliases "
                f"could not be listed to rule out an alias. Run the full gh command instead.")
    hidden = sorted(unknown & aliases)
    if hidden:
        return (f"runs the gh alias {hidden[0]}, which this check cannot see through. Run "
                f"the full gh command instead.")
    return None


def pr_create_problem(arguments, context_changed, branches):
    """A PR into a protected branch (or into the repo default, when no
    --base is given) is allowed only from head `dev`. `branches` are the
    branches the command may be on (see possible_branches)."""
    if arguments is None:
        return "opens a PR whose base and head cannot be read from the command text."
    bases = option_values(arguments, "--base", "-B")
    if bases and all(short_branch(base) not in PROTECTED_BRANCHES for base in bases):
        return None
    heads = option_values(arguments, "--head", "-H")
    if heads:
        head = heads[-1]
    elif context_changed or len(branches) != 1 or None in branches:
        return ("opens a PR into main/master (or the default branch) after changing "
                "directory or branch, so its head is unknown. Pass --head dev explicitly.")
    else:
        head = next(iter(branches))
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


def pr_merge_base(arguments, context_changed, command, switched):
    """Look up the base branch of the PR `gh pr merge` would merge. Returns
    the branch name, or None when it cannot be determined."""
    selector = positionals(arguments, PR_MERGE_OPTIONS_WITH_VALUE)[:1]
    repo = option_values(arguments, "--repo", "-R")[-1:]
    explicit = bool(repo) or bool(selector and "://" in selector[0])
    # The lookup runs in this hook's own directory and environment, so a
    # command that changes either can make it check a different PR.
    if (context_changed or GH_TARGET_VARIABLES.search(command)) and not explicit:
        return None
    if GH_HOST_VARIABLE.search(command):
        return None
    # Without a selector gh merges the current branch's PR, and the command
    # may have switched branch before it runs.
    if switched and not selector:
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


def pr_merge_problem(arguments, context_changed, command, switched):
    if arguments is None:
        return "merges a PR in a way that cannot be read from the command text."
    base = pr_merge_base(arguments, context_changed, command, switched)
    if base is None:
        selector = positionals(arguments, PR_MERGE_OPTIONS_WITH_VALUE)[:1]
        if GH_HOST_VARIABLE.search(command):
            fix = "drop GH_HOST from the command and run the merge on its own"
        elif context_changed or GH_TARGET_VARIABLES.search(command):
            fix = ("pass --repo owner/name, since the command changes the directory or gh's "
                   "target repository")
        elif switched and not selector:
            fix = "name the PR number, since the command switches branch first"
        else:
            fix = "name the PR explicitly"
        return ("merges a PR (or enables auto-merge) whose base branch could not be "
                "determined with gh pr view. Merges into main/master are the owner's; "
                f"{fix}, so its base can be checked.")
    if base in PROTECTED_BRANCHES:
        return (f"merges a PR (or enables auto-merge) into {base}. Only the repository "
                f"owner merges into {base}.")
    return None


def graphql_text(arguments):
    """The GraphQL document(s) a `gh api graphql` call would send, or None
    when part of it comes from somewhere this hook cannot read. A query
    built by a command substitution ("$(cat <<'EOF' ...)") reaches this
    check empty, since the substitution is lifted out as its own command,
    so a missing or empty query is unreadable too."""
    texts = []
    has_query = bool(option_values(arguments, "--input"))
    for name, short in (("--raw-field", "-f"), ("--field", "-F")):
        for value in option_values(arguments, name, short):
            key, _, field = value.partition("=")
            if key == "query":
                if not field.strip():
                    return None
                has_query = True
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
    return "\n".join(texts) if has_query else None


def api_problem(arguments):
    if arguments is None:
        return "calls gh api in a way that cannot be read from the command text."
    endpoints = positionals(arguments, API_OPTIONS_WITH_VALUE)
    endpoint = endpoints[0].split("?", 1)[0] if endpoints else ""
    # gh accepts absolute URLs; check the path whatever host it names.
    endpoint = re.sub(r"^[A-Za-z][A-Za-z0-9+.-]*://[^/]*", "", endpoint).strip("/")
    if endpoint == "graphql" or endpoint.endswith("/graphql"):
        text = graphql_text(arguments)
        if text is None:
            return ("sends a GraphQL document this hook cannot read (a missing query, stdin, an "
                    "unreadable file, or a command substitution). Pass the query inline or with "
                    "-F query=@file so it can be checked for merge and ref mutations.")
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
            # A redirection glued to the word (`dev>/tmp/log`) is not part of it.
            word = re.split(r"[0-9]*[<>]", argument, maxsplit=1)[0]
            if word:
                found.append(word)
        index += 1
    return flags, (found if repository_from_option else found[1:])


def embedded_scripts(tokens, index):
    """The shell text that the command word tokens[index] runs, as a list:
    `eval <words>`, and `<shell> [options] -c '<script>'` (also `script -c`).
    Option clusters may carry the value-taking -o/-O (`-euo pipefail`). A
    `$'...'` script reaches here as `$...`, so it is also read without the
    `$`. Empty for any other word."""
    name = os.path.basename(tokens[index])
    if name == "eval":
        return [" ".join(tokens[index + 1:])] if index + 1 < len(tokens) else []
    if name not in SCRIPT_RUNNERS:
        return []
    position = index + 1
    while position < len(tokens) and tokens[position][:1] in {"-", "+"} and len(tokens[position]) > 1:
        cluster = tokens[position]
        if cluster == "--":
            return []
        if cluster.startswith("--"):  # --login, --norc: no -c inside a long option
            position += 1
            continue
        values = sum(cluster[1:].count(option) for option in "oO")
        if "c" in cluster[1:]:
            script_at = position + 1 + values
            if script_at >= len(tokens):
                return []
            script = tokens[script_at]
            return [script, script[1:]] if script.startswith("$") else [script]
        position += 1 + values
    return []


def push_invocations(command):
    """Yield the argument list of each `git push` the shell would run: from
    the tokenized commands, so a quoted argument that only mentions
    `git push ... main` (a PR body, a commit message) is not a push, and
    from `bash -c` scripts. Yields None for a push whose arguments cannot be
    read; only text that cannot be tokenized falls back to a raw scan."""
    commands = simple_commands(command)
    if commands is None:
        for match in PUSH_COMMAND.finditer(command):
            try:
                yield shlex.split(match.group("arguments"))
            except ValueError:
                yield None
        return
    for tokens in commands:
        for index, token in enumerate(tokens):
            scripts = embedded_scripts(tokens, index)
            for script in scripts:
                yield from push_invocations(script)
            if not scripts and os.path.basename(token) == "git" and tokens[index + 1:index + 2] == ["push"]:
                yield tokens[index + 2:]


def push_names_protected(command):
    """Whether a push names main/master as a destination (or source-only
    refspec, which pushes to the same name)."""
    for arguments in push_invocations(command):
        if arguments is None:
            return True
        _, refspecs = push_flags_and_refspecs(arguments)
        for refspec in refspecs:
            source, colon, destination = refspec.partition(":")
            if short_branch(destination if colon else source) in PROTECTED_BRANCHES:
                return True
    return False


def push_rewrites_dev(command, branches):
    """Whether a push force-updates or deletes the shared `dev` branch.
    `branches` are the branches the command may be on; an unknown one may
    be dev."""
    on_dev = INTEGRATION_BRANCH in branches or None in branches
    branch = INTEGRATION_BRANCH if on_dev else next(iter(branches), "")
    for arguments in push_invocations(command):
        if arguments is None:
            return True
        flags, refspecs = push_flags_and_refspecs(arguments)
        short_flags = "".join(f[1:] for f in flags if not f.startswith("--"))
        long_flags = [f.split("=", 1)[0] for f in flags if f.startswith("--")]
        force = "f" in short_flags or any(
            is_option_prefix(f, "--force", "--force-with-lease") for f in long_flags)
        delete = "d" in short_flags or any(
            is_option_prefix(f, "--delete", minimum=4) for f in long_flags)
        if not refspecs:
            if force and branch == INTEGRATION_BRANCH:
                return True
            continue
        for refspec in refspecs:
            source, colon, destination = refspec.partition(":")
            if not colon:
                destination = source
            if destination.lstrip("+") in {"HEAD", "@"}:
                destination = branch
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
    tokens = shell_tokens(command)
    if tokens is None:
        # Untokenizable: still join every backslash-newline, so the raw-text
        # checks see a continued `git push` as one line.
        return re.sub(r"\\\r?\n", "", command), True
    output = []
    context_changed = any(token in DIRECTORY_CHANGERS for token in tokens)
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
    return " ".join(token if set(token) <= SHELL_OPERATORS else shlex.quote(token)
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
    for arguments in push_invocations(command):
        if arguments is None:
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
    for arguments in push_invocations(command):
        if arguments is None:
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


def push_problem(command, context_changed, branches):
    """`branches` are the branches the command may be on, with None for a
    branch switch that cannot be read."""
    if push_names_protected(command):
        return (
            "pushes directly to main/master. It is human-gated, full stop -- an agent "
            "never pushes to it or merges into it. Work reaches main only through the "
            "dev -> main promotion PR, which the repository owner merges."
        )
    if push_rewrites_dev(command, branches):
        return (
            "force-pushes or deletes dev. dev is the shared integration branch and the "
            "head of the dev -> main promotion PR; add new commits instead of rewriting it."
        )
    if push_can_update_main_broadly(command):
        return (
            "uses a bulk or matching refspec that can update main without naming it. "
            "Push explicit non-main branches instead."
        )
    if (context_changed or None in branches) and push_uses_implicit_ref(command):
        return ("leaves the push target implicit where it can resolve to main. Name an "
                "explicit non-main destination.")
    protected = sorted(PROTECTED_BRANCHES & branches)
    branch = protected[0] if protected else None
    if branch and push_uses_implicit_ref(command):
        return f"pushes the current branch ({branch}) upstream. Same rule as a direct push to main."
    return None


def gh_problem(command, context_changed, switched, branches):
    """The first blocked `gh` call in the command. The merge check runs last
    because it is the only one that makes a network call."""
    calls = list(gh_calls(command))
    if not calls:
        return None
    if None in calls:
        return "runs gh in a way that cannot be read from the command text (unbalanced quoting)."
    problem = gh_alias_problem(calls)
    if problem:
        return problem
    checks = (
        (("pr", "create"), lambda arguments: pr_create_problem(arguments, context_changed, branches)),
        (("pr", "edit"), pr_edit_problem),
        (("api",), api_problem),
        (("repo", "sync"), repo_sync_problem),
        (("pr", "merge"), lambda arguments: pr_merge_problem(arguments, context_changed, command, switched)),
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
    try:
        reason = command_problem(command)
    except Exception as error:  # A crash must block, never fall through to allow.
        reason = f"could not be checked ({type(error).__name__}); run it in simpler steps."
    if reason:
        sys.stderr.write(f"DANGEROUS GIT COMMAND blocked: this command {reason}\n")
        return 2
    return 0


def command_problem(command):
    command, context_changed = normalize_git_options(command)
    normalized = normalize_quoting(command)
    switched = branch_switched(command)
    branches = possible_branches(command, switched)

    return (
        push_problem(command, context_changed, branches)
        or gh_problem(command, context_changed, switched, branches)
        or destructive_problem(normalized)
    )


if __name__ == "__main__":
    sys.exit(main())
