#!/usr/bin/env python3
"""
Executable tests for this plugin's hooks -- the repo's first executable test
file (ADR 0006, "hooks carry executable tests": a mechanical rule deserves a
mechanical check). Drives each hook as a subprocess through its real, only
contract -- JSON on stdin, allow (exit 0) or block (exit 2, with a stderr
message) via exit code -- the contract Claude Code and Codex both rely on.
Never imports or calls a hook's internals (its regexes, its functions): a
hook could rewrite its whole implementation and these tests would still be
the right check, because they only assert on the contract.

Python standard library only, no test framework -- the same no-dependency
discipline the hooks themselves follow. Run directly:

    python3 hooks/test_hooks.py

Future hooks land with their own table of cases added to this file, not a
new test file.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HOOKS_DIR = Path(__file__).resolve().parent
REPO_ROOT = HOOKS_DIR.parent

_total = 0
_failed = []


def check(name, condition, detail=""):
    global _total
    _total += 1
    if condition:
        print(f"ok   {name}")
    else:
        print(f"FAIL {name} {detail}".rstrip())
        _failed.append(name)


def run_hook_process(script, stdin_text, cwd=REPO_ROOT):
    """Run a hook through its complete subprocess contract."""
    return subprocess.run(
        [sys.executable, str(HOOKS_DIR / script)],
        input=stdin_text,
        capture_output=True,
        text=True,
        cwd=cwd,
        timeout=10,
    )


def run_hook(script, stdin_text, cwd=REPO_ROOT):
    """Run a hook script as a subprocess with raw text on stdin, exactly as
    Claude Code and Codex invoke it. Returns (exit_code, stderr)."""
    proc = run_hook_process(script, stdin_text, cwd=cwd)
    return proc.returncode, proc.stderr


def run_hook_bash(script, command, cwd=REPO_ROOT):
    """Run a hook with a Claude Code-shaped PreToolUse payload for a Bash
    tool call carrying `command`."""
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    return run_hook(script, payload, cwd=cwd)


def git(repo, *args):
    """Run a quiet Git setup command for a temporary hook-contract repo."""
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr}")


def init_git_repo(repo, with_tracker=True):
    git(repo, "init", "-q")
    git(repo, "config", "user.name", "Hook Tests")
    git(repo, "config", "user.email", "hooks@example.invalid")
    if not with_tracker:
        return
    tracker = repo / ".scratch"
    tracker.mkdir()
    (tracker / "spec.md").write_text("Status: open\n", encoding="utf-8")
    git(repo, "add", ".scratch/spec.md")
    git(repo, "commit", "-qm", "add tracker")


def dispatch_payload(tool_name, command=None):
    tool_input = {} if command is None else {"command": command}
    return json.dumps({"tool_name": tool_name, "tool_input": tool_input})


# ---------------------------------------------------------------------------
# block-dangerous-git.py: push-to-main and PR-to-main, plain/quoted/
# interpolation-adjacent spellings, all must block.
# ---------------------------------------------------------------------------

BLOCK_PUSH_TO_MAIN = [
    'git push origin master',
    'git push origin HEAD:refs/heads/master',
    'git push origin HEAD:heads/master',
    'git push origin HEAD:heads/main',
    'git commit -m wip#3 && git push origin main',
    'git commit -m "docs: explain <<EOF handling"\ngit push origin HEAD:main',
    "/bin/bash <<'EOF'\ngit push origin HEAD:main\nEOF",
    'git commit -m "$(printf "Fix #3")" && git push origin HEAD:main',
    'git push origin main>/dev/null',
    "git commit -F - <<'EOF'\nfix path C:\\\nEOF\ngit push origin HEAD:main",
    '# see C:\\\ngit push origin main',
    'git push \\\n  origin \\\n  main',
    'git push origin :main',
    'git -C /tmp/repo push',
    'git -c push.default=matching push origin',
    'cd /tmp/repo && git push',
    'git -C /tmp/repo push origin main',
    'git -c color.ui=false push origin HEAD:main',
    'git --no-pager push origin main',
    'git --git-dir=/tmp/repo/.git push origin main',
    'git push origin main',
    'git push origin "main"',
    "git push origin 'main'",
    'git push origin "ma"in',
    "git push origin m'ai'n",
    'git push origin refs/heads/main',
    'git push origin "refs/heads/main"',
    'git push -u origin main',
    'git push origin HEAD:main',
]

for cmd in BLOCK_PUSH_TO_MAIN:
    code, err = run_hook_bash("block-dangerous-git.py", cmd)
    check(f"block-dangerous-git blocks push-to-main: {cmd!r}",
          code == 2 and "main" in err, f"(code={code}, err={err!r})")

BLOCK_PR_TO_MAIN = [
    'gh pr create --base main --head feature/x --title "x"',
    'gh pr create --base "main" --head feature/x --title "x"',
    "gh pr create --base 'main' --head feature/x --title x",
    'gh pr create -B main -H feature/x --title x',
    'gh pr create --base=master --head=feature/x',
    'gh pr create --base main --head Dlybeck:dev',
    'gh pr create --title x --head feature/x',
    'cd /tmp/repo && gh pr create --base main --title x',
    'gh pr edit 5 --base=main',
    'gh pr edit 5 --base="main"',
    'gh pr edit 5 -B master',
    'gh pr edit 5 --base refs/heads/main',
]

for cmd in BLOCK_PR_TO_MAIN:
    code, err = run_hook_bash("block-dangerous-git.py", cmd)
    check(f"block-dangerous-git blocks PR-to-main: {cmd!r}",
          code == 2 and "main" in err, f"(code={code}, err={err!r})")

# Feature-branch pushes and feature/main-page-style lookalikes must pass,
# quoted or not -- the boundary behavior the fix must not break.
PASS_LOOKALIKES = [
    'git -C /tmp/repo status && git push origin feature/auth',
    'git -C "/tmp/repo with spaces" push origin feature/auth',
    'git -c color.ui=false status',
    'git push origin feature/main-page',
    'git push origin "feature/main-page"',
    "git push origin 'feature/main-page'",
    'git push origin feature-branch',
    'git push origin maintenance',
    'git push origin "maintenance"',
    'gh pr create --base dev --title "x"',
    'gh pr create --base develop --title "x"',
    'gh pr create --base feature/main-page --title "x"',
    'git push origin feature/master-plan',
    'git push origin mastery',
]

for cmd in PASS_LOOKALIKES:
    code, err = run_hook_bash("block-dangerous-git.py", cmd)
    check(f"block-dangerous-git allows lookalike: {cmd!r}",
          code == 0, f"(code={code}, err={err!r})")

# The dev -> main promotion PR: opening it from head dev, editing its body,
# commenting, and replying on review threads are all allowed.
PASS_PROMOTION_PR = [
    'gh pr create --base main --head dev --title "Promote dev" --body-file report.md',
    'gh pr create -B main -H dev --title x',
    'gh pr create --base=master --head=dev',
    'gh pr edit 12 --body-file report.md',
    'gh pr edit 12 --title "Promote dev to main"',
    'gh pr edit 12 --base dev',
    'gh pr comment 12 --body "🤖 Agent: updated the report"',
    'gh pr view 12 --comments',
    'gh pr list --base main --head dev --state open --json number',
    'gh api repos/o/r/pulls/12/comments',
    'gh api repos/o/r/pulls/12/comments/345/replies -f body="🤖 Agent: fixed in abc123"',
    'gh api repos/o/r/issues/12/comments -f body=x',
    'gh api repos/o/r/contents/README.md',
    'gh api -X GET repos/o/r/git/refs/heads/main',
    "gh api graphql -f query='query { viewer { login } }'",
    'gh repo sync',
    'gh repo sync owner/fork --branch dev',
]

for cmd in PASS_PROMOTION_PR:
    code, err = run_hook_bash("block-dangerous-git.py", cmd)
    check(f"block-dangerous-git allows promotion-PR work: {cmd!r}",
          code == 0 and err == "", f"(code={code}, err={err!r})")

# gh api writes that merge a PR, move a ref, or commit content, and GraphQL
# mutations that do the same, are blocked whatever branch they name.
BLOCK_GH_WRITES = [
    'gh api -X PUT repos/o/r/pulls/12/merge',
    'gh api --method=PUT /repos/o/r/pulls/12/merge -f merge_method=merge',
    'gh api repos/o/r/merges -f base=main -f head=dev',
    'gh api -X PATCH repos/o/r/git/refs/heads/main -f sha=abc',
    'gh api repos/o/r/git/refs -f ref=refs/heads/x -f sha=abc',
    'gh api -XDELETE repos/o/r/git/refs/heads/dev',
    'gh api -X PUT repos/o/r/contents/README.md -f message=x -f content=eA==',
    'gh api repos/o/r/merge-upstream -f branch=main',
    "gh api graphql -f query='mutation { mergePullRequest(input: {pullRequestId: \"x\"}) { clientMutationId } }'",
    "gh api graphql -f query='mutation { enablePullRequestAutoMerge(input: {}) { clientMutationId } }'",
    "gh api graphql -F query='mutation { updateRef(input: {}) { clientMutationId } }'",
    "gh api graphql -f query='mutation { createCommitOnBranch(input: {}) { clientMutationId } }'",
    'gh api graphql -F query=@/nonexistent/query.graphql',
    "gh api https://api.github.com/graphql -f query='mutation { mergePullRequest(input: {}) { clientMutationId } }'",
    "gh api https://ghe.example.com/api/graphql -f query='mutation { updateRef(input: {}) { clientMutationId } }'",
    'gh api -X PUT https://api.github.com/repos/o/r/pulls/12/merge',
    'gh api graphql --input -',
    'gh repo sync owner/fork',
    'gh repo sync owner/fork --branch main',
]

for cmd in BLOCK_GH_WRITES:
    code, err = run_hook_bash("block-dangerous-git.py", cmd)
    check(f"block-dangerous-git blocks gh write: {cmd!r}",
          code == 2 and err.startswith("DANGEROUS GIT COMMAND blocked"),
          f"(code={code}, err={err!r})")

with tempfile.TemporaryDirectory() as temp_dir:
    for name, text, blocked in (
        ("merge.graphql", "mutation { mergePullRequest(input: {}) { clientMutationId } }", True),
        ("query.graphql", "query { repository(owner: \"o\", name: \"r\") { id } }", False),
    ):
        path = Path(temp_dir) / name
        path.write_text(text, encoding="utf-8")
        code, err = run_hook_bash("block-dangerous-git.py", f"gh api graphql -F query=@{path}")
        check(f"block-dangerous-git reads GraphQL file {name}",
              code == (2 if blocked else 0), f"(code={code}, err={err!r})")

# Force-pushing or deleting dev rewrites the promotion PR's head.
BLOCK_DEV_REWRITE = [
    'git push --force origin dev',
    'git push -f origin dev',
    'git push -uf origin dev',
    'git push origin +dev',
    'git push --force-with-lease origin HEAD:dev',
    'git push origin +HEAD:refs/heads/dev',
    'git push origin --delete dev',
    'git push origin :dev',
    # Git accepts any unambiguous prefix of a long option.
    'git push --force-w origin dev',
    'git push --force-with origin dev',
    'git push --force-with-lease=dev:abc123 origin dev',
    'git push --del origin dev',
    'git push --dele origin dev',
    # Git resolves a heads/<branch> destination to refs/heads/<branch>.
    'git push -f origin HEAD:heads/dev',
    'git push -f origin dev>/tmp/log',
    'git push origin :heads/dev',
]

for cmd in BLOCK_DEV_REWRITE:
    code, err = run_hook_bash("block-dangerous-git.py", cmd)
    check(f"block-dangerous-git blocks dev rewrite: {cmd!r}",
          code == 2 and "dev" in err, f"(code={code}, err={err!r})")

PASS_DEV_PUSHES = [
    'git push origin dev',
    'git push -u origin dev',
    'git push origin HEAD:dev',
    'git push --force origin feature/x',
    'git push origin +feature/x',
    'git push -f origin develop',
    'git push origin --delete feature/x',
    'git push --dry-run origin dev',
    'git push --follow-tags origin dev',
]

for cmd in PASS_DEV_PUSHES:
    code, err = run_hook_bash("block-dangerous-git.py", cmd)
    check(f"block-dangerous-git allows dev push: {cmd!r}",
          code == 0 and err == "", f"(code={code}, err={err!r})")

# `gh pr merge` looks up the PR's base with `gh pr view`. A fake gh on PATH
# answers with FAKE_GH_BASE (or fails) and logs what it was asked.
FAKE_GH = """#!/usr/bin/env python3
import json, os, sys
with open(os.environ["FAKE_GH_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps(sys.argv[1:]) + "\\n")
if sys.argv[1:3] == ["alias", "list"]:
    aliases = os.environ.get("FAKE_GH_ALIASES", "")
    if aliases == "FAIL":
        sys.exit(1)
    print(aliases)
    sys.exit(0)
base = os.environ.get("FAKE_GH_BASE", "")
if sys.argv[1:3] != ["pr", "view"] or base == "FAIL":
    sys.exit(1)
print(base)
"""

with tempfile.TemporaryDirectory() as temp_dir:
    bin_dir = Path(temp_dir) / "bin"
    bin_dir.mkdir()
    fake_gh = bin_dir / "gh"
    fake_gh.write_text(FAKE_GH, encoding="utf-8")
    fake_gh.chmod(0o755)
    gh_log = Path(temp_dir) / "gh.jsonl"

    def run_merge(command, base, aliases="co: pr checkout"):
        gh_log.write_text("", encoding="utf-8")
        environment = {
            **os.environ,
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            "FAKE_GH_LOG": str(gh_log),
            "FAKE_GH_BASE": base,
            "FAKE_GH_ALIASES": aliases,
        }
        proc = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "block-dangerous-git.py")],
            input=json.dumps({"tool_name": "Bash", "tool_input": {"command": command}}),
            capture_output=True, text=True, cwd=REPO_ROOT, timeout=30, env=environment,
        )
        calls = [json.loads(line) for line in gh_log.read_text().splitlines() if line]
        return proc.returncode, proc.stderr, calls

    for command, base, blocked in (
        ("gh pr merge 12 --merge", "main", True),
        ("gh pr merge 12 --auto --squash", "main", True),
        ("gh pr merge 12 --merge", "master", True),
        ("gh pr merge 12 --merge", "FAIL", True),
        ("gh pr merge 12 --merge", "", True),
        ("gh pr merge --merge", "main", True),
        ("gh pr merge 12 --squash --delete-branch", "dev", False),
        ("gh pr merge 12 --auto --merge", "feature/x", False),
        ('gh pr merge 12 --merge --subject "Merge feature/x"', "dev", False),
        ("gh pr merge 12 --merge && gh pr merge 13 --merge", "dev", False),
    ):
        code, err, calls = run_merge(command, base)
        check(f"block-dangerous-git gh pr merge base={base or 'empty'!s}: {command!r}",
              code == (2 if blocked else 0) and (blocked or err == ""),
              f"(code={code}, err={err!r})")

    code, err, calls = run_merge("gh pr merge 12 --merge -R owner/repo", "dev")
    check("block-dangerous-git looks up the merge base for the named PR and repo",
          code == 0 and calls == [["pr", "view", "12", "--json", "baseRefName", "--jq",
                                   ".baseRefName", "--repo", "owner/repo"]],
          f"(code={code}, calls={calls!r})")

    code, err, calls = run_merge("cd /tmp && gh pr merge 12 --merge", "dev")
    check("block-dangerous-git blocks merge after cd without --repo, no lookup",
          code == 2 and calls == [], f"(code={code}, calls={calls!r})")

    code, err, calls = run_merge("cd /tmp && gh pr merge 12 --merge --repo owner/repo", "dev")
    check("block-dangerous-git allows merge after cd with explicit --repo",
          code == 0 and len(calls) == 1, f"(code={code}, calls={calls!r})")

    # The lookup runs in the hook's own directory and environment: a command
    # that points gh elsewhere without --repo must block, not check the wrong PR.
    for command in (
        "GH_REPO=owner/other gh pr merge 12 --merge",
        "export GH_REPO=owner/other; gh pr merge 12 --merge",
        "pushd /tmp/other && gh pr merge 12 --merge",
        "GH_HOST=ghe.example.com gh pr merge 12 --merge --repo owner/repo",
    ):
        code, err, calls = run_merge(command, "dev")
        check(f"block-dangerous-git blocks merge with redirected gh target: {command!r}",
              code == 2 and calls == [], f"(code={code}, calls={calls!r})")

    code, err, calls = run_merge("GH_REPO=owner/other gh pr merge 12 --merge -R owner/other", "dev")
    check("block-dangerous-git allows GH_REPO merge with matching explicit --repo",
          code == 0 and len(calls) == 1, f"(code={code}, calls={calls!r})")

    # gh accepts -R/--repo between `pr` and the subcommand.
    for command in ("gh pr -R owner/repo merge 12 --merge", "gh pr --repo=owner/repo merge 12"):
        code, err, calls = run_merge(command, "main")
        check(f"block-dangerous-git sees merge after a leading repo flag: {command!r}",
              code == 2 and "into main" in err and calls and "owner/repo" in calls[0][-1],
              f"(code={code}, err={err!r}, calls={calls!r})")
    for command in ("gh pr -R owner/repo edit 5 --base main",
                    "gh pr -R owner/repo create --base main --head feature/x"):
        code, err, calls = run_merge(command, "dev")
        check(f"block-dangerous-git sees PR command after a leading repo flag: {command!r}",
              code == 2, f"(code={code}, err={err!r})")

    # An option value spelled gh or git is a value, not a new command.
    code, err, calls = run_merge("gh pr merge --subject gh 12 --merge", "main")
    check("block-dangerous-git keeps the PR selector after a value spelled gh",
          code == 2 and any(call[:3] == ["pr", "view", "12"] for call in calls),
          f"(code={code}, calls={calls!r})")
    for command in (
        "gh api -t gh -X PUT repos/o/r/pulls/5/merge",
        "gh api --template git graphql -f query='mutation { mergePullRequest(input: {}) { clientMutationId } }'",
    ):
        code, err, calls = run_merge(command, "dev")
        check(f"block-dangerous-git reads gh api past a value spelled gh/git: {command!r}",
              code == 2, f"(code={code}, err={err!r})")

    # Newlines end a command even after a comment.
    for command in ("echo ready\ngh pr merge 12 --merge",
                    "gh pr list # open PRs\ngh pr merge 12 --merge"):
        code, err, calls = run_merge(command, "main")
        check(f"block-dangerous-git splits commands at newlines: {command!r}",
              code == 2 and "into main" in err, f"(code={code}, err={err!r})")

    # Aliases can hide a merge: defining one is blocked, and so is running one.
    for command, aliases in (
        ("gh alias set pm 'pr merge'", "co: pr checkout"),
        ("gh alias import aliases.yml", "co: pr checkout"),
        ("gh pm 12", "pm: pr merge"),
        ("gh co 12", "co: pr checkout"),
        ("gh dash", "FAIL"),
    ):
        code, err, calls = run_merge(command, "dev", aliases)
        check(f"block-dangerous-git blocks gh alias use: {command!r} ({aliases})",
              code == 2 and "alias" in err, f"(code={code}, err={err!r})")
    for command in ("gh dash", "gh alias list", "gh pr checkout 12"):
        code, err, calls = run_merge(command, "dev", "co: pr checkout")
        check(f"block-dangerous-git allows non-alias gh command: {command!r}",
              code == 0 and err == "", f"(code={code}, err={err!r})")

    # Backslash-newline continuations (the layout GitHub's docs use for gh api)
    # and mid-word `#` (which is not a shell comment) hide nothing.
    for command, base in (
        ("gh api \\\n  --method PUT \\\n  -H \"Accept: application/vnd.github+json\" \\\n"
         "  /repos/o/r/pulls/5/merge \\\n  -f merge_method=merge", "dev"),
        ("gh api \\\n  --method PATCH \\\n  /repos/o/r/git/refs/heads/main \\\n  -f sha=abc", "dev"),
        ("gh api \\\n  --method DELETE \\\n  /repos/o/r/git/refs/heads/dev", "dev"),
        ("gh \\\n  pr merge 12 --merge", "main"),
        ("echo a#b; gh pr merge 12 --squash", "main"),
        ("gh pr comment 12 --body fixes#3 && gh pr merge 12", "main"),
    ):
        code, err, calls = run_merge(command, base)
        check(f"block-dangerous-git sees through continuation/mid-word #: {command!r}",
              code == 2, f"(code={code}, err={err!r})")

    # A branch switch earlier in the command makes the hook's current branch
    # (and its current-branch PR) the wrong thing to check.
    for command in ("git checkout dev && gh pr merge --merge",
                    "git switch dev && gh pr merge --squash",
                    "gh pr checkout 5 && gh pr merge --merge",
                    "git checkout feature/x && gh pr create --base main --title x"):
        code, err, calls = run_merge(command, "dev")
        check(f"block-dangerous-git blocks bare PR command after a branch switch: {command!r}",
              code == 2, f"(code={code}, err={err!r})")
    for command in ("git checkout feature/x && gh pr merge 12 --merge",
                    "git switch dev && gh pr create --base main --head dev --title x"):
        code, err, calls = run_merge(command, "dev")
        check(f"block-dangerous-git allows explicit PR command after a branch switch: {command!r}",
              code == 0 and err == "", f"(code={code}, err={err!r})")

    # Heredoc bodies are data (report text often holds an apostrophe), unless
    # a shell reads them. Real comments are dropped; `bash -c` scripts are read.
    for command in (
        "gh pr comment 12 --body-file - <<'EOF'\n🤖 Agent: David's comment is fixed in abc123.\nEOF",
        "gh pr edit 12 --body-file - <<'EOF'\n## Task\nit's done\nEOF",
        "gh pr create --base main --head dev --title x --body-file - <<'EOF'\nIt's ready\nEOF",
        "cat > /tmp/report.md <<'EOF'\nDavid's call\nEOF\ngh pr edit 12 --body-file /tmp/report.md",
        "git commit -F - <<'EOF'\nfix(hooks): don't block\nEOF",
        "gh pr list # David's open PRs",
        "git commit -m \"$(cat <<'EOF'\nfix: David's change\nEOF\n)\"",
        "gh pr comment 12 --body \"$(cat <<'EOF'\n🤖 Agent: it's fixed in abc123\nEOF\n)\"",
        "git push origin feature/x # not main",
    ):
        code, err, calls = run_merge(command, "main")
        check(f"block-dangerous-git allows heredoc/comment text: {command!r}",
              code == 0 and err == "", f"(code={code}, err={err!r})")
    for command in (
        "bash <<'EOF'\ngh pr merge 12 --merge\nEOF",
        "/bin/bash <<'EOF'\ngh pr merge 12 --merge\nEOF",
        "bash -o pipefail -c 'gh pr merge 12 --merge'",
        # `<<EOF` inside quotes or a comment is not a heredoc.
        'echo "use <<EOF"\ngh pr merge 12 --merge',
        "# write it with cat <<EOF\ngh pr merge 12 --merge",
        # Command substitution inside double quotes is left unstripped.
        'gh pr comment 12 --body "$(printf "Fixed #3")" && gh pr merge 12 --merge',
        "bash -c 'gh pr merge 12 --merge'",
        "sh -c \"gh api -X PUT repos/o/r/pulls/12/merge\"",
        "bash -lc 'gh pr -R o/r merge 12'",
    ):
        code, err, calls = run_merge(command, "main")
        check(f"block-dangerous-git reads commands run by a shell: {command!r}",
              code == 2, f"(code={code}, err={err!r})")

    # Command substitutions inside double quotes are read as commands.
    for command in (
        'PR_URL="$(gh pr create --fill --head feature/x)"',
        'out="$(gh pr merge 12 --merge 2>&1)"',
        'echo "`gh pr merge 12`"',
        "r=\"$(gh api graphql -f query='mutation { mergePullRequest(input: {}) { clientMutationId } }')\"",
        # A backslash-newline inside a quoted heredoc body or a comment does
        # not continue the line, so it hides nothing after it.
        "cat > r.md <<'EOF'\nnpm run x \\\nEOF\ngh pr merge 12 --merge",
        "# see C:\\\ngh pr merge 12 --merge",
    ):
        code, err, calls = run_merge(command, "main")
        check(f"block-dangerous-git reads quoted substitutions and stray backslashes: {command!r}",
              code == 2, f"(code={code}, err={err!r})")
    for command in (
        'PR_URL="$(gh pr create --base main --head dev --title x --body-file r.md)"',
        "gh pr edit 7 --body \"$(cat <<'EOF'\nA 27\\\" monitor (big)\nEOF\n)\"",
        "gh pr edit 7 --body \"$(cat <<'EOF'\nA 27\" monitor\nEOF\n)\"",
    ):
        code, err, calls = run_merge(command, "main")
        check(f"block-dangerous-git allows quoted substitution bodies: {command!r}",
              code == 0 and err == "", f"(code={code}, err={err!r})")

    # Pre-review: a GraphQL query built by a command substitution is unreadable.
    for command in (
        "gh api graphql -f query=\"$(cat <<'EOF'\nmutation { mergePullRequest(input: "
        "{pullRequestId: \\\"x\\\"}) { clientMutationId } }\nEOF\n)\"",
        'gh api graphql -f query="$(cat q.graphql)"',
        "gh api graphql -F owner=o",
    ):
        code, err, calls = run_merge(command, "dev")
        check(f"block-dangerous-git blocks GraphQL it cannot read: {command!r}",
              code == 2, f"(code={code}, err={err!r})")

    # Pre-review: text that only mentions a push to main is not a push.
    for command in (
        'gh pr create --base main --head dev --title "Promote dev to main" '
        '--body "Agents never git push to main; David merges."',
        'gh pr comment 12 --body "🤖 Agent: the hook blocks git push origin main as before"',
        'git commit -m "docs: agents never git push to main"',
        'grep -rn "git push origin main" hooks/',
        "gh pr comment 12 --body-file - <<'END-OF-BODY'\nit's done\nEND-OF-BODY",
        "cat <<\\EOF\nit's here\nEOF",
    ):
        code, err, calls = run_merge(command, "main")
        check(f"block-dangerous-git allows text about pushes and any heredoc word: {command!r}",
              code == 0 and err == "", f"(code={code}, err={err!r})")
    for command in ("bash -c 'git push origin main'", 'out="$(git push origin main 2>&1)"'):
        code, err, calls = run_merge(command, "dev")
        check(f"block-dangerous-git still blocks a push run by a shell: {command!r}",
              code == 2 and "main" in err, f"(code={code}, err={err!r})")

    # Pre-review: a blocked merge after cd says what fixes it.
    code, err, calls = run_merge("cd /tmp && gh pr merge 12 --merge", "dev")
    check("block-dangerous-git tells a merge after cd to pass --repo",
          code == 2 and "--repo owner/name" in err, f"(code={code}, err={err!r})")

    code, err, calls = run_merge("gh pr merge 12 --merge; gh pr merge 13 --merge", "main")
    check("block-dangerous-git blocks when any merge in the command targets main",
          code == 2 and "into main" in err, f"(code={code}, err={err!r})")

# Generated reports live outside the commit-gated tracker. Check the real
# status command without weakening protection for any .scratch directory.
with tempfile.TemporaryDirectory() as temp_dir:
    repo = Path(temp_dir)
    init_git_repo(repo)
    reports = repo / ".reports" / "status"
    reports.mkdir(parents=True)
    (reports / "snapshot.md").write_text("Dated progress snapshot\n", encoding="utf-8")
    for state in ("untracked", "staged", "modified"):
        if state == "staged":
            git(repo, "add", ".reports/status")
        elif state == "modified":
            git(repo, "commit", "-qm", "save snapshot")
            (reports / "snapshot.md").write_text("Updated snapshot\n", encoding="utf-8")
        code, err = run_hook(
            "require-committed-claim.py", dispatch_payload("Agent"), cwd=repo,
        )
        check(f"require-committed-claim allows {state} status report",
              code == 0 and err == "", f"(code={code}, err={err!r})")

    for relative in ("spec.md", "map.md", "issues/001.md", "status-reports/claim.md"):
        tracker_file = repo / ".scratch" / relative
        tracker_file.parent.mkdir(parents=True, exist_ok=True)
        tracker_file.write_text("Uncommitted tracker change\n", encoding="utf-8")
        code, err = run_hook(
            "require-committed-claim.py", dispatch_payload("Agent"), cwd=repo,
        )
        check(f"require-committed-claim blocks {relative} alongside reports",
              code == 2 and f".scratch/{relative}" in err
              and ".reports/status/snapshot.md" not in err,
              f"(code={code}, err={err!r})")
        git(repo, "add", ".scratch")
        git(repo, "commit", "-qm", "save tracker fixture")

# Current-branch behavior must be explicit and independent of the branch on
# which this repository's CI happens to run. A main checkout blocks implicit
# current-branch pushes; an explicit feature refspec is still safe. Bulk or
# matching pushes are blocked from every branch because they can include main.
with tempfile.TemporaryDirectory() as temp_dir:
    repo = Path(temp_dir)
    init_git_repo(repo, with_tracker=False)
    (repo / "README.md").write_text("hook fixture\n", encoding="utf-8")
    git(repo, "add", "README.md")
    git(repo, "commit", "-qm", "initial commit")
    git(repo, "branch", "-M", "main")

    for cmd in (
        "git push",
        "git push origin",
        'git push "/tmp/remote repo.git"',
        "git push --repo origin",
        "git push --recurse-submodules check origin",
        "git push origin HEAD",
        "git push origin +HEAD",
        "git push origin @",
        "git push origin feature/auth && git push",
        "git push origin feature/auth; git push origin",
    ):
        code, err = run_hook_bash("block-dangerous-git.py", cmd, cwd=repo)
        check(f"block-dangerous-git blocks implicit push from main: {cmd!r}",
              code == 2 and "current branch (main)" in err,
              f"(code={code}, err={err!r})")

    for cmd in (
        "git push origin feature/auth",
        "git push origin HEAD:feature/auth",
        "git push origin @:feature/auth",
        'git push "/tmp/remote repo.git" feature/auth',
        "git push --repo origin feature/auth",
    ):
        code, err = run_hook_bash("block-dangerous-git.py", cmd, cwd=repo)
        check(f"block-dangerous-git allows explicit feature push from main: {cmd!r}",
              code == 0 and err == "", f"(code={code}, err={err!r})")

    unbounded_pushes = (
        "git push --all origin",
        "git push --al origin",
        "git push origin --branches",
        "git push origin --bra",
        "git push --mirror origin",
        "git push --mi origin",
        "git push origin :",
        "git push origin +:",
        "git push origin refs/heads/*:refs/heads/*",
    )
    for cmd in unbounded_pushes:
        code, err = run_hook_bash("block-dangerous-git.py", cmd, cwd=repo)
        check(f"block-dangerous-git blocks unbounded push from main: {cmd!r}",
              code == 2 and "can update main" in err,
              f"(code={code}, err={err!r})")

    code, err = run_hook_bash("block-dangerous-git.py", "gh pr create --base main", cwd=repo)
    check("block-dangerous-git blocks PR into main from a main checkout",
          code == 2, f"(code={code}, err={err!r})")

    # From a main checkout: a switch chained by && to the push leaves main
    # behind; a `;` does not, since a failed switch would push main.
    git(repo, "branch", "dev")
    git(repo, "branch", "feature/x")
    code, err = run_hook_bash(
        "block-dangerous-git.py",
        "git checkout dev && git merge --no-ff feature/x && git push", cwd=repo)
    check("block-dangerous-git allows a chained switch to dev then push from main",
          code == 0 and err == "", f"(code={code}, err={err!r})")
    for cmd in ("git checkout dev; git push", "git checkout dev\ngit push",
                "git checkout dev || git push"):
        code, err = run_hook_bash("block-dangerous-git.py", cmd, cwd=repo)
        check(f"block-dangerous-git keeps main when the switch may fail: {cmd!r}",
              code == 2, f"(code={code}, err={err!r})")
    git(repo, "branch", "-q", "--delete", "dev")
    git(repo, "branch", "-q", "--delete", "feature/x")

    git(repo, "switch", "-qc", "dev")
    code, err = run_hook_bash("block-dangerous-git.py", "git push", cwd=repo)
    check("block-dangerous-git allows implicit push from dev",
          code == 0 and err == "", f"(code={code}, err={err!r})")

    for cmd in ("gh pr create --base main --title x", "gh pr create --fill"):
        code, err = run_hook_bash("block-dangerous-git.py", cmd, cwd=repo)
        check(f"block-dangerous-git allows promotion PR from a dev checkout: {cmd!r}",
              code == 0 and err == "", f"(code={code}, err={err!r})")

    for cmd in ("git push --force", "git push -f origin HEAD", "git push origin +@"):
        code, err = run_hook_bash("block-dangerous-git.py", cmd, cwd=repo)
        check(f"block-dangerous-git blocks force push from a dev checkout: {cmd!r}",
              code == 2 and "dev" in err, f"(code={code}, err={err!r})")

    git(repo, "switch", "-qc", "feature/x")
    code, err = run_hook_bash("block-dangerous-git.py", "gh pr create --base main", cwd=repo)
    check("block-dangerous-git blocks PR into main from a feature checkout",
          code == 2 and "feature/x" in err, f"(code={code}, err={err!r})")
    code, err = run_hook_bash("block-dangerous-git.py", "git push --force", cwd=repo)
    check("block-dangerous-git allows force push of a feature checkout",
          code == 0 and err == "", f"(code={code}, err={err!r})")

    # A literal switch to a readable branch moves the effective current branch.
    for cmd in ("git checkout dev && git merge --ff-only feature/x && git push",
                "git switch dev && git push",
                "git checkout -b feature/y && git push -u origin HEAD",
                "git switch dev && gh pr create --base main --head dev --title x",
                "git switch dev && gh pr create --base main --title x",
                # Pre-review: each push counts the last switch before it.
                "git checkout main && git pull && git checkout dev && git merge main && git push",
                "git checkout main && git pull --ff-only && git checkout feature/x && "
                "git rebase main && git push --force-with-lease"):
        code, err = run_hook_bash("block-dangerous-git.py", cmd, cwd=repo)
        check(f"block-dangerous-git follows a literal branch switch: {cmd!r}",
              code == 0 and err == "", f"(code={code}, err={err!r})")
    for cmd in ("git checkout main && git push",
                "git checkout dev && git push -f",
                "git checkout dev && git push --force origin HEAD",
                "git checkout notes.txt && git push",
                "gh pr checkout 5 && git push",
                "git switch feature/x && gh pr create --base main",
                "git switch dev; gh pr create --base main --title x",
                # Every branch the command passes through counts, not just the last.
                "git checkout main && git merge dev && git push && git checkout dev",
                "git switch main\ngit merge --ff-only dev\ngit push origin\ngit switch dev",
                "git checkout dev && git push -f && git switch -c feature/next"):
        code, err = run_hook_bash("block-dangerous-git.py", cmd, cwd=repo)
        check(f"block-dangerous-git blocks after a switch it cannot clear: {cmd!r}",
              code == 2, f"(code={code}, err={err!r})")

    git(repo, "switch", "-qc", "master")
    code, err = run_hook_bash("block-dangerous-git.py", "git push", cwd=repo)
    check("block-dangerous-git blocks implicit push from master",
          code == 2 and "current branch (master)" in err, f"(code={code}, err={err!r})")
    git(repo, "switch", "-q", "dev")

    for cmd in unbounded_pushes:
        code, err = run_hook_bash("block-dangerous-git.py", cmd, cwd=repo)
        check(f"block-dangerous-git blocks unbounded push from dev: {cmd!r}",
              code == 2 and "can update main" in err,
              f"(code={code}, err={err!r})")

# The four destructive-op patterns still block outright...
BLOCK_DESTRUCTIVE = [
    'git -C /tmp/repo reset --hard',
    'git -c color.ui=false clean -fd',
    'git --no-pager branch -D some-branch',
    'git --work-tree=/tmp/repo restore .',
    'git reset --hard',
    'git reset --hard HEAD~1',
    'git clean -f',
    'git clean -fd',
    'git branch -D some-branch',
    'git checkout .',
    'git restore .',
]

for cmd in BLOCK_DESTRUCTIVE:
    code, err = run_hook_bash("block-dangerous-git.py", cmd)
    check(f"block-dangerous-git blocks destructive op: {cmd!r}",
          code == 2, f"(code={code}, err={err!r})")

# ...and their safe lookalikes still pass.
PASS_DESTRUCTIVE_LOOKALIKES = [
    'git reset --soft HEAD~1',
    'git resetter --hard',
    'git clean -n',
    'git clean --dry-run',
    'git branch -d some-branch',
    'git checkout feature-branch',
    'git checkout main.txt',
    'git restore file.py',
]

for cmd in PASS_DESTRUCTIVE_LOOKALIKES:
    code, err = run_hook_bash("block-dangerous-git.py", cmd)
    check(f"block-dangerous-git allows safe lookalike: {cmd!r}",
          code == 0, f"(code={code}, err={err!r})")

# Non-Bash tool calls are always a no-op, regardless of command text.
code, err = run_hook(
    "block-dangerous-git.py",
    json.dumps({"tool_name": "Edit", "tool_input": {"command": "git push origin main"}}),
)
check("block-dangerous-git ignores non-Bash tool", code == 0 and err == "",
      f"(code={code}, err={err!r})")

# Malformed stdin must fail open: exit 0, no stderr.
MALFORMED_STDIN = ["", "not json", "null", "[]", '{"tool_name": "Bash"}']
MALFORMED_STDIN += [
    json.dumps({"tool_name": "Bash", "tool_input": value})
    for value in ([], "invalid", 7)
]
MALFORMED_STDIN += [
    json.dumps({"tool_name": "Bash", "tool_input": {"command": value}})
    for value in ([], {}, 7)
]
MALFORMED_STDIN += [json.dumps({"model": ["invalid"]})]

# Input deep enough to exhaust the scanner's recursion blocks rather than
# crashing (a crash exits 1, which the host treats as allow).
code, err = run_hook_bash("block-dangerous-git.py", 'echo "$(' * 2000 + "true" + ')"' * 2000)
check("block-dangerous-git blocks when analysis fails", code == 2 and "could not be checked" in err,
      f"(code={code}, err={err!r})")

for raw in MALFORMED_STDIN:
    code, err = run_hook("block-dangerous-git.py", raw)
    check(f"block-dangerous-git fails open on malformed stdin {raw!r}",
          code == 0 and err == "", f"(code={code}, err={err!r})")

# ---------------------------------------------------------------------------
# require-committed-claim.py: same fail-open contract on malformed stdin.
# ---------------------------------------------------------------------------

for raw in MALFORMED_STDIN:
    code, err = run_hook("require-committed-claim.py", raw)
    check(f"require-committed-claim fails open on malformed stdin {raw!r}",
          code == 0 and err == "", f"(code={code}, err={err!r})")

# A non-dispatch tool call is also a no-op regardless of stdin shape.
code, err = run_hook(
    "require-committed-claim.py",
    json.dumps({"tool_name": "Edit", "tool_input": {"command": "claude --bg foo"}}),
)
check("require-committed-claim ignores non-dispatch tool", code == 0 and err == "",
      f"(code={code}, err={err!r})")

# Temporary repositories exercise all tracker states through the real `git
# status` call made by the hook, including the Codex Agent alias and raw tool
# name. A test fixture that mocks `dirty_tracker_files` would miss precisely
# the contract this hook exists to enforce.
with tempfile.TemporaryDirectory() as temp_dir:
    repo = Path(temp_dir)
    init_git_repo(repo)

    for tool_name in ("Workflow", "Agent", "spawn_agent"):
        code, err = run_hook(
            "require-committed-claim.py",
            dispatch_payload(tool_name),
            cwd=repo,
        )
        check(f"require-committed-claim allows clean {tool_name} dispatch",
              code == 0 and err == "", f"(code={code}, err={err!r})")

    issue = repo / ".scratch" / "issues" / "001.md"
    issue.parent.mkdir()
    issue.write_text("Status: claimed\n", encoding="utf-8")
    for tool_name in ("Workflow", "Agent", "spawn_agent"):
        code, err = run_hook(
            "require-committed-claim.py",
            dispatch_payload(tool_name),
            cwd=repo,
        )
        check(f"require-committed-claim blocks untracked claim before {tool_name}",
              code == 2 and ".scratch/issues/001.md" in err,
              f"(code={code}, err={err!r})")

    git(repo, "add", ".scratch/issues/001.md")
    code, err = run_hook(
        "require-committed-claim.py",
        dispatch_payload("Agent"),
        cwd=repo,
    )
    check("require-committed-claim blocks staged claim before Agent",
          code == 2 and ".scratch/issues/001.md" in err,
          f"(code={code}, err={err!r})")

    git(repo, "commit", "-qm", "claim ticket")
    code, err = run_hook(
        "require-committed-claim.py",
        dispatch_payload("spawn_agent"),
        cwd=repo,
    )
    check("require-committed-claim allows committed claim before spawn_agent",
          code == 0 and err == "", f"(code={code}, err={err!r})")

    issue.write_text("Status: resolved\n", encoding="utf-8")
    code, err = run_hook(
        "require-committed-claim.py",
        dispatch_payload("Agent"),
        cwd=repo,
    )
    check("require-committed-claim blocks modified claim before Agent",
          code == 2 and ".scratch/issues/001.md" in err,
          f"(code={code}, err={err!r})")

    code, err = run_hook(
        "require-committed-claim.py",
        dispatch_payload("Bash", "claude --bg /delegate"),
        cwd=repo,
    )
    check("require-committed-claim blocks claude --bg with dirty tracker",
          code == 2 and ".scratch/issues/001.md" in err,
          f"(code={code}, err={err!r})")

    code, err = run_hook(
        "require-committed-claim.py",
        dispatch_payload("Bash", "claude /delegate"),
        cwd=repo,
    )
    check("require-committed-claim allows non-background claude command",
          code == 0 and err == "", f"(code={code}, err={err!r})")

with tempfile.TemporaryDirectory() as temp_dir:
    repo = Path(temp_dir)
    init_git_repo(repo, with_tracker=False)
    for tool_name, command in (
        ("Agent", None),
        ("spawn_agent", None),
        ("Bash", "claude --bg /delegate"),
    ):
        code, err = run_hook(
            "require-committed-claim.py",
            dispatch_payload(tool_name, command),
            cwd=repo,
        )
        check(f"require-committed-claim allows {tool_name} without .scratch",
              code == 0 and err == "", f"(code={code}, err={err!r})")

# ---------------------------------------------------------------------------
# delegate-recommend.py: fail-open input handling and SessionStart stdout JSON.
# ---------------------------------------------------------------------------

for raw in MALFORMED_STDIN:
    proc = run_hook_process("delegate-recommend.py", raw)
    check(f"delegate-recommend fails open on malformed stdin {raw!r}",
          proc.returncode == 0 and proc.stdout == "" and proc.stderr == "",
          f"(code={proc.returncode}, out={proc.stdout!r}, err={proc.stderr!r})")

for name, payload in (
    ("missing model", {}),
    ("nonmatching model", {"model": "claude-opus-5"}),
):
    proc = run_hook_process("delegate-recommend.py", json.dumps(payload))
    check(f"delegate-recommend is silent for {name}",
          proc.returncode == 0 and proc.stdout == "" and proc.stderr == "",
          f"(code={proc.returncode}, out={proc.stdout!r}, err={proc.stderr!r})")

with tempfile.TemporaryDirectory() as temp_dir:
    proc = run_hook_process(
        "delegate-recommend.py",
        json.dumps({"model": "claude-FABLE-5"}),
        cwd=Path(temp_dir),
    )
    try:
        output = json.loads(proc.stdout)
    except json.JSONDecodeError:
        output = {}
    context = output.get("hookSpecificOutput", {})
    check("delegate-recommend emits default-model SessionStart JSON",
          proc.returncode == 0
          and proc.stderr == ""
          and context.get("hookEventName") == "SessionStart"
          and "claude-FABLE-5" in context.get("additionalContext", "")
          and "fable" in context.get("additionalContext", "").lower(),
          f"(code={proc.returncode}, out={proc.stdout!r}, err={proc.stderr!r})")

with tempfile.TemporaryDirectory() as temp_dir:
    repo = Path(temp_dir)
    config = repo / "docs" / "agents"
    config.mkdir(parents=True)
    (config / "delegate.md").write_text(
        "# Delegate configuration\n\nRouter model: haiku\n",
        encoding="utf-8",
    )
    proc = run_hook_process(
        "delegate-recommend.py",
        json.dumps({"model": "claude-HAIKU-4"}),
        cwd=repo,
    )
    try:
        output = json.loads(proc.stdout)
    except json.JSONDecodeError:
        output = {}
    context = output.get("hookSpecificOutput", {})
    check("delegate-recommend honors configured model with valid JSON",
          proc.returncode == 0
          and proc.stderr == ""
          and context.get("hookEventName") == "SessionStart"
          and "claude-HAIKU-4" in context.get("additionalContext", "")
          and "haiku" in context.get("additionalContext", "").lower(),
          f"(code={proc.returncode}, out={proc.stdout!r}, err={proc.stderr!r})")


# Timing is exercised through the same CLI/stdin boundary as the installed hook.
def timing(args=(), payload=None, now=1000000000, cwd=REPO_ROOT):
    launcher = (
        "import runpy,sys; from pathlib import Path; from unittest.mock import patch; "
        "script=sys.argv.pop(1); instant=float(sys.argv.pop(1)); "
        "sys.argv[0]=script; sys.path.insert(0, str(Path(script).parent)); "
        "clock=patch('time.time', return_value=instant); clock.start(); "
        "runpy.run_path(script, run_name='__main__')"
    )
    return subprocess.run(
        [sys.executable, "-c", launcher, str(HOOKS_DIR / "run-timing.py"),
         str(now), *args],
        input=json.dumps(payload) if payload is not None else "",
        text=True, capture_output=True, cwd=cwd, timeout=10,
    )


with tempfile.TemporaryDirectory() as directory:
    workspace = Path(directory)
    started = timing(("start", "--session", "alpha", "--deadline", "2001-09-09T03:46:40Z"),
                     cwd=workspace)
    cue = timing(payload={"session_id": "alpha", "hook_event_name": "PostToolUse"},
                 cwd=workspace)
    check("timing starts an opt-in session and emits only remaining time",
          started.returncode == 0 and cue.returncode == 0
          and json.loads(cue.stdout).get("hookSpecificOutput", {}).get("additionalContext")
          == "Time remaining: 120 minutes.", started.stderr + cue.stderr)

    event = {"session_id": "alpha", "hook_event_name": "PostToolUse"}
    for elapsed, expected in ((1, ""), (299, ""), (300, "Time remaining: 115 minutes.")):
        result = timing(payload=event, now=1000000000 + elapsed, cwd=workspace)
        actual = (json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
                  if result.stdout else "")
        check(f"timing cue spacing at {elapsed} seconds", result.returncode == 0 and actual == expected)

    for payload in ({"session_id": "beta", "hook_event_name": "PostToolUse"},
                    {"session_id": "alpha", "hook_event_name": "PreToolUse"},
                    {"hook_event_name": "PostToolUse"}, None):
        result = timing(payload=payload, now=1000000600, cwd=workspace)
        check(f"timing is silent outside its session/event: {payload}",
              result.returncode == 0 and result.stdout == "" and result.stderr == "")

    restored = timing(payload={"session_id": "alpha", "hook_event_name": "SessionStart"},
                      now=1000000301, cwd=workspace)
    check("timing restores current time to a refreshed context",
          json.loads(restored.stdout)["hookSpecificOutput"]["additionalContext"]
          == "Time remaining: 115 minutes.")

    before = json.loads(timing(("status", "--session", "alpha"),
                              now=1000002699, cwd=workspace).stdout)
    due = json.loads(timing(("status", "--session", "alpha"),
                           now=1000002700, cwd=workspace).stdout)
    reset = json.loads(timing(("report", "--session", "alpha"),
                             now=1000001200, cwd=workspace).stdout)
    after = json.loads(timing(("status", "--session", "alpha"),
                             now=1000002700, cwd=workspace).stdout)
    check("timing report is due at the 45-minute maximum gap", not before["report_due"] and due["report_due"])
    check("milestone report resets its clock but preserves the deadline",
          reset["report_due_at"] == 1000003900 and not after["report_due"]
          and reset["deadline"] == before["deadline"] == 1000007200)

    replacement = timing(("start", "--session", "alpha", "--deadline", "2001-09-09T05:46:40Z"),
                         cwd=workspace)
    check("timing refuses to silently replace an active deadline", replacement.returncode != 0)
    expired = timing(payload=event, now=1000007200, cwd=workspace)
    repeated = timing(payload=event, now=1000007201, cwd=workspace)
    check("deadline cue is immediate and emitted once",
          json.loads(expired.stdout)["hookSpecificOutput"]["additionalContext"]
          == "Time remaining: 0 minutes." and repeated.stdout == "")
    finished = timing(("finish", "--session", "alpha"), now=1000007202, cwd=workspace)
    quiet = timing(payload=event, now=1000007500, cwd=workspace)
    check("finished run leaves no active timing cues",
          not json.loads(finished.stdout)["active"] and quiet.stdout == "")

with tempfile.TemporaryDirectory() as directory:
    workspace = Path(directory)
    for deadline in ("2001-09-09T03:46:40", "2001-09-08T00:00:00Z", "nonsense"):
        result = timing(("start", "--session", "invalid", "--deadline", deadline), cwd=workspace)
        check(f"timing rejects invalid or ambiguous deadline: {deadline}", result.returncode != 0)
    timing(("start", "--session", "beta", "--deadline", "2001-09-09T03:46:40Z",
            "--report-seconds", "0"), cwd=workspace)
    disabled = json.loads(timing(("status", "--session", "beta"), now=1000004000, cwd=workspace).stdout)
    check("timed reporting can be disabled independently", disabled["report_due_at"] is None)
    # Corrupt external state is a fault injection, not an assertion on implementation internals.
    for state in (workspace / ".reports" / ".run-timing").glob("*.json"):
        state.write_text("not JSON")
    corrupt = timing(payload={"session_id": "beta", "hook_event_name": "PostToolUse"}, cwd=workspace)
    check("corrupt advisory state cannot block tools or invent a cue",
          corrupt.returncode == 0 and corrupt.stdout == "" and corrupt.stderr == "")

with tempfile.TemporaryDirectory() as directory:
    workspace = Path(directory)
    started = timing(("start", "--session", "waiter", "--deadline", "2001-09-09T03:46:40Z"),
                     cwd=workspace)
    waited = timing(("wait", "--session", "waiter"), now=1000002700, cwd=workspace)
    check("OS wait returns when the report is due, without checking a job",
          waited.returncode == 0 and json.loads(waited.stdout)["reason"] == "report_due",
          waited.stderr)
    receipt = workspace / "receipt.json"
    receipt.write_text('{"exit_status": 1}')
    available = timing(("wait", "--session", "waiter", "--receipt", str(receipt)),
                       now=1000000100, cwd=workspace)
    check("receipt availability is not misreported as job success",
          json.loads(available.stdout)["reason"] == "receipt_available"
          and "success" not in json.loads(available.stdout))
    expiry = timing(("wait", "--session", "waiter", "--receipt", str(receipt)),
                    now=1000007200, cwd=workspace)
    check("deadline takes precedence over an available receipt",
          json.loads(expiry.stdout)["reason"] == "deadline")
    timing(payload={"session_id": "waiter", "hook_event_name": "PostToolUse"},
           now=1000007200, cwd=workspace)
    restored = timing(payload={"session_id": "waiter", "hook_event_name": "SessionStart"},
                      now=1000007201, cwd=workspace)
    check("expired deadline remains visible after context refresh",
          json.loads(restored.stdout)["hookSpecificOutput"]["additionalContext"]
          == "Time remaining: 0 minutes.")

with tempfile.TemporaryDirectory() as directory:
    from concurrent.futures import ThreadPoolExecutor

    workspace = Path(directory)
    timing(("start", "--session", "parallel", "--deadline", "2001-09-09T03:46:40Z"),
           cwd=workspace)
    with ThreadPoolExecutor(max_workers=4) as pool:
        cues = list(pool.map(lambda _: timing(payload={
            "session_id": "parallel", "hook_event_name": "PostToolUse"}, cwd=workspace), range(4)))
    check("concurrent tool completions emit one cue per interval",
          sum(bool(result.stdout) for result in cues) == 1
          and all(result.returncode == 0 for result in cues))

with tempfile.TemporaryDirectory() as directory:
    from datetime import datetime, timedelta, timezone
    import time

    workspace = Path(directory)
    deadline = (datetime.now(timezone.utc) + timedelta(seconds=6)).isoformat()
    start = subprocess.run([sys.executable, str(HOOKS_DIR / "run-timing.py"), "start",
                            "--session", "real-wait", "--deadline", deadline,
                            "--report-seconds", "1"], cwd=workspace, capture_output=True, text=True)
    began = time.monotonic()
    result = subprocess.run([sys.executable, str(HOOKS_DIR / "run-timing.py"), "wait",
                             "--session", "real-wait"], cwd=workspace, capture_output=True,
                            text=True, timeout=4)
    elapsed = time.monotonic() - began
    check("OS wait blocks until its real reporting boundary without model calls",
          start.returncode == result.returncode == 0
          and json.loads(result.stdout)["reason"] == "report_due" and 0.5 <= elapsed < 4)

print()
if _failed:
    print(f"{len(_failed)}/{_total} check(s) failed:")
    for name in _failed:
        print(f"  - {name}")
    sys.exit(1)

print(f"all {_total} checks passed.")
sys.exit(0)
