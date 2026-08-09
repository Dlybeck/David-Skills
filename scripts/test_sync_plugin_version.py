#!/usr/bin/env python3
"""Hermetic contract tests for sync-plugin-version.mjs."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().with_name("sync-plugin-version.mjs")
NODE = shutil.which("node")
PACKAGE_NAME = "david-skills"
OLD_VERSION = "1.5.0"
NEW_VERSION = "2.3.4"


def write_json(path: Path, document: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


def make_fixture(
    root: Path,
    *,
    plugin_version: str = OLD_VERSION,
    lock_version: str = OLD_VERSION,
    lock_name: str = PACKAGE_NAME,
    lock_root_name: str = PACKAGE_NAME,
) -> None:
    scripts = root / "scripts"
    scripts.mkdir()
    shutil.copy2(SCRIPT, scripts / SCRIPT.name)

    write_json(
        root / "package.json",
        {"name": PACKAGE_NAME, "version": NEW_VERSION, "private": True},
    )
    plugin = {
        "name": PACKAGE_NAME,
        "version": plugin_version,
        "description": "fixture metadata must survive synchronization",
    }
    write_json(root / ".claude-plugin" / "plugin.json", plugin)
    write_json(root / ".codex-plugin" / "plugin.json", plugin)
    write_json(
        root / "package-lock.json",
        {
            "name": lock_name,
            "version": lock_version,
            "lockfileVersion": 3,
            "requires": True,
            "packages": {
                "": {
                    "name": lock_root_name,
                    "version": lock_version,
                    "license": "MIT",
                },
                "node_modules/example": {
                    "version": "9.8.7",
                    "integrity": "sha512-fixture",
                },
            },
        },
    )


def run_sync(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    assert NODE is not None
    return subprocess.run(
        [NODE, str(root / "scripts" / SCRIPT.name), *arguments],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )


@unittest.skipUnless(NODE, "Node.js is unavailable; skipping Node contract tests")
class SyncPluginVersionTests(unittest.TestCase):
    def test_check_reports_drift_without_mutating_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            make_fixture(root)
            watched = (
                root / ".claude-plugin" / "plugin.json",
                root / ".codex-plugin" / "plugin.json",
                root / "package-lock.json",
            )
            before = {path: path.read_bytes() for path in watched}

            result = run_sync(root, "--check")

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("package.json is 2.3.4", result.stderr)
            self.assertEqual(before, {path: path.read_bytes() for path in watched})

    def test_mutation_synchronizes_manifests_and_both_lock_versions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            make_fixture(root)

            result = run_sync(root)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for manifest_path in (
                root / ".claude-plugin" / "plugin.json",
                root / ".codex-plugin" / "plugin.json",
            ):
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                self.assertEqual(manifest["version"], NEW_VERSION)
                self.assertEqual(manifest["name"], PACKAGE_NAME)
                self.assertEqual(
                    manifest["description"],
                    "fixture metadata must survive synchronization",
                )

            lock = json.loads((root / "package-lock.json").read_text(encoding="utf-8"))
            self.assertEqual(lock["version"], NEW_VERSION)
            self.assertEqual(lock["packages"][""]["version"], NEW_VERSION)
            self.assertEqual(lock["name"], PACKAGE_NAME)
            self.assertEqual(lock["packages"][""]["name"], PACKAGE_NAME)
            self.assertEqual(lock["packages"]["node_modules/example"]["version"], "9.8.7")

            check_result = run_sync(root, "--check")
            self.assertEqual(
                check_result.returncode,
                0,
                check_result.stdout + check_result.stderr,
            )

    def test_mismatched_lock_identity_is_never_rewritten(self) -> None:
        mismatches = (
            ("wrong-top-level-name", PACKAGE_NAME),
            (PACKAGE_NAME, "wrong-root-package-name"),
        )
        for lock_name, root_name in mismatches:
            with self.subTest(lock_name=lock_name, root_name=root_name):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    root = Path(temporary_directory)
                    make_fixture(
                        root,
                        lock_name=lock_name,
                        lock_root_name=root_name,
                    )
                    lock_path = root / "package-lock.json"
                    watched = (
                        root / ".claude-plugin" / "plugin.json",
                        root / ".codex-plugin" / "plugin.json",
                        lock_path,
                    )
                    before = {path: path.read_bytes() for path in watched}

                    result = run_sync(root)

                    self.assertNotEqual(
                        result.returncode,
                        0,
                        result.stdout + result.stderr,
                    )
                    self.assertIn("Refusing to rewrite package identity", result.stderr)
                    self.assertEqual(before, {path: path.read_bytes() for path in watched})


if __name__ == "__main__":
    unittest.main(verbosity=2)
