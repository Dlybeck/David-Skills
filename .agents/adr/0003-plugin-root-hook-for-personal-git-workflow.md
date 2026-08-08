# Ship personal-git-workflow's `main` guard as a plugin-root hook, not a per-repo setup skill

`personal-git-workflow`'s central rule — `main` is human-only, no agent ever pushes to it or
opens a PR into it — already failed once as prose alone, in a project using an earlier version
of this skill before it carried a hook. An instruction the agent has to remember and re-apply
correctly every session is exactly the kind of rule that quietly breaks once. It needed a
mechanical backstop, not stronger wording.

## The constraint: this repo has never shipped a plugin-level hook before

`CLAUDE.md` and every file under `.agents/` are silent on hooks — grepping for the word turns
up nothing. There was no existing convention here to follow, and no reason to assume one from
the buckets/skills-array conventions that *do* exist (those are about which skills the plugin
exposes, not about repo-wide side effects a plugin can register).

Matt's own `misc/git-guardrails-claude-code` skill covers similar ground — a `PreToolUse` hook
blocking dangerous git commands — but ships it as a **skill that walks a human through manually
installing a hook in their own project's `.claude/settings.json`**. That's opt-in per repo, and
it depends on `jq`, which is not guaranteed present (confirmed absent on the server this
decision was made on). Both properties reintroduce the exact failure mode this decision exists
to close: a step that can be skipped, and a dependency that can be missing.

## Decision

Ship the hook (`hooks/hooks.json` + `hooks/block-dangerous-git.py`) at the **plugin root**
instead — so installing this plugin protects every repo it's enabled in automatically, with no
per-repo setup step to forget. The script is Python standard-library only, no `jq`.

Checked real precedent rather than guessing at Claude Code's actual auto-discovery behavior: of
six installed Claude Code plugins inspected on the machine this was built on, five auto-discover
a `hooks/hooks.json` at the plugin root with no manifest field required; the sixth (the
org's sibling `denali-platform` plugin) declares it explicitly (`"hooks": "./hooks/hooks.json"`)
even though the path is the default anyway. This repo's `.claude-plugin/plugin.json` now does
the same — relies on auto-discovery **and** declares the field explicitly, since the second
costs nothing and removes any doubt on a repo shipping its first hook.

**Correction, first real install attempt:** "costs nothing" was wrong. Declaring
`"hooks": "./hooks/hooks.json"` explicitly, on top of the auto-discovery that was already
loading the same file, made the plugin fail to load outright —
`Duplicate hooks file detected: ./hooks/hooks.json resolves to already-loaded file .../hooks/hooks.json`.
`denali-platform`'s explicit declaration apparently tolerates this in whatever Claude Code
version it was last validated against; this repo's did not. Fixed by removing the field —
auto-discovery alone is sufficient and is what every other observed plugin actually relies on.
The belt choked the suspenders. Lesson: "matches an observed precedent" isn't the same as
"verified to actually work" — the first real `claude plugin install` run is what caught this,
not the precedent survey.

## Consequence: `git-guardrails-claude-code` is redundant, so it's removed

Once `personal-git-workflow`'s hook exists and has no `jq` dependency, keeping the older skill
around serves no purpose beyond confusion about which one to set up. Removed per
`skills/deprecated/README.md`'s stated process (delete outright, name the replacement in the
changeset) rather than archived as a stub.

**Correction, same day:** the first version of this hook only ported the `main`-push/PR
pattern and dropped `git-guardrails-claude-code`'s other four patterns (`reset --hard`, force
`clean`, `branch -D`, `checkout .`/`restore .`) without noticing — "ours is more precise on
push scope" was true but incomplete, and the deletion happened before a full pattern-by-pattern
diff was done against what was being removed. Caught in review before merge, not after. Fixed
by restoring those four as unconditional (branch-agnostic) blocks in the same hook, renamed
`block-dangerous-git.py` to match its actual scope. The lesson generalizes: a "this supersedes
that" claim needs a full diff of what's covered, not just confirmation that the one thing you
were focused on is better.

## Known gap this doesn't close

The hook only fires for a **Claude Code plugin install**. This repo also ships via `skills.sh`
for other harnesses (Codex, etc.), which copies skill files but not repo-root files like
`hooks/`. A `skills.sh` install gets `personal-git-workflow`'s written discipline only, not the
mechanical block — `SKILL.md` says so explicitly rather than leaving a silent gap. Closing this
for real would mean either a Codex-side hook equivalent (unclear if one exists) or accepting
that the guarantee is Claude-Code-specific until that's revisited.

## Update, 2026-08-07: the skill is retired, the hook is not

`personal-git-workflow` (the skill — teaching prose on branch caps, staleness audits, the
merge-vs-PR decision) is removed. David's call: the actual thing he cared about enforcing was
always the mechanical `main` guard, not the methodology essay around it, and this ADR's whole
point from the start was that the guard doesn't need the skill to exist — it's a plugin-root
hook, auto-discovered independent of any skill folder. Nothing here changes as a result:
`hooks/hooks.json` and `hooks/block-dangerous-git.py` are untouched and still block the same
two categories (push/PR into `main`; the four branch-agnostic destructive ops) exactly as
before. The hook's own error-message text no longer points at "the personal-git-workflow
skill" for an explanation, since that name no longer resolves to anything — the messages are
now self-contained. This repo's own branch model (`main ← dev ← feature/**`, David the only
merge gate) still holds as working practice; it's just no longer taught as an installable skill
for other repos.

## Update, 2026-08-08: a second plugin-root hook, same known gap

`hooks/require-committed-claim.py` ships the same way, for the same reason: `delegate`'s "commit
the claim before dispatching" rule had already failed once as prose alone — a real dispatch ran
against an uncommitted ticket claim, invisible to the worker's own isolated worktree — so it got
the identical mechanical backstop this ADR's opening paragraph argues for, added as a second entry
in the same plugin-root `hooks/hooks.json` rather than a new mechanism.

The "Known gap this doesn't close" section above was written for `block-dangerous-git.py` alone,
but it's not specific to that hook — it's a property of shipping *any* hook as a plugin-root file:
a `skills.sh` install for another harness copies skill files, not `hooks/`, so it never gets this
guard either. `require-committed-claim.py` inherits that same gap unchanged. A `skills.sh` install
still gets the corrected prose (`docs/agents/issue-tracker.md`, its seed template, and
`delegate/SKILL.md`'s Dispatch step all now say "commit," not "save") — just not the mechanical
block behind it, exactly the same shape of gap as `personal-git-workflow`'s written discipline
once had. No new decision needed here, just naming it rather than leaving a second silent instance
of a gap this ADR already knows about.

## Update, 2026-08-08: the third hook, `delegate-recommend.py`, gets the ADR coverage it shipped without

`hooks/delegate-recommend.py` has been in `hooks/hooks.json` since `delegate` shipped, but was
the one hook with no decision record — an audit against upstream flagged the omission. Naming it
here now rather than writing a new ADR, since it's a smaller instance of this ADR's subject, not
a new decision: a SessionStart hook that surfaces a recommendation to enter `/delegate` when the
active model matches the configured Router model. Unlike its two siblings it enforces nothing —
informational only, never blocks, fail-silent when the `model` field is absent or doesn't match
(the documented-as-not-guaranteed field is matched case-insensitively by substring), and
`/delegate` remains a manual, explicit trigger regardless of what it prints. The `skills.sh` gap
above applies to it the same as the others, and matters even less: a missing recommendation is
just silence, which is already its common case. Separately, hooks now carry executable tests —
that precedent lives in ADR 0006, noted here because this ADR is where anyone touching a hook
will be reading.
