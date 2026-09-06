"""
Shared helper for this plugin's hook scripts. Not a hook itself -- nothing in
hooks.json points here directly.

Every hook in this directory receives its input as a JSON object on stdin and
must behave as a no-op (exit 0, silent) if that input is missing or malformed,
since a hook that raises on bad input breaks the session it's attached to.
That "parse or give up quietly" logic was duplicated verbatim across hooks;
this is the one copy.
"""
import json
import sys


def read_hook_input():
    """Parse the hook's stdin as JSON. Returns the parsed dict, or None if
    stdin isn't valid JSON (missing, empty, malformed) or doesn't parse to a
    dict (Claude Code's hook payloads always are, but valid JSON like `[]` or
    `null` is not, and callers here immediately do `data.get(...)`)."""
    try:
        data = json.load(sys.stdin)
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    tool_input = data.get("tool_input")
    if tool_input is not None:
        if not isinstance(tool_input, dict):
            return None
        command = tool_input.get("command")
        if command is not None and not isinstance(command, str):
            return None
    model = data.get("model")
    if model is not None and not isinstance(model, str):
        return None
    return data
