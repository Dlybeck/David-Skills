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
]

for cmd in PASS_LOOKALIKES:
    code, err = run_hook_bash("block-dangerous-git.py", cmd)
    check(f"block-dangerous-git allows lookalike: {cmd!r}",
          code == 0, f"(code={code}, err={err!r})")

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

    git(repo, "switch", "-qc", "dev")
    code, err = run_hook_bash("block-dangerous-git.py", "git push", cwd=repo)
    check("block-dangerous-git allows implicit push from dev",
          code == 0 and err == "", f"(code={code}, err={err!r})")

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
