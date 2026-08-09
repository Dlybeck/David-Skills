#!/usr/bin/env python3
"""Hermetic behavioral tests for scripts/direct-release.sh.

The test process also acts as the mocked npm, node, and gh executables when
invoked through symlinks with those names. Every fixture uses a temporary
checkout and local bare remote; no network or real repository refs are used.
"""

from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
RELEASE_SCRIPT = SCRIPT_DIR / "direct-release.sh"


def write_json(path: Path, document: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


def append_json_line(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(f"{json.dumps(value)}\n")


def read_json_lines(path: Path) -> list[Any]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def mock_npm() -> int:
    arguments = sys.argv[1:]
    append_json_line(Path(os.environ["MOCK_NPM_LOG"]), arguments)

    if arguments == ["test"]:
        return 0
    if arguments != ["run", "version"]:
        print(f"unexpected mocked npm arguments: {arguments!r}", file=sys.stderr)
        return 64

    checkout = Path.cwd()
    package_path = checkout / "package.json"
    package = json.loads(package_path.read_text(encoding="utf-8"))
    major, minor, patch = (int(part) for part in package["version"].split("."))
    new_version = f"{major}.{minor}.{patch + 1}"
    package["version"] = new_version
    write_json(package_path, package)

    lock_path = checkout / "package-lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["version"] = new_version
    lock["packages"][""]["version"] = new_version
    write_json(lock_path, lock)

    for relative_path in (
        ".claude-plugin/plugin.json",
        ".codex-plugin/plugin.json",
    ):
        manifest_path = checkout / relative_path
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["version"] = new_version
        write_json(manifest_path, manifest)

    changelog_path = checkout / "CHANGELOG.md"
    previous_changelog = changelog_path.read_text(encoding="utf-8")
    release_entry = (
        f"## {new_version}\n\n"
        "### Patch Changes\n\n"
        "- Exercise the direct release path.\n\n"
    )
    changelog_path.write_text(
        previous_changelog.replace("# david-skills\n\n", f"# david-skills\n\n{release_entry}", 1),
        encoding="utf-8",
    )

    for changeset in (checkout / ".changeset").glob("*.md"):
        if changeset.name != "README.md":
            changeset.unlink()

    unexpected_file = os.environ.get("MOCK_UNEXPECTED_FILE")
    if unexpected_file:
        path = checkout / unexpected_file
        path.write_text(f"{path.read_text(encoding='utf-8')}changed\n", encoding="utf-8")

    return 0


def mock_node() -> int:
    arguments = sys.argv[1:]
    if len(arguments) == 2 and arguments[0] == "-p":
        package = json.loads(Path("package.json").read_text(encoding="utf-8"))
        print(package["version"])
        return 0

    if arguments:
        print(f"unexpected mocked node arguments: {arguments!r}", file=sys.stderr)
        return 64

    # Consume the here-document supplied by make_release_notes.
    sys.stdin.read()
    version = os.environ["RELEASE_VERSION"]
    notes_path = Path(os.environ["RELEASE_NOTES"])
    changelog_lines = Path("CHANGELOG.md").read_text(encoding="utf-8").splitlines()
    heading = f"## {version}"
    try:
        start = changelog_lines.index(heading)
    except ValueError:
        body = f"Release v{version}"
    else:
        end = next(
            (
                index
                for index in range(start + 1, len(changelog_lines))
                if changelog_lines[index].startswith("## ")
            ),
            len(changelog_lines),
        )
        body = "\n".join(changelog_lines[start + 1 : end]).strip()
        if not body:
            body = f"Release v{version}"
    notes_path.write_text(f"{body}\n", encoding="utf-8")
    return 0


def mock_gh() -> int:
    arguments = sys.argv[1:]
    append_json_line(Path(os.environ["MOCK_GH_LOG"]), arguments)
    state_path = Path(os.environ["MOCK_GH_STATE"])
    existing_releases = (
        set(json.loads(state_path.read_text(encoding="utf-8")))
        if state_path.exists()
        else set()
    )

    if len(arguments) >= 3 and arguments[:2] == ["release", "view"]:
        return 0 if arguments[2] in existing_releases else 1

    if len(arguments) >= 3 and arguments[:2] == ["release", "create"]:
        tag = arguments[2]
        if "--verify-tag" not in arguments:
            print("mock gh requires --verify-tag", file=sys.stderr)
            return 64
        remote_tag = subprocess.run(
            ["git", "ls-remote", "--exit-code", "origin", f"refs/tags/{tag}"],
            check=False,
            capture_output=True,
            text=True,
        )
        if remote_tag.returncode != 0:
            print(f"mock gh could not find remote tag {tag}", file=sys.stderr)
            return 1
        existing_releases.add(tag)
        state_path.write_text(
            f"{json.dumps(sorted(existing_releases))}\n", encoding="utf-8"
        )
        return 0

    print(f"unexpected mocked gh arguments: {arguments!r}", file=sys.stderr)
    return 64


class ReleaseFixture:
    def __init__(self, *, pending_changeset: bool, current_tag: bool = False) -> None:
        self._temporary = tempfile.TemporaryDirectory(prefix="david-skills-release-")
        self.root = Path(self._temporary.name)
        self.checkout = self.root / "checkout"
        self.remote = self.root / "remote.git"
        self.bin_dir = self.root / "bin"
        self.runner_temp = self.root / "runner-temp"
        self.npm_log = self.root / "npm.jsonl"
        self.gh_log = self.root / "gh.jsonl"
        self.gh_state = self.root / "gh-state.json"

        self.checkout.mkdir()
        self.bin_dir.mkdir()
        self.runner_temp.mkdir()
        self.git_environment = os.environ.copy()
        self.git_environment.update(
            {
                "GIT_CONFIG_GLOBAL": "/dev/null",
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_TERMINAL_PROMPT": "0",
                "LC_ALL": "C",
            }
        )

        self.run(["git", "init", "--bare", "--initial-branch=main", str(self.remote)])
        self.git("init", "--initial-branch=main")
        self.git("config", "user.name", "Release Test")
        self.git("config", "user.email", "release-test@example.com")
        self._write_repository(pending_changeset=pending_changeset)
        self.git("add", ".")
        self.git("commit", "-m", "test: release fixture")
        self.base_sha = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("remote", "add", "origin", str(self.remote))
        self.git(
            "push",
            "origin",
            "HEAD:refs/heads/main",
            "HEAD:refs/heads/dev",
        )
        if current_tag:
            self.git("tag", "-a", "v1.5.0", "-m", "v1.5.0")
            self.git("push", "origin", "refs/tags/v1.5.0")
        self.git("switch", "--detach", self.base_sha)

        for command in ("npm", "node", "gh"):
            (self.bin_dir / command).symlink_to(Path(__file__).resolve())

        self.environment = self.git_environment.copy()
        self.environment.update(
            {
                "PATH": f"{self.bin_dir}{os.pathsep}{os.environ['PATH']}",
                "GITHUB_REPOSITORY": "local/david-skills",
                "RELEASE_EVENT_NAME": "push",
                "RELEASE_EVENT_SHA": self.base_sha,
                "GH_TOKEN": "test-token",
                "GITHUB_TOKEN": "test-token",
                "RUNNER_TEMP": str(self.runner_temp),
                "MOCK_NPM_LOG": str(self.npm_log),
                "MOCK_GH_LOG": str(self.gh_log),
                "MOCK_GH_STATE": str(self.gh_state),
            }
        )

    def cleanup(self) -> None:
        self._temporary.cleanup()

    def _write_repository(self, *, pending_changeset: bool) -> None:
        shutil.copy2(RELEASE_SCRIPT, self.checkout / "scripts-direct-release.sh")
        (self.checkout / "scripts-direct-release.sh").chmod(0o755)
        write_json(
            self.checkout / "package.json",
            {"name": "david-skills", "version": "1.5.0", "private": True},
        )
        write_json(
            self.checkout / "package-lock.json",
            {
                "name": "david-skills",
                "version": "1.5.0",
                "lockfileVersion": 3,
                "packages": {
                    "": {"name": "david-skills", "version": "1.5.0"}
                },
            },
        )
        for relative_path in (
            ".claude-plugin/plugin.json",
            ".codex-plugin/plugin.json",
        ):
            write_json(
                self.checkout / relative_path,
                {"name": "david-skills", "version": "1.5.0"},
            )
        (self.checkout / ".changeset").mkdir()
        (self.checkout / ".changeset" / "README.md").write_text(
            "# Changesets\n", encoding="utf-8"
        )
        if pending_changeset:
            (self.checkout / ".changeset" / "release.md").write_text(
                '---\n"david-skills": patch\n---\n\nExercise direct releases.\n',
                encoding="utf-8",
            )
        (self.checkout / "CHANGELOG.md").write_text(
            "# david-skills\n\n## 1.5.0\n\nBaseline release.\n",
            encoding="utf-8",
        )
        (self.checkout / "UNEXPECTED.txt").write_text("unchanged\n", encoding="utf-8")

    def run(
        self,
        arguments: list[str],
        *,
        cwd: Path | None = None,
        environment: dict[str, str] | None = None,
        check: bool = True,
        input_text: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            arguments,
            cwd=cwd or self.checkout,
            env=environment or self.git_environment,
            check=False,
            capture_output=True,
            text=True,
            input=input_text,
        )
        if check and result.returncode != 0:
            raise AssertionError(
                f"command failed ({result.returncode}): {arguments!r}\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

    def git(
        self,
        *arguments: str,
        check: bool = True,
        input_text: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return self.run(["git", *arguments], check=check, input_text=input_text)

    def bare_git(
        self, *arguments: str, check: bool = True
    ) -> subprocess.CompletedProcess[str]:
        return self.run(["git", f"--git-dir={self.remote}", *arguments], check=check)

    def run_release(self, **environment: str) -> subprocess.CompletedProcess[str]:
        release_environment = self.environment.copy()
        release_environment.update(environment)
        return self.run(
            ["bash", "scripts-direct-release.sh"],
            environment=release_environment,
            check=False,
        )

    def prepare_moved_commit(self) -> str:
        tree = self.git("rev-parse", f"{self.base_sha}^{{tree}}").stdout.strip()
        moved_sha = self.git(
            "commit-tree",
            tree,
            "-p",
            self.base_sha,
            input_text="test: concurrent ref movement\n",
        ).stdout.strip()
        self.git("push", "origin", f"{moved_sha}:refs/heads/fixture-moved")
        return moved_sha

    def move_remote_ref(self, branch: str, moved_sha: str) -> None:
        self.bare_git(
            "update-ref",
            f"refs/heads/{branch}",
            moved_sha,
            self.base_sha,
        )

    def move_remote_ref_from_pre_push(self, branch: str, moved_sha: str) -> None:
        hook = self.checkout / ".git" / "hooks" / "pre-push"
        command = " ".join(
            shlex.quote(part)
            for part in (
                "git",
                f"--git-dir={self.remote}",
                "update-ref",
                f"refs/heads/{branch}",
                moved_sha,
                self.base_sha,
            )
        )
        hook.write_text(f"#!/usr/bin/env bash\nset -eu\n{command}\n", encoding="utf-8")
        hook.chmod(0o755)

    def remote_ref(self, ref: str) -> str | None:
        result = self.bare_git("rev-parse", "--verify", "--quiet", ref, check=False)
        return result.stdout.strip() if result.returncode == 0 else None

    def remote_file(self, ref: str, path: str) -> str:
        return self.bare_git("show", f"{ref}:{path}").stdout

    @property
    def npm_calls(self) -> list[list[str]]:
        return read_json_lines(self.npm_log)

    @property
    def gh_calls(self) -> list[list[str]]:
        return read_json_lines(self.gh_log)


class DirectReleaseTests(unittest.TestCase):
    def fixture(
        self, *, pending_changeset: bool, current_tag: bool = False
    ) -> ReleaseFixture:
        fixture = ReleaseFixture(
            pending_changeset=pending_changeset, current_tag=current_tag
        )
        self.addCleanup(fixture.cleanup)
        return fixture

    def test_releases_directly_without_a_pull_request(self) -> None:
        fixture = self.fixture(pending_changeset=True)

        result = fixture.run_release()

        self.assertEqual(result.returncode, 0, result.stderr)
        main_sha = fixture.remote_ref("refs/heads/main")
        self.assertIsNotNone(main_sha)
        self.assertNotEqual(main_sha, fixture.base_sha)
        self.assertEqual(fixture.remote_ref("refs/heads/dev"), main_sha)
        self.assertEqual(fixture.remote_ref("refs/tags/v1.5.1^{}"), main_sha)
        self.assertEqual(
            fixture.bare_git("cat-file", "-t", "refs/tags/v1.5.1").stdout.strip(),
            "tag",
        )
        self.assertEqual(
            fixture.bare_git("show", "-s", "--format=%s", main_sha).stdout.strip(),
            "chore: release v1.5.1",
        )
        self.assertEqual(
            fixture.bare_git("rev-parse", f"{main_sha}^").stdout.strip(),
            fixture.base_sha,
        )
        released_package = json.loads(fixture.remote_file(main_sha, "package.json"))
        released_lock = json.loads(fixture.remote_file(main_sha, "package-lock.json"))
        self.assertEqual(released_package["version"], "1.5.1")
        self.assertEqual(released_lock["version"], "1.5.1")
        self.assertEqual(released_lock["packages"][""]["version"], "1.5.1")
        self.assertIsNone(fixture.remote_ref("refs/heads/changeset-release/main"))
        self.assertEqual(
            fixture.npm_calls,
            [["test"], ["run", "version"], ["test"]],
        )
        self.assertEqual(
            [call[:2] for call in fixture.gh_calls],
            [["release", "view"], ["release", "create"]],
        )
        self.assertFalse(
            any("pr" in argument for call in fixture.gh_calls for argument in call)
        )

    def test_requires_main_and_dev_to_be_exactly_aligned(self) -> None:
        fixture = self.fixture(pending_changeset=True)
        moved_sha = fixture.prepare_moved_commit()
        fixture.move_remote_ref("dev", moved_sha)

        result = fixture.run_release()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("origin/main and origin/dev must be aligned", result.stderr)
        self.assertEqual(fixture.remote_ref("refs/heads/main"), fixture.base_sha)
        self.assertEqual(fixture.remote_ref("refs/heads/dev"), moved_sha)
        self.assertIsNone(fixture.remote_ref("refs/tags/v1.5.1"))
        self.assertEqual(fixture.npm_calls, [["test"]])
        self.assertEqual(fixture.gh_calls, [])

    def test_exact_lease_refuses_a_race_after_the_final_fetch(self) -> None:
        fixture = self.fixture(pending_changeset=True)
        moved_sha = fixture.prepare_moved_commit()
        fixture.move_remote_ref_from_pre_push("dev", moved_sha)

        result = fixture.run_release()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(f"but expected {fixture.base_sha}", result.stderr)
        self.assertIn("atomic transaction failed", result.stderr)
        self.assertEqual(fixture.remote_ref("refs/heads/main"), fixture.base_sha)
        self.assertEqual(fixture.remote_ref("refs/heads/dev"), moved_sha)
        self.assertIsNone(fixture.remote_ref("refs/tags/v1.5.1"))
        self.assertEqual(
            fixture.npm_calls,
            [["test"], ["run", "version"], ["test"]],
        )
        self.assertEqual(fixture.gh_calls, [])

    def test_recovers_a_missing_github_release_for_the_current_tag(self) -> None:
        fixture = self.fixture(pending_changeset=False, current_tag=True)
        moved_sha = fixture.prepare_moved_commit()
        fixture.move_remote_ref("dev", moved_sha)

        result = fixture.run_release(
            RELEASE_EVENT_NAME="workflow_dispatch",
            RELEASE_RECOVERY_TAG="v1.5.0",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(fixture.remote_ref("refs/heads/main"), fixture.base_sha)
        self.assertEqual(fixture.remote_ref("refs/heads/dev"), moved_sha)
        self.assertEqual(fixture.remote_ref("refs/tags/v1.5.0^{}"), fixture.base_sha)
        self.assertEqual(fixture.npm_calls, [["test"]])
        self.assertEqual(
            [call[:2] for call in fixture.gh_calls],
            [["release", "view"], ["release", "create"]],
        )
        notes = fixture.runner_temp / "david-skills-v1.5.0.md"
        self.assertIn("Baseline release.", notes.read_text(encoding="utf-8"))

    def test_refuses_files_outside_the_versioning_allowlist(self) -> None:
        fixture = self.fixture(pending_changeset=True)

        result = fixture.run_release(MOCK_UNEXPECTED_FILE="UNEXPECTED.txt")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("versioning modified tracked files outside", result.stderr)
        self.assertIn("UNEXPECTED.txt", result.stderr)
        self.assertEqual(fixture.remote_ref("refs/heads/main"), fixture.base_sha)
        self.assertEqual(fixture.remote_ref("refs/heads/dev"), fixture.base_sha)
        self.assertIsNone(fixture.remote_ref("refs/tags/v1.5.1"))
        self.assertEqual(fixture.gh_calls, [])

    def test_no_changeset_and_no_current_tag_is_a_noop(self) -> None:
        fixture = self.fixture(pending_changeset=False)

        result = fixture.run_release()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("No pending Changesets; nothing to release.", result.stdout)
        self.assertEqual(fixture.remote_ref("refs/heads/main"), fixture.base_sha)
        self.assertEqual(fixture.remote_ref("refs/heads/dev"), fixture.base_sha)
        self.assertIsNone(fixture.remote_ref("refs/tags/v1.5.0"))
        self.assertEqual(fixture.npm_calls, [["test"]])
        self.assertEqual(fixture.gh_calls, [])


def main() -> int:
    invoked_as = Path(sys.argv[0]).name
    if invoked_as == "npm":
        return mock_npm()
    if invoked_as == "node":
        return mock_node()
    if invoked_as == "gh":
        return mock_gh()

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DirectReleaseTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
