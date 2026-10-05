#!/usr/bin/env python3
"""
BLOCK DANGEROUS GIT: hard-block two categories of git command before they
run, mechanical backstops rather than written discipline the agent has to
remember correctly every time:

1. Writes to `main` without a human directly at the keyboard --
   `git push` targeting `main` and `gh pr merge` targeting a PR based on
   `main`, including auto-merge. Creating or editing a PR into `main` is
   allowed: it proposes work for human review without updating the branch.
   Scoped to `main` only: this repo's own policy is
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
full destructive-pattern list but scoped more precisely on the push/merge side
(main only, not every push) and without depending on `jq`.

Bounded static inspection, not an authorization sandbox. Inspect executable
shell positions and supported literal Python process calls, never run submitted
code. Dynamic code, external scripts, other interpreters, and API writes need
separate enforcement. See ADR 0003 for coverage and adoption boundaries.
"""
import ast
import json
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


class ShellWord(str):
    """A quoted/escaped word that must not become shell punctuation."""


def shell_operator(token):
    return bool(token) and not isinstance(token, ShellWord) and set(token) <= set(";&|()\n")


def shell_without_comments(source):
    """Remove word-initial shell comments, preserving their newline boundary."""
    output = []
    quote = None
    escaped = False
    comment = False
    word_start = True
    index = 0
    while index < len(source):
        char = source[index]
        index += 1
        if comment:
            if char == "\n":
                output.append(char)
                comment = False
                word_start = True
            continue
        # A continuation joins words before comment recognition, but a
        # backslash inside a comment cannot consume its terminating newline.
        if char == "\\" and quote != "'" and not escaped and source[index:index + 1] == "\n":
            index += 1
            continue
        if escaped:
            output.append(char)
            escaped = False
            word_start = False
        elif char == "\\" and quote != "'":
            output.append(char)
            escaped = True
            word_start = False
        elif char in "\"'":
            output.append(char)
            if quote == char:
                quote = None
            elif quote is None:
                quote = char
            word_start = False
        elif quote is None and char == "#" and word_start:
            comment = True
        else:
            output.append(char)
            word_start = quote is None and (char.isspace() or char in ";&|()<>")
    return "".join(output)


def shell_tokens(command):
    # Shell line continuations disappear before word splitting. Removing
    # them even inside literals is conservative for this text guard.
    command = shell_without_comments(command).replace("\\\n", "")
    # shlex removes quotes, so a literal ';' would otherwise become syntax.
    # Protect quoted/escaped punctuation through tokenization, then restore it.
    replacements = {}
    for char in ";&|()\n<>":
        codepoint = 0xE000 + len(replacements)
        while chr(codepoint) in command or chr(codepoint) in replacements.values():
            codepoint += 1
        replacements[char] = chr(codepoint)
    protected = []
    quote = None
    escaped = False
    for char in command:
        if escaped:
            protected.append(replacements.get(char, char))
            escaped = False
        elif char == "\\" and quote != "'":
            protected.append(char)
            escaped = True
        elif char in "\"'":
            protected.append(char)
            if quote == char:
                quote = None
            elif quote is None:
                quote = char
        elif quote:
            protected.append(replacements.get(char, char))
        else:
            protected.append(char)
    lexer = shlex.shlex("".join(protected), posix=True, punctuation_chars=";&|()\n<>")
    lexer.commenters = ""  # Comments are already removed without eating newlines.
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    result = []
    for token in lexer:
        is_word = any(value in token for value in replacements.values())
        for char, replacement in replacements.items():
            token = token.replace(replacement, char)
        result.append(ShellWord(token) if is_word else token)
    return result


SHELLS = {"sh", "bash", "dash", "zsh", "ksh"}
PROCESS_CALLS = {"subprocess.run", "subprocess.call", "subprocess.check_call",
                 "subprocess.check_output", "subprocess.Popen", "os.system", "os.popen"}
CONTEXT_BUILTINS = {"cd", "pushd", "popd", "source", ".", "export", "unset", "alias", "function"}


def python_commands(source):
    """Extract literal argv/shell calls from inline Python without evaluation.

    Support normal import aliases and literal assignments, including inside
    function bodies. This is deliberately not Python control-flow analysis:
    an uncalled function can be blocked, and computed commands can be missed.
    """
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return
    aliases = {}
    literals = {}

    def name(node):
        if isinstance(node, ast.Name):
            return aliases.get(node.id, node.id)
        if isinstance(node, ast.Attribute):
            return f"{name(node.value)}.{node.attr}"
        return ""

    def literal(node):
        if isinstance(node, ast.Name):
            return literals.get(node.id)
        if isinstance(node, ast.Call) and not node.keywords:
            if isinstance(node.func, ast.Attribute) and node.func.attr == "split" and not node.args:
                value = literal(node.func.value)
                return value.split() if isinstance(value, str) else None
            if name(node.func) == "shlex.split" and len(node.args) == 1:
                value = literal(node.args[0])
                try:
                    return shlex.split(value) if isinstance(value, str) else None
                except ValueError:
                    return None
        try:
            return ast.literal_eval(node)
        except (ValueError, TypeError, SyntaxError):
            return None

    # Source order matters for common `args = [...]; subprocess.run(args)`.
    for node in sorted(ast.walk(tree), key=lambda item: getattr(item, "lineno", 0)):
        if isinstance(node, ast.Import):
            for item in node.names:
                aliases[item.asname or item.name] = item.name
        elif isinstance(node, ast.ImportFrom) and node.module in {"subprocess", "os"}:
            for item in node.names:
                aliases[item.asname or item.name] = f"{node.module}.{item.name}"
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    literals[target.id] = literal(node.value)
        elif isinstance(node, ast.Call) and name(node.func) in PROCESS_CALLS:
            keywords = {item.arg: item.value for item in node.keywords}
            argument = node.args[0] if node.args else keywords.get("args")
            value = literal(argument)
            shell = literal(keywords.get("shell")) is True
            # Python may change cwd/env before a call. Do not trust the hook's
            # shell context for implicit refs or PR-base lookups from Python.
            context_changed = True
            if name(node.func) in {"os.system", "os.popen"} or shell:
                if isinstance(value, (list, tuple)) and value:
                    value = value[0]  # POSIX shell=True uses argv[0] as code.
                if isinstance(value, str):
                    for command, changed in executable_commands(value):
                        yield command, changed or context_changed
            elif isinstance(value, (list, tuple)) and value and all(isinstance(v, str) for v in value):
                for command, changed in executable_argv(list(value)):
                    yield command, changed or context_changed


def command_substitutions(source, heredoc=False):
    """Find shell substitutions outside single quotes, including in double quotes.

    Nested parentheses are balanced; this is not a full shell grammar (for
    example, complex case statements and arithmetic expansion are unsupported).
    In an unquoted heredoc, quote characters in the body are ordinary data;
    only backslash escapes suppress substitutions. Inside $(...), normal
    shell quoting still controls the balancing of parentheses.
    """
    if heredoc:
        source = source.replace("\\\n", "")
    quote = None
    word_start = True
    comment = False
    index = 0
    while index < len(source):
        char = source[index]
        if comment:
            if char == "\n":
                comment = False
                word_start = True
            index += 1
            continue
        if char == "\\" and quote != "'":
            if source[index + 1:index + 2] != "\n":
                word_start = False
            index += 2
            continue
        if not heredoc and quote is None and char == "#" and word_start:
            comment = True
            index += 1
            continue
        opening = index + 1
        if char == "$":
            while source.startswith("\\\n", opening):
                opening += 2
        if not heredoc and char == "'" and quote != '"':
            quote = None if quote == "'" else "'"
            word_start = False
        elif not heredoc and char == '"' and quote != "'":
            quote = None if quote == '"' else '"'
            word_start = False
        elif quote != "'" and ((char == "$" and source[opening:opening + 1] == "(") or char == "`"):
            start = opening + 1 if char == "$" else index + 1
            end = start
            depth = 1
            inner_quote = None
            inner_word_start = True
            inner_comment = False
            while end < len(source):
                current = source[end]
                if inner_comment:
                    if current == "\n":
                        inner_comment = False
                        inner_word_start = True
                    end += 1
                    continue
                if current == "\\" and inner_quote != "'":
                    # A continuation joins words; a quoted/escaped # cannot
                    # start a comment. Backslashes inside comments are data.
                    if source[end + 1:end + 2] != "\n":
                        inner_word_start = False
                    end += 2
                    continue
                if char == "`" and current == "`":
                    break
                if current in "\"'":
                    if inner_quote == current:
                        inner_quote = None
                    elif inner_quote is None:
                        inner_quote = current
                    inner_word_start = False
                elif inner_quote is None and char == "$":
                    if current == "#" and inner_word_start:
                        inner_comment = True
                    elif current == "(":
                        depth += 1
                        inner_word_start = True
                    elif current == ")":
                        depth -= 1
                        if depth == 0:
                            break
                        inner_word_start = True
                    else:
                        inner_word_start = current in " \t\n;&|<>"
                end += 1
            if end < len(source):
                yield source[start:end]
                index = end
            word_start = False
        elif not heredoc and quote is None:
            word_start = char in " \t\n;&|()<>"
        index += 1


def executable_argv(tokens, input_source=None):
    """Unwrap common literal launchers; ordinary arguments remain inert."""
    assignments = False
    # Assignments and redirections can alternate before the executable.
    while tokens:
        if tokens[0] in {"if", "then", "elif", "else", "while", "until", "do", "!", "{"}:
            tokens = tokens[1:]
            continue
        if re.match(r"^[A-Za-z_]\w*=", tokens[0]):
            assignments = True
            tokens = tokens[1:]
            continue
        offset = 1 if tokens[0].isdigit() and len(tokens) > 1 else 0
        if not isinstance(tokens[offset], ShellWord) and re.fullmatch(r"[<>]+|[<>]&", tokens[offset]):
            tokens = tokens[offset + 2:]
        else:
            break
    if not tokens:
        return
    program = tokens[0].rsplit("/", 1)[-1]
    if program in {"command", "exec", "sudo", "env"}:
        # Handle plain wrappers and env assignments; options with values are
        # not guessed, because guessing can reinterpret inert option text.
        rest = tokens[1:]
        if rest and rest[0] == "--":
            rest = rest[1:]
        if rest and not rest[0].startswith("-"):
            for command, changed in executable_argv(rest, input_source):
                yield command, changed or assignments or program in {"env", "sudo"}
        return
    if program in SHELLS:
        index = 1
        while index < len(tokens):
            argument = tokens[index]
            if argument in {"--rcfile", "--init-file", "-o", "-O"}:
                if argument in {"--rcfile", "--init-file"}:
                    assignments = True  # Startup code can change PR lookup context.
                index += 2
                continue
            if argument == "--" or not argument.startswith("-"):
                break  # External script operands end interpreter option parsing.
            if not argument.startswith("--") and "c" in argument and index + 1 < len(tokens):
                for command, changed in executable_commands(tokens[index + 1]):
                    yield command, changed or assignments
                return
            index += 1
        if input_source is not None and index == len(tokens):
            for command, changed in executable_commands(input_source):
                yield command, changed or assignments
        return
    if re.fullmatch(r"python(?:\d+(?:\.\d+)*)?", program):
        index = 1
        while index < len(tokens):
            argument = tokens[index]
            if argument in {"-W", "-X"}:
                index += 2
                continue
            if argument in {"-m", "--"} or not argument.startswith("-") or argument == "-":
                break
            if argument.startswith("-c"):
                source = argument[2:] or (tokens[index + 1] if index + 1 < len(tokens) else "")
                yield from python_commands(source)
                return
            index += 1
        if input_source is not None and (index == len(tokens) or tokens[index:] == ["-"]):
            yield from python_commands(input_source)
        return
    if program == "eval" and len(tokens) > 1:
        for command, changed in executable_commands(" ".join(tokens[1:])):
            yield command, changed or assignments
        return
    # Keep context-changing commands for the merge preflight, but never
    # recursively inspect quoted arguments of rg/grep/printf/git log/etc.
    yield shlex.join([program, *tokens[1:]]), assignments


def literal_pipe_input(tokens):
    """Recognize common literal producers, only when feeding an interpreter."""
    if not tokens:
        return None
    if tokens[0] == "echo" and all(not item.startswith("-") for item in tokens[1:]):
        return " ".join(tokens[1:]) + "\n"
    if tokens[0] == "printf" and len(tokens) > 1:
        if tokens[1] in {"%s", "%s\\n"}:
            return "".join(item + ("\n" if tokens[1] == "%s\\n" else "") for item in tokens[2:])
        if "%" not in tokens[1] and len(tokens) == 2:
            return tokens[1].replace("\\n", "\n")
    return None


def shell_segments(tokens):
    """Separate syntax tokens from words while retaining literal pipeline input."""
    segment = []
    input_source = None
    for token in [*tokens, ";"]:
        if shell_operator(token):
            yield segment, input_source
            input_source = literal_pipe_input(segment) if token == "|" else None
            segment = []
        else:
            segment.append(token)


def heredoc_word(line, start):
    """Read one complete delimiter word, with shell quote removal only.

    Complex or multiline words are uncertain: callers must keep the remaining
    source rather than treating a guessed prefix as a body boundary.
    """
    index = start
    while index < len(line) and line[index] in " \t":
        index += 1
    start = index
    quote = None
    quoted = False
    delimiter = []
    if line[index:index + 1] == "#":
        return None  # An unquoted word-initial # starts a shell comment.
    while index < len(line):
        char = line[index]
        if char == "\n":
            break
        if char == "\\" and quote != "'":
            quoted = True
            if index + 1 == len(line) or line[index + 1] == "\n":
                return None
            following = line[index + 1]
            if quote == '"' and following not in '$`"\\':
                delimiter.append("\\")
            delimiter.append(following)
            index += 2
            continue
        if char in "\"'":
            if quote == char:
                quote = None
            elif quote is None:
                quote = char
            else:
                delimiter.append(char)
            quoted = True
        elif quote is None:
            if char in " \t;&|()<>":
                break
            if char == "`" or (char == "$" and line[index + 1:index + 2] in {"(", "'", '"'}):
                return None
            delimiter.append(char)
        else:
            delimiter.append(char)
        index += 1
    if quote is not None or index == start:
        return None
    return index, "".join(delimiter), quoted


def executable_commands(source):
    """Read shell command positions, inline -c code, and simple here-docs."""
    # A here-doc is data unless consumed by a supported interpreter on this
    # command line. No external files are opened and no code is executed.
    heredoc = re.compile(r"(?<!<)<<(?!<)(-?)")
    lines = source.splitlines(keepends=True)
    index = 0
    shell_source = []
    quote = None
    escaped = False
    word_start = True
    uncertain_tail = None
    while index < len(lines):
        line = lines[index]
        # Redirection operators inside a search pattern/string are inert.
        # Carry lexical state between header lines; heredoc bodies are data
        # and must not alter the surrounding shell's quote/comment state.
        unquoted = set()
        for position, char in enumerate(line):
            if escaped:
                escaped = False
                if char != "\n":
                    word_start = False
                continue
            if char == "\\" and quote != "'":
                escaped = True
                if line[position + 1:position + 2] != "\n":
                    word_start = False
            elif char in "\"'":
                if quote == char:
                    quote = None
                elif quote is None:
                    quote = char
                word_start = False
            elif quote is None and char == "#" and word_start:
                # A comment cannot introduce a heredoc or change quote state.
                word_start = True
                break
            elif quote is None:
                unquoted.add(position)
                word_start = char.isspace() or char in ";&|()<>"
        matches = [item for item in heredoc.finditer(line) if item.start() in unquoted]
        if not matches:
            shell_source.append(line)
            index += 1
            continue
        match = matches[0]
        word = heredoc_word(line, match.end()) if len(matches) == 1 else None
        end = index + 1
        terminator_end = end
        if word is not None:
            word_end, delimiter, quoted = word
            while end < len(lines):
                candidate = lines[end].removesuffix("\n")
                if match[1]:
                    candidate = candidate.lstrip("\t")
                terminator_end = end
                # Bash joins unquoted body lines before checking the marker.
                # Keep both physical bounds so joined terminator lines are not
                # included in the body passed to a supported interpreter.
                while not quoted and lines[terminator_end].endswith("\n"):
                    backslashes = len(candidate) - len(candidate.rstrip("\\"))
                    if not backslashes % 2:
                        break
                    terminator_end += 1
                    if terminator_end == len(lines):
                        break
                    following = lines[terminator_end].removesuffix("\n")
                    if match[1]:
                        following = following.lstrip("\t")
                    candidate = candidate[:-1] + following
                if terminator_end == len(lines):
                    end = len(lines)
                    break
                if candidate == delimiter:
                    break
                end = terminator_end + 1
        if word is None or end == len(lines):
            # Never drop later lines on a guessed delimiter, multiple bodies,
            # or a missing terminator. Inspect the uncertain tail line by line
            # as well, so unfinished quoting cannot hide a following command.
            if uncertain_tail is None:
                uncertain_tail = index + 1
            if word is not None and not quoted:
                for substitution in command_substitutions("".join(lines[index + 1:]), heredoc=True):
                    yield from executable_commands(substitution)
            shell_source.append(line)
            index += 1
            continue
        body = []
        index += 1
        while index < end:
            body.append(lines[index].lstrip("\t") if match[1] else lines[index])
            index += 1
        index = terminator_end + 1
        # A header can follow a multiline quoted argument. Tokenize the whole
        # retained prefix so a closing quote has its matching opening quote.
        header = "".join(shell_source) + line[:match.start()]
        try:
            tokens = shell_tokens(header)
        except ValueError:
            tokens = []
        code = "".join(body)
        segments = list(shell_segments(tokens))
        if segments:
            yield from executable_argv(segments[-1][0], input_source=code)
        if not quoted:
            for substitution in command_substitutions(code, heredoc=True):
                yield from executable_commands(substitution)
        # Retain commands after the delimiter declaration (e.g. cat <<EOF;
        # git push ...), while dropping the data redirection itself.
        shell_source.append(line[:match.start()] + line[word_end:])
    if uncertain_tail is not None:
        for line in lines[uncertain_tail:]:
            for command, _ in executable_commands(line):
                yield command, True
    source = "".join(shell_source)
    # Inspect original substitution boundaries before removing continuations:
    # a backslash in an inner comment must not eat its terminating newline.
    for substitution in command_substitutions(source):
        yield from executable_commands(substitution)
    source = shell_without_comments(source)
    try:
        tokens = shell_tokens(source)
    except ValueError:
        # Malformed text cannot be tokenized. Preserve the old conservative
        # fallback, but do not mistake a normal quoted search for execution.
        yield source, True
        return
    if any(tokens[index + 1:index + 3] == ["()", "{"]
           or tokens[index + 1:index + 4] == ["(", ")", "{"]
           for index in range(len(tokens) - 2)):
        yield "function", True
    for segment, input_source in shell_segments(tokens):
        yield from executable_argv(segment, input_source)


def pr_merge_arguments(command):
    """Read a single extracted gh command, preserving literal argument data."""
    try:
        tokens = shell_tokens(command)
    except ValueError:
        if re.search(r'\bgh\b.*\bpr\s+merge\b', command, re.DOTALL):
            yield None
        return

    if not tokens or tokens[0] != "gh":
        return
    args = tokens[1:]
    # gh accepts the inherited repository flag before `pr` as well.
    prefix = []
    while args and args[0].startswith("-"):
        option = args.pop(0)
        prefix.append(option)
        if option in {"-R", "--repo"} and args:
            prefix.append(args.pop(0))
    if args[:2] == ["pr", "merge"]:
        yield prefix + args[2:]


def pr_merge_target(arguments):
    """Return literal selector/repository arguments for a read-only PR lookup.

    Unknown flags, substitutions, and ambiguous selectors cannot establish
    the actual base. Never execute or forward merge flags to the lookup.
    """
    if arguments is None:
        return None
    flags = {"--admin", "--auto", "--delete-branch", "--disable-auto",
             "--merge", "--rebase", "--squash", "-d", "-m", "-r", "-s"}
    value_flags = {"--author-email", "--body", "--body-file", "--match-head-commit",
                   "--subject", "-A", "-b", "-F", "-t", "-R", "--repo"}
    selector = []
    repository = None
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        option, equals, value = argument.partition("=")
        if argument in flags:
            index += 1
            continue
        if argument.startswith("-R") and argument != "-R":
            option, equals, value = "-R", "=", argument[2:]
        if option in value_flags:
            if not equals:
                index += 1
                if index >= len(arguments):
                    return None
                value = arguments[index]
            if option in {"-R", "--repo"}:
                if repository is not None or not value:
                    return None
                repository = value
        elif argument.startswith("-"):
            return None
        else:
            selector.append(argument)
        index += 1
    if len(selector) > 1 or any(c in "".join(selector + [repository or ""]) for c in "$`"):
        return None
    return selector + (["--repo", repository] if repository else [])


def merge_context_changed(command):
    # A preflight lookup cannot predict preceding shell commands that change
    # cwd/current branch, CLI configuration, or the PR's proposed base.
    # Strip quotes here as well to cover token concatenation inside wrappers.
    normalized, context_changed = normalize_git_options(command)
    try:
        tokens = shell_tokens(normalized)
    except ValueError:
        return True
    if context_changed:
        return True
    for index in range(len(tokens)):
        if index and not shell_operator(tokens[index - 1]):
            continue
        args = tokens[index:]
        if args[0] in CONTEXT_BUILTINS:
            return True
        if args[:2] in (["git", "switch"], ["git", "checkout"], ["git", "config"], ["git", "remote"],
                        ["gh", "config"], ["gh", "auth"]):
            return True
        if args[:3] in (["gh", "pr", "create"], ["gh", "pr", "edit"], ["gh", "pr", "checkout"],
                        ["gh", "repo", "set-default"]):
            return True
    return False


def pr_merge_block_reason(command, context_changed):
    for arguments in pr_merge_arguments(command):
        target = pr_merge_target(arguments)
        # Shell changes to cwd, environment, or executable resolution cannot
        # be safely reproduced by a subprocess in the hook's own context.
        if target is None or context_changed or merge_context_changed(command):
            return "cannot verify the PR merge base. Resolve the target in the current repository first."
        try:
            result = subprocess.run(
                ["gh", "pr", "view", *target, "--json", "baseRefName"],
                capture_output=True, text=True, timeout=5,
            )
            base = json.loads(result.stdout).get("baseRefName") if result.returncode == 0 else None
            if not isinstance(base, str) or not base or base != base.strip():
                raise ValueError("missing PR base")
        except (OSError, subprocess.TimeoutExpired, ValueError, AttributeError):
            return "cannot verify the PR merge base. A failed lookup never authorizes a merge."
        if base in {"main", "refs/heads/main"}:
            return "merges a PR into main (or schedules auto-merge). main is human-gated; only the human may merge it."
    return None


def normalize_git_options(command):
    """Expose Git subcommands behind global options to the existing guards.

    This is still a shell-text heuristic, not an authorization sandbox. When
    options or a shell cd can change ref resolution, require explicit push
    destinations rather than trusting the hook process's current branch.
    """
    try:
        tokens = shell_tokens(command)
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
    return " ".join(token if shell_operator(token) else shlex.quote(token)
                    for token in output), context_changed


def normalize_quoting(command):
    """Strip shell quote characters (`"` and `'`) from the command text
    before pattern matching, so `git push origin "main"` (or an
    interpolation-adjacent spelling like `"ma"in`, which a real shell
    concatenates to `main` the same way) matches exactly like the unquoted
    form. Applied only to extracted executable Git commands: the boundary
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


def command_block_reason(command, context_changed):
    command, options_changed = normalize_git_options(command)
    context_changed = context_changed or options_changed
    normalized = normalize_quoting(command)
    try:
        tokens = shell_tokens(command)
    except ValueError:
        tokens = []
    if not tokens:
        return pr_merge_block_reason(command, True)
    # Only actionable Git subcommands reach the legacy pattern checks. For
    # example, a git log --grep argument containing a push is inspection data.
    if tokens and tokens[:2] not in (["git", "push"], ["git", "reset"],
                                    ["git", "clean"], ["git", "branch"],
                                    ["git", "checkout"], ["git", "restore"]):
        return pr_merge_block_reason(command, context_changed) if tokens[0] == "gh" else None

    reason = None
    if PUSH_TO_MAIN.search(normalized):
        reason = (
            "pushes directly to main. main is human-gated; an agent may open a PR "
            "for human review, but only the human may push or merge into main."
        )
    elif push_can_update_main_broadly(command):
        reason = (
            "uses a bulk or matching refspec that can update main without naming it. "
            "Push explicit non-main branches instead."
        )
    elif context_changed and push_uses_implicit_ref(command):
        reason = "leaves the push target implicit where it can resolve to main. Name an explicit non-main destination."
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

    return reason


def main():
    data = read_hook_input()
    if data is None or data.get("tool_name") != "Bash":
        return 0

    original_command = (data.get("tool_input") or {}).get("command") or ""
    commands = list(executable_commands(original_command))
    context_commands = [command for command, _ in commands
                        if command.split(" ", 1)[0] in
                        CONTEXT_BUILTINS | {"git", "gh"}]
    context_changed = (any(changed for _, changed in commands)
                       or merge_context_changed("; ".join(context_commands)))
    reason = None
    for command, changed in commands:
        reason = command_block_reason(command, context_changed or changed)
        if reason:
            break

    if reason:
        sys.stderr.write(f"DANGEROUS GIT COMMAND blocked: this command {reason}\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
