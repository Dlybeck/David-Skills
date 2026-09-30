#!/usr/bin/env python3
"""Opt-in run timing. Hook output is a time fact, never planning advice.

The CLI registers a deadline for one session in one workspace. Installed hooks
are silent otherwise. State and cue updates are atomic and serialized on POSIX.
No model calls, worker dispatch, background service, or goal lifecycle changes.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile
import time

from _shared import read_hook_input


def workspace_root(cwd):
    directory = Path(cwd).resolve()
    for parent in (directory, *directory.parents):
        if (parent / ".git").exists():
            return parent
    return directory


def state_path(workspace, session):
    if not isinstance(session, str) or not session.strip():
        raise ValueError("a runtime session ID is required")
    folder = workspace / ".reports" / ".run-timing"
    if not folder.resolve().is_relative_to(workspace):
        raise ValueError("timing state must stay inside the workspace")
    name = hashlib.sha256(session.encode()).hexdigest()
    return folder / (name + ".json")


@contextmanager
def locked(path):
    import fcntl

    with path.with_suffix(".lock").open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield


def read_state(path, workspace, session):
    state = json.loads(path.read_text())
    if (state["schema_version"] != 1 or state["session_id"] != session
            or state["workspace"] != str(workspace)
            or type(state["active"]) is not bool
            or type(state["expiry_emitted"]) is not bool):
        raise ValueError("timing state identity or schema is invalid")
    for name in ("deadline", "started_at", "last_report_at", "cue_seconds", "report_seconds"):
        number = state[name]
        if type(number) not in (int, float) or not math.isfinite(number):
            raise ValueError("timing state contains an invalid clock value")
    if state["cue_seconds"] <= 0 or state["report_seconds"] < 0:
        raise ValueError("timing intervals are invalid")
    cue = state["last_cue_at"]
    if cue is not None and (type(cue) not in (int, float) or not math.isfinite(cue)):
        raise ValueError("timing cue timestamp is invalid")
    return state


def save_state(path, state):
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        json.dump(state, handle)
        handle.write("\n")
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def snapshot(state, now):
    report_at = (state["last_report_at"] + state["report_seconds"]
                 if state["report_seconds"] else None)
    return {
        "active": state["active"], "deadline": state["deadline"],
        "remaining_seconds": max(0, state["deadline"] - now),
        "report_due_at": report_at,
        "report_due": bool(state["active"] and report_at is not None and now >= report_at),
        "deadline_reached": now >= state["deadline"],
    }


def hook():
    data = read_hook_input()
    if not data or data.get("hook_event_name") not in ("PostToolUse", "SessionStart"):
        return
    try:
        workspace = workspace_root(data.get("cwd") or Path.cwd())
        session = data.get("session_id")
        path = state_path(workspace, session)
        if not path.is_file():
            return
        with locked(path):
            state = read_state(path, workspace, session)
            if not state["active"]:
                return
            now = time.time()
            expired = now >= state["deadline"]
            refresh = data["hook_event_name"] == "SessionStart"
            if expired and state["expiry_emitted"] and not refresh:
                return
            previous = state["last_cue_at"]
            if not expired and not refresh and previous is not None and now - previous < state["cue_seconds"]:
                return
            minutes = math.ceil(max(0, state["deadline"] - now) / 60)
            state["last_cue_at"] = now
            state["expiry_emitted"] = expired
            save_state(path, state)
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": data["hook_event_name"],
            "additionalContext": f"Time remaining: {minutes} minutes.",
        }}))
    except (OSError, ValueError, KeyError, TypeError, ImportError):
        # Timing is advisory; malformed or unavailable state must not block work.
        return


def deadline_epoch(value):
    instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if instant.tzinfo is None or instant.utcoffset() is None:
        raise ValueError("deadline needs an explicit timezone, such as Z or -07:00")
    return instant.astimezone(timezone.utc).timestamp()


def wait_for_boundary(path, workspace, session, receipt):
    """Wait inside this process; a receipt being present is not a success verdict."""
    while True:
        state = read_state(path, workspace, session)
        now = time.time()
        current = snapshot(state, now)
        if not current["active"]:
            reason = "finished"
        elif current["deadline_reached"]:
            reason = "deadline"
        elif receipt is not None and receipt.is_file():
            reason = "receipt_available"
        elif current["report_due"]:
            reason = "report_due"
        else:
            boundary = min(state["deadline"], current["report_due_at"] or state["deadline"])
            time.sleep(min(0.5, max(0, boundary - now)))
            continue
        print(json.dumps({**current, "reason": reason}))
        return 0


def main():
    import sys

    if len(sys.argv) == 1:
        hook()
        return 0
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("start", "status", "report", "finish", "wait"))
    sessions = {value for name in ("CODEX_THREAD_ID", "CLAUDE_CODE_SESSION_ID")
                if (value := os.environ.get(name))}
    parser.add_argument("--session", default=next(iter(sessions)) if len(sessions) == 1 else None)
    parser.add_argument("--deadline", help="Absolute ISO-8601 time with timezone")
    parser.add_argument("--cue-seconds", type=int, default=300)
    parser.add_argument("--report-seconds", type=int, default=2700, help="0 disables timed reports")
    parser.add_argument("--receipt", type=Path, help="Exact job receipt to wait for, without judging its contents")
    args = parser.parse_args()
    try:
        workspace = workspace_root(Path.cwd())
        path = state_path(workspace, args.session)
        now = time.time()
        if args.receipt is not None and args.action != "wait":
            raise ValueError("--receipt is only valid for wait")
        if args.action == "wait":
            return wait_for_boundary(path, workspace, args.session, args.receipt)
        if args.action == "start":
            if not args.deadline:
                raise ValueError("start requires the user's agreed absolute deadline")
            deadline = deadline_epoch(args.deadline)
            if deadline <= now or args.cue_seconds <= 0 or args.report_seconds < 0:
                raise ValueError("deadline must be in the future and intervals must be valid")
            path.parent.mkdir(parents=True, exist_ok=True)
        with locked(path):
            if args.action == "start":
                if path.exists() and read_state(path, workspace, args.session)["active"]:
                    raise ValueError("this session already has an active timer; finish it first")
                state = {
                    "schema_version": 1, "session_id": args.session,
                    "workspace": str(workspace), "active": True,
                    "deadline": deadline, "started_at": now,
                    "cue_seconds": args.cue_seconds, "report_seconds": args.report_seconds,
                    "last_report_at": now, "last_cue_at": None, "expiry_emitted": False,
                }
            else:
                state = read_state(path, workspace, args.session)
                if args.action == "report":
                    if not state["active"]:
                        raise ValueError("the timer has ended")
                    state["last_report_at"] = now
                elif args.action == "finish":
                    state["active"] = False
            if args.action != "status":
                save_state(path, state)
            print(json.dumps(snapshot(state, now)))
        return 0
    except (OSError, ValueError, KeyError, TypeError, ImportError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
