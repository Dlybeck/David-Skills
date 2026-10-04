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
import shlex
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
# block-dangerous-git.py: pushes to main block; proposed PRs to main allow
# human review without updating the protected branch.
# ---------------------------------------------------------------------------

# Only the guard receives these command strings; the proposed command is never
# executed. This catches the observed subprocess argv bypass at the JSON seam.
for command, expected in (
    ("python3 -c 'import subprocess; subprocess.run([\"git\", \"push\", \"--set-upstream\", \"origin\", \"main\"])'", 2),
    ('rg -n "git push --set-upstream origin main" hooks', 0),
):
    code, err = run_hook_bash("block-dangerous-git.py", command)
    check(f"executable Python main push: {command!r}", code == expected,
          f"(code={code}, err={err!r})")

# Guard-only fixtures: no submitted Python/shell source is run, even when the
# hook allows it. The fixture directory has no remote and no protected refs.
with tempfile.TemporaryDirectory() as temp_dir:
    fixture = Path(temp_dir)
    python_cases = [
        ('import subprocess as sp; sp.run(["git", "push", "origin", "HEAD:main"])', 2),
        ('from subprocess import run as launch; launch(args=("git", "push", "origin", "main"))', 2),
        ('import subprocess; args = ["git", "push", "origin", "main"]; subprocess.run(args)', 2),
        ('import subprocess; subprocess.run("git push origin main".split())', 2),
        ('import shlex as lex, subprocess; subprocess.run(lex.split("git push origin main"))', 2),
        ('import subprocess; subprocess.call(["/usr/bin/git", "push", "origin", "main"])', 2),
        ('import subprocess; subprocess.check_call(["git", "push", "--all", "origin"])', 2),
        ('import subprocess; subprocess.check_output(["git", "reset", "--hard"])', 2),
        ('import subprocess; subprocess.Popen(["git", "push", "origin", "main"])', 2),
        ('import subprocess; subprocess.run("git push origin main", shell=True)', 2),
        ('import subprocess; subprocess.run(["git push origin main", "ignored"], shell=True)', 2),
        ('import subprocess; subprocess.run(["bash", "-lc", "git push origin main"])', 2),
        ('import os; os.system("git push origin main")', 2),
        ('from os import popen; popen("git push origin main")', 2),
        ('import subprocess; subprocess.run(["git", "push"], cwd="/tmp/other")', 2),
        ('import subprocess; subprocess.run(["git", "push", "origin", "feature/main-page"])', 0),
        ('import subprocess; subprocess.run(["git", "push", "origin", "HEAD:feature/auth"], cwd="/tmp/other")', 0),
        ('import subprocess; subprocess.run(["gh", "pr", "create", "--base", "main", "--title", "x"])', 0),
        ('import subprocess; subprocess.run(["gh", "pr", "edit", "5", "--base=main"])', 0),
        ('import subprocess; subprocess.run(["rg", "git push origin main", "."])', 0),
        ('import subprocess; subprocess.run(["git", "log", "--grep=git push origin main"])', 0),
        ('import subprocess; subprocess.run("git push origin main")', 0),  # shell=False: not split into argv
        ('print("subprocess.run([\\\"git\\\", \\\"push\\\", \\\"origin\\\", \\\"main\\\"])")', 0),
        ('# git push origin main\nprint("git push origin main")', 0),
    ]
    for source, expected in python_cases:
        for command in ("python3 -c " + shlex.quote(source),
                        "python3 - <<'PY'\n" + source + "\nPY\n"):
            code, err = run_hook_bash("block-dangerous-git.py", command, cwd=fixture)
            check(f"Python executable/data boundary: {command!r}", code == expected,
                  f"(code={code}, err={err!r})")

    shell_cases = [
        ('/usr/bin/git push origin main', 2),
        ('> /tmp/log git push origin main', 2),
        ('2>/tmp/log git push origin main', 2),
        ('2>&1 git push origin main', 2),
        ('GIT_TRACE=1 > /tmp/log git push origin main', 2),
        ('> /tmp/log GIT_TRACE=1 git push origin main', 2),
        ('GIT_TRACE=1 > /tmp/log rg "git push origin main" .', 0),
        ('command git push origin main', 2),
        ('if true; then git push origin main; fi', 2),
        ('for item in one; do git push origin main; done', 2),
        ('{ git push origin main; }', 2),
        ('env git push origin main', 2),
        ('env GH_REPO=other/project git push origin main', 2),
        ('sudo git push origin main', 2),
        ('sh -c \'git push origin "ma"in\'', 2),
        ('bash --norc -c \'git push origin main\'', 2),
        ('bash --noprofile --norc -lc \'git push origin main\'', 2),
        ('bash --rcfile /tmp/bashrc -c \'git push origin main\'', 2),
        ('bash -o posix -c \'git push origin main\'', 2),
        ('bash --norc -c \'rg "git push origin main" .\'', 0),
        ('bash inspect.sh -c \'git push origin main\'', 0),
        ('python3 inspect.py -c \'import subprocess; subprocess.run(["git","push","origin","main"])\'', 0),
        ('bash -lc \'rg "git push origin main" hooks\'', 0),
        ('eval \'git push origin main\'', 2),
        ('rg "$(git push origin main)" .', 2),
        ('printf "%s" "`git push origin main`"', 2),
        ("rg '$(git push origin main)' .", 0),
        ('rg -n "git push --set-upstream origin main" hooks', 0),
        ('grep -R "gh pr merge 5 --auto" .', 0),
        ('printf "%s\\n" "git push origin main"', 0),
        ("printf '%s\\n' ';' git push origin main", 0),
        ("rg -n ';' git push origin main", 0),
        ("rg -n '|' git push origin main", 0),
        ("rg -n \\; git push origin main", 0),
        ("printf '%s\\n' 'git push origin main' | sh", 2),
        ("echo 'git push origin main' | bash", 2),
        ("printf 'git push origin main\\n' | sh", 2),
        ("printf '%s\\n' 'git push origin main' | rg push", 0),
        ("printf '%s\\n' 'import subprocess; subprocess.run([\"git\",\"push\",\"origin\",\"main\"])' | python3 -", 2),
        ('git log --grep="git push origin main"', 0),
        ('cat <<\'EOF\'\ngit push origin main\nEOF\n', 0),
        ('rg "<<PY" .\ngit push origin main', 2),
        ('rg "<<PY" .', 0),
        ('cat <<EOF\n$(git push origin main)\nEOF\n', 2),
        ('sh <<\'EOF\'\ngit push origin main\nEOF\n', 2),
        ('env python3 - <<\'PY\'\nimport subprocess\nsubprocess.run(["git", "push", "origin", "main"])\nPY\n', 2),
        ('cd /tmp && python3 - <<\'PY\'\nimport subprocess\nsubprocess.run(["git", "push", "origin", "main"])\nPY\n', 2),
        ('true && sh <<\'EOF\'\ngit push origin main\nEOF\n', 2),
        ('rg "git push origin main" .; git push origin main', 2),
        ('rg "git push origin main" . && git push origin HEAD:feature/auth', 0),
        ('gh pr create --base main --title "gh pr merge 5 --auto"', 0),
    ]
    for command, expected in shell_cases:
        code, err = run_hook_bash("block-dangerous-git.py", command, cwd=fixture)
        check(f"shell executable/data boundary: {command!r}", code == expected,
              f"(code={code}, err={err!r})")

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
    'git \\\n push origin main',
    'git push \\\n origin HEAD:main',
    'bash -lc "git \\\n push origin main"',
]

for cmd in BLOCK_PUSH_TO_MAIN:
    code, err = run_hook_bash("block-dangerous-git.py", cmd)
    check(f"block-dangerous-git blocks push-to-main: {cmd!r}",
          code == 2 and "main" in err, f"(code={code}, err={err!r})")

PASS_PR_TO_MAIN = [
    'gh pr create --base main --title "x"',
    'gh pr create --base "main" --title "x"',
    "gh pr create --base 'main' --title x",
    'gh pr create --draft --base=main --head dev --title x',
    'gh pr create -B main --head dev --title x',
    'gh pr create --base m"ai"n --title x',
    'cd /tmp/repo && gh pr create --base main --title x',
    'gh pr create --base main --title x; gh pr edit 5 --base main',
    'bash -lc \"gh pr create --base main --title x\"',
    'gh pr edit 5 --base=main',
    'gh pr edit 5 --base="main"',
]

for cmd in PASS_PR_TO_MAIN:
    code, err = run_hook_bash("block-dangerous-git.py", cmd)
    check(f"block-dangerous-git allows PR-to-main: {cmd!r}",
          code == 0 and err == "", f"(code={code}, err={err!r})")

# Merge policy uses only a read-only lookup. A stand-in gh records argv so
# tests prove repository/selector routing without network or actual merges.
with tempfile.TemporaryDirectory() as temp_dir:
    fixture = Path(temp_dir)
    fake_gh = fixture / "gh"
    calls = fixture / "calls.jsonl"
    fake_gh.write_text(
        f"#!{sys.executable}\n"
        "import json, os, sys, time\n"
        "with open(os.environ['TEST_GH_CALLS'], 'a') as log:\n"
        "    log.write(json.dumps(sys.argv[1:]) + '\\n')\n"
        "time.sleep(float(os.environ.get('TEST_GH_DELAY', '0')))\n"
        "print(os.environ['TEST_GH_RESPONSE'])\n"
        "sys.exit(int(os.environ.get('TEST_GH_EXIT', '0')))\n",
        encoding="utf-8",
    )
    fake_gh.chmod(0o755)
    environment = dict(os.environ, PATH=f"{fixture}{os.pathsep}{os.environ['PATH']}",
                       TEST_GH_CALLS=str(calls))

    def merge_hook(command, response='{"baseRefName":"main"}', exit_code=0, delay=0):
        calls.write_text("", encoding="utf-8")
        process = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "block-dangerous-git.py")],
            input=json.dumps({"tool_name": "Bash", "tool_input": {"command": command}}),
            capture_output=True, text=True, cwd=REPO_ROOT, timeout=10,
            env=dict(environment, TEST_GH_RESPONSE=response,
                     TEST_GH_EXIT=str(exit_code), TEST_GH_DELAY=str(delay)),
        )
        lookups = [json.loads(line) for line in calls.read_text().splitlines()]
        return process, lookups

    MERGE_CASES = [
        ("gh pr merge 5", ["5"]),
        ("gh pr merge --squash 5", ["5"]),
        ('gh pr merge "5" --rebase', ["5"]),
        ("gh pr merge 5 --merge --auto", ["5"]),
        ("gh pr merge 5 --admin", ["5"]),
        ("gh pr merge --squash", []),
        ("gh pr merge feature/auth --rebase", ["feature/auth"]),
        ("gh pr merge 5 -R other/project --squash", ["5", "--repo", "other/project"]),
        ("gh --repo=other/project pr merge 5 --auto", ["5", "--repo", "other/project"]),
        ("gh -R other/project pr merge 5", ["5", "--repo", "other/project"]),
        ("gh pr merge 5 -Rother/project", ["5", "--repo", "other/project"]),
        ("gh pr merge https://github.com/other/project/pull/5 --squash",
         ["https://github.com/other/project/pull/5"]),
        ("gh pr merge 5 --subject 'merge review' --body-file /tmp/body --match-head-commit abc",
         ["5"]),
        ("true && gh pr merge 5 --squash", ["5"]),
        ("gh pr view 5; gh pr merge 5 --auto", ["5"]),
        ("true\ngh pr merge 5 --rebase", ["5"]),
        ('bash -lc "gh pr merge 5 --squash"', ["5"]),
        ('sh -c \'gh pr merge "5" --auto\'', ["5"]),
        ('sh -c \'gh pr m"er"ge 5 --auto\'', ["5"]),
        ('bash -lc \'gh p"r" merge 5 --squash\'', ["5"]),
        ('bash -lc \'g"h" pr merge 5 --squash\'', ["5"]),
        ('sh -c \'g\\h pr merge 5 --auto\'', ["5"]),
        ('gh \\\n pr merge 5 --squash', ["5"]),
        ('gh pr \\\n merge 5 --auto', ["5"]),
        ('bash -lc "gh \\\n pr merge 5 --squash"', ["5"]),
        ('(gh pr merge 5 --squash)', ["5"]),
        ('gh pr m"er"ge 5 --rebase', ["5"]),
    ]
    for command, target in MERGE_CASES:
        for base, expected_code in (("main", 2), ("dev", 0), ("feature/main-page", 0)):
            process, lookups = merge_hook(command, json.dumps({"baseRefName": base}))
            check(f"PR merge base {base}: {command!r}",
                  process.returncode == expected_code
                  and ("human-gated" in process.stderr if expected_code else process.stderr == "")
                  and lookups == [["pr", "view", *target, "--json", "baseRefName"]],
                  f"(code={process.returncode}, err={process.stderr!r}, calls={lookups!r})")

    for response, exit_code in (
        ('{"baseRefName":"dev"}', 1), ("", 0), ("not json", 0),
        ("null", 0), ("[]", 0), ("{}", 0), ('{"baseRefName":7}', 0),
        ('{"baseRefName":""}', 0), ('{"baseRefName":" main "}', 0),
    ):
        process, _ = merge_hook("gh pr merge 5 --squash", response, exit_code)
        check(f"PR merge blocks failed/malformed lookup: {response!r}/{exit_code}",
              process.returncode == 2 and "cannot verify" in process.stderr,
              process.stderr)
    process, _ = merge_hook("gh pr merge 5 --squash", delay=6)
    check("PR merge lookup timeout blocks", process.returncode == 2 and "cannot verify" in process.stderr)

    for command in (
        "gh pr merge 5 6", "gh pr merge 5 --unknown-flag", "gh pr merge 5 --repo",
        "gh pr merge '$PR'", "gh pr merge 5 --repo '$REPO'", "gh pr merge '5",
        "cd /tmp/other && gh pr merge 5", "GH_REPO=other/project gh pr merge 5",
        "env GH_REPO=other/project gh pr merge 5",
        "gh pr merge 5 -R first/project --repo second/project",
        'bash -lc "cd /tmp/other && gh pr merge 5 --squash"',
        'sh -c \'c"d" /tmp/other && gh pr m"er"ge 5 --auto\'',
        'bash -lc "c\\d /tmp/other && gh pr merge 5"',
        'bash -lc "git -C /tmp/other status && gh pr merge 5"',
        'bash -lc "GH_REPO=other/project gh pr merge 5"',
        "pushd /tmp/other && gh pr merge 5", "git switch other && gh pr merge --squash",
        "gh pr edit 5 --base main && gh pr merge 5 --squash",
        "gh pr create --base main --title x; gh pr merge --auto",
        'bash -lc "gh pr edit 5 --base main; gh pr merge 5 --auto"',
        'gh(){ command gh -R other/project "$@"; }; gh pr merge 5',
        "alias gh='gh -R other/project'; gh pr merge 5",
        "gh repo set-default other/project && gh pr merge 5 --squash",
        'bash -lc "gh repo set-default other/project && gh pr merge 5"',
        "git remote set-url origin https://github.com/other/project && gh pr merge 5",
        "git config remote.origin.url https://github.com/other/project && gh pr merge 5",
        "gh config set host other.host && gh pr merge 5",
        "GH_REPO=other/project bash -c 'gh pr merge 5'",
        "GH_REPO=other/project sh <<'SH'\ngh pr merge 5\nSH\n",
        "GH_REPO=other/project eval 'gh pr merge 5'",
        "bash --rcfile /tmp/config -c 'gh pr merge 5'",
        ". /tmp/config && gh pr merge 5",
        "python3 -c 'import subprocess; subprocess.run([\"gh\", \"pr\", \"merge\", \"5\", \"--auto\"])'",
        "python3 - <<'PY'\nimport subprocess\nsubprocess.run(['gh', 'pr', 'merge', '5'])\nPY\n",
    ):
        process, lookups = merge_hook(command, '{"baseRefName":"dev"}')
        check(f"PR merge blocks ambiguous context/target: {command!r}",
              process.returncode == 2 and "cannot verify" in process.stderr and lookups == [],
              f"(code={process.returncode}, err={process.stderr!r}, calls={lookups!r})")

    process, lookups = merge_hook('rg "gh pr merge 5 --auto" .', "not json")
    check("inert merge search performs no PR lookup", process.returncode == 0 and lookups == [])
    process, lookups = merge_hook('rg "git push origin main" .; gh pr merge 5', '{"baseRefName":"dev"}')
    check("inert search preserves verified non-main merge", process.returncode == 0
          and lookups == [["pr", "view", "5", "--json", "baseRefName"]])

    process, lookups = merge_hook("gh pr merge 5 && gh pr merge 6", '{"baseRefName":"dev"}')
    check("PR merge verifies every shell-composed target", process.returncode == 0
          and lookups == [["pr", "view", str(number), "--json", "baseRefName"] for number in (5, 6)])
    for command in PASS_PR_TO_MAIN:
        process, lookups = merge_hook(command, "not json")
        check(f"proposed main PR requires no merge lookup: {command!r}",
              process.returncode == 0 and process.stderr == "" and lookups == [])

    for command in (
        "gh pr create --base main --title x && git push origin main",
        "gh pr edit 5 --base main; git push origin HEAD:main",
        "gh pr create --base main --title x\ngit push origin main",
        'bash -lc "gh pr create --base main --title x; git push origin main"',
    ):
        process, lookups = merge_hook(command)
        check(f"proposed PR does not authorize composed main push: {command!r}",
              process.returncode == 2 and "pushes directly to main" in process.stderr and lookups == [])

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
