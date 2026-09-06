#!/usr/bin/env python3
"""Opt-in bounded native Codex evaluations; never part of npm test.

Uses the existing ChatGPT login. Does not install plugins or change user config.
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
import subprocess
import tempfile
import time

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
        },
        "prompt": "Use $pursue-goal for the goal in CONTRACT.md. Complete the bounded research and implementation from evidence, then report the result and any remaining limits. I am delegating the choices inside that contract. Do not manufacture tickets or a new spec.",
    },
}


def run(command, cwd, **kwargs):
    return subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True,
                          timeout=15, **kwargs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=CASES)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    if not 1 <= args.timeout <= 180:
        parser.error("timeout must be 1..180 seconds")
    case = CASES[args.case]
    folder = Path(tempfile.mkdtemp(prefix=f"david-eval-{args.case}-"))
    project = folder / "project"
    project.mkdir()
    snapshot = {}
    if not case.get("installed"):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        for relative in manifest["skills"]:
            source = (ROOT / relative).resolve()
            source.relative_to(ROOT)  # Refuse a manifest path outside this repository.
            target = project / ".agents/skills" / source.name
            shutil.copytree(source, target)
            for path in source.rglob("*"):
                if path.is_file():
                    snapshot[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
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
    (folder / "request.txt").write_text(case["prompt"] + "\n")
    command = ["codex", "exec", "--ephemeral", "--json", "-s", "workspace-write",
               "-C", str(project), "-c", 'forced_login_method="chatgpt"',
               "-c", "mcp_servers.arr-suite.enabled=false",
               "-c", "mcp_servers.openaiDeveloperDocs.enabled=false",
               "-c", "features.apps=false", "-c", "features.memories=false",
               "-o", str(folder / "answer.md")]
    if not case.get("installed"):
        command += ["-c", 'plugins."david-skills@david-skills".enabled=false']
    command += [case["prompt"]]
    env = os.environ.copy()
    env.pop("OPENAI_API_KEY", None)  # This evaluation must use existing subscription auth.
    started = time.monotonic()
    receipt = {"case": args.case, "project": str(project), "mode":
               "installed-plugin" if case.get("installed") else "candidate-project-skills"}
    print(json.dumps({"started": receipt, "receipt": str(folder / "receipt.json")}), flush=True)
    with (folder / "trace.jsonl").open("w") as trace, (folder / "stderr.log").open("w") as errors:
        try:
            process = subprocess.run(command, stdout=trace, stderr=errors, env=env,
                                     timeout=args.timeout, cwd=project)
            receipt.update(status="finished", exit_code=process.returncode)
        except subprocess.TimeoutExpired:
            receipt.update(status="timeout", exit_code=None)
        except OSError as exc:
            receipt.update(status="launch-failed", error=str(exc))
    receipt["elapsed_seconds"] = round(time.monotonic() - started, 2)
    receipt["git_status"] = run(["git", "status", "--porcelain"], project).stdout
    (folder / "changes.patch").write_text(run(["git", "diff", "HEAD"], project).stdout)
    (folder / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt), flush=True)
    return 0 if receipt.get("exit_code") == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
