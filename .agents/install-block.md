# The canonical install block

Change installation wording here first, then propagate it. David Skills is David's private,
personal fork of [mattpocock/skills](https://github.com/mattpocock/skills), shipped as the
`david-skills` plugin from the marketplaces in this repository. It is not the
`mattpocock-skills` package in Claude Code's official marketplace; that is Matt's original.

## Private-repository authentication

Every new machine must be able to clone the private GitHub repository:

<canonical-block name="github-auth">

```bash
gh auth login
gh auth setup-git
```

</canonical-block>

## Claude Code — the plugin

<canonical-block name="claude-code">

```
/plugin marketplace add Dlybeck/David-Skills
/plugin install david-skills@david-skills
```

</canonical-block>

Add the marketplace once. To update a later release, refresh the catalog and then update the
qualified plugin:

```
/plugin marketplace update david-skills
/plugin update david-skills@david-skills
```

## Codex — the plugin

<canonical-block name="codex">

```bash
codex plugin marketplace add Dlybeck/David-Skills --ref main
codex plugin add david-skills@david-skills
```

</canonical-block>

This is a remote installation: Codex clones the GitHub marketplace into its managed cache. It
does not link to a local checkout. The Codex plugin ships all promoted skills, including the
human-invoked `advise`, `autopilot`, and `yolopilot` wrappers and their model-invoked
`pursue-goal` engine.

The plugin carries Git guardrail hooks. Codex does not trust plugin hooks silently: review and
enable them when prompted, or inspect them with `/hooks`. Start a new task after installation.

Update the remote snapshot with:

```bash
codex plugin marketplace upgrade david-skills
```

The upgrade refreshes the Git snapshot and reinstalls the configured plugin from that snapshot.

Maintainers testing an unreleased integration branch may replace `--ref main` with `--ref dev`.
Published instructions and ordinary installs always use `main`.

## Other agents or editable copies — skills.sh

[skills.sh](https://skills.sh) copies editable skill files into a project. Use the whole-set form
only when an editable copy is intentional:

<canonical-block name="skills-sh-whole-set">

```bash
npx skills@latest add Dlybeck/David-Skills
```

Pick the skills and target agents you want, and include `setup`. This route copies only skill
files; it does not install plugin-root hooks.

</canonical-block>

Use the single-skill form wherever one skill is named on its own:

<canonical-block name="skills-sh-one-skill">

```bash
npx skills@latest add Dlybeck/David-Skills --skill <name>
```

```bash
npx skills@latest update <name>
```

</canonical-block>

The flag is `--skill <name>` with a space. The `--skill=<name>` form may be ignored by the
installer.

## The routes are exclusive

A plugin is a managed bundle fetched from GitHub. skills.sh writes ordinary files the user owns
and edits. Installing both for the same harness duplicates every selected skill, so always tell
users to pick one.

## Upstream

[mattpocock/skills](https://github.com/mattpocock/skills) remains the methodology source and is
configured as the read-only `upstream` Git remote. It is mentioned for attribution and upstream
syncs, not as the installation target for David Skills.
