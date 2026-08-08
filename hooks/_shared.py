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
    return data if isinstance(data, dict) else None
