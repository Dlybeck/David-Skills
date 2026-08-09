#!/usr/bin/env python3
"""Validate the repository's plugin manifests, catalogs, and skill metadata."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
PROMOTED_BUCKETS = ("engineering", "productivity")
ALL_SKILL_BUCKETS = (*PROMOTED_BUCKETS, "misc", "in-progress")
CODEX_EXCLUSIONS = {"ask-claude", "autopilot", "yolopilot"}
JSON_FILES = (
    "package.json",
    "package-lock.json",
    ".changeset/config.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
    "hooks/hooks.json",
)

errors: list[str] = []


def error(message: str) -> None:
    errors.append(message)


def load_json(relative_path: str) -> Any:
    path = ROOT / relative_path
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        error(f"missing required JSON file: {relative_path}")
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        error(f"invalid JSON in {relative_path}: {exc}")
    return None


def skill_dirs(bucket: str) -> list[Path]:
    return sorted(
        (skill_file.parent for skill_file in (ROOT / "skills" / bucket).glob("*/SKILL.md")),
        key=lambda path: path.name,
    )


def manifest_paths(manifest: Any, manifest_path: str) -> set[str]:
    if not isinstance(manifest, dict):
        return set()

    paths = manifest.get("skills")
    if not isinstance(paths, list) or not all(isinstance(item, str) for item in paths):
        error(f"{manifest_path}: 'skills' must be an array of paths")
        return set()

    if len(paths) != len(set(paths)):
        error(f"{manifest_path}: duplicate skill paths")

    return set(paths)


def check_versions(documents: dict[str, Any]) -> None:
    package = documents.get("package.json")
    if not isinstance(package, dict) or not isinstance(package.get("version"), str):
        error("package.json: missing string version")
        return

    package_name = package.get("name")
    package_version = package["version"]
    if package_name != "david-skills":
        error("package.json: package name must be 'david-skills'")
    for path in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
        manifest = documents.get(path)
        if not isinstance(manifest, dict):
            continue
        if manifest.get("name") != "david-skills":
            error(f"{path}: plugin name must be 'david-skills'")
        if manifest.get("version") != package_version:
            error(
                f"{path}: version {manifest.get('version')!r} does not match "
                f"package.json version {package_version!r}"
            )

    lock = documents.get("package-lock.json")
    if not isinstance(lock, dict):
        return
    lock_packages = lock.get("packages")
    if not isinstance(lock_packages, dict):
        error("package-lock.json: 'packages' must be an object")
        root_package = None
    else:
        root_package = lock_packages.get("")
    if lock.get("name") != package_name:
        error(
            f"package-lock.json: name {lock.get('name')!r} does not match "
            f"package.json name {package_name!r}"
        )
    if lock.get("version") != package_version:
        error(
            f"package-lock.json: version {lock.get('version')!r} does not match "
            f"package.json version {package_version!r}"
        )
    if not isinstance(root_package, dict) or root_package.get("name") != package_name:
        root_name = root_package.get("name") if isinstance(root_package, dict) else None
        error(
            f"package-lock.json: root package name {root_name!r} does not match "
            f"package.json name {package_name!r}"
        )
    if not isinstance(root_package, dict) or root_package.get("version") != package_version:
        root_version = root_package.get("version") if isinstance(root_package, dict) else None
        error(
            f"package-lock.json: root package version {root_version!r} does not match "
            f"package.json version {package_version!r}"
        )

    try:
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        error(f"cannot read CHANGELOG.md: {exc}")
        return
    first_heading = re.search(r"^##\s+([^\s]+)\s*$", changelog, re.MULTILINE)
    if first_heading is None:
        error("CHANGELOG.md: missing a version heading")
    elif first_heading.group(1) != package_version:
        error(
            f"CHANGELOG.md: latest version {first_heading.group(1)!r} does not match "
            f"package.json version {package_version!r}"
        )


def check_manifests(documents: dict[str, Any]) -> None:
    promoted = {
        f"./{path.relative_to(ROOT).as_posix()}"
        for bucket in PROMOTED_BUCKETS
        for path in skill_dirs(bucket)
    }

    claude = manifest_paths(
        documents.get(".claude-plugin/plugin.json"), ".claude-plugin/plugin.json"
    )
    codex = manifest_paths(
        documents.get(".codex-plugin/plugin.json"), ".codex-plugin/plugin.json"
    )
    codex_expected = {
        path for path in promoted if Path(path).name not in CODEX_EXCLUSIONS
    }

    compare_sets(".claude-plugin/plugin.json skills", claude, promoted)
    compare_sets(".codex-plugin/plugin.json skills", codex, codex_expected)


def compare_sets(label: str, actual: set[str], expected: set[str]) -> None:
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        error(f"{label}: missing {', '.join(missing)}")
    if extra:
        error(f"{label}: unexpected {', '.join(extra)}")


def frontmatter_name(skill_file: Path) -> str | None:
    try:
        text = skill_file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        error(f"cannot read {skill_file.relative_to(ROOT)}: {exc}")
        return None

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        error(f"{skill_file.relative_to(ROOT)}: missing YAML frontmatter")
        return None

    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        error(f"{skill_file.relative_to(ROOT)}: unterminated YAML frontmatter")
        return None

    for line in lines[1:end]:
        match = re.match(r"^name\s*:\s*(.+?)\s*$", line)
        if match:
            return match.group(1).strip("'\"")

    error(f"{skill_file.relative_to(ROOT)}: frontmatter has no name")
    return None


def check_skill_metadata() -> None:
    seen_names: dict[str, Path] = {}
    for bucket in ALL_SKILL_BUCKETS:
        for directory in skill_dirs(bucket):
            skill_file = directory / "SKILL.md"
            name = frontmatter_name(skill_file)
            if name != directory.name:
                error(
                    f"{skill_file.relative_to(ROOT)}: frontmatter name {name!r} "
                    f"does not match directory {directory.name!r}"
                )
            if name in seen_names:
                error(
                    f"duplicate skill name {name!r}: {seen_names[name].relative_to(ROOT)} "
                    f"and {skill_file.relative_to(ROOT)}"
                )
            elif name is not None:
                seen_names[name] = skill_file

            metadata = directory / "agents" / "openai.yaml"
            if not metadata.is_file():
                error(f"{directory.relative_to(ROOT)}: missing agents/openai.yaml")


def markdown_skill_links(readme: Path, pattern: re.Pattern[str]) -> set[str]:
    try:
        text = readme.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        error(f"cannot read {readme.relative_to(ROOT)}: {exc}")
        return set()
    return {match.group(1) for match in pattern.finditer(text)}


def check_catalogs() -> None:
    root_pattern = re.compile(
        r"\(\./skills/((?:engineering|productivity)/[^/)]+)/SKILL\.md(?:#[^)]*)?\)"
    )
    root_actual = markdown_skill_links(ROOT / "README.md", root_pattern)
    root_expected = {
        f"{bucket}/{directory.name}"
        for bucket in PROMOTED_BUCKETS
        for directory in skill_dirs(bucket)
    }
    compare_sets("README.md promoted skill catalog", root_actual, root_expected)

    bucket_pattern = re.compile(r"\(\./([^/)]+)/SKILL\.md(?:#[^)]*)?\)")
    for bucket in ALL_SKILL_BUCKETS:
        directory = ROOT / "skills" / bucket
        actual = markdown_skill_links(directory / "README.md", bucket_pattern)
        expected = {path.name for path in skill_dirs(bucket)}
        compare_sets(f"skills/{bucket}/README.md catalog", actual, expected)


def marketplace_plugin(document: Any, path: str) -> dict[str, Any] | None:
    if not isinstance(document, dict):
        return None
    if document.get("name") != "david-skills":
        error(f"{path}: marketplace name must be 'david-skills'")
    plugins = document.get("plugins")
    if not isinstance(plugins, list):
        error(f"{path}: 'plugins' must be an array")
        return None
    matches = [
        plugin
        for plugin in plugins
        if isinstance(plugin, dict) and plugin.get("name") == "david-skills"
    ]
    if len(matches) != 1:
        error(f"{path}: expected exactly one 'david-skills' plugin entry")
        return None
    return matches[0]


def check_marketplaces(documents: dict[str, Any]) -> None:
    claude_path = ".claude-plugin/marketplace.json"
    claude_plugin = marketplace_plugin(documents.get(claude_path), claude_path)
    if claude_plugin is not None and claude_plugin.get("source") not in (".", "./"):
        error(f"{claude_path}: plugin source must point at the repository root")

    codex_path = ".agents/plugins/marketplace.json"
    codex_plugin = marketplace_plugin(documents.get(codex_path), codex_path)
    if codex_plugin is None:
        return
    source = codex_plugin.get("source")
    source_is_root = source in (".", "./") or (
        isinstance(source, dict)
        and source.get("source") == "local"
        and source.get("path") in (".", "./")
    )
    if not source_is_root:
        error(f"{codex_path}: plugin source must be local and point at the repository root")


def check_agent_instructions_link() -> None:
    path = ROOT / "AGENTS.md"
    if not path.is_symlink():
        error("AGENTS.md must be a symlink to CLAUDE.md")
        return
    if os.readlink(path) != "CLAUDE.md":
        error(f"AGENTS.md points to {os.readlink(path)!r}, expected 'CLAUDE.md'")


def tracked_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        error(f"git ls-files failed: {result.stderr.decode(errors='replace').strip()}")
        return []
    return [
        ROOT / item.decode(errors="surrogateescape")
        for item in result.stdout.split(b"\0")
        if item
    ]


def check_legacy_name() -> None:
    # Keep the retired project name out of this validator too, so the scan is self-checking.
    retired_name = "den" + "ali"
    for path in tracked_paths():
        if not path.is_file():
            continue
        try:
            content = path.read_bytes()
        except OSError as exc:
            error(f"cannot scan {path.relative_to(ROOT)}: {exc}")
            continue
        if b"\0" in content:
            continue
        if retired_name in content.decode("utf-8", errors="replace").casefold():
            error(f"{path.relative_to(ROOT)}: contains the retired project name")


def main() -> int:
    documents = {path: load_json(path) for path in JSON_FILES}
    check_versions(documents)
    check_manifests(documents)
    check_skill_metadata()
    check_catalogs()
    check_marketplaces(documents)
    check_agent_instructions_link()
    check_legacy_name()

    if errors:
        print(f"Repository validation failed with {len(errors)} error(s):", file=sys.stderr)
        for message in errors:
            print(f"- {message}", file=sys.stderr)
        return 1

    promoted_count = sum(len(skill_dirs(bucket)) for bucket in PROMOTED_BUCKETS)
    all_count = sum(len(skill_dirs(bucket)) for bucket in ALL_SKILL_BUCKETS)
    print(
        f"Repository validation passed: {promoted_count} promoted skills, "
        f"{all_count} total skills."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
