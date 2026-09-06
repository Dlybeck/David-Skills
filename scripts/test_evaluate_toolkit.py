#!/usr/bin/env python3
"""Offline evaluator-contract tests. Never launch Codex or consume model usage."""
import io
import json
import signal
import subprocess
import unittest
from unittest.mock import MagicMock, patch

from evaluate_toolkit import classify_trace, execute


def trace(*events):
    return "\n".join(json.dumps(event) for event in events)


COMPLETE = {"type": "turn.completed", "usage": {"input_tokens": 10}}


class TraceTests(unittest.TestCase):
    def test_clean_completion_requires_behavioral_review(self):
        result = classify_trace(trace({"type": "thread.started"}, COMPLETE), 0)
        self.assertEqual(result["status"], "needs-review")
        self.assertEqual(result["behavioral_verdict"], "not-evaluated")
        self.assertEqual(result["runtime_issues"], [])

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


if __name__ == "__main__":
    unittest.main()
