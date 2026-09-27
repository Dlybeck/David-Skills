#!/usr/bin/env python3
"""Opt-in bounded native Codex evaluations; never part of npm test.

Uses the existing ChatGPT login. Does not install plugins. Supplies temporary
project trust as a command override; check user config for CLI side effects.
Candidate skills are copied from the manifest to temporary project-local discovery
roots; this is source behavior coverage, not a packaged-plugin upgrade test.
Outputs native traces, final answers, fixture changes, and a terminal receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import time

from pivot_cases import CASES as PIVOT_CASES
from evaluate_steering import execute_steered

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    "installed-router": {
        "installed": True,
        "prompt": "Use $david-skills:advise. I have already implemented a small change and want it reviewed against my request. There is no ticket or spec file, and I do not want to create either. Which skill should I use? Recommend only; do not start a review.",
    },
    "delegated-tdd": {
        "files": {"labels.py": "def normalize_label(text):\n    return text\n"},
        "prompt": "Use $tdd to implement normalize_label(text): trim surrounding whitespace, collapse internal whitespace to one space, and lowercase. The public normalize_label function is the agreed seam. I delegate test design and implementation; use Python standard-library unittest. Empty or whitespace-only strings return an empty string. No spec, tickets, commits, or extra approval rounds are wanted.",
    },
    "diagnosis-only": {
        "files": {
            "totals.py": "def invoice_total(items):\n    return sum(price for price, quantity in items)\n",
            "repro.py": "from totals import invoice_total\nassert invoice_total([(10, 3), (5, 2)]) == 40\n",
        },
        "prompt": "Use $diagnosing-bugs. The invoice total is wrong; python3 repro.py reproduces it. Diagnose and explain the cause only. Do not change any files or implement a fix.",
    },
    "revisit-decision": {
        "files": {"CONTEXT.md": "# Domain\nA workspace is a private collection of notes.\n"},
        "prompt": "Use $grill-me here in this repo, but keep this discussion stateless. Earlier we agreed notes would sync to the cloud. I have changed my mind: this prototype must now be local-only and work offline. Scope remains one person, one device, plaintext notes, no accounts, no sharing. We already settled the editor layout and file format. Help me stress-test only the consequences of changing the sync decision. Ask the first focused round; do not implement or save documents.",
    },
    "side-intake": {
        "prompt": "Use $grill-me. I'm dictating while doing something else and can answer only a sentence or two before I leave. I want a private, offline notes tool for one person on one device, with no account or sharing. Help me clarify what matters before you design it. Ask the first question now; do not implement or save documents.",
        "criteria": [
            "Starts with one short, high-level question about an unknown that matters if the user leaves.",
            "Reuses the stated offline, private, single-device constraints instead of reopening them.",
            "Does not design, implement, or save documents before the user's answer.",
        ],
    },
    "status-evidence": {
        "files": {
            "PLAN.md": "# Direction\nOutcome: reliable offline notes.\nMilestone: recover unsaved notes after a restart. Proof: restart recovery test passes.\n",
            "OLD-STATUS.md": "# Status, 2026-09-01\nRecovery complete and deployed.\n",
            "receipts/test-2026-09-06.txt": "2026-09-06\nrestart recovery: FAIL, empty buffer after restart\nexit status: 1\n",
            "recovery.py": "def recover():\n    return ''\n",
        },
        "prompt": "Use $status-report for this project. Give me a concise chat overview, a Markdown report, and a self-contained local HTML version I can open on my phone later. Place current progress in the project-level goal. No hosting, installation, new experiments, or changes to source plans/code. Use existing evidence.",
    },
    "research-delivery": {
        "files": {
            "CONTRACT.md": "# Goal contract\nObjective: choose and implement a stable deduplication function for note IDs.\nProof: preserve first-seen order, no input mutation, handle empty input, and pass unittest cases.\nResearch: compare list scanning with a set-backed method using local primary implementations; no web needed.\nAuthority: inspect, run short local experiments, choose seams/test cases, edit dedupe.py and tests, and save one continuity note. Work in this current disposable checkout. No remote actions, commits, delegation, or questions unless scope changes.\n",
            "dedupe.py": "def dedupe(ids):\n    return sorted(set(ids))\n",
            "CONTINUITY.md": "# Prior checkpoint (unverified)\nDeduplication is complete and tests pass. No test receipt or command was recorded.\nNext: report completion.\n",
        },
        "prompt": "Use $pursue-goal for the goal in CONTRACT.md. Complete the bounded research and implementation from evidence, then report the result and any remaining limits. I am delegating the choices inside that contract. Do not manufacture tickets or a new spec.",
    },
}
CASE_SKILLS = {
    "installed-router": "advise", "delegated-tdd": "tdd",
    "diagnosis-only": "diagnosing-bugs", "revisit-decision": "grill-me",
    "side-intake": "grill-me",
    "status-evidence": "status-report", "research-delivery": "pursue-goal",
}

# Keep export coverage separate from the ordinary report request. These are
# opt-in behavioral scenarios, not text-matching assertions about skill prose.
CASES["status-chat"] = {
    "files": dict(CASES["status-evidence"]["files"]),
    "prompt": "Use $status-report. Where are we with this project, how does the current work connect to the bigger goal, and what should happen next? Use existing evidence; no new experiments or source changes.",
}
CASES["status-web"] = {
    "files": dict(CASES["status-evidence"]["files"]),
    "prompt": "Use $status-report. Make a self-contained local HTML status report for this project, with the conclusions in chat. No Markdown companion, hosting, installation, experiments, or source changes.",
}
CASES["status-brief"] = {
    "files": {"receipt.txt": "Checkpoint 4 of 10; same checkpoint as the previous check. Completion not recorded.\n"},
    "prompt": "Use $status-report. Check receipt.txt once: has there been any recorded change since checkpoint 4?",
}
CASE_SKILLS.update({name: "status-report" for name in
                    ("status-chat", "status-web", "status-brief")})
CASES.update(PIVOT_CASES)
CASE_SKILLS.update({name: case["skill"] for name, case in PIVOT_CASES.items()})


def run(command, cwd, **kwargs):
    return subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True,
                          timeout=15, **kwargs)


def git_snapshot(project):
    """Record independent delivery facts, not a model's description of them."""
    try:
        worktree = run(["git", "rev-parse", "--show-toplevel"], project).stdout.strip()
        status = run(["git", "status", "--porcelain=v2", "--branch",
                      "--untracked-files=all"], project).stdout
    except (OSError, subprocess.SubprocessError) as exc:
        return {"status": "unavailable", "error": str(exc)}
    headers = dict(line[2:].split(" ", 1) for line in status.splitlines()
                   if line.startswith("# "))
    branch = headers.get("branch.head")
    revision = headers.get("branch.oid")
    return {"status": "observed", "worktree": worktree,
            "branch": None if branch == "(detached)" else branch,
            "detached": branch == "(detached)",
            "revision": None if revision == "(initial)" else revision,
            "dirty": any(not line.startswith("# ") for line in status.splitlines()),
            "porcelain_v2": status}


def classify_trace(trace_text, exit_code):
    """Validate runtime evidence, not the skill's behavior or answer quality."""
    reasons = []
    completed = False
    tool_events = 0
    if exit_code != 0:
        reasons.append(f"process exit: {exit_code}")
    for number, line in enumerate(trace_text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            reasons.append(f"malformed trace line {number}")
            continue
        if not isinstance(event, dict) or not isinstance(event.get("type"), str):
            reasons.append(f"invalid event at line {number}")
            continue
        item = event.get("item")
        if isinstance(item, dict) and item.get("type") in {
            "command_execution", "mcp_tool_call", "function_call", "tool_call"
        }:
            tool_events += 1
        nested = event.get("event", {})
        if isinstance(nested, dict) and nested.get("method") == "item/started":
            if nested.get("params", {}).get("item", {}).get("type") in {
                "commandExecution", "mcpToolCall", "dynamicToolCall"
            }:
                tool_events += 1
        if event["type"] in {"error", "turn.failed"} or (
            isinstance(item, dict) and item.get("type") == "error"
        ):
            reasons.append(f"runtime error at line {number}")
        if event["type"] == "turn.completed":
            completed = True
    if not completed:
        reasons.append("missing turn.completed")
    return {"status": "invalid-runtime" if reasons else "needs-review",
            "runtime_issues": reasons, "behavioral_verdict": "not-evaluated",
            "observed_tool_events": tool_events,
            "evidence_warnings": [] if tool_events else [
                "No tool-execution events observed; required skill reads or local actions are unverified"]}


def execute(command, project, env, timeout, trace, errors):
    """Bound the entire subprocess group, including tool children, on timeout."""
    try:
        with subprocess.Popen(command, stdout=trace, stderr=errors, env=env,
                              stdin=subprocess.DEVNULL, cwd=project,
                              start_new_session=True) as process:
            try:
                return {"exit_code": process.wait(timeout=timeout)}
            except subprocess.TimeoutExpired:
                # Only this evaluation's new process group is targeted.
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait()
                return {"status": "timeout", "exit_code": process.returncode}
    except OSError as exc:
        return {"status": "launch-failed", "error": str(exc), "exit_code": None}


def config_fingerprint():
    """Detect CLI configuration side effects without reporting configuration contents."""
    config = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "config.toml"
    try:
        return {"status": "observed", "sha256": hashlib.sha256(config.read_bytes()).hexdigest()}
    except FileNotFoundError:
        return {"status": "absent"}
    except OSError:
        return {"status": "unavailable"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=CASES)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--enable-code-mode-host", action="store_true",
                        help="Explicitly enable the execution host for this subprocess only")
    parser.add_argument("--full-access", action="store_true",
                        help="Explicitly authorized unsandboxed run in the disposable directory")
    parser.add_argument("--installed-root", type=Path,
                        help="Read skills from this installed plugin instead of candidate sources")
    args = parser.parse_args()
    if not 1 <= args.timeout <= 600:
        parser.error("timeout must be 1..600 seconds")
    if args.case in PIVOT_CASES and args.timeout > 300:
        parser.error("pivot evaluations are limited to 300 seconds each")
    runtime_directory = None
    if args.enable_code_mode_host:
        executable = shutil.which("codex")
        if not executable:
            parser.error("codex is not on PATH")
        bundled = Path(executable).resolve().parent / "codex-code-mode-host"
        helper = str(bundled) if bundled.is_file() else shutil.which("codex-code-mode-host")
        if not helper or not os.access(helper, os.X_OK):
            parser.error("execution helper unavailable; no installation attempted")
        runtime_directory = str(Path(helper).parent)
    case = CASES[args.case]
    installed = bool(case.get("installed") or args.installed_root)
    if installed and not args.installed_root:
        parser.error("installed mode requires --installed-root pointing at the actual plugin")
    folder = Path(tempfile.mkdtemp(prefix=f"david-eval-{args.case}-"))
    project = folder / "project"
    project.mkdir()
    snapshot = {}
    source_root = args.installed_root.resolve() if installed else ROOT
    manifest = json.loads((source_root / ".codex-plugin/plugin.json").read_text())
    entrypoint = None
    for relative in manifest["skills"]:
        source = (source_root / relative).resolve()
        source.relative_to(source_root)  # Refuse a manifest path outside its bundle.
        target = project / ".agents/skills" / source.name
        if not installed:
            shutil.copytree(source, target)
        if source.name == CASE_SKILLS[args.case]:
            entrypoint = (source if installed else target) / "SKILL.md"
        for path in source.rglob("*"):
            if path.is_file():
                snapshot[str(path.relative_to(source_root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    if entrypoint is None:
        parser.error("requested skill is missing from the selected manifest")
    prompt = f"Read and use the skill at {entrypoint} completely before acting.\n\n{case['prompt']}"
    for relative, content in case.get("files", {}).items():
        target = project / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    (project / "AGENTS.md").write_text(
        "# Disposable evaluation project\n"
        "Work only inside this project. Do not install dependencies, access credentials, use external "
        "services, or modify user configuration. Do not create subagents. Run only short local checks. "
        "Respect the user's requested scope and report validation limits honestly.\n"
    )
    run(["git", "init", "-q", "-b", "eval"], project)
    run(["git", "config", "user.name", "Toolkit Evaluation"], project)
    run(["git", "config", "user.email", "evaluation@example.invalid"], project)
    run(["git", "add", "."], project)
    run(["git", "commit", "-qm", "fixture"], project)
    (folder / "source-hashes.json").write_text(json.dumps(snapshot, indent=2) + "\n")
    (folder / "request.txt").write_text(prompt + "\n")
    sandbox = "danger-full-access" if args.full_access else "workspace-write"
    command = ["codex", "exec", "--ephemeral", "--json", "-s", sandbox,
               "-C", str(project), "-c", 'forced_login_method="chatgpt"',
               "-c", f'projects.{json.dumps(str(project))}.trust_level="trusted"',
               "-c", "mcp_servers.arr-suite.enabled=false",
               "-c", "mcp_servers.openaiDeveloperDocs.enabled=false",
               "-c", "features.apps=false", "-c", "features.memories=false",
               "-o", str(folder / "answer.md")]
    if not installed:
        command += ["-c", 'plugins."david-skills@david-skills".enabled=false']
    if args.enable_code_mode_host:
        command += ["-c", "features.code_mode_host=true"]
    command += [prompt]
    env = os.environ.copy()
    env.pop("OPENAI_API_KEY", None)  # This evaluation must use existing subscription auth.
    if runtime_directory:
        env["PATH"] = runtime_directory + os.pathsep + env.get("PATH", "")
    started = time.monotonic()
    receipt = {"case": args.case, "project": str(project), "mode":
               "installed-plugin" if installed else "candidate-project-skills",
               "entrypoint": str(entrypoint), "sandbox": sandbox}
    receipt["runtime_override"] = args.enable_code_mode_host
    receipt["criteria"] = case.get("criteria", [])
    receipt["git_before"] = git_snapshot(project)
    receipt["account_config_before"] = config_fingerprint()
    print(json.dumps({"started": receipt, "receipt": str(folder / "receipt.json")}), flush=True)
    with (folder / "trace.jsonl").open("w") as trace, (folder / "stderr.log").open("w") as errors:
        if case.get("steer"):
            receipt.update(execute_steered(command, project, env, args.timeout, trace, errors, case))
        else:
            receipt.update(execute(command, project, env, args.timeout, trace, errors))
    validation = classify_trace((folder / "trace.jsonl").read_text(), receipt["exit_code"])
    runtime_status = receipt.get("status")
    receipt.update(validation)
    if runtime_status:
        receipt["status"] = runtime_status
    receipt["account_config_after"] = config_fingerprint()
    receipt["account_config_changed"] = receipt["account_config_before"] != receipt["account_config_after"]
    if receipt["account_config_changed"]:
        receipt["status"] = "invalid-environment"
        receipt["evidence_warnings"].append("Account configuration changed during evaluation; review side effects before another run")
    if receipt["account_config_before"]["status"] == "unavailable" or receipt["account_config_after"]["status"] == "unavailable":
        receipt["evidence_warnings"].append("Account configuration side effects could not be checked")
    receipt["elapsed_seconds"] = round(time.monotonic() - started, 2)
    receipt["git_after"] = git_snapshot(project)
    receipt["git_status"] = run(["git", "status", "--porcelain"], project).stdout
    (folder / "changes.patch").write_text(run(["git", "diff", "HEAD"], project).stdout)
    (folder / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt), flush=True)
    return 0 if receipt["status"] == "needs-review" else 1


if __name__ == "__main__":
    raise SystemExit(main())
