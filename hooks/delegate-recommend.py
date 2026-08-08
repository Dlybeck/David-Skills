#!/usr/bin/env python3
"""
DELEGATE RECOMMEND: on SessionStart, best-effort check whether the active model
matches `delegate`'s configured (or default) Router model, and if so, surface
a recommendation to run `/delegate` via `additionalContext` -- informational
only. This never blocks the session and never runs anything by itself;
`/delegate` is always a manual, explicit invocation regardless of what this
prints.

The `model` field on SessionStart's input is documented as NOT guaranteed to
be present, and its exact value format isn't documented either (a session id
was seen reporting a full name like "claude-fable-5", not a bare "fable") --
so this matches case-insensitively via substring, and silently does nothing
when the field is absent or doesn't match. Silence is the expected, common
case, not a bug: most sessions are not on the configured light model, and
some sessions never get a `model` field at all.

Reads the configured Router model from docs/agents/delegate.md's
"Router model:" line if that file exists (delegate writes it on first use);
falls back to "fable" -- the skill's own documented default -- otherwise.
"""
import json
import re
import sys
from pathlib import Path

from _shared import read_hook_input

ROUTER_MODEL_LINE = re.compile(r'^Router model:\s*(.+)$', re.IGNORECASE | re.MULTILINE)
DEFAULT_LIGHT_MODEL = "fable"
CONFIG_PATH = Path("docs/agents/delegate.md")


def configured_light_model():
    if not CONFIG_PATH.exists():
        return DEFAULT_LIGHT_MODEL
    try:
        text = CONFIG_PATH.read_text()
    except Exception:
        return DEFAULT_LIGHT_MODEL
    match = ROUTER_MODEL_LINE.search(text)
    return match.group(1).strip() if match else DEFAULT_LIGHT_MODEL


def main():
    data = read_hook_input()
    if data is None:
        return 0

    model = data.get("model")
    if not model:
        return 0  # not guaranteed present -- expected, not an error

    light_model = configured_light_model()
    if light_model.lower() not in model.lower():
        return 0

    message = (
        f"The active model ({model}) looks like delegate's configured Router "
        f"model ({light_model}). If ticket work comes up this session, "
        "/delegate dispatches it to heavier worker subagents in one bounded "
        "run instead of this model doing the work itself. This is a "
        "recommendation only -- /delegate always runs manually."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": message,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
