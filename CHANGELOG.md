# denali-dev

## 1.5.0

### Minor Changes

- [`f171b1c`](https://github.com/DenaliAI-Automation/Denali-DEV/commit/f171b1c2b9f72e75c96a2b6063efdb58424d4693) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - Add **`autopilot`** to the Engineering bucket: manually-triggered, never-scheduled unattended
  work mode ("I'm leaving, keep working without me"). A pre-departure `/grilling` session locks the
  goal condition and any scope/guardrails in the current, foreground session — before backgrounding,
  since an unattended run needs its destination settled while a human is still there to settle it.
  It then launches via `claude --bg` (survives full disconnection, unlike the harness's own
  session-scoped `/loop`) driving native `/goal`.

  No hard time/token ceiling: per ADR 0005, Denali's AI team routinely kicks off legitimately
  long-running work as the actual task, and a blunt cap would kill it mid-flight. The **Confidence
  guideline** is the safety net instead — act freely inside locked scope or on an existing strong
  confidence signal, log and leave anything else for review — applied continuously and once more
  holistically before the run ends. Each unit of work ends with a fully autonomous `/code-review`
  pass, with real findings fixed before continuing; idle capacity runs `/re-architect`'s own
  exploration/scoring steps directly (skipping its human-gated pick-and-grill steps), acting only on
  `Strong`-scored candidates. Completes its own git cycle into `dev` autonomously — only `main`
  stays human-gated, already covered unconditionally by the existing `hooks/block-dangerous-git.py`.

  Adds a general "Delegated continuation of a user-invoked skill's own process" section to
  `.agents/invocation.md`, since this is the same pattern `delegate` already needed for
  `/implement`, now needed twice more here (continuing this skill's own process unattended; running
  `/re-architect`'s scan without its pick-and-grill steps).

- [`3aa9c01`](https://github.com/DenaliAI-Automation/Denali-DEV/commit/3aa9c013ec1ac0aa94f25bddacbeec32fae3a4a5) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - Rework **`delegate`** from a toggled session mode into a bounded, on-call dispatch run: invoke
  `/delegate` when a frontier of ready tickets exists; it claims, dispatches whole tickets to
  worker subagents, integrates each finished branch, and is over when the frontier is drained —
  nothing persists between runs, and the toggle is gone. First real use showed the mode framing
  failing in practice (recommended by model-match before any tickets existed, pitched per-frontier
  anyway, left on-and-inert after the work drained) while the state behind it was nothing but
  conversational memory; ADR 0007 records the full reasoning, including why the skill survives at
  all next to the harness's own orchestration tooling (the tooling is mechanism, the skill is house
  process) and why the dispatcher still never reviews worker output.

  Riding along: Setup drops the orchestration-mechanics questions and asks exactly two things with
  precise units (Worker model; Max concurrent workers — tickets in flight at once); the run's
  integration step is now written down (sequential `--no-ff` merges, checkout verified against
  `HEAD` after each); the worker brief gains the fast-forward-first instruction for stale
  worktrees; `CONTEXT.md`'s **Delegate**/**Router** entries and the Confidence-guideline
  relationship are rewritten model-neutral; `ask-claude`, both READMEs, the docs page, and the
  SessionStart hook's recommendation wording are re-synced to the new semantics.

- [`f171b1c`](https://github.com/DenaliAI-Automation/Denali-DEV/commit/f171b1c2b9f72e75c96a2b6063efdb58424d4693) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - Add **`delegate`** to the Engineering bucket: a standing mode, entered with `/delegate`, where a
  light model (Fable is the flagship case, but any cheap/expensive pair works) acts strictly as a
  **Router** over `/implement`'s place in the main chain — classify a frontier ticket and hand it
  off whole to a Sonnet/Opus subagent worker, never decomposing work, judging a worker's partial
  result, or trying to recover a stuck worker itself. That's the documented failure mode a weak
  model given real orchestration duties falls into; classify-and-handoff only is the
  well-precedented, safe version. The user stays present throughout — a stuck worker surfaces
  straight to them, never to an automatic stronger-model fallback.

  Adds a general "claim the ticket" convention to `docs/agents/issue-tracker.md` and both seed
  templates (mirroring `wayfinder`'s own claim step, not a `delegate`-specific mechanism), so "find
  the frontier" can honestly include "unclaimed" again. Also documents directly that
  `/implement`'s advisory-only code-review means `Status: resolved` isn't proof a review finding
  was addressed — `delegate`'s own dispatch prompt asks workers for that explicitly rather than
  trusting ticket status alone. Setup (router model, worker model(s), dispatch mechanism) lives in
  its own config file, `docs/agents/delegate.md`, written on first use and separate from `/setup`'s
  issue-tracker/triage/domain scope.

- [`7b2edec`](https://github.com/DenaliAI-Automation/Denali-DEV/commit/7b2edec8cc024016d77d668ad59002f604f5753b) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - **Breaking:** remove **GitLab** as a first-class `setup` tracker option. GitLab was inherited
  from upstream at the fork and never revisited — this team has no GitLab license, so it was
  never actually usable here. GitLab is not gone as a tracker choice, only as a ready-made
  template: describing it through `setup`'s freeform "other" path still works exactly as it does
  for Linear, Azure DevOps, or any tracker without first-class support. `issue-tracker-gitlab.md`
  deleted; every "ships as a ready-made template" claim about GitLab removed from `setup`'s docs,
  `README.md`, and `wayfinder`'s docs. Illustrative, non-claim mentions elsewhere (a GitLab `!67`
  reference-format example in `code-review`'s docs, community-usage anecdotes in `triage`'s and
  `wayfinder`'s FAQs) are unaffected — they never claimed first-class support in the first place.

- [`2e90aa6`](https://github.com/DenaliAI-Automation/Denali-DEV/commit/2e90aa67a64aee3b6694c245579ddd77ee2f64eb) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - **Breaking:** remove the **`personal-git-workflow`** skill from the Engineering bucket. No
  replacement — its actual value was the mechanical `main`-push/PR guard (`hooks/hooks.json` +
  `hooks/block-dangerous-git.py`), which is a plugin-root hook independent of any skill folder
  and is unaffected by this removal: it still hard-blocks any push or PR into `main`, and still
  unconditionally blocks `reset --hard`, force `clean`, `branch -D`, and `checkout .`/`restore .`.
  Only the teaching prose (branch caps, staleness audits, merge-vs-PR guidance) is gone. Every
  cross-reference removed (both READMEs, `plugin.json`, the docs page, `ask-claude`'s routing);
  the hook's own error-message text no longer names the skill, since it's now self-contained. See
  ADR 0003's 2026-08-07 update note for the reasoning.

- [`fb13de6`](https://github.com/DenaliAI-Automation/Denali-DEV/commit/fb13de607e7a313253475500c9be78ef72805013) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - Add **`soc2`** to the Engineering bucket: a user-invoked, on-demand gate that runs Denali's
  existing SOC2 compliance policy (`denali-platform:denali-soc2-compliance`) against a diff,
  spec, ticket, or wizard script before it ships. It owns no policy content of its own — every
  rule, policy ID, and compliant alternative lives in that skill; `soc2` is only the seam that
  calls it from inside a `denali-dev` flow, so there is exactly one place the actual ruleset can
  drift.

  Deliberately kept separate from `code-review` rather than folded in as a third axis, and
  deliberately manual rather than model-invoked: most of what this plugin produces (its own docs,
  non-Denali repos, side projects) never touches regulated data, so firing a compliance pass on
  every review or every ticket would be noise far more often than signal. Reach for it explicitly
  when the artifact in front of you actually warrants it.

- [`efd2971`](https://github.com/DenaliAI-Automation/Denali-DEV/commit/efd29712733a1f740dbf436c6fdec5abdd6cc61e) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - Add **`yolopilot`** to the Engineering bucket: a lighter-entry sibling to `autopilot`, for a
  loose, last-second handoff with no time for a pre-departure `/grilling` round. It shows a short,
  non-blocking warning naming the elevated risk, states its own best-guess interpretation of the
  loose instruction, then launches immediately — no wait for a reply between any step — reusing
  `autopilot`'s exact mechanism (`claude --bg` driving a self-set `/goal`), the same working loop
  (the per-unit `/code-review` gate, `Strong`-only `/re-architect` idle work, the same stopping
  logic), and the same Confidence guideline, unchanged, now anchored to the agent's own stated
  interpretation instead of a jointly-grilled goal.

  The one hard rule that earns it a distinct identity: it never merges into `dev` on its own. It
  completes its own git cycle only up through a pushed, reviewable feature branch — committing more
  often and at a finer grain than `autopilot` throughout the run, since there's no upfront-verified
  scope to lean on and the git history itself has to carry that audit trail — leaving the actual
  `--no-ff` merge for a human decision, which the AI can then carry out itself as a follow-up
  action. Before stopping, it runs one additional whole-branch `/code-review` pass, using its own
  stated interpretation as the stand-in for a spec, and closes with a deliberately explanatory
  message (why key decisions were made, what was assumed, what's riskiest) that recommends running
  `/to-spec` retroactively and offers `/teach` as an optional next step.

  `CONTEXT.md` gains a `Yolopilot` entry, fulfilling the Relationships section's existing
  forward-looking note that a future unattended skill should answer to the Confidence guideline too.
  `main` remains untouched; no changes to `hooks/block-dangerous-git.py`.

### Patch Changes

- [`9c4e9d1`](https://github.com/DenaliAI-Automation/Denali-DEV/commit/9c4e9d150938a392430c4b399d944754e129519f) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - Record the fork's identity decision as **ADR 0006**: this plugin encodes Denali's in-house
  practice, not a portable skills collection. House assumptions (the `dev ← feature/**` branch
  model with `main` human-gated, always-on plugin-root hooks, Denali-specific skills) are licensed
  and get _declared_; the bounding rule is that an assumption must hold in **every install of the
  plugin**, not just this development checkout — checkout-relative paths, pointers to unshipped
  `.scratch/` files, and dead docs URLs are lies, not assumptions, and are being fixed under the
  same spec. The ADR also records the new precedent that every hook lands with executable test
  cases at its stdin→exit-code contract.

  Bookkeeping riding along: ADR 0003 gains a dated update covering `delegate-recommend.py` (the
  one hook that shipped without a decision record — informational-only, fail-silent, `/delegate`
  stays manual); ADR 0005 gains a dated note putting autopilot's fenced `re-architect` bypass on
  the record (`Strong`-scored candidates only, everything below logged for review, behavior
  unchanged); the README's opening now states the in-house identity instead of implying
  portability.

- [`f171b1c`](https://github.com/DenaliAI-Automation/Denali-DEV/commit/f171b1c2b9f72e75c96a2b6063efdb58424d4693) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - Corrects **`autopilot`**'s own changelog entry: a same-cycle detour tried running it inline —
  staying in the invoking session and dispatching each chunk of work as a background subagent via
  the `Agent`/`Workflow` tool, the same pattern `/code-review` already uses for its own two axes —
  on the reasoning that `claude --bg`'s "survives disconnection" guarantee was redundant with the
  terminal multiplexer every session already runs inside, while `--bg`'s own more restrictive
  network sandbox had caused a `git push` to time out on a real run.

  That detour didn't hold up and never shipped as final. Its core assumption was that the assistant
  could set Claude Code's native `/goal` on itself from within an already-running session; verified
  false — `/goal` only fires on literal input to a session, a human typing it or a fresh session's
  own launch argument, never anything the assistant writes in its own output. Without a
  self-settable `/goal`, the inline design's "hands-off" property was never actually true, so the
  subagent-dispatch mechanic is gone. Separately, the network-sandbox cost didn't reproduce on a
  second live run over the same remote, and nothing in Claude Code's own docs supports background
  sessions having a different network posture — that finding is now treated as unconfirmed, not a
  cost designed around.

  **What actually ships**, and is the only mechanism `autopilot` has ever launched with in a
  released version: right after the pre-departure grill locks the goal condition, `autopilot`
  launches `claude --bg` with `/goal <condition>` as the literal launch argument, verified directly
  with a real Stop hook confirmed active — the one mechanism that delivers a genuinely zero-keystroke
  unattended run. `claude --bg`'s automatic worktree isolation is documented as a property of the
  mechanism, and is what actually resolves the "keep chatting here, lose track of it" risk that
  briefly motivated dropping `--bg` in the first place. The closing report lives in the background
  session itself, read back via `claude agents`/`claude logs` — not in the inline conversation.

  Two follow-on fixes land alongside the correction: the `/goal` condition now states its checkable
  essentials (the git cycle, the review gate) directly in the condition text itself, rather than
  leaning on a trailing `SKILL.md` pointer the evaluator can't resolve — the one live test that
  proved this mechanism used a bare condition, so a pointer only the working session could follow
  risked being the sole place a hard rule lived. And `.agents/invocation.md`'s "Delegated
  continuation" section is reworded to honestly define both cases it covers — a different worker
  carrying out another user-invoked skill's process, and a skill continuing its own — a definitional
  gap present since the section's first version, surfaced by restoring `autopilot`'s
  self-continuation citation. ADR 0005 gets a third dated update note, not a rewrite: the decision
  it actually records (no hard time/token ceiling, Confidence guideline instead) stays untouched.

- [`6d130a2`](https://github.com/DenaliAI-Automation/Denali-DEV/commit/6d130a2d91555b173374dd5a562656bceaf65023) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - `autopilot` and `yolopilot` fix the three install-portability defects ADR 0006 named. Both
  `SKILL.md`s and both docs pages now state the `dev`-integration-branch assumption
  (`main ← dev ← feature/**`, `main` human-gated) as an explicit prerequisite up front, citing ADR
  0006 as the ruling that licenses stating it rather than generalizing it away —
  `docs/engineering/autopilot.md`'s "no persistent config file or prior setup is required" line is
  corrected to name it. Both skills' `claude --bg` launch arguments are rebuilt to carry the goal
  condition and guardrails inline as content instead of pointing at
  `skills/engineering/<skill>/SKILL.md` — a path that only resolves in this checkout, not from a
  plugin-cache or `skills.sh` install. `autopilot`'s stuck/no-progress guidance moves out of the
  `.scratch/autopilot/spec.md` Out of Scope pointer no install ships and into the skill's own
  Ending section.

- [`c1c8d20`](https://github.com/DenaliAI-Automation/Denali-DEV/commit/c1c8d200f96255ef69776ea29fe0d7cfcad8fb22) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - Fix docs-page cross-links that pointed at `aihero.dev/skills-<name>` for skills whose pages
  never existed there: the renamed trio (`ask-claude`, `re-architect`, `setup`) and the fork-added
  four (`delegate`, `autopilot`, `yolopilot`, `soc2`). Every such link, across every docs page that
  carried one, now points at the real file instead — `./<name>.md` within a bucket,
  `../<bucket>/<name>.md` across `engineering/`/`productivity/`.

  `.agents/writing-docs.md` and `CLAUDE.md` no longer claim this docs tree is published on
  `aihero.dev`; both now state the actual convention (repo-relative cross-links, `docs/<bucket>/`
  as repo organisation only) and keep the `aihero.dev` page template as the noted historical
  origin of the format, not a live pipeline. Links that genuinely serve Matt's own published
  pages — his original, un-renamed skills, `aihero.dev` articles, the AI Coding Dictionary — are
  untouched.

- [`e541b68`](https://github.com/DenaliAI-Automation/Denali-DEV/commit/e541b68b2bd52a20b79448dc51a30eba46f7d5c9) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - Closes a quoting bypass in `block-dangerous-git.py`: `git push origin "main"` (or `'main'`, or an
  interpolation-adjacent spelling like `"ma"in` that a real shell concatenates to `main` the same
  way) slipped past the push-to-main and PR-base-main patterns, because the boundary regexes
  required `main` to be directly preceded by whitespace/`:`/`+`, and a quote character sitting
  between "origin" and "main" broke that adjacency. The main-only push guard is a rule that already
  failed once as prose (ADR 0003) — a re-quoting trick sidestepping its mechanical backstop is
  exactly the failure mode it exists to close. Fix: strip shell quote characters (`"` and `'`) from
  the command text before pattern matching, so quoted and unquoted spellings match identically.
  `feature/main-page` and similar near-misses are unaffected — the boundary characters the patterns
  check for are still present after quotes are removed.

  Also adds `hooks/test_hooks.py`, the repo's first executable test (per ADR 0006's "hooks carry
  executable tests" precedent). Python standard library only, no framework, runnable directly via
  `python3 hooks/test_hooks.py`. Drives each hook as a subprocess through its real, only contract —
  JSON on stdin, allow (exit 0) or block (exit 2) via exit code — never touching internals: a
  table of plain/quoted/interpolation-adjacent push- and PR-to-main spellings that must block,
  feature-branch pushes and `feature/main-page`-style lookalikes that must pass, the four
  destructive-op patterns and their safe lookalikes, and malformed stdin failing open (exit 0,
  silent) for both `block-dangerous-git.py` and `require-committed-claim.py`. Future hooks add
  their cases to this file rather than starting a new one.

- [`99e98d8`](https://github.com/DenaliAI-Automation/Denali-DEV/commit/99e98d83672fc64097ed2ca4553a6d6fe6c1bbf4) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - Fixes a real gap surfaced by a live `delegate` dispatch: a ticket "claimed" by setting
  `Status: claimed` and saving — per `docs/agents/issue-tracker.md`'s convention — was never
  actually committed, so the dispatched worker's own isolated `Workflow` worktree (built from the
  last commit, not this checkout's working tree) never saw it. The same ticket sat fully untracked
  through its entire claim → dispatch → resolve lifecycle; the worker had to reach outside its own
  worktree with raw Python just to record the outcome on disk.

  Two layers, not just a re-wording — prose alone already missed this once:

  - **Mechanized**: a new `PreToolUse` hook, `hooks/require-committed-claim.py`, wired in
    `hooks/hooks.json` against `Bash` (matched to a `claude --bg` launch) and `Workflow` (any call).
    Blocks the dispatch outright while anything under `.scratch/` has uncommitted changes, with a
    message explaining why and what to do. No-ops entirely when the repo's tracker isn't local
    markdown (a real tracker's claim is an instant API call — this bug class can't happen there).
    Same philosophy as the existing `block-dangerous-git.py`: a hook that can't forget beats an
    agent that has to remember correctly every time.
  - **Corrected the prose that was actually wrong**: `docs/agents/issue-tracker.md` and its seed
    template `skills/engineering/setup/issue-tracker-local.md` now say to _commit_ a publish/claim/
    resolve write, not just save it — kept in sync across both files. `delegate/SKILL.md`'s Dispatch
    step restates the committed-claim requirement inline, at the exact point dispatch happens.

- [`9e85e11`](https://github.com/DenaliAI-Automation/Denali-DEV/commit/9e85e11cfa78545f3b26d12771e80a59840db9ee) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - Writing pass over the fork's own drift from `writing-for-agents`, per the philosophy audit.

  Single source of truth: the Confidence guideline's full definition lives in `CONTEXT.md` alone —
  `autopilot`, `yolopilot`, `ask-claude`, and both docs pages now carry a pointer plus at most a
  one-clause gloss instead of restating it. The worktree-from-last-commit fact is owned by
  `docs/agents/issue-tracker.md`; the seed template (`skills/engineering/setup/issue-tracker-local.md`)
  now states the generic git truth without naming `claude --bg` or `Workflow`, and both
  `hooks/require-committed-claim.py`'s docstring and `delegate`'s Dispatch step point at the
  convention doc instead of retelling the incident that motivated it.

  Negation pass: `delegate` and `yolopilot` prohibitions are rephrased positively wherever a
  positive phrasing exists — the genuine hard guardrails (Router never decomposes/judges/rescues;
  `yolopilot` never merges into `dev` unattended) stay as prohibitions, paired with their positive
  counterpart.

  Justification pass: cut in-body design-argument asides from `delegate/SKILL.md` ("Prior art is
  consistent that...", "confirmed the hard way, not a hypothetical", "that was never a real Setup
  choice") that already have a home — the `delegate` changeset and `docs/agents/issue-tracker.md`
  carry the rationale, so the skill body states process instead of re-arguing it.

  Mechanical sweep: `delegate/SKILL.md`'s `## Common questions` section is gone (its docs page
  already carries the Q&A); `soc2/SKILL.md`'s H1 is recased to `# SOC2`, matching its siblings'
  Title Case; the stray blank line splitting the engineering README's Model-invoked list is
  removed; `autopilot`'s and `yolopilot`'s frontmatter descriptions are trimmed toward one short,
  human-facing line, with the exact trimmed string propagated to both READMEs.

## 1.4.0

### Minor Changes

- [`d70fce5`](https://github.com/DenaliAI-Automation/Denali-DEV/commit/d70fce59bfda3fb2bc49c57dfe8149b60901f90d) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - **Breaking:** rename the plugin/marketplace/package identity itself, **`denali-skills-dev`** → **`denali-dev`**. Every plugin-sourced skill gets namespaced as `<plugin>:<skill>` by Claude Code, so a shorter plugin name shortens every single invocation, not just the ones that happened to repeat "denali" or "skills" in their own name. Renamed across `package.json`, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json`. The GitHub repo itself is **not** renamed to match — it stays `Denali-DEV` (see the separate repo rename), since the org's push-to-`main` exemption depends on the exact `-DEV` suffix and a mismatch there is a real risk, not a style choice. Reinstall under the new plugin name; the old one is gone (no alias).

- [`d70fce5`](https://github.com/DenaliAI-Automation/Denali-DEV/commit/d70fce59bfda3fb2bc49c57dfe8149b60901f90d) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - **Breaking:** rename **`setup-denali-skills`** → **`setup`**. Claude Code namespaces every plugin skill as `<plugin>:<skill>` — with the plugin itself renamed to `denali-dev` in this same release, `setup-denali-skills` would have stuttered as `denali-dev:setup-denali-skills`, repeating "denali" twice for no reason. No behavior change: still the same prompt-driven, run-once scaffolding for a repo's issue tracker, triage labels, and domain-doc layout. Every cross-reference updated (both READMEs, `plugin.json`, the docs page, every skill that names it as a hard dependency per ADR 0001, `ask-claude`'s routing, and the live `.out-of-scope/` entry). Reinstall under the new name; the old name is gone (no alias).

## 1.3.0

### Minor Changes

- [`3b67f34`](https://github.com/DenaliAI-Automation/Denali-Skills-DEV/commit/3b67f349da1f65ceb3e6026f20d4afafe1623a9a) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - **Breaking:** rename **`ask-matt`** → **`ask-claude`**. This is a private Denali fork, not Matt's personal repo — the router's identity (its title, its display name) named the wrong person for this context. No behavior change: still the same hand-maintained map over every skill in the set, still user-invoked only. Every cross-reference updated (top-level + Engineering READMEs, `plugin.json`, `CLAUDE.md`'s self-maintenance rule, `.agents/writing-docs.md`'s "point to the router" instruction, and the "Where it fits" link on every other docs page). Reinstall under the new name; the old name is gone (no alias).

- [`ec901a6`](https://github.com/DenaliAI-Automation/Denali-Skills-DEV/commit/ec901a657cb703176cb52e96e5e5949e1c67c099) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - Add **`personal-git-workflow`** to the Engineering bucket: a `main ← dev ← feature/**` branching model for solo/dev-quality repos, distinct from an org's own PR-gated production workflow. `main` is human-only, full stop — no agent merges into it or opens a PR into it, not even "to have it ready to click." Feature branches are capped at 3-4 open, forcing a finish/merge/archive/park decision instead of letting them quietly accumulate.

  That `main` rule is now hook-enforced, not just written: a bundled `PreToolUse` hook (`hooks/hooks.json` + `hooks/block-dangerous-git.py`, plugin root, stdlib Python only) hard-blocks any `git push` targeting `main` and any `gh pr create`/`gh pr edit --base main` before the command runs. The same hook also unconditionally blocks four local-destructive git operations regardless of branch — `git reset --hard`, a force `git clean`, `git branch -D`, `git checkout .`/`git restore .` — since there's no "it's fine on a feature branch" case for losing uncommitted work. Ships at the plugin root rather than requiring a per-repo setup step, so installing this plugin protects every repo it's enabled in automatically — Claude Code plugin installs only; a `skills.sh` install gets the written discipline but not the automatic block, and the skill says so.

  This also **replaces `misc/git-guardrails-claude-code`** (removed in a separate changeset), matching its full blocked-pattern list, but scoped more precisely on the push/PR side (main only, not every push — a deliberate divergence matching this skill's own policy that dev/feature pushes are fine for an agent to do on its own) and without the `jq` dependency.

  Now wired as a promoted skill — plugin entry, top-level + Engineering READMEs under **Model-invoked**, a docs page at `docs/engineering/personal-git-workflow.md`, and a Standalone route in `ask-claude`.

- [`3b67f34`](https://github.com/DenaliAI-Automation/Denali-Skills-DEV/commit/3b67f349da1f65ceb3e6026f20d4afafe1623a9a) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - **Breaking:** rename **`improve-codebase-architecture`** → **`re-architect`** — shorter, matching Denali's own naming preference from the Phase 2 terminology review. No behavior change: still the periodic-maintenance survey that scans for deepening opportunities and hands them off through a grilling session. Every cross-reference updated (both READMEs, `plugin.json`, `diagnosing-bugs`' post-mortem hand-off, `grilling`'s and `domain-modeling`'s and `codebase-design`'s docs pages, `ask-claude`'s routing). Reinstall under the new name; the old name is gone (no alias).

- [`3b67f34`](https://github.com/DenaliAI-Automation/Denali-Skills-DEV/commit/3b67f349da1f65ceb3e6026f20d4afafe1623a9a) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - **Breaking:** rename **`setup-matt-pocock-skills`** → **`setup-denali-skills`**. Same reasoning as the `ask-claude` rename — this is a private Denali fork, and the setup skill's name is the first thing anyone installing it types. No behavior change: still the same prompt-driven, run-once scaffolding for a repo's issue tracker, triage labels, and domain-doc layout. This is the most widely cross-referenced rename of the three (it's a **hard dependency** — see ADR 0001 — for `to-tickets`, `to-spec`, `triage`, `code-review`, and `wayfinder`, all of which say "run `/setup-denali-skills` if not" verbatim): every one of those, both READMEs, `plugin.json`, `CONTEXT.md`, `.agents/install-block.md`, `.agents/writing-docs.md`, `ask-claude`'s routing, and both live `.out-of-scope/` entries updated. `CHANGELOG.md` and ADR 0001's own historical narrative keep the old name, since they describe what was true at the time. Reinstall under the new name; the old name is gone (no alias).

### Patch Changes

- [`ec901a6`](https://github.com/DenaliAI-Automation/Denali-Skills-DEV/commit/ec901a657cb703176cb52e96e5e5949e1c67c099) Thanks [@DAI-DLybeck](https://github.com/DAI-DLybeck)! - Remove **`git-guardrails-claude-code`** from `skills/misc/`. It was never in the Claude Code plugin, but it was installable through [skills.sh](https://skills.sh/mattpocock/skills), so this is what leaves that listing.

  Superseded by **`/personal-git-workflow`** (added in a separate changeset), which carries the same idea — a `PreToolUse` hook blocking dangerous git commands before they run — and matches this skill's full blocked-pattern list (`git reset --hard`, force `git clean`, `git branch -D`, `git checkout .`/`git restore .`), plus the push/PR case, scoped more precisely there: it only blocks pushes/PRs that actually target `main`, not every `git push` (deliberate — the new skill's own policy is that dev/feature pushes are fine for an agent to do on its own). Needs nothing beyond Python's standard library (the old hook depended on `jq`), and ships at the plugin root automatically instead of requiring a per-repo "copy this script and edit your settings.json" setup step.

  `skills/misc/` is otherwise unchanged.

## 1.2.3

### Patch Changes

- [#779](https://github.com/mattpocock/skills/pull/779) [`efce423`](https://github.com/mattpocock/skills/commit/efce423018fc6468a3239621f1c1bcaacc723801) Thanks [@mattpocock](https://github.com/mattpocock)! - Make `diagnosing-bugs` redact secrets.

  - Add a **Redact** section to `SKILL.md`. The skill has the agent show commands, outputs and captured artifacts; the section makes redaction the first move on each — write `<REDACTED>`, build loops against env vars so the credential stays in the environment, and quote only the signal-carrying lines of a captured artifact.
  - The Phase 1 completion criterion said "paste the invocation and its output". It now says show it redacted, and Phase 1 asks the user for a **redacted** captured artifact.
  - Note in `scripts/hitl-loop.template.sh` that `capture` prints its value back to the terminal, so it takes observations while signing in stays a `step`.

- [#781](https://github.com/mattpocock/skills/pull/781) [`14bfbbd`](https://github.com/mattpocock/skills/commit/14bfbbd8654a8d2910299e1a004c19c1979687d8) Thanks [@mattpocock](https://github.com/mattpocock)! - Drop Claude Code's tool and agent-type names from the subagent-dispatch instructions in `code-review`, `codebase-design`, and `improve-codebase-architecture`, so the step is followable on Codex and other harnesses.

- [#783](https://github.com/mattpocock/skills/pull/783) [`c0fd1e9`](https://github.com/mattpocock/skills/commit/c0fd1e973e040347d424e09934099f1bd6c2dee0) Thanks [@mattpocock](https://github.com/mattpocock)! - wizard: remove the time estimate. The template drops `TOTAL_MINUTES` and the time-remaining display, `stage` takes a name only, and progress is counted in stages.

## 1.2.2

### Patch Changes

- [#766](https://github.com/mattpocock/skills/pull/766) [`4aaccb5`](https://github.com/mattpocock/skills/commit/4aaccb58d40559d7e3c59a029b2290ae5ba538de) Thanks [@mattpocock](https://github.com/mattpocock)! - Make `writing-for-agents` model-invokable in Codex again.

  - Drop `policy.allow_implicit_invocation: false` from `agents/openai.yaml`. Codex filtered the skill out of the model-visible skills list, so its description could not trigger it — only an explicit `$writing-for-agents` mention worked.
  - Update the stale `interface.display_name` and `interface.short_description`, which still named the old `writing-great-skills` skill.
  - Move the skill from the **User-invoked** list to the **Model-invoked** list in `README.md` and `skills/productivity/README.md`.

## 1.2.0

### Minor Changes

- [#551](https://github.com/mattpocock/skills/pull/551) [`697d4ce`](https://github.com/mattpocock/skills/commit/697d4ce9742da558fd1ba6697c8e9775e2e302dd) Thanks [@mattpocock](https://github.com/mattpocock)! - Add Codex metadata alongside each skill's Claude Code frontmatter so the set works in both harnesses without generated copies.

  - Add an `agents/openai.yaml` beside every `SKILL.md` with Codex UI metadata (`interface.display_name`, `interface.short_description`).
  - Mark every user-invoked skill with `policy.allow_implicit_invocation: false`, the Codex analog of `disable-model-invocation: true`, so Codex excludes it from implicit invocation while explicit `$skill` invocation still works.
  - Document the dual-harness invocation model in `.agents/invocation.md`, `CLAUDE.md`, and the promoted-bucket READMEs.
  - Add `AGENTS.md` as a symlink to `CLAUDE.md` so Codex reads the same repo instructions.

- [#593](https://github.com/mattpocock/skills/pull/593) [`0f2bdbd`](https://github.com/mattpocock/skills/commit/0f2bdbdb06220d2df3718b8f0483157c6c8a8600) Thanks [@mattpocock](https://github.com/mattpocock)! - Graduate **`to-questionnaire`** out of `in-progress/` into the **Productivity** bucket, so it ships in the plugin. It turns a decision you can't answer alone into a Markdown questionnaire for the one person who can — filled in async, or worked through together in a meeting.

  Its defining move is that it grills you about the **send**, not the subject: a normal grilling session interrogates the topic, which is exactly what you can't answer here, so the interview asks only who the questionnaire is going to and what you need back, then aims every question at the gap between the two.

  Now wired as a promoted skill — plugin entry, top-level + Productivity READMEs under **User-invoked**, a docs page at `docs/productivity/to-questionnaire.md`, and a Standalone route in `ask-matt` framing it as the inverse of `/grill-me` (mine someone else, not yourself).

- [#680](https://github.com/mattpocock/skills/pull/680) [`b3376f8`](https://github.com/mattpocock/skills/commit/b3376f8d39848dd08572ec2667da4739a67c8c04) Thanks [@mattpocock](https://github.com/mattpocock)! - Graduate **`wizard`** out of `in-progress/` into the **Engineering** bucket, so it ships in the plugin — and make it model-invoked. It generates an interactive bash script that walks a human through a manual procedure — third-party setup, a one-off migration, an A→B state transition — opening each URL, saying what to click, capturing the values, and writing them into `.env` files and GitHub Actions secrets.

  The delightful UX is pre-solved by the bundled `template.sh` (progress with time-remaining, confirmation gates, cross-platform URL opening including WSL, hidden secret entry, idempotent `.env` upserts, `gh secret`/`gh variable` writes with graceful degradation, closing skip summary). Everything above the `STAGES` marker is a fixed library that's never hand-edited — the skill's job is only to scope the procedure and author its **stages**.

  Engineering rather than Productivity: it reads `.env*`, `docker-compose*`, framework config and every `secrets.*`/`vars.*` reference in `.github/workflows/` to scope itself, writes CI secrets, and verifies its output with `bash -n` and `shellcheck`.

  Because it is model-invoked, the agent can reach for it the moment it hits a step only a human can perform, instead of dumping numbered instructions into the chat and hoping you follow them. Typing `/wizard` works exactly as before — model-invocation only ever _adds_ the agent's reach. The description is written as the pointer that decides when it fires: what it produces, four trigger branches (provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, a one-off migration or cutover), and an explicit non-trigger — don't invoke it for steps the agent can perform itself. Work an agent can do, an agent should do; the wizard is for the clicks, approvals and dashboard trips you would not hand to one. The stage-list confirmation before a line is written now doubles as the proposal when the agent fires it mid-build.

  Now wired as a promoted skill — plugin entry, top-level + Engineering READMEs under **Model-invoked**, a docs page at `docs/engineering/wizard.md`, and a Standalone route in `ask-matt` for the steps only a human can take. Model-invocation also puts it out of the reach of [#693](https://github.com/mattpocock/skills/issues/693), which drops user-invoked skills from the listing on Claude's desktop and web surfaces.

- [#763](https://github.com/mattpocock/skills/pull/763) [`77d207e`](https://github.com/mattpocock/skills/commit/77d207ef03219cc603e2832e1159cbdd1c91818e) Thanks [@mattpocock](https://github.com/mattpocock)! - Reshape the **`prototype`** skill around two ideas: the demo is **a single shareable HTML file**, and the prototype is **a primary source**.

  The logic branch now produces one self-contained file (plain HTML/CSS/JS, no build, no server) instead of a terminal app — a non-developer can open it by double-click and drive it in their own domain language: a labelled state panel, always-available free-play buttons, and a set of tabbed **guided walkthroughs**, each a scenario with the ordered buttons to press underneath it. The portable pure-logic module still lifts into the real code; the HTML shell is the throwaway.

  Throwaway no longer means deleted. Rather than being removed once it has answered its question, the prototype is captured as runnable evidence on a throwaway branch (`prototype/<name>`) out of main, with a context pointer to it left on the implementation issue — so the main branch keeps only the validated decision while the exploration stays findable. The answer (verdict + question) is still captured durably in an issue/ADR/commit.

- [#536](https://github.com/mattpocock/skills/pull/536) [`42a5b70`](https://github.com/mattpocock/skills/commit/42a5b70fcacc7baff1977b13f3919fb2f63af14e) Thanks [@mattpocock](https://github.com/mattpocock)! - Ship the skill set as a native **Claude Code plugin**, listed in Claude Code's official marketplace. You can now subscribe to the promoted skills as a managed, read-only bundle instead of copying editable files:

  ```bash
  claude plugins install mattpocock-skills
  ```

  Or, from inside a session:

  ```
  /plugin install mattpocock-skills
  ```

  There is no marketplace to add first — the official marketplace is configured by default.

  `.claude-plugin/plugin.json` carries the full plugin metadata (version, description, author, license, keywords) and the explicit list of promoted skills. `skills.sh` remains the universal installer (and the path for Codex and other harnesses today); a native Codex plugin is deferred — see `.agents/adr/0002-ship-as-a-claude-code-plugin.md` for why.

- [#751](https://github.com/mattpocock/skills/pull/751) [`355fa74`](https://github.com/mattpocock/skills/commit/355fa7420b418af838998f7ec4365ceda1c8dfcc) Thanks [@mattpocock](https://github.com/mattpocock)! - Add **`wait-what`** — a one-word corrective for model verbosity. Type it the moment a message doesn't land, and the agent re-pitches it: a little context, ASD-STE100 Simplified Technical English, and the ubiquitous language from your `CONTEXT.md`. User-invoked, three lines long.

  The mechanism is the name. Concision skills fail by growing — a 400-line skill still leaves the model verbose — so this one is a single precise leading word and nothing else. Names that describe the _output_ (`/tldr`, `/no-fluff`) make the model clip words and lose you further; naming the _listener's_ state asks for both halves at once, fewer words **and** the context you were missing. It also reuses the leading words already in your global `CLAUDE.md`, so the skill, `CLAUDE.md` and every `CONTEXT.md` reach for the same tokens.

  It repairs one message; it doesn't prevent the next one. The cure for jargon is a shared language built upfront with `/grill-with-docs`; this is what you reach for when you don't have one yet.

- [#763](https://github.com/mattpocock/skills/pull/763) [`77d207e`](https://github.com/mattpocock/skills/commit/77d207ef03219cc603e2832e1159cbdd1c91818e) Thanks [@mattpocock](https://github.com/mattpocock)! - Name the `/wayfinder` unit a **decision ticket**, and burn research tickets down with subagents.

  People kept reading a wayfinder ticket as an ordinary _implementation_ ticket — a slice of a build to execute — when wayfinder uses them as **decision tickets**: questions whose resolution is a decision. The skill description and its opening line now introduce the term (and say what makes it one), with the `ask-matt` / engineering README blurbs and the docs page matching — while "ticket" stays the everyday word once the term is established. `CONTEXT.md` records **Decision ticket** as a domain term, so the "avoid: ticket" guidance no longer contradicts wayfinder's deliberate use of the word.

  Research tickets are no longer parked for a separately-launched session. Research stays a real ticket type — it's a genuine shared blocker that downstream decisions hang on, and that dependency is exactly what the frontier's blocking edges exist to render. What changes is how it's resolved: because research is AFK, charting doesn't stop and read it. After creating the tickets, the charting session fires a `/research` subagent for each research ticket to burn it down in parallel, capturing the findings on a throwaway `research/<name>` branch with a context pointer. Research tickets are the one exception to _one ticket per session_.

- [#763](https://github.com/mattpocock/skills/pull/763) [`77d207e`](https://github.com/mattpocock/skills/commit/77d207ef03219cc603e2832e1159cbdd1c91818e) Thanks [@mattpocock](https://github.com/mattpocock)! - **Breaking:** rename **`writing-great-skills`** → **`writing-for-agents`**, restructure it, and add a new leading word.

  The reference now covers any document an agent consumes — skills, `AGENTS.md` / `CLAUDE.md`, docs reached by a pointer — not just skills. `GLOSSARY.md` is merged into `SKILL.md` (one authoritative treatment per term; the `_Avoid_` synonym lists and the standalone Predictability definition are gone); the skill-only mechanics (frontmatter, model- vs user-invoked, router skills, the invocation cut of splitting) are disclosed to a new `SKILL-MECHANICS.md`. The skill is now **model-invoked**: it fires when creating or editing skills or modifying `AGENTS.md`/`CLAUDE.md`. `ask-matt`'s pointer updated. Reinstall under the new name; the old name is gone (no alias).

  The pruning section gains **cache**. Single source of truth now reaches past the document into the environment — `package.json` scripts, config files, directory layout, `--help` output are themselves authoritative, so a doc that restates them is a cache of a lookup, earning its load only when the lookup is expensive. The positive target: cache what the agent cannot find by looking (unwritten conventions, the reason behind a choice, gotchas no config confesses), and leave one-file, one-command lookups to the environment, where they cannot go stale.

- [#533](https://github.com/mattpocock/skills/pull/533) [`45afd80`](https://github.com/mattpocock/skills/commit/45afd8074a8b7de5fe073845d080fa9dd6c429fa) Thanks [@mattpocock](https://github.com/mattpocock)! - Add a YAGNI scoping filter to the **`improve-codebase-architecture`** skill's Explore step. Instead of scanning the whole repo evenly, it now scopes to where change is actually landing: if you name a direction it takes it, otherwise it reads the last ~20 commit messages to bias exploration toward actively-developed paths. A deepening opportunity in code nobody touches is a refactor you'll never cash in — the leverage only pays off where you keep editing — so the report stops tidying dormant corners of the repo.

### Patch Changes

- [#763](https://github.com/mattpocock/skills/pull/763) [`77d207e`](https://github.com/mattpocock/skills/commit/77d207ef03219cc603e2832e1159cbdd1c91818e) Thanks [@mattpocock](https://github.com/mattpocock)! - Sharpen `/ask-matt` — the router now covers phase boundaries, the two wayfinder mistakes, and two skills it never mentioned.

  **Phase boundaries.** A **phase** is a chunk of work inside a session — the grilling, the implementation, the QA — and the boundary between two of them is where you decide what to do with the context you've built. The two-bullet `Crossing sessions` section is replaced by a decision tree carrying all five options in order (**continue**, `/clear`, `/handoff`, **subagent**, `/compact`), with the reasoning disclosed in a new `PHASE-BOUNDARIES.md`. Three fixes come with it:

  - **`/handoff` was oversold.** It read as the general bridge between context windows. It's narrow: you need it only when something has to _travel_ — a new harness, a new directory, a colleague, or a side task forked mid-phase. What it buys is portability.
  - **`/compact` is the default, not the first reach.** It sits at the bottom of the tree, after the four cheaper or more precise questions above it. Starting there produces a session that's confidently wrong about whatever the summary flattened.
  - **Two branches were missing entirely.** **Continue** is the one to rule out first — it's the only move that keeps the conversation as a primary source rather than a summary of one — and a **subagent** handles anything scoped tightly enough to run AFK.

  Context hygiene's escape hatch now says `/compact` rather than `/handoff` (same harness, same directory, at a boundary — the handoff clause doesn't apply), and the smart zone figure is updated from ~120k to ~150k tokens.

  **Wayfinder routing.** The two mistakes people most often make with the heaviest, most cognitively demanding flow:

  - **Over-reaching for it.** It's slower and denser than a single grill, so it's flagged as the heaviest flow and reserved for the idea that genuinely won't fit one session — a well-scoped feature belongs on `/grill-with-docs`, not here.
  - **Losing the way at the handoff.** When the map clears, wayfinder hands off, it doesn't build: merge onto the main flow at `/to-spec` (which collapses the map's linked decisions into a buildable plan) rather than looping the map straight into `/implement`. Straight-to-`/implement` is only for efforts that turned out genuinely small.

  **Missing routes.** `/grilling` and `/resolving-merge-conflicts` were absent from the router altogether and are now in it, and `grill-me` splits from `grill-with-docs` on whether you are in a working directory.

- [#502](https://github.com/mattpocock/skills/pull/502) [`44eed54`](https://github.com/mattpocock/skills/commit/44eed545186ffd0263e8004867750b80cfddd215) Thanks [@mattpocock](https://github.com/mattpocock)! - Make `/setup-matt-pocock-skills` friendlier and align the local-markdown tracker with the current spec.

  - **Triage labels** are now asked about only when the `triage` skill is installed, and then as a single recommended-yes question ("keep the default triage labels?") instead of an override interrogation. When `triage` isn't installed, the section — and `docs/agents/triage-labels.md` — are skipped.
  - **External PRs as a request surface** is no longer a setup question. The GitHub/GitLab templates still carry the flag, defaulted off; a user can flip it in `docs/agents/issue-tracker.md` later.
  - **Domain docs** default to single-context without asking; multi-context is only offered when the repo shows monorepo signals.
  - **Local-markdown tickets** are now one file per ticket under `.scratch/<feature>/issues/<NN>-<slug>.md` — never a single combined `tickets.md`. `/to-tickets` and the local issue-tracker template now agree, and the spec file is `spec.md` (not `PRD.md`) to match `/to-spec`.

  Docs pages for `setup-matt-pocock-skills` and `to-tickets` re-synced.

- [#532](https://github.com/mattpocock/skills/pull/532) [`170ad48`](https://github.com/mattpocock/skills/commit/170ad48655825783d0193e850e31a9aac957bb95) Thanks [@mattpocock](https://github.com/mattpocock)! - Reword **`grilling`** for general use. Its description and body no longer scope the interview to a software plan: "this plan" → "this", "enact the plan" → "act on it", and "exploring the codebase" → "exploring the environment". The technique is unchanged; it now reads as a stress-test of any plan, decision, or idea.

- [#593](https://github.com/mattpocock/skills/pull/593) [`a4b2009`](https://github.com/mattpocock/skills/commit/a4b2009a1a3ac9575506c10b4c84f08f9bba7a38) Thanks [@mattpocock](https://github.com/mattpocock)! - Rework **`grilling`** from one-question-at-a-time to round-by-round. It now maps the decision tree and asks the whole **frontier** — every question whose prerequisites are already settled — in a single numbered round, then recomputes the frontier from the user's answers and asks the next round. Same 13 questions land in ~3 rounds instead of 13. Facts the environment can answer are dispatched to background sub-agents so research never blocks the round: only questions downstream of a running exploration wait for it. The session ends when the frontier is empty.

  Every question in a round is emitted in one fixed shape — `❓ **Q1** - **<title>**`, then the body (prose or multiple choices), then the recommendation on its own `➡️` line. A round reads as a scannable numbered list with each recommendation visually separated from the question, so you can answer by number instead of quoting questions back.

  `grill-me`, `grill-with-docs` and `triage` run the frontier a round at a time as well — `triage`'s grill step and `grilling`'s Codex `short_description` now say so instead of describing the old rhythm. The opt-out for one-question-at-a-time (a line in your global `CLAUDE.md`) is unchanged.

- [#752](https://github.com/mattpocock/skills/pull/752) [`c66bdee`](https://github.com/mattpocock/skills/commit/c66bdeeee002d81e3f8b21403c07f9a0d7bea6da) Thanks [@mattpocock](https://github.com/mattpocock)! - Remove six skills from the repo. None of them was in the Claude Code plugin, but all six were installable through [skills.sh](https://skills.sh/mattpocock/skills), which serves every skill in the repo — so this is what leaves that listing, and where each one went.

  Four retired skills, each already absorbed by a skill that does the job better:

  - **`ubiquitous-language`** → **`/domain-modeling`**, which builds and maintains the whole domain model rather than dumping a glossary from one conversation.
  - **`design-an-interface`** → **`/codebase-design`**. Nothing is lost: the "design it twice" technique — parallel sub-agents generating radically different designs, from Ousterhout — ships inside that skill as `DESIGN-IT-TWICE.md`.
  - **`qa`** → **`/triage`** and **`/to-tickets`**.
  - **`request-refactor-plan`** → **`/to-spec`** and **`/improve-codebase-architecture`**.

  And two that were only ever mine — tied to my own machine and never meant for anyone else. The `personal/` bucket goes with them:

  - **`edit-article`**
  - **`obsidian-vault`**, which hardcoded a path to my own Obsidian vault.

  `skills/deprecated/` stays as a bucket, now empty. `skills/in-progress/` is unchanged and is now described for what it actually is: a beta channel, published on purpose, installable one skill at a time through skills.sh.

- [#734](https://github.com/mattpocock/skills/pull/734) [`a2f9333`](https://github.com/mattpocock/skills/commit/a2f9333669ff53db762c87ecda5a15442060a3be) Thanks [@mattpocock](https://github.com/mattpocock)! - Finish the `to-prd` → `to-spec` rename: "spec" is now the only term in the shipped text.

  - **`to-spec`** no longer opens with "you may know this document as a PRD" — the parenthetical is dropped from the skill and its docs page. The local-markdown tracker template drops the same hedge.
  - **`code-review`** talks about the originating issue/spec rather than issue/PRD, in its frontmatter description, its two-axis summary, and the spec-source search order. Both READMEs re-synced.
  - **The GitHub and GitLab tracker templates** now say "Issues and specs for this repo live as GitHub/GitLab issues" — they had been left on "PRDs" when the local template was updated, so the stale term propagated into every repo they were written into.
  - **`docs/engineering/research.md`** pointed at `https://aihero.dev/skills-to-prd`, a dead slug for the renamed skill; it now links `to-spec` like the other nineteen docs pages do.

  The CHANGELOG and existing changesets still name PRDs where they document the rename itself, which is correct.

## 1.1.0

### Minor Changes

- [#406](https://github.com/mattpocock/skills/pull/406) [`930a450`](https://github.com/mattpocock/skills/commit/930a450089f77a49af09001d955db8452a4b867d) Thanks [@mattpocock](https://github.com/mattpocock)! - Bring the **`ask-matt`** router up to date with the full skill set. It now maps five skills it was missing: **`tdd`** (woven into the main flow as the red-green engine `implement` drives), **`diagnosing-bugs`** (a new "Something's broken" on-ramp — there was previously no route for a bug), **`domain-modeling`** and **`codebase-design`** (a new "Vocabulary underneath" section), and **`grilling`** (the shared interview primitive). `prototype` is fleshed out as a standalone and the description broadens from "user-invoked skills" to "the skills". A maintenance rule is added to `CLAUDE.md` so any future skill add/rename/remove or flow change triggers an `ask-matt` re-check, beside the existing docs-page re-sync rule.

- [#464](https://github.com/mattpocock/skills/pull/464) [`639df6e`](https://github.com/mattpocock/skills/commit/639df6e7386dfddc739b2aecdeff37a876f2483b) Thanks [@mattpocock](https://github.com/mattpocock)! - Promote and harden **`code-review`**. The in-progress **`review`** skill is renamed to **`code-review`** and moved from `in-progress/` into `engineering/`: it now ships in the plugin, is listed in the top-level and Engineering READMEs (Model-invoked), and has a docs page at `docs/engineering/code-review.md`. The `/implement` skill and docs point at `/code-review`.

  It also gains an always-on **Fowler smell baseline** on its Standards axis — a curated ~12 high-signal "Bad Smells in Code" (Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest) inlined into `SKILL.md` as a fixed baseline alongside whatever the repo documents, not a new third axis. Two binding rules keep it safe: a documented repo standard overrides the baseline, and every smell is reported as a judgement call, never a hard violation.

- [#464](https://github.com/mattpocock/skills/pull/464) [`639df6e`](https://github.com/mattpocock/skills/commit/639df6e7386dfddc739b2aecdeff37a876f2483b) Thanks [@mattpocock](https://github.com/mattpocock)! - Sharpen **`grilling`** on two fronts.

  **A confirmation gate.** The agent won't enact the plan until you confirm the shared understanding has been reached — turning the skill's existing "shared understanding" completion criterion into an explicit stop-gate. The `description` also recruits the pretrained **`grill`** leading word ("Grill the user relentlessly") to sharpen invocation, and the docs page is re-synced.

  **Facts vs. decisions.** Grilling now splits _facts_ (look them up — explore the codebase) from _decisions_ (put each one to the human and wait for their answer). The old blanket line — "if a question can be answered by exploring the codebase, explore the codebase instead" — was written for the live-human case, but once another skill runs grilling inside a resolve-the-ticket frame it read as license to answer _decisions_ autonomously too. Separating the two keeps a grilling agent from racing ahead and answering its own questions.

- [#463](https://github.com/mattpocock/skills/pull/463) [`af6d692`](https://github.com/mattpocock/skills/commit/af6d6922c3e2b5288eef155346cbe319e4ed3bd0) Thanks [@mattpocock](https://github.com/mattpocock)! - Add two adjacent Steering failure modes to **`writing-great-skills`**, both about how language you think of as "off" still steers the agent. **Negation** — the _elephant_ — is steering by prohibition: naming what _not_ to do drags the forbidden behaviour into context and makes it _more_ available, not less (_don't think of an elephant_), so the cure is to prompt the **positive**. **Negative Space** — the void — is blindness to the steering done by what you leave _out_: every decision a skill declines is delegated to the agent's priors rather than left neutral, so the cure is to read a draft for its silences and decide each omission deliberately (fill it, or leave it open as a real **branch**). Kept as two entries, not one — they carry different diagnostics and different cures — each a full `GLOSSARY.md` entry plus a `SKILL.md` failure-mode bullet, matching how every other failure mode is carried.

- [`850873c`](https://github.com/mattpocock/skills/commit/850873cd73d5f81826ebf512ad35d2b1e113001f) Thanks [@mattpocock](https://github.com/mattpocock)! - Make the **`prototype`** skill model-invoked, so the agent can reach for it autonomously (and other skills can too). Its description is rewritten around the leading word _prototype_ — throwaway code that answers a design question — with one trigger per branch (state/logic sanity-check, or UI exploration).

- [#409](https://github.com/mattpocock/skills/pull/409) [`0d74d01`](https://github.com/mattpocock/skills/commit/0d74d01cbc64ca27778a49b38599f70c534e76a0) Thanks [@mattpocock](https://github.com/mattpocock)! - Add the **`research`** skill — a small, model-invoked skill that spins up a **background agent** to investigate a question against **primary sources** (official docs, source code, specs, first-party APIs), then leaves a single cited Markdown file wherever the repo keeps such notes. It's delegable reading legwork: you keep working while it reads, and get back a document to grill, plan, or design against. Listed in the top-level and Engineering READMEs (Model-invoked), added to `.claude-plugin/plugin.json`, given a docs page at `docs/engineering/research.md`, and routed as a Standalone in `ask-matt`.

- [#469](https://github.com/mattpocock/skills/pull/469) [`a0329ba`](https://github.com/mattpocock/skills/commit/a0329ba95751f58566ed7ab484475917a68f1629) Thanks [@mattpocock](https://github.com/mattpocock)! - Split the **`to-issues`** skill into a lean **Process** and a **Reference** section, and teach it to handle a **wide refactor** — a single mechanical change (like renaming a column) whose **blast radius** fans across the whole codebase, breaking thousands of call sites at once so no vertical slice can land green. The drafting step now points at two co-located reference blocks: the **Vertical slice rules** for ordinary tracer bullets, and **Wide refactors**, which slices the change by **expand–contract** (expand the new form beside the old, migrate call sites in batches sized by blast radius, then contract the old form away) so CI stays green batch to batch — or, when it can't, only at a final integrate-and-verify issue. The issue body template moves into Reference too.

- [#464](https://github.com/mattpocock/skills/pull/464) [`386d4ff`](https://github.com/mattpocock/skills/commit/386d4ff719a7c420ad1454232d0436b01f1b8c17) Thanks [@mattpocock](https://github.com/mattpocock)! - Unify the planning skills. **`to-prd` is renamed to `to-spec`** — "spec" is now the single through-line term (it still opens with "you may know this document as a PRD" for discoverability). **`to-plan` and `to-issues` are merged into one `to-tickets` skill, and `to-issues` is deleted.**

  `to-tickets` breaks a plan, spec, or conversation into a set of **tickets** — tracer-bullet vertical slices, each declaring its **blocking edges**. That one artifact reads two ways depending on the tracker `/setup-matt-pocock-skills` configured: a **local file** (`tickets.md`) writes the edges as text and you work it top-to-bottom by hand; a **real tracker** writes them as native blocking links, so any ticket whose blockers are done is on the frontier and several agents can run at once. The edges live in the ticket either way — the medium only decides whether anything acts on them in parallel.

  Publishing prefers the tracker's **native sub-issues** for parent → slice and **native blocking edges** for `Blocked by` where the tracker supports them, keeping the `## Parent` / `## Blocked by` body sections as the fallback. The "What to build" template points at where a `/prototype`'s code lives rather than inlining a snippet from it.

  `ask-matt`'s main flow now routes `idea → /to-spec → /to-tickets → /implement`, and there are human-facing docs pages at `docs/engineering/to-spec.md` and `docs/engineering/to-tickets.md`.

- [#464](https://github.com/mattpocock/skills/pull/464) [`0557d57`](https://github.com/mattpocock/skills/commit/0557d57579d9b3d39839fdaf8d4a6542b17539ce) Thanks [@mattpocock](https://github.com/mattpocock)! - Settle wayfinder's place in the docs as a **situational on-ramp**, not the new main entry flow — the grill-led _idea → ship_ chain stays the front door (crowning wayfinder as the default spine is a v2-sized move, not a 1.1). The **`ask-matt`** router now names wayfinder's concrete triggers — a greenfield project or a huge feature build, too big for one session — and the two grill front doors (**`grill-me`**, **`grill-with-docs`**) signpost _up_ to wayfinder for the effort that's too big to hold in one session, so the on-ramp is discoverable from where a reader actually starts.

- [#464](https://github.com/mattpocock/skills/pull/464) [`639df6e`](https://github.com/mattpocock/skills/commit/639df6e7386dfddc739b2aecdeff37a876f2483b) Thanks [@mattpocock](https://github.com/mattpocock)! - Graduate and reframe **`wayfinder`** — the skill for planning a huge chunk of work, more than one agent session can hold. It moves out of `in-progress/` into `engineering/` (plugin entry, top-level + Engineering READMEs under **User-invoked**, a docs page at `docs/engineering/wayfinder.md`, and a route in `ask-matt`), landing as a mature skill. The rename and reframe that got it there:

  - **`decision-mapping` is renamed to `wayfinder`**, invoked as `/wayfinder`. "Decision map" was jargony and inaccurate — only one ticket type is actually a decision. The reframe charts a route through a foggy problem instead, giving one coherent leading-word frame — **fog of war**, **frontier**, **the map** — rather than an invented term layered on top.
  - **Destination as the leading word.** Wayfinding finds the _way_ to a destination; it doesn't charge at building it. Naming the destination is the first act of charting — it fixes the scope and shapes every ticket — so the map gains a `## Destination` field every session orients to, and triage pins it before any ticket exists.
  - **Plan, don't do.** The map produces **decisions, not deliverables**; it's done when nothing is left to decide before someone builds the thing. An effort can override this in its Notes.
  - **The map is an index, not a store.** A decision lives in exactly one place — its ticket — so the map only gists and links, never restates; graduating fog into a ticket clears the graduated patch so nothing lingers in two places.
  - **Collaborative by default.** The map moves off a local Markdown file onto the repo's issue tracker: a single `wayfinder:map` issue whose tickets are its child issues — one shared URL the team can watch. Sessions load the map at low resolution and zoom into tickets on demand. Wayfinder stays tracker-agnostic (GitHub, GitLab, local-markdown) behind a pointer in `docs/agents/issue-tracker.md`, and `setup-matt-pocock-skills` seeds the "Wayfinding operations" section.
  - **Claim by assignment, not a label.** A session claims a ticket by assigning it to the driving dev — the assignee _is_ the claim — freeing the label vocabulary to `wayfinder:<type>` alone.
  - **Native blocking.** Blocking prefers the tracker's native dependency relationship, which renders the frontier visually in the tracker's own UI so the human sees what's takeable without opening the map. GitHub and GitLab templates spell out the native recipe, with a body-convention fallback.
  - **Fog vs. out of scope, split.** Two plainly-named map sections — `## Not yet specified` (in-scope fog that graduates as the frontier advances) and `## Out of scope` (work ruled beyond the destination, closed, never graduating) — so beyond-destination work no longer reads as takeable frontier.
  - **A fourth `task` ticket type.** For literal manual work that blocks a decision (provisioning access, moving data, signing up for a service) — the one type that _does_ rather than decides, earning its place by unblocking a decision.
  - **HITL / AFK ticket classification.** Every ticket type is **HITL** (human in the loop — grilling, prototype) or **AFK** (agent alone — research; task is either). A HITL ticket only resolves through the live exchange, so "wait for the human" falls out of the label — a grilling agent that answers its own questions has, by definition, broken HITL. (This fixes students' reports of `/wayfinder` grilling _itself_ instead of the human.)
  - **No-fog early exit restored.** If the opening breadth-first grilling surfaces no fog, the journey is small enough for one session — so it stops and asks how you'd like to proceed rather than building a map nobody needs.

### Patch Changes

- [#464](https://github.com/mattpocock/skills/pull/464) [`639df6e`](https://github.com/mattpocock/skills/commit/639df6e7386dfddc739b2aecdeff37a876f2483b) Thanks [@mattpocock](https://github.com/mattpocock)! - Reshape **`tdd`** into a reference-only skill and add a missing anti-pattern.

  **Reference-only.** The red → green → refactor loop is anchored by leading words the model already holds, so the step-by-step Workflow was largely restating the loop. Dropped the Workflow and per-cycle checklist; folded their one durable idea — vertical slices / tracer bullets — into the Anti-patterns section and a short Rules-of-the-loop list. Introduced **seam** as the leading word for where tests go: test only at pre-agreed seams, confirmed with the user before any test is written. Also dropped the refactor stage — TDD is now red → green; refactoring belongs to the review stage, so the refactor rule and `refactoring.md` moved out (its home is `code-review`).

  **Tautological tests.** Added the tautological-test anti-pattern: a test whose assertion is recomputed the way the code computes it passes by construction and gives zero confidence — distinct from the implementation-coupling anti-pattern already covered. Added as a peer at the same sites: a Philosophy principle (expected values must come from an independent source of truth), a checklist gate, and a BAD/GOOD example pair in `tests.md`.

- [`e00eadb`](https://github.com/mattpocock/skills/commit/e00eadb4bb32c3d5a631ead1a5ed5d6a7c5f74e2) Thanks [@mattpocock](https://github.com/mattpocock)! - Extend the **`triage`** skill to triage external pull requests, treating a PR as an issue with attached code that runs through the same roles and state machine. PRs flow inline alongside issues (gated by a per-repo setup toggle), discovery surfaces only external PRs, the bug-only "reproduce" step is generalized into a single "verify the claim" step, and a redundancy check resolves already-implemented requests to `wontfix` without polluting the out-of-scope knowledge base. `setup-matt-pocock-skills` gains the PRs-as-a-request-surface toggle for GitHub/GitLab.

- [#472](https://github.com/mattpocock/skills/pull/472) [`d869d45`](https://github.com/mattpocock/skills/commit/d869d45afc32beab1c2d1350f8de5e81589512cd) Thanks [@mattpocock](https://github.com/mattpocock)! - Fix **`wayfinder`** hardcoding the issue-tracker doc path, which broke the indirection the rest of the suite relies on.

  `to-issues`, `to-prd`, and `triage` never name a path — they resolve the tracker through the `### Issue tracker` block that `setup-matt-pocock-skills` writes into `CLAUDE.md` / `AGENTS.md`, which points at the tracker doc wherever it lives. Wayfinder instead pinned the literal `docs/agents/issue-tracker.md`, so in a repo that keeps its agent docs elsewhere it silently fell back to the local-markdown tracker — even one whose `CLAUDE.md` clearly declares GitHub issues. It now resolves the doc via that same pointer and reads its "Wayfinding operations" section by name, keeping the indirection consistent across the suite.

## 1.0.1

### Patch Changes

- [`d20ee26`](https://github.com/mattpocock/skills/commit/d20ee2684e2a9442698ac3c1e0f2c5b68c4cf296) Thanks [@mattpocock](https://github.com/mattpocock)! - Make the **`teach`** skill reuse-first. Lessons are now built from reusable **components** in `./assets/` — stylesheets, quiz widgets, simulators, diagram helpers. Reuse is the default: the agent reads `./assets/` before authoring a lesson, builds from what's there, and extracts anything new and reusable into a component rather than inlining it.

## 1.0.0

### Major Changes

- [`47bde84`](https://github.com/mattpocock/skills/commit/47bde84da032afb2e5058f997f3bbca47d321dbd) Thanks [@mattpocock](https://github.com/mattpocock)! - Add the **`ask-matt`** skill — a user-invoked router that points you at the right skill or flow for your situation.

  **Breaking:** `ask-matt` routes over the other user-invoked skills in this repo, so it expects them to be installed.

- [`47bde84`](https://github.com/mattpocock/skills/commit/47bde84da032afb2e5058f997f3bbca47d321dbd) Thanks [@mattpocock](https://github.com/mattpocock)! - Add the shared design skills and rewire existing skills onto them.

  - New **`codebase-design`** skill — the deep-module vocabulary (module, interface, depth, seam, adapter) and the principles for putting a lot of behaviour behind a small interface. The language that previously lived in `improve-codebase-architecture/LANGUAGE.md` now lives here, generalized for reuse across skills.
  - New **`domain-modeling`** skill — actively build and sharpen a project's domain model, stress-testing terms against the glossary and keeping `CONTEXT.md` and ADRs current.
  - `improve-codebase-architecture` now draws its architecture vocabulary from `/codebase-design` and its domain model from `/domain-modeling`.
  - `tdd` now leans on `/codebase-design` for interface-design guidance — its inline `deep-modules.md` / `interface-design.md` notes were removed in favour of the shared skill.
  - `grill-with-docs` now builds the domain model inline via `/domain-modeling`.

  **Breaking:** these skills now depend on the new `codebase-design` / `domain-modeling` skills, so you must install them too.

- [`47bde84`](https://github.com/mattpocock/skills/commit/47bde84da032afb2e5058f997f3bbca47d321dbd) Thanks [@mattpocock](https://github.com/mattpocock)! - Remove the **`caveman`** and **`zoom-out`** skills.

  - `caveman` was a duplicate of another skill I was testing and was never meant to be public.
  - `zoom-out` went unused in practice, so it's been removed from the repo.

  **Breaking:** both skills have been removed.

- [`47bde84`](https://github.com/mattpocock/skills/commit/47bde84da032afb2e5058f997f3bbca47d321dbd) Thanks [@mattpocock](https://github.com/mattpocock)! - Rename the **`diagnose`** skill to **`diagnosing-bugs`**.

  **Breaking:** invoke it as `/diagnosing-bugs` — the old `/diagnose` name no longer exists.

- [`47bde84`](https://github.com/mattpocock/skills/commit/47bde84da032afb2e5058f997f3bbca47d321dbd) Thanks [@mattpocock](https://github.com/mattpocock)! - Replace **`write-a-skill`** with **`writing-great-skills`**.

  - Removed `write-a-skill`.
  - Added `writing-great-skills` (plus its `GLOSSARY.md`) — a reference for writing and editing skills well: the vocabulary and principles that make a skill predictable, hunting no-ops down to the sentence level.
  - Exposed `grilling` as a model-invoked skill — the reusable interview loop behind `grill-me` and `grill-with-docs`.

  **Breaking:** `write-a-skill` has been removed; use `writing-great-skills` instead.

### Minor Changes

- [`47bde84`](https://github.com/mattpocock/skills/commit/47bde84da032afb2e5058f997f3bbca47d321dbd) Thanks [@mattpocock](https://github.com/mattpocock)! - Add the **`resolving-merge-conflicts`** skill — a loop for resolving an in-progress git merge or rebase conflict. Standalone, with no dependencies on other skills.

- [`47bde84`](https://github.com/mattpocock/skills/commit/47bde84da032afb2e5058f997f3bbca47d321dbd) Thanks [@mattpocock](https://github.com/mattpocock)! - Rename the skill taxonomy from **Commands / Skills** to **User-invoked / Model-invoked** across the docs, and add `docs/invocation.md` defining the split: user-invoked skills are reachable only when you type them and exist to orchestrate; model-invoked skills can also be reached automatically when the task fits. A user-invoked skill may invoke model-invoked skills, but never another user-invoked one.

### Patch Changes

- [`47bde84`](https://github.com/mattpocock/skills/commit/47bde84da032afb2e5058f997f3bbca47d321dbd) Thanks [@mattpocock](https://github.com/mattpocock)! - Tighten the **`review`** skill: fail-fast ref check, single-sourced rules, and no-op cuts.
