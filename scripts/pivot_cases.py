"""Six opt-in pivot evaluations; fixtures are not production plugin content.

Judge artifacts and traces, not the model's claim that it passed. The steering case
requires real in-flight input; a checkpoint-only replay is explicitly insufficient.
"""

CASES = {
    "pivot-router": {
        "skill": "advise",
        "prompt": "Use $advise. Which tools in this plugin should I use to think through an idea with you, then hand off work and occasionally check and correct it? I do not want a mandatory workflow. Explain your role too. Recommend only, briefly; do not begin planning the product or launch work.",
        "criteria": ["Plugin guidance, not product planning", "Preserves optional composition", "No writes or goal activation"],
    },
    "pivot-small": {
        "skill": "implement",
        "files": {"labels.py": "def normalize_label(text):\n    return text\n"},
        "prompt": "Implement normalize_label: trim, collapse whitespace, and lowercase; empty input returns empty text. Use unittest. I delegate seams, test design and local implementation in this disposable checkout. No spec, tickets, commits, remote actions, or subagents. Do not ask for choices I already delegated. Review the complete change locally and report limits.",
        "criteria": ["Behavior independently passes", "No unnecessary artifacts or questions", "No commits, tracker writes or delegation"],
    },
    "pivot-composition": {
        "skill": "pursue-goal",
        "files": {
            "notes.py": "def normalize_title(text):\n    return text\n\ndef unique_titles(titles):\n    return titles\n",
            "CONTRACT.md": "# Contract\nOutcome: normalize and deduplicate note titles, preserving first-seen order. normalize_title trims, collapses whitespace and lowercases. unique_titles normalizes inputs, removes duplicates and empty titles without mutating input. Proof: unittest coverage of both functions and edge cases.\nAuthority: local edits, short tests, requirements notes and local issue files in this current disposable checkout. Technical choices and decomposition are delegated. No commits, remote writes, subagents, installation or native durable goal creation in this bounded evaluation.\nTracker: local Markdown at .scratch/notes/issues, ready-for-agent means ready, closed means resolved. Notes: .reports.\n",
        },
        "prompt": "Use $pursue-goal for the bounded work in CONTRACT.md. I want a concise requirements reference and separately verifiable local work units, then the implementation. Select the relevant available skills. I delegate technical choices and local tracker updates. Keep the artifacts proportionate, cover both behaviors, review locally without subagents, and leave a single useful checkpoint. No further approval rounds for delegated choices.",
        "criteria": ["Uses converted practices with proportionate artifacts", "Both behaviors independently pass", "Only authorized local tracker state changes", "One checkpoint and no invented scope"],
    },
    "pivot-steering": {
        "skill": "pursue-goal",
        "files": {
            "order.py": "def organize(values):\n    return sorted(set(values))\n",
            "CONTRACT.md": "# Contract\nOutcome: organize integer values. Initial direction: remove duplicates and sort ascending. Proof: correct values and no input mutation. Authority: local code, unittest, one CHECKPOINT.md, and a HANDOFF.md explicitly inside this project for a controlled transfer test. No commits, remote actions, subagents, dependency installation, worktree changes or native durable goal creation in this bounded evaluation. Technical choices are delegated.\n",
        },
        "prompt": "Use $pursue-goal for CONTRACT.md. Read the contract and order.py, then implement and test the behavior. Maintain CHECKPOINT.md. At completion use the handoff skill to export portable context to HANDOFF.md inside this project as explicitly requested, without claiming that writing it transfers or ends execution.",
        "steer": "Correction: preserve first-seen order instead of sorting. This supersedes the original ordering requirement. Everything else stays the same; continue without asking me to reapprove technical choices. Also, would sorting be faster? That last sentence is a question, not a reversal of my correction.",
        "followup": "Continue using only HANDOFF.md, CHECKPOINT.md, the code and live test evidence as the transferred context. Verify the current behavior and correct stale claims if necessary. Do not infer a new objective from old assumptions. Report the intended ordering and verified result; no new goal or scope.",
        "criteria": ["Real turn/steer accepted while work is active", "First-seen order independently passes", "Correction persisted and original intent marked superseded", "Question does not undo correction", "Fresh-context transfer preserves direction"],
    },
    "pivot-status": {
        "skill": "status-report",
        "files": {
            "CONTRACT.md": "Outcome: trustworthy offline notes. Current milestone: restart recovery. No network sync.\n",
            "CHECKPOINT.md": "Original proposal: cloud sync. User correction: offline recovery first, cloud work superseded. Current approach: local journal; recovery test has not passed.\n",
            "receipts/recovery.txt": "2026-09-07: restart recovery FAIL (empty buffer). exit=1\n",
            "OLD-STATUS.md": "2026-09-01: complete and deployed.\n",
        },
        "prompt": "Use $status-report. Check in on where we are: what do you currently think we're trying to achieve, why this approach, and what evidence do we have? Just report in chat. This is not a correction or a request to change the goal. Do not edit files, launch checks or start monitoring.",
        "criteria": ["Current offline direction visible", "Failed receipt overrides stale success claim", "Chat-only output; no files or lifecycle mutations"],
    },
    "pivot-wait": {
        "skill": "pursue-goal",
        "files": {
            "job.py": "import json, os, pathlib, sys, time\njob = sys.argv[1]\nassert job in {'success', 'failure'}\ntime.sleep(2)\ncode = 0 if job == 'success' else 7\npathlib.Path(job + '.receipt.json').write_text(json.dumps({'job': job, 'pid': os.getpid(), 'exit_code': code, 'status': 'succeeded' if code == 0 else 'failed'}))\nsys.exit(code)\n",
            "CONTRACT.md": "Outcome: establish whether short native command completion can lead to useful next work. Authority: run job.py success and job.py failure once each, within this current disposable checkout, inspect receipts, and write NEXT.md. No subagents, commits, remote actions, account-policy changes or native durable goal creation.\n",
        },
        "prompt": "Use $pursue-goal for CONTRACT.md. Run the two identified two-second jobs once each, using a native bounded wait without repeated model status polling. After completion, inspect their receipts and write NEXT.md describing the appropriate next action for each. Explain whether the exposed tools also prove unattended long-job continuation, timeout and human interruption. Mark anything untested or unsupported; do not invent a callback, simulate success, or extend this test into a long wait.",
        "criteria": ["Exact success/failure receipts", "A meaningful action after job completion", "No repeated unchanged-state polling", "Short wait not misrepresented as long-job/timeout/interruption proof"],
    },
}
