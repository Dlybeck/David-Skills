#!/usr/bin/env python3
"""Validate the autonomous-pilot scenario suite and its source contracts."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCENARIOS = ROOT / ".agents" / "evals" / "pilot-scenarios.json"
EXPECTED_IDS = {
    "research-heavy-ai-feasibility",
    "benchmark-optimization",
    "ambiguous-product-build",
    "scoped-feature-delivery",
    "human-authority-boundary",
    "dirty-checkout-isolation",
    "yolopilot-learning-postflight",
}


def require_text(path: str, fragments: tuple[str, ...], errors: list[str]) -> None:
    text = (ROOT / path).read_text(encoding="utf-8")
    for fragment in fragments:
        if fragment not in text:
            errors.append(f"{path}: missing pilot contract fragment {fragment!r}")


def main() -> int:
    errors: list[str] = []
    data = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        errors.append("pilot scenarios: schema_version must be 1")

    scenarios = data.get("scenarios")
    if not isinstance(scenarios, list):
        errors.append("pilot scenarios: scenarios must be an array")
        scenarios = []

    ids: set[str] = set()
    entrypoints: set[str] = set()
    for index, scenario in enumerate(scenarios):
        label = f"pilot scenarios[{index}]"
        if not isinstance(scenario, dict):
            errors.append(f"{label}: must be an object")
            continue
        identifier = scenario.get("id")
        if not isinstance(identifier, str) or not identifier:
            errors.append(f"{label}: id must be a non-empty string")
        elif identifier in ids:
            errors.append(f"{label}: duplicate id {identifier!r}")
        else:
            ids.add(identifier)
        entrypoint = scenario.get("entrypoint")
        if entrypoint not in {"autopilot", "yolopilot"}:
            errors.append(f"{label}: invalid entrypoint {entrypoint!r}")
        else:
            entrypoints.add(entrypoint)
        if not isinstance(scenario.get("prompt"), str) or not scenario["prompt"].strip():
            errors.append(f"{label}: prompt must be a non-empty string")
        assertions = scenario.get("assertions")
        if not isinstance(assertions, list) or len(assertions) < 3:
            errors.append(f"{label}: requires at least three assertions")
        elif not all(isinstance(item, str) and item.strip() for item in assertions):
            errors.append(f"{label}: assertions must be non-empty strings")

    if ids != EXPECTED_IDS:
        errors.append(
            "pilot scenarios: ids differ; missing="
            f"{sorted(EXPECTED_IDS - ids)}, extra={sorted(ids - EXPECTED_IDS)}"
        )
    if entrypoints != {"autopilot", "yolopilot"}:
        errors.append("pilot scenarios: both pilot entrypoints require coverage")

    require_text(
        "skills/engineering/pursue-goal/SKILL.md",
        (
            "**Research**",
            "**Discovery**",
            "**Delivery**",
            "**Optimization**",
            "**Target reached**",
            "**Authority boundary**",
            "**Evidence plateau**",
        ),
        errors,
    )
    require_text(
        "skills/engineering/autopilot/SKILL.md",
        ("Invoke `/pursue-goal`", "merge into `dev`", "`main`"),
        errors,
    )
    require_text(
        "skills/engineering/yolopilot/SKILL.md",
        ("without pausing for a reply", "never merges", "quick learning digest", "/teach"),
        errors,
    )
    require_text(
        "skills/engineering/pursue-goal/references/codex.md",
        ("native goal", "linked worktree", "not status polling"),
        errors,
    )

    if errors:
        print(f"Pilot scenario validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Pilot scenario validation passed: {len(scenarios)} scenarios.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
