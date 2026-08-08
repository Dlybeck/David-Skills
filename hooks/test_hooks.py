#!/usr/bin/env python3
"""
Executable tests for this plugin's hooks -- the repo's first executable test
file (ADR 0006, "hooks carry executable tests": a mechanical rule deserves a
mechanical check). Drives each hook as a subprocess through its real, only
contract -- JSON on stdin, allow (exit 0) or block (exit 2, with a stderr
message) via exit code -- the same contract Claude Code itself relies on.
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
import subprocess
import sys
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


def run_hook(script, stdin_text):
    """Run a hook script as a subprocess with raw text on stdin, exactly as
    Claude Code invokes it. Returns (exit_code, stderr)."""
    proc = subprocess.run(
        [sys.executable, str(HOOKS_DIR / script)],
        input=stdin_text,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        timeout=10,
    )
    return proc.returncode, proc.stderr


def run_hook_bash(script, command):
    """Run a hook with a Claude Code-shaped PreToolUse payload for a Bash
    tool call carrying `command`."""
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    return run_hook(script, payload)


# ---------------------------------------------------------------------------
# block-dangerous-git.py: push-to-main and PR-to-main, plain/quoted/
# interpolation-adjacent spellings, all must block.
# ---------------------------------------------------------------------------

BLOCK_PUSH_TO_MAIN = [
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
    'gh pr create --base main --title "x"',
    'gh pr create --base "main" --title "x"',
    "gh pr create --base 'main' --title x",
    'gh pr edit 5 --base=main',
    'gh pr edit 5 --base="main"',
]

for cmd in BLOCK_PR_TO_MAIN:
    code, err = run_hook_bash("block-dangerous-git.py", cmd)
    check(f"block-dangerous-git blocks PR-to-main: {cmd!r}",
          code == 2 and "main" in err, f"(code={code}, err={err!r})")

# Feature-branch pushes and feature/main-page-style lookalikes must pass,
# quoted or not -- the boundary behavior the fix must not break.
PASS_LOOKALIKES = [
    'git push origin feature/main-page',
    'git push origin "feature/main-page"',
    "git push origin 'feature/main-page'",
    'git push origin feature-branch',
    'git push origin maintenance',
    'git push origin "maintenance"',
    'gh pr create --base dev --title "x"',
    'gh pr create --base develop --title "x"',
]

for cmd in PASS_LOOKALIKES:
    code, err = run_hook_bash("block-dangerous-git.py", cmd)
    check(f"block-dangerous-git allows lookalike: {cmd!r}",
          code == 0, f"(code={code}, err={err!r})")

# The four destructive-op patterns still block outright...
BLOCK_DESTRUCTIVE = [
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


print()
if _failed:
    print(f"{len(_failed)}/{_total} check(s) failed:")
    for name in _failed:
        print(f"  - {name}")
    sys.exit(1)

print(f"all {_total} checks passed.")
sys.exit(0)
