# 01 — Build `yolopilot`

**What to build:** The full `yolopilot` skill — no pre-departure grilling, a short non-blocking
warning plus a stated best-guess interpretation, launch via `claude --bg` with `/goal` as the
literal launch argument (checkable essentials inline, `SKILL.md` pointer for the working
session's own benefit), finer-grained and more frequent commits than `autopilot` throughout the
run, the same working loop otherwise (`/code-review` gate, `Strong`-only `/re-architect` idle
work, same stopping logic), and the real divergence — completes its own git cycle up to a
pushed, reviewable branch but never merges into `dev` automatically. Before stopping: one final
whole-branch `/code-review` pass, then a deliberately explanatory closing message (not a terse
status line) that recommends `/to-spec` retroactively and offers `/teach` as an optional next
step. Full registry integration matching `autopilot`/`delegate`'s shape.

**Blocked by:** None — can start immediately.

**Status:** resolved

- [ ] New user-invoked skill `yolopilot` at `skills/engineering/yolopilot/` (`SKILL.md` +
      `agents/openai.yaml`, `disable-model-invocation: true` / `policy.allow_implicit_invocation:
      false`)
- [ ] No pre-departure grilling round documented; entry sequence is: show a short, 1-2 sentence,
      non-blocking warning naming the elevated risk → state its own best-guess interpretation of
      the loose instruction → launch immediately, no wait for a reply between any step
- [ ] Launches via `claude --bg` with `/goal <condition>` as the literal launch argument, stating
      the checkable essentials (the git rule) directly in the condition text, with a `SKILL.md`
      pointer for the working session's own benefit only
- [ ] Confidence guideline inherited unchanged from `autopilot` — anchored to the agent's own
      stated interpretation; no new mechanical threshold documented
- [ ] Commits land more frequently and at finer grain throughout the working loop than
      `autopilot`'s do — documented explicitly as deliberate, not incidental
- [ ] Never merges into `dev` automatically — completes its git cycle up through a pushed,
      reviewable branch only; once approved, the AI can perform the actual merge (`--no-ff`) as a
      follow-up action
- [ ] The rest of the working loop (the `/code-review` gate per unit, `Strong`-only
      `/re-architect` idle-capacity handling, the same stopping logic) is inherited unchanged from
      `autopilot`
- [ ] Before stopping, runs one additional `/code-review` pass across the whole branch, passing
      its own stated interpretation as the stand-in for a spec
- [ ] Closing message is deliberately explanatory (why key decisions were made, what was assumed,
      what's riskiest) rather than a terse status line
- [ ] Closing message recommends running `/to-spec` retroactively, and offers (does not default
      into) `/teach` as an optional next step
- [ ] `main` remains untouched; no changes made to `hooks/block-dangerous-git.py`
- [ ] `CONTEXT.md` gains an entry for `yolopilot`, fulfilling the Relationships section's existing
      forward-looking note about a future unattended skill answering to the Confidence guideline
- [ ] Registry integration complete: `.claude-plugin/plugin.json`, top-level `README.md`,
      `skills/engineering/README.md` (User-invoked), `docs/engineering/yolopilot.md`, `ask-claude`'s
      `SKILL.md` map
- [ ] No reference to a specific person (e.g. "David") anywhere in the skill's own text — generic
      "the user" throughout, matching the fix already applied to `autopilot`
- [ ] `claude plugin validate . --strict` passes
