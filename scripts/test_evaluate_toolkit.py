#!/usr/bin/env python3
"""Offline evaluator-contract tests. Never launch Codex or consume model usage."""
import io
import json
import signal
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest.mock import MagicMock, patch

from evaluate_toolkit import CASES, classify_trace, execute, git_snapshot, main, run
from evaluate_steering import SteeringProtocol, execute_steered
from pivot_cases import CASES as PIVOT_CASES


def trace(*events):
    return "\n".join(json.dumps(event) for event in events)


COMPLETE = {"type": "turn.completed", "usage": {"input_tokens": 10}}


class TraceTests(unittest.TestCase):
    def test_clean_completion_requires_behavioral_review(self):
        result = classify_trace(trace({"type": "thread.started"}, COMPLETE), 0)
        self.assertEqual(result["status"], "needs-review")
        self.assertEqual(result["behavioral_verdict"], "not-evaluated")
        self.assertEqual(result["runtime_issues"], [])
        self.assertEqual(result["observed_tool_events"], 0)
        self.assertTrue(result["evidence_warnings"])

    def test_runtime_errors_invalidate_even_exit_zero(self):
        for event in (
            {"type": "item.completed", "item": {"type": "error", "message": "host disabled"}},
            {"type": "error", "message": "host disabled"},
            {"type": "turn.failed", "error": {"message": "failed"}},
        ):
            with self.subTest(event=event):
                self.assertEqual(classify_trace(trace(event, COMPLETE), 0)["status"],
                                 "invalid-runtime")

    def test_nonzero_invalidates_completed_trace(self):
        self.assertEqual(classify_trace(trace(COMPLETE), 1)["status"], "invalid-runtime")

    def test_incomplete_or_malformed_trace_is_invalid(self):
        for value in ("", trace({"type": "turn.started"}), "{", "[]", "null",
                      trace(COMPLETE) + '\n{"type":', trace({"type": 3}, COMPLETE)):
            with self.subTest(value=value):
                self.assertEqual(classify_trace(value, 0)["status"], "invalid-runtime")

    def test_failed_test_command_is_behavioral_evidence_not_runtime_failure(self):
        event = {"type": "item.completed", "item": {
            "type": "command_execution", "exit_code": 1, "status": "completed"}}
        self.assertEqual(classify_trace(trace(event, COMPLETE), 0)["status"], "needs-review")


class ExecutionTests(unittest.TestCase):
    def test_real_success_failure_and_timeout_receipts(self):
        with tempfile.TemporaryDirectory() as temp:
            for script, expected in (("pass", 0), ("raise SystemExit(7)", 7)):
                with tempfile.TemporaryFile(mode="w+") as output:
                    result = execute([sys.executable, "-c", script], temp, {}, 2, output, output)
                self.assertEqual(result["exit_code"], expected)
            with tempfile.TemporaryFile(mode="w+") as output:
                result = execute([sys.executable, "-c", "import time; time.sleep(10)"],
                                 temp, {}, 0.1, output, output)
            self.assertEqual(result["status"], "timeout")
            self.assertLess(result["exit_code"], 0)

    @patch("evaluate_toolkit.os.killpg")
    @patch("evaluate_toolkit.subprocess.Popen")
    def test_timeout_cancels_only_own_process_group(self, popen, killpg):
        process = MagicMock(pid=12345, returncode=-signal.SIGKILL)
        process.wait.side_effect = [subprocess.TimeoutExpired("fixture", 1), -signal.SIGKILL]
        popen.return_value.__enter__.return_value = process
        result = execute(["fixture"], "/tmp", {}, 1, io.StringIO(), io.StringIO())
        self.assertEqual(result["status"], "timeout")
        killpg.assert_called_once_with(12345, signal.SIGKILL)
        self.assertTrue(popen.call_args.kwargs["start_new_session"])
        self.assertEqual(popen.call_args.kwargs["stdin"], subprocess.DEVNULL)

    @patch("evaluate_toolkit.subprocess.Popen", side_effect=FileNotFoundError("fixture"))
    def test_launch_failure_is_explicit(self, _popen):
        result = execute(["fixture"], "/tmp", {}, 1, io.StringIO(), io.StringIO())
        self.assertEqual(result["status"], "launch-failed")
        self.assertIsNone(result["exit_code"])


class HarnessTests(unittest.TestCase):
    def test_missing_local_setup_fixture_has_setup_and_bug_signals(self):
        case = CASES["missing-local-setup"]
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            for relative, content in case["files"].items():
                target = project / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)

            missing = subprocess.run(["bash", "test.sh"], cwd=project,
                                     capture_output=True, text=True)
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("No module named 'david_eval_local_labeltools'", missing.stderr)

            subprocess.run(["bash", "bootstrap.sh"], cwd=project, check=True)
            buggy = subprocess.run(["bash", "test.sh"], cwd=project,
                                   capture_output=True, text=True)
            self.assertNotEqual(buggy.returncode, 0)
            self.assertIn("AssertionError", buggy.stderr)

            source = project / "vendor/david_eval_local_labeltools.py"
            source.write_text(source.read_text().replace(
                "value.strip().lower()", "' '.join(value.split()).lower()"))
            subprocess.run(["bash", "bootstrap.sh"], cwd=project, check=True)
            fixed = subprocess.run(["bash", "test.sh"], cwd=project,
                                   capture_output=True, text=True)
            self.assertEqual(fixed.returncode, 0, fixed.stderr)

    def test_pivot_budget_cannot_exceed_five_minutes(self):
        with patch("sys.argv", ["evaluate_toolkit.py", "pivot-small", "--timeout", "301"]), redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                main()
        self.assertEqual(error.exception.code, 2)

    def test_pivot_has_six_distinct_evidence_cases(self):
        self.assertEqual(len(PIVOT_CASES), 6)
        for case in PIVOT_CASES.values():
            self.assertTrue(case["criteria"])
        self.assertIn("steer", PIVOT_CASES["pivot-steering"])
        self.assertIn("followup", PIVOT_CASES["pivot-steering"])

    def test_candidate_and_installed_modes_with_explicit_full_access(self):
        for installed in (False, True):
            with self.subTest(installed=installed), tempfile.TemporaryDirectory() as temp:
                root = Path(temp) / "bundle"
                source = root / "skills/engineering/tdd"
                source.mkdir(parents=True)
                (source / "SKILL.md").write_text("Test fixture discipline.\n")
                (source / "reference.md").write_text("Supporting evidence.\n")
                (root / ".codex-plugin").mkdir()
                (root / ".codex-plugin/plugin.json").write_text(json.dumps({
                    "skills": ["skills/engineering/tdd"]}))
                output = Path(temp) / "evaluation"
                output.mkdir()
                argv = ["evaluate_toolkit.py", "delegated-tdd"]
                if installed:
                    argv += ["--installed-root", str(root), "--full-access"]

                def fake_execute(command, project, env, timeout, stream, errors):
                    self.assertEqual(command[command.index("-s") + 1],
                                     "danger-full-access" if installed else "workspace-write")
                    self.assertNotIn("OPENAI_API_KEY", env)
                    self.assertIn(f'projects.{json.dumps(str(project))}.trust_level="trusted"', command)
                    self.assertIn("Read and use the skill at", command[-1])
                    (project / "labels.py").write_text("# Fixture change, not a model execution.\n")
                    stream.write(trace(COMPLETE) + "\n")
                    return {"exit_code": 0}

                with patch("evaluate_toolkit.ROOT", root), \
                     patch("evaluate_toolkit.tempfile.mkdtemp", return_value=str(output)), \
                     patch("evaluate_toolkit.execute", side_effect=fake_execute), \
                     patch("sys.argv", argv), redirect_stdout(io.StringIO()):
                    self.assertEqual(main(), 0)
                receipt = json.loads((output / "receipt.json").read_text())
                self.assertEqual(receipt["status"], "needs-review")
                self.assertEqual(receipt["git_before"]["branch"], "eval")
                self.assertFalse(receipt["git_before"]["detached"])
                self.assertFalse(receipt["git_before"]["dirty"])
                self.assertTrue(receipt["git_after"]["dirty"])
                self.assertEqual(receipt["git_after"]["branch"], "eval")
                self.assertEqual(receipt["git_before"]["revision"], receipt["git_after"]["revision"])
                self.assertIn("labels.py", receipt["git_after"]["porcelain_v2"])
                copied = output / "project/.agents/skills/tdd/reference.md"
                self.assertEqual(copied.exists(), not installed)
                self.assertEqual(len(json.loads((output / "source-hashes.json").read_text())), 2)


class SteeringProtocolTests(unittest.TestCase):
    def test_offline_transport_roundtrip_and_timeout(self):
        # This is a fake RPC server, not evidence of native model behavior.
        server = '''import json, sys
for line in sys.stdin:
    message = json.loads(line)
    ident = message.get('id')
    result = {}
    if ident in (2, 6): result = {'thread': {'id': 'thread-' + str(ident)}}
    if ident in (3, 7): result = {'turn': {'id': 'turn-' + str(ident)}}
    if ident == 4: result = {'turnId': 'turn-3'}
    if ident is not None: print(json.dumps({'id': ident, 'result': result}), flush=True)
    if ident == 3:
        print(json.dumps({'method': 'item/started', 'params': {'item': {'type': 'commandExecution'}}}), flush=True)
    if ident in (4, 7):
        print(json.dumps({'method': 'turn/completed', 'params': {'turn': {'status': 'completed'}}}), flush=True)
'''
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "project"
            project.mkdir()
            script = project / "app-server"
            case = {"steer": "correction", "followup": "artifact context"}
            command = [sys.executable, "exec", "-s", "workspace-write", "initial"]
            script.write_text(server)
            with tempfile.TemporaryFile(mode="w+") as output, tempfile.TemporaryFile(mode="w+") as errors:
                result = execute_steered(command, project, {}, 2, output, errors, case)
                output.seek(0)
                events = output.read()
            self.assertEqual(result["exit_code"], 0)
            self.assertTrue(result["steer_accepted"])
            self.assertTrue(result["fresh_context_transfer"])
            self.assertEqual(classify_trace(events, 0)["status"], "needs-review")
            script.write_text("import time; time.sleep(10)\n")
            with tempfile.TemporaryFile(mode="w+") as output, tempfile.TemporaryFile(mode="w+") as errors:
                result = execute_steered(command, project, {}, 0.1, output, errors, case)
            self.assertEqual(result["status"], "timeout")
            self.assertFalse(result["fresh_context_transfer"])

    def make_protocol(self):
        return SteeringProtocol("/tmp/fixture", "initial", "correction", "artifact context", "workspace-write")

    def test_real_steer_then_fresh_thread_not_transcript_replay(self):
        protocol = self.make_protocol()
        requests = protocol.handle({"id": 1, "result": {}})
        self.assertEqual(requests[1]["method"], "thread/start")
        start = protocol.handle({"id": 2, "result": {"thread": {"id": "thread-1"}}})[0]
        self.assertEqual(start["params"]["input"][0]["text"], "initial")
        protocol.handle({"id": 3, "result": {"turn": {"id": "turn-1"}}})
        event = {"method": "item/started", "params": {"item": {"type": "commandExecution"}}}
        steer = protocol.handle(event)[0]
        self.assertEqual(steer["method"], "turn/steer")
        self.assertEqual(steer["params"]["expectedTurnId"], "turn-1")
        self.assertEqual(protocol.handle(event), [])
        protocol.handle({"id": 4, "result": {"turnId": "turn-1"}})
        complete = {"method": "turn/completed", "params": {"turn": {"status": "completed"}}}
        self.assertEqual(protocol.handle(complete)[0]["method"], "thread/start")
        fresh = protocol.handle({"id": 6, "result": {"thread": {"id": "thread-2"}}})[0]
        self.assertEqual(fresh["params"]["input"][0]["text"], "artifact context")
        protocol.handle({"id": 7, "result": {"turn": {"id": "turn-2"}}})
        protocol.handle(complete)
        self.assertTrue(protocol.finished)
        self.assertTrue(protocol.accepted)
        self.assertEqual(protocol.completed_turns, 2)
        self.assertIsNone(protocol.error)

    def test_completion_without_steering_is_not_a_pass(self):
        protocol = self.make_protocol()
        protocol.handle({"method": "turn/completed", "params": {"turn": {"status": "completed"}}})
        self.assertTrue(protocol.finished)
        self.assertIsNotNone(protocol.error)
        self.assertFalse(protocol.accepted)

    def test_rejected_steer_and_interrupted_turn_stop_explicitly(self):
        for event in ({"id": 4, "error": {"message": "turn mismatch"}},
                      {"method": "turn/completed", "params": {"turn": {"status": "interrupted"}}}):
            protocol = self.make_protocol()
            protocol.handle(event)
            self.assertTrue(protocol.finished)
            self.assertIsNotNone(protocol.error)
            self.assertEqual(protocol.completed_turns, 0)


class GitEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        run(["git", "init", "-q", "-b", "review"], self.project)
        run(["git", "config", "user.name", "Evidence Test"], self.project)
        run(["git", "config", "user.email", "test@example.invalid"], self.project)
        (self.project / "source.txt").write_text("baseline\n")
        run(["git", "add", "source.txt"], self.project)
        run(["git", "commit", "-qm", "baseline"], self.project)
        self.revision = run(["git", "rev-parse", "HEAD"], self.project).stdout.strip()

    def test_named_branch_and_revision_are_observed(self):
        result = git_snapshot(self.project)
        self.assertEqual(result["worktree"], str(self.project.resolve()))
        self.assertEqual(result["branch"], "review")
        self.assertEqual(result["revision"], self.revision)
        self.assertFalse(result["detached"])
        self.assertFalse(result["dirty"])

    def test_detached_checkout_is_not_a_named_branch(self):
        run(["git", "switch", "--detach", "-q", self.revision], self.project)
        result = git_snapshot(self.project)
        self.assertTrue(result["detached"])
        self.assertIsNone(result["branch"])
        self.assertEqual(result["revision"], self.revision)

    def test_tracked_and_untracked_changes_are_retained_as_evidence(self):
        (self.project / "source.txt").write_text("changed\n")
        (self.project / "new.txt").write_text("untracked\n")
        result = git_snapshot(self.project)
        self.assertTrue(result["dirty"])
        self.assertIn("source.txt", result["porcelain_v2"])
        self.assertIn("? new.txt", result["porcelain_v2"])

    def test_unavailable_git_is_not_reported_as_clean(self):
        with patch("evaluate_toolkit.run", side_effect=FileNotFoundError("git unavailable")):
            result = git_snapshot(self.project)
        self.assertEqual(result["status"], "unavailable")
        self.assertNotIn("dirty", result)


if __name__ == "__main__":
    unittest.main()
