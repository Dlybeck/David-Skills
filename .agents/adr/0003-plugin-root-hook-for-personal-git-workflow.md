# Plugin-root hooks enforce David's personal Git workflow

## Context

Prose rules were not enough to prevent agents attempting destructive Git operations or writing
directly to the human-gated `main` branch. The original guard also blocked proposed pull requests
into `main`; amended 2026-10-04 to permit David's human review workflow.

## Decision

Ship the guardrails as plugin-root hooks under `hooks/`, so they apply wherever David enables
the plugin:

- `block-dangerous-git.py` blocks destructive commands and agent pushes or PR merges into
  `main`, including auto-merge. Creating or editing a PR targeting `main` is allowed for human
  review. Before `gh pr merge`, a read-only `gh pr view` resolves the base: verified non-main
  bases are allowed; main, failed lookups, and ambiguous targets or shell contexts are blocked.
- `require-committed-claim.py` ensures local-markdown work is claimed in a committed state
  before delegate dispatch.
- `delegate-recommend.py` may recommend the delegate workflow for a matching router model.

Claude Code and Codex auto-discover `hooks/hooks.json` at the plugin root. Do not also declare the
same hooks file in either plugin manifest; doing both can load it twice. Codex requires the user
to review and trust plugin hooks before they run.

These are intentionally global personal defaults. A project that should not inherit them should
not enable the plugin wholesale; use skills.sh to install selected skills instead. A skills-only
copy deliberately carries no hooks.

Every hook change must add or update table-driven coverage in `hooks/test_hooks.py`.

## Static inspection boundary (2026-10-04)

The Git guard is a local backstop, not complete command or API enforcement. It reads the
`Bash` PreToolUse JSON contract and never executes the submitted command. Ordinary quoted
arguments to read-only searches, `printf`, and `git log` are data; command substitutions inside
them still run and are inspected. PR proposal arguments also remain data. Direct pushes,
destructive commands, and verified main PR merges retain their existing policy.
Shell comments retain their terminating newline as a command separator. Quote state carries
across shell lines before detecting here-docs. In unquoted here-doc bodies, quote characters
are data and do not suppress command substitutions; backslash escapes still apply. Quoted
delimiters suppress the outer shell's body expansions, while a supported interpreter consuming
that body is inspected as executable code. See the [Bash here-document expansion rules](https://www.gnu.org/s/bash/manual/html_node/Redirections.html#Here-Documents).
Here-strings (`<<<`) do not start heredoc bodies. The scanner reads complete delimiter
words, including punctuation and shell quote removal, and only removes a body after finding
its exact closing delimiter (with leading tab stripping for `<<-`). Unquoted body lines join
at escaped newlines before delimiter comparison; quoted bodies keep those lines literal.
Missing, multiline, or otherwise unrecognized delimiters (including dollar-prefixed quote
forms) and multiple heredocs on one header retain their source;
the remaining lines are also inspected independently in an uncertain context. This can block
literal write commands in unproved data bodies rather than silently hide subsequent commands.

Supported executable forms include command lists/groups and common control prefixes,
leading literal redirections,
absolute executable paths, plain `command`/`exec`/`sudo`/`env` wrappers, shell `-c`/`-lc`,
literal `eval`, simple shell/Python here-docs (including after command prefixes), and literal
`echo`/common `printf` output piped directly into a supported interpreter.
Inline Python (`-c` or stdin here-doc)
is parsed with the standard-library AST. Literal list/tuple argv and shell strings passed to
`subprocess.run`, `call`, `check_call`, `check_output`, `Popen`, or `os.system`/`popen` are
inspected, including import aliases, keyword `args`, simple literal assignments, and literal
string `.split()`/`shlex.split()` argv construction.
Python process calls require explicit non-main push destinations; PR merges from Python
are blocked as unverifiable because preceding Python can change cwd/environment. Creating or
editing PRs targeting main is still allowed. No submitted Python is evaluated or imported.

The parser does not model shell/Python execution completely. Computed argv, runtime aliases,
mutable variables, indirect calls, `exec`/`eval` in Python, external script/module contents,
computed/file-fed pipelines or here-string input into interpreters, complex/multiple here-docs, unsupported launcher options,
other interpreter APIs (for example Node child_process or os.execv), Git aliases/configured
refspecs, HTTP/SDK writes, and tools outside the `Bash` matcher can escape inspection.
Python control flow is not evaluated, so a literal process call in an uncalled function can
be blocked. Git/PR preflight state can change before execution. These limitations must not be
represented as a universal security guarantee or worked around to perform a prohibited action.

## Separate enforcement options

The local hook can provide early feedback. GitHub branch rules restricting updates/merges to
main and bypass actors can enforce the remote boundary across command languages, subject to
the repository/account capabilities; see [GitHub's protected-branch documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).
Credential scoping or an execution broker can reduce
which actors can write; a sandbox can constrain subprocess/network access. A local pre-push
hook is another feedback layer but is bypassable and does not cover API merges.

These are proposals, not configured settings. Local tests or a hook update do not establish
remote enforcement. Adoption requires David's approval of the source change, normal reviewed
integration into dev, human promotion to main, release validation, and a separately approved
installed-hook refresh. Any branch-rule, credential, or permission change requires its own
explicit approval and verification of who can bypass it.
