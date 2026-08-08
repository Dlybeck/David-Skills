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


def run_hook_bash(script, command):
    """Run a hook with a Claude Code-shaped PreToolUse payload for a Bash
    tool call carrying `command`."""
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    return run_hook(script, payload)


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


print()
if _failed:
    print(f"{len(_failed)}/{_total} check(s) failed:")
    for name in _failed:
        print(f"  - {name}")
    sys.exit(1)

print(f"all {_total} checks passed.")
sys.exit(0)
