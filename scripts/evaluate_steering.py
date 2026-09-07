"""Disposable app-server transport for one bounded steering evaluation.

Not a plugin runtime or a persistent service. Uses real turn/steer, then a fresh
thread with artifact-only context. OS event reads do not invoke a polling model.
"""
import json
import os
import selectors
import signal
import subprocess
import time


class SteeringProtocol:
    def __init__(self, project, prompt, correction, followup, sandbox):
        self.project = str(project)
        self.prompt, self.correction, self.followup = prompt, correction, followup
        self.sandbox = sandbox
        self.thread = self.turn = None
        self.phase = 0
        self.sent = self.accepted = self.finished = False
        self.completed_turns = 0
        self.error = None

    def request(self, ident, method, params):
        return {"id": ident, "method": method, "params": params}

    def start_thread(self, ident):
        return self.request(ident, "thread/start", {
            "cwd": self.project, "approvalPolicy": "never",
            "sandbox": self.sandbox, "ephemeral": True,
        })

    def handle(self, event):
        if "error" in event:
            self.error = event["error"]
            self.finished = True
            return []
        ident, result = event.get("id"), event.get("result", {})
        method, params = event.get("method"), event.get("params", {})
        if ident == 1:
            return [{"method": "initialized", "params": {}}, self.start_thread(2)]
        if ident in (2, 6):
            self.thread = result["thread"]["id"]
            return [self.request(3 if ident == 2 else 7, "turn/start", {
                "threadId": self.thread,
                "input": [{"type": "text", "text": self.prompt if ident == 2 else self.followup}],
            })]
        if ident in (3, 7) or method == "turn/started":
            self.turn = (result if ident in (3, 7) else params)["turn"]["id"]
        if ident == 4:
            self.accepted = result.get("turnId") == self.turn
        if (method == "item/started" and self.phase == 0 and not self.sent
                and self.turn and params.get("item", {}).get("type") in
                {"commandExecution", "mcpToolCall", "dynamicToolCall"}):
            self.sent = True
            return [self.request(4, "turn/steer", {
                "threadId": self.thread, "expectedTurnId": self.turn,
                "input": [{"type": "text", "text": self.correction}],
            })]
        if method == "turn/completed":
            status = params.get("turn", {}).get("status")
            if status != "completed":
                self.error = {"message": f"turn ended as {status}"}
                self.finished = True
                return []
            self.completed_turns += 1
            if self.phase == 0 and self.accepted:
                self.phase = 1
                self.turn = None
                return [self.start_thread(6)]
            self.finished = True
            if not self.accepted:
                self.error = {"message": "No verified in-flight steering; do not score a static replay as passing"}
        return []


def execute_steered(command, project, env, timeout, trace, errors, case):
    configs = []
    for index, arg in enumerate(command[:-1]):
        if arg == "-c":
            configs.extend(["-c", command[index + 1]])
    sandbox = command[command.index("-s") + 1]
    protocol = SteeringProtocol(project, command[-1], case["steer"], case["followup"], sandbox)
    started = time.monotonic()
    answers = []
    process = None
    selector = selectors.DefaultSelector()
    buffer = b""
    outcome = {"exit_code": 1}
    try:
        process = subprocess.Popen([command[0], "app-server", *configs], cwd=project,
                                   env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=errors, start_new_session=True)
        selector.register(process.stdout, selectors.EVENT_READ)

        def send(message):
            trace.write(json.dumps({"type": "app-server-request", "request": message}) + "\n")
            trace.flush()
            process.stdin.write((json.dumps(message) + "\n").encode())
            process.stdin.flush()

        send(protocol.request(1, "initialize", {"clientInfo": {
            "name": "david_skills_evaluation", "title": "Disposable steering evaluation", "version": "1"},
            "capabilities": {"experimentalApi": True}}))
        while not protocol.finished:
            remaining = timeout - (time.monotonic() - started)
            if remaining <= 0 or not selector.select(remaining):
                outcome["status"] = "timeout"
                break
            chunk = os.read(process.stdout.fileno(), 65536)
            if not chunk:
                outcome["status"] = "invalid-runtime"
                break
            buffer += chunk
            while b"\n" in buffer and not protocol.finished:
                line, buffer = buffer.split(b"\n", 1)
                event = json.loads(line)
                trace.write(json.dumps({"type": "app-server-event", "event": event}) + "\n")
                trace.flush()
                params = event.get("params", {})
                if event.get("method") == "item/completed":
                    item = params.get("item", {})
                    if item.get("type") == "agentMessage":
                        answers.append(item.get("text", ""))
                # Approval/tool requests must not be implicitly approved by this test client.
                if "id" in event and "method" in event:
                    send({"id": event["id"], "error": {"code": -32601,
                          "message": "Evaluation cannot grant additional authority"}})
                    protocol.error = {"message": "Runtime requested unsupported human/tool interaction"}
                    protocol.finished = True
                    break
                for request in protocol.handle(event):
                    send(request)
        if protocol.error:
            trace.write(json.dumps({"type": "error", "error": protocol.error}) + "\n")
        elif protocol.finished and protocol.completed_turns == 2 and protocol.accepted:
            trace.write(json.dumps({"type": "turn.completed"}) + "\n")
            outcome["exit_code"] = 0
        outcome.update({"steer_sent": protocol.sent, "steer_accepted": protocol.accepted,
                        "completed_turns": protocol.completed_turns,
                        "fresh_context_transfer": protocol.completed_turns == 2})
    except (OSError, ValueError, KeyError, TypeError) as exc:
        outcome.update({"status": "invalid-runtime", "error": str(exc)})
    finally:
        selector.close()
        if process is not None:
            # Terminate only the app-server process group created by this evaluation.
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            try:
                process.stdin.close()
            except OSError:
                pass
            process.stdout.close()
        (project.parent / "answer.md").write_text("\n\n".join(answers) + "\n")
    return outcome
