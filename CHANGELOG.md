# david-skills

## 1.7.0

### Minor Changes

- [`7037848`](https://github.com/Dlybeck/David-Skills/commit/70378481d5dfddbf1d464e64c6d529022ca77033) Thanks [@Dlybeck](https://github.com/Dlybeck)! - Adapt question rounds to focused or brief attention, including voice-friendly intake and
  last-second handoffs. Use available host tools for sources, visuals, and previews when they
  materially help, while keeping the plugin usable across AI hosts.

- [`c5e7c2d`](https://github.com/Dlybeck/David-Skills/commit/c5e7c2de9198c0046f724e93bd146a0eeeb65e7c) Thanks [@Dlybeck](https://github.com/Dlybeck)! - Document David's development preferences; make requirements capture, ticket decomposition,
  implementation, and context handoff model-callable without expanding their authority. Preserve
  skill purposes and add human steering, correction continuity, and intent-aware status reports
  to the adaptive pilots. Add bounded pivot evaluations and explicit wait/resume capability limits;
  do not claim unattended long-job continuation is verified on every host.

- [#2](https://github.com/Dlybeck/David-Skills/pull/2) [`3133a89`](https://github.com/Dlybeck/David-Skills/commit/3133a895c6ebd8601feefb8aa1a3fc4f9a58967f) Thanks [@Dlybeck](https://github.com/Dlybeck)! - Add a fresh independent PR reviewer and an authorized developer repair/re-review loop alongside
  the existing Standards/Spec checks. Keep actionable comments pinned, clean reviews quiet, and
  main merges subject to explicit final human approval.

- [`7657c57`](https://github.com/Dlybeck/David-Skills/commit/7657c575c74829a0488c54a8953d99422a2af5d3) Thanks [@Dlybeck](https://github.com/Dlybeck)! - Add a reusable philosophy review that checks projects and proposed changes against their
  owner-adopted founding principles without turning optional practices into a mandatory workflow.

- [`f887ac9`](https://github.com/Dlybeck/David-Skills/commit/f887ac9a63bdab4f824fa0f4d246147e7de1d950) Thanks [@Dlybeck](https://github.com/Dlybeck)! - Add a model- and user-callable status-report skill connecting verified current progress to
  long-term project goals, with in-chat reports and useful visuals by default; Markdown snapshots
  and webpages are opt-in exports.

- [`4968136`](https://github.com/Dlybeck/David-Skills/commit/4968136b49b53f50c79fbbdb13554efeea6596c9) Thanks [@Dlybeck](https://github.com/Dlybeck)! - Add optional user deadlines, factual timing hooks, and milestone/maximum-gap reports to
  autonomous runs. Preserve no-polling boundaries and select tests by changed behavior and risk.

### Patch Changes

- [`19c526e`](https://github.com/Dlybeck/David-Skills/commit/19c526e8af62411b8ba42fb810e6407ca71a83d7) Thanks [@Dlybeck](https://github.com/Dlybeck)! - Ground pilot checkpoint metadata in command results. Add independent before/after Git evidence
  and separate chat-default, webpage-only, and brief-status scenarios to the opt-in evaluator.

- [`819fd0f`](https://github.com/Dlybeck/David-Skills/commit/819fd0f23320bf2a8cd4053cde5a096834e5d029) Thanks [@Dlybeck](https://github.com/Dlybeck)! - Keep skill composition user-owned: make setup conditional, reuse agreed or delegated TDD seams,
  scope interviews, avoid mandatory small-lookup delegation, and preserve diagnosis/planning-only
  authority. Clarify prototype promotion, merge staging, delegated completion, pilot checkpoints,
  and narrower user delivery boundaries. Synchronize human documentation and local sibling links.
  Harden Git guards against global-option forms that could hide a main push.
  Bound Wayfinder's research dispatch across tickets and reject invalid native runtime traces in
  the opt-in evaluator, with offline regression coverage that consumes no model usage.

- [`823b251`](https://github.com/Dlybeck/David-Skills/commit/823b2515f8eeca030bf285adfcb91d7d48babf4f) Thanks [@Dlybeck](https://github.com/Dlybeck)! - Treat routine local toolchain, dependency, and test-environment setup as part of authorized
  implementation and bug diagnosis. Reuse applicable standing grants across tasks, and ask only
  when a specific host or human-only boundary remains.

- [#3](https://github.com/Dlybeck/David-Skills/pull/3) [`f613b6a`](https://github.com/Dlybeck/David-Skills/commit/f613b6a2b3af33f1da5d5a982fde6569cd195a98) Thanks [@Dlybeck](https://github.com/Dlybeck)! - Route reviewed delivery by repository branch ownership and applicable standing grants. Complete
  authorized agent-owned integration without repeated human handoffs, retain human-owned promotion
  approval, and keep explicit restrictions and missing-authority boundaries conservative.

- [`3c9c443`](https://github.com/Dlybeck/David-Skills/commit/3c9c443f3febda3b2210759f1234a78f195f50db) Thanks [@Dlybeck](https://github.com/Dlybeck)! - Keep goals active through supported blocking waits. Distinguish quiet waiting from recurring AI
  polling, and require evidence of an actual host limitation before reporting that autonomous
  continuation is unavailable.

- [`f887ac9`](https://github.com/Dlybeck/David-Skills/commit/f887ac9a63bdab4f824fa0f4d246147e7de1d950) Thanks [@Dlybeck](https://github.com/Dlybeck)! - Include staged, unstaged, and new files in work-in-progress code reviews, and accept explicit
  requests or confirmed goal contracts as requirements evidence without mandatory tracker setup.
  Keep Autopilot's fallback review branch local unless pushing it is explicitly authorized.

## 1.6.0

### Minor Changes

- [`3e9fe8d`](https://github.com/Dlybeck/David-Skills/commit/3e9fe8dac1469721eb2a460d115ffe1d40e6c021) Thanks [@Dlybeck](https://github.com/Dlybeck)! - Port Autopilot and Yolopilot to Codex through a shared adaptive `pursue-goal` engine, ship the
  harness-neutral `advise` router in both plugins, and retire the legacy `ask-claude` name.

## 1.5.1

### Patch Changes

- [`29e21f6`](https://github.com/Dlybeck/David-Skills/commit/29e21f63b8daa669aefd645acf2ff731128c39d7) Thanks [@Dlybeck](https://github.com/Dlybeck)! - Add native Codex plugin installation, harden hook and repository validation,
  remove the obsolete `scaffold-exercises` and `setup-pre-commit` skills, and
  replace generated version pull requests with direct human-gated releases. Update
  the locked YAML parsers to patched releases.

## 1.5.0

### Personal baseline

- Publish the collection under the **David Skills** identity.
- Align the package, Claude Code plugin, marketplace, repository metadata, and installation
  commands with `Dlybeck/David-Skills` and `david-skills`.
- Preserve the MIT license and attribution to
  [Matt Pocock's original skills repository](https://github.com/mattpocock/skills).
- Keep David's personal `main ← dev ← feature/**` workflow and plugin-root safety hooks.
- Remove the work-only compliance adapter and stale rollout/session artifacts from the personal
  distribution.
