#!/usr/bin/env python3
"""Usage log: how David-Skills is used, read from what chats already record.

Claude Code already writes every chat to a transcript as it happens: each
prompt, skill load and tool call, with times, folder and branch. This tool
adds what that record lacks: a compact copy in one place (the log folder,
kept on a big disk), how each piece of work ended, and a report that answers
the questions without digging. It never changes what a chat does.

    usage-log.py setup --log-dir DIR    create the log folder and note the start date
    usage-log.py update                 read new or changed transcripts into the log
    usage-log.py outcome WORK OUTCOME   record how a piece of work ended (David's word wins)
    usage-log.py report [--since DATE] [--project NAME]

As a SessionStart hook (no arguments) it starts `update` in the background at
most every 15 minutes, and does nothing at all until `setup` has been run.
Standard library only.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

CONFIG = Path(os.environ.get("DAVID_SKILLS_USAGE_CONFIG")
              or Path.home() / ".config" / "david-skills" / "usage-log.json")
MIN_INTERVAL = 15 * 60
IDLE_GAP = 15 * 60  # a pause longer than this does not count as working time
TRIVIAL_BRANCHES = {None, "", "HEAD", "main", "master", "dev"}
REVIEW_WORDS = re.compile(r"review|verif|audit|re-?check", re.I)
COMMAND = re.compile(r"<command-name>/?([^<\s]+)</command-name>")
TIMESTAMP = re.compile(r'"timestamp":\s*"([^"]+)"')
WANTED = re.compile(r'"type":\s*"(?:user|assistant|pr-link|custom-title)"')
WORKTREE = re.compile(r"/\.(?:claude/)?worktrees/")


# ---------------------------------------------------------------- config

def load_config():
    try:
        config = json.loads(CONFIG.read_text())
        config["log_dir"] = Path(config["log_dir"]).expanduser()
        config["transcripts"] = Path(config.get("transcripts")
                                     or Path.home() / ".claude" / "projects").expanduser()
        return config
    except (OSError, ValueError, KeyError, TypeError):
        return None


def write_json(path, value):
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=1, sort_keys=True) + "\n")
    os.replace(temporary, path)


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_time(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except (AttributeError, ValueError):
        return None


# ---------------------------------------------------------------- reading a chat

def project_of(cwd):
    if not cwd:
        return "unknown", None
    root = WORKTREE.split(cwd, maxsplit=1)[0].rstrip("/") or cwd
    return Path(root).name or root, root


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(block.get("text", "") for block in content
                        if isinstance(block, dict) and block.get("type") == "text")
    return ""


def who_sent(record, first_prompt, agent_started):
    """'david', 'agent' or 'system', from the labels the harness writes."""
    origin = (record.get("origin") or {}).get("kind")
    turn = record.get("turnOrigin")
    if origin == "task-notification" or turn in ("task_notification", "host_synthetic"):
        return "system"
    if turn == "peer" or turn == "sdk":
        return "agent"
    if origin == "human" or turn == "human":
        return "agent" if (first_prompt and agent_started) else "david"
    return "system"


def read_transcript(path, by, session):
    """Fold one transcript file into the session summary being built."""
    first_prompt = True
    with open(path, errors="replace") as handle:
        for line in handle:
            stamp = TIMESTAMP.search(line)
            if stamp:
                session["times"].append(stamp.group(1))
            if not WANTED.search(line):
                continue  # most lines are API bookkeeping; skip them unparsed
            try:
                record = json.loads(line)
            except ValueError:
                continue
            kind = record.get("type")
            t = record.get("timestamp")
            if kind == "custom-title" and by != "subagent":
                session["title"] = record.get("customTitle") or session["title"]
            elif kind == "pr-link" and record.get("prUrl"):
                if record["prUrl"] not in session["prs"]:
                    session["prs"].append(record["prUrl"])
            elif kind == "user" and not record.get("isMeta") and by != "subagent":
                note_prompt(record, t, session, first_prompt)
                first_prompt = False
            elif kind == "assistant":
                if record.get("cwd") and not session["cwd"]:
                    session["cwd"] = record["cwd"]
                branch = record.get("gitBranch")
                if branch and branch not in session["branches"]:
                    session["branches"].append(branch)
                model = (record.get("message") or {}).get("model")
                if model and not model.startswith("<") and model not in session["models"]:
                    session["models"].append(model)
                for block in (record.get("message") or {}).get("content") or []:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        note_tool(block, t, by, session)


def note_prompt(record, t, session, first_prompt):
    content = (record.get("message") or {}).get("content")
    text = text_of(content).strip()
    if not text or text.startswith(("<local-command", "[Request interrupted")):
        return
    if record.get("cwd") and not session["cwd"]:
        session["cwd"] = record["cwd"]
    branch = record.get("gitBranch")
    if branch and branch not in session["branches"]:
        session["branches"].append(branch)
    if first_prompt:
        session["started_by"] = ("agent" if record.get("sessionKind") == "bg"
                                 or record.get("entrypoint") in ("sdk-cli", "sdk-py", "sdk-ts")
                                 or record.get("turnOrigin") in ("sdk", "peer", "host_synthetic")
                                 else "david")
    sender = who_sent(record, first_prompt, session["started_by"] == "agent")
    command = COMMAND.search(text)
    if command and sender == "david":
        session["events"].append({"t": t, "kind": "skill", "name": command.group(1), "by": "david"})
    if text.startswith("This session is being continued"):
        return
    if sender == "david":
        session["events"].append({"t": t, "kind": "david", "text": " ".join(text.split())[:120]})


def note_tool(block, t, by, session):
    name, given = block.get("name"), block.get("input") or {}
    if name == "Skill" and given.get("skill"):
        session["events"].append({"t": t, "kind": "skill", "name": given["skill"],
                                  "by": "subagent" if by == "subagent" else "model"})
    elif name in ("Agent", "Task"):
        what = str(given.get("description") or "")[:100]
        session["events"].append({
            "t": t, "kind": "agent", "name": given.get("subagent_type") or "general-purpose",
            "what": what, "review": bool(REVIEW_WORDS.search(what)), "by": by})
    elif name == "Workflow":
        session["events"].append({"t": t, "kind": "agent", "name": "workflow",
                                  "what": "workflow", "review": False, "by": by})


def active_minutes(times):
    stamps = sorted(s for s in (parse_time(t) for t in times) if s is not None)
    total = sum(min(b - a, IDLE_GAP) for a, b in zip(stamps, stamps[1:]))
    return round(total / 60)


def summarise(main_file):
    session = {"schema": 1, "harness": "claude", "session_id": main_file.stem, "title": None,
               "cwd": None, "branches": [], "models": [], "prs": [], "events": [],
               "times": [], "started_by": None}
    read_transcript(main_file, "main", session)
    for sub in sorted((main_file.parent / main_file.stem / "subagents").glob("*.jsonl")):
        read_transcript(sub, "subagent", session)
    times = sorted(t for t in session.pop("times") if parse_time(t) is not None)
    if not times:
        return None
    session["events"].sort(key=lambda e: e.get("t") or "")
    session["started"], session["ended"] = times[0], times[-1]
    session["active_minutes"] = active_minutes(times)
    session["project"], session["repo"] = project_of(session["cwd"])
    real = [b for b in session["branches"] if b not in TRIVIAL_BRANCHES]
    session["work"] = (session["prs"][-1] if session["prs"]
                       else f"{session['project']}:{real[-1]}" if real
                       else f"{session['project']}:session:{session['session_id'][:8]}")
    events = session["events"]
    session["counts"] = {
        "skills": sum(e["kind"] == "skill" for e in events),
        "david_prompts": sum(e["kind"] == "david" for e in events),
        "agents": sum(e["kind"] == "agent" for e in events),
        "reviews": sum(e["kind"] == "agent" and e["review"] for e in events)
                   + sum(e["kind"] == "skill" and "review" in e["name"] for e in events),
    }
    return session


# ---------------------------------------------------------------- outcomes

def git(repo, *args):
    try:
        return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True,
                              timeout=20).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def pr_outcome(url, cache):
    known = cache.get(url)
    if isinstance(known, dict) and known.get("state") in ("MERGED", "CLOSED"):
        return known  # final; no need to ask GitHub again
    try:
        out = subprocess.run(["gh", "pr", "view", url, "--json", "state,baseRefName,mergedAt,closedAt"],
                             capture_output=True, text=True, timeout=30)
        found = json.loads(out.stdout) if out.returncode == 0 else None
        if isinstance(found, dict) and found.get("state"):
            cache[url] = found
    except (OSError, ValueError, subprocess.SubprocessError):
        pass  # offline or no access: keep what was known, try again next run
    known = cache.get(url)
    return known if isinstance(known, dict) and known.get("state") else None


def work_outcome(work, sessions, pr_cache):
    """How a piece of work ended, as far as git and GitHub can tell."""
    if work.startswith("https://"):
        pr = pr_outcome(work, pr_cache)
        if not pr:
            return None
        if pr["state"] == "MERGED":
            return {"outcome": f"merged to {pr.get('baseRefName')}", "at": pr.get("mergedAt"),
                    "source": "github"}
        if pr["state"] == "CLOSED":
            return {"outcome": "closed without merging", "at": pr.get("closedAt"), "source": "github"}
        return {"outcome": "open", "source": "github"}
    if ":session:" in work:
        return None
    repo = next((s["repo"] for s in sessions if s.get("repo")), None)
    branch = work.split(":", 1)[1]
    if not repo or not Path(repo).is_dir():
        return None
    tip = git(repo, "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}")
    if not tip:
        return {"outcome": "branch gone", "source": "git"}
    # A branch whose newest commit predates the work has nothing of its own yet;
    # its tip sits inside dev only because it was cut from there.
    committed = git(repo, "log", "-1", "--format=%ct", tip)
    if committed.isdigit() and int(committed) < min(parse_time(s["started"]) or 0 for s in sessions):
        return {"outcome": "no commits yet", "source": "git"}
    for target in ("origin/main", "main", "origin/dev", "dev"):
        if git(repo, "rev-parse", "--verify", "--quiet", target) and subprocess.run(
                ["git", "-C", repo, "merge-base", "--is-ancestor", tip, target],
                capture_output=True).returncode == 0:
            return {"outcome": f"merged to {target.split('/')[-1]}", "source": "git"}
    return {"outcome": "open", "source": "git"}


# ---------------------------------------------------------------- commands

def setup(log_dir):
    log_dir = Path(log_dir).expanduser().resolve()
    (log_dir / "sessions").mkdir(parents=True, exist_ok=True)
    started = log_dir / "started"
    if not started.exists():
        started.write_text(datetime.now().date().isoformat() + "\n")
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    config = load_config() or {}
    write_json(CONFIG, {"log_dir": str(log_dir),
                        "transcripts": str(config.get("transcripts")
                                           or Path.home() / ".claude" / "projects")})
    print(f"Logging to {log_dir}, started {started.read_text().strip()}.")
    return 0


def update(config):
    import fcntl

    log_dir, began = config["log_dir"], time.time()
    (log_dir / "sessions").mkdir(parents=True, exist_ok=True)
    with open(log_dir / ".lock", "a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            return 0  # another update is already running
        seen_path = log_dir / "seen.json"
        try:
            seen = json.loads(seen_path.read_text())
        except (OSError, ValueError):
            seen = {}
        changed = 0
        for main_file in sorted(config["transcripts"].glob("*/*.jsonl")):
            parts = [main_file, *sorted((main_file.parent / main_file.stem / "subagents").glob("*.jsonl"))]
            try:
                mark = [[str(p), p.stat().st_size, p.stat().st_mtime] for p in parts]
            except OSError:
                continue
            if seen.get(str(main_file)) == mark:
                continue
            try:
                record = summarise(main_file)
            except Exception as error:  # one odd transcript must not stop the rest
                print(f"{main_file}: {error!r}", file=sys.stderr)
                continue
            if record:
                write_json(log_dir / "sessions" / f"claude-{record['session_id']}.json", record)
            seen[str(main_file)] = mark
            changed += 1
        write_json(seen_path, seen)
        sessions = load_sessions(log_dir)
        problem = None
        try:
            refresh_outcomes(log_dir, sessions)
        except Exception as error:  # outcomes are filled in again next run
            problem = repr(error)
            print(f"outcomes: {problem}", file=sys.stderr)
        with open(log_dir / "runs.jsonl", "a") as runs:
            runs.write(json.dumps({"at": now_iso(), "seconds": round(time.time() - began, 1),
                                   "changed": changed, "sessions": len(sessions),
                                   **({"problem": problem} if problem else {})}) + "\n")
    return 0


def load_sessions(log_dir):
    sessions = []
    for path in sorted((log_dir / "sessions").glob("*.json")):
        try:
            sessions.append(json.loads(path.read_text()))
        except (OSError, ValueError):
            continue
    return sessions


def refresh_outcomes(log_dir, sessions):
    path = log_dir / "outcomes.json"
    try:
        known = json.loads(path.read_text())
    except (OSError, ValueError):
        known = {}
    pr_cache = known.pop("_pr_cache", {})
    by_work = defaultdict(list)
    for session in sessions:
        by_work[session["work"]].append(session)
    for work, group in by_work.items():
        found = work_outcome(work, group, pr_cache)
        if found:
            known[work] = found
    known["_pr_cache"] = pr_cache
    write_json(path, known)


def outcomes(log_dir):
    try:
        found = json.loads((log_dir / "outcomes.json").read_text())
    except (OSError, ValueError):
        found = {}
    found.pop("_pr_cache", None)
    try:
        for line in (log_dir / "outcomes-david.jsonl").read_text().splitlines():
            entry = json.loads(line)
            found[entry["work"]] = {**entry, "source": "david"}
    except (OSError, ValueError, KeyError):
        pass
    return found


def record_outcome(config, work, outcome, note):
    with open(config["log_dir"] / "outcomes-david.jsonl", "a") as handle:
        handle.write(json.dumps({"work": work, "outcome": outcome, "note": note,
                                 "at": now_iso()}) + "\n")
    print(f"Recorded: {work} -> {outcome}")
    return 0


def pipeline(events):
    steps = []
    for event in events:
        if event["kind"] == "skill":
            name = event["name"].split(":")[-1]
            if not steps or steps[-1] != name:
                steps.append(name)
    return steps


def report(config, since, project):
    log_dir = config["log_dir"]
    sessions = [s for s in load_sessions(log_dir)
                if (not since or s["ended"] >= since) and (not project or s["project"] == project)
                and (s["events"] or s["active_minutes"])]  # skip empty probe chats
    try:
        started = (log_dir / "started").read_text().strip()
    except OSError:
        started = "unknown"
    ended = outcomes(log_dir)
    out = [f"# David-Skills usage", "",
           f"Logging started {started}. Covers {len(sessions)} chats"
           + (f" from {min(s['started'] for s in sessions)[:10]} to {max(s['ended'] for s in sessions)[:10]}"
              if sessions else "") + ".", ""]

    uses = defaultdict(lambda: {"david": 0, "model": 0, "subagent": 0, "projects": set(), "last": ""})
    for s in sessions:
        for e in s["events"]:
            if e["kind"] == "skill":
                row = uses[e["name"]]
                row[e["by"]] += 1
                row["projects"].add(s["project"])
                row["last"] = max(row["last"], e.get("t") or "")
    out += ["## Skills", "", "| Skill | Uses | By David | By the model | In subagents | Projects | Last used |",
            "|---|---|---|---|---|---|---|"]
    for name, row in sorted(uses.items(), key=lambda kv: -(kv[1]["david"] + kv[1]["model"] + kv[1]["subagent"])):
        total = row["david"] + row["model"] + row["subagent"]
        out.append(f"| {name} | {total} | {row['david']} | {row['model']} | {row['subagent']} | "
                   f"{', '.join(sorted(row['projects']))} | {row['last'][:10]} |")

    per_project = defaultdict(Counter)
    for s in sessions:
        c = per_project[s["project"]]
        c["chats"] += 1
        c["active_minutes"] += s["active_minutes"]
        for key, value in s["counts"].items():
            c[key] += value
    out += ["", "## Projects", "", "| Project | Chats | Active hours | Skill uses | David stepped in | Reviews |",
            "|---|---|---|---|---|---|"]
    for name, c in sorted(per_project.items(), key=lambda kv: -kv[1]["chats"]):
        out.append(f"| {name} | {c['chats']} | {c['active_minutes'] / 60:.1f} | {c['skills']} | "
                   f"{c['david_prompts']} | {c['reviews']} |")

    work = defaultdict(list)
    for s in sessions:
        work[s["work"]].append(s)
    shapes = defaultdict(Counter)
    out += ["", "## Pieces of work", "",
            "Newest first. A piece of work is a pull request, else a branch, else a single chat.", ""]
    for key, group in sorted(work.items(), key=lambda kv: max(s["ended"] for s in kv[1]), reverse=True):
        events = sorted((e for s in group for e in s["events"]), key=lambda e: e.get("t") or "")
        steps = pipeline(events)
        result = ended.get(key, {}).get("outcome", "not known yet")
        if steps:
            shapes[" → ".join(steps)][result] += 1
        reviews = sum(s["counts"]["reviews"] for s in group)
        titles = "; ".join(dict.fromkeys(s["title"] for s in group if s["title"]))
        out += [f"### {key}", "",
                f"- {group[0]['project']}, {min(s['started'] for s in group)[:16].replace('T', ' ')}"
                f" to {max(s['ended'] for s in group)[:16].replace('T', ' ')} UTC,"
                f" {sum(s['active_minutes'] for s in group)} active minutes, {len(group)} chat(s)"
                + (f": {titles}" if titles else ""),
                f"- Skills in order: {' → '.join(steps) if steps else 'none'}",
                f"- Reviews or checks: {reviews}" + (f" ({reviews - 1} again after the first)" if reviews > 1 else ""),
                f"- How it ended: {result}"]
        stepped = [e for e in events if e["kind"] == "david"]
        if stepped:
            out.append(f"- David stepped in {len(stepped)} time(s):")
            out += [f"  - {e['t'][:16].replace('T', ' ')} {e['text']}" for e in stepped[:8]]
            if len(stepped) > 8:
                out.append(f"  - … and {len(stepped) - 8} more")
        out.append("")
    out += ["## Skill sequences and how they ended", "", "| Sequence | Times | How they ended |", "|---|---|---|"]
    for shape, results in sorted(shapes.items(), key=lambda kv: -sum(kv[1].values())):
        out.append(f"| {shape} | {sum(results.values())} | "
                   + ", ".join(f"{k}: {v}" for k, v in results.most_common()) + " |")
    print("\n".join(out))
    return 0


def hook():
    """SessionStart: start a background update when one is due. Never blocks or prints."""
    try:
        sys.stdin.read()
        config = load_config()
        if not config or not config["log_dir"].is_dir():
            return
        # The marker is touched before each attempt, so a failing or slow update
        # still waits its turn instead of being restarted by every new chat.
        marker = config["log_dir"] / ".last-attempt"
        if marker.exists() and time.time() - marker.stat().st_mtime < MIN_INTERVAL:
            return
        marker.touch()
        with open(config["log_dir"] / "update-errors.log", "a") as errors:
            subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "update"],
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=errors,
                             start_new_session=True)
    except Exception:
        return  # logging must never get in the way of a chat


def main():
    if len(sys.argv) == 1:
        hook()
        return 0
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("setup").add_argument("--log-dir", required=True)
    commands.add_parser("update")
    told = commands.add_parser("outcome")
    told.add_argument("work", help="the piece of work as the report names it (PR link, project:branch, ...)")
    told.add_argument("outcome", help="for example: accepted, merged to dev, abandoned, redone")
    told.add_argument("--note", default="")
    shown = commands.add_parser("report")
    shown.add_argument("--since", help="ISO date, for example 2026-11-22")
    shown.add_argument("--project")
    args = parser.parse_args()
    if args.command == "setup":
        return setup(args.log_dir)
    config = load_config()
    if not config:
        print(f"No usage log set up yet ({CONFIG} missing). Run: usage-log.py setup --log-dir DIR",
              file=sys.stderr)
        return 1
    if args.command == "update":
        return update(config)
    if args.command == "outcome":
        return record_outcome(config, args.work, args.outcome, args.note)
    return report(config, args.since, args.project)


if __name__ == "__main__":
    sys.exit(main())
