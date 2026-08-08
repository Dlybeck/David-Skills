# The canonical install block

One install story, one wording. `README.md`, `.changeset/*`, and any other installation
instructions must say this and nothing else. Change it here first, then propagate.

David Skills is David's private, personal fork of
[mattpocock/skills](https://github.com/mattpocock/skills), shipped as the `david-skills`
plugin from the single-plugin marketplace in this repository. It is not the
`mattpocock-skills` package in Claude Code's official marketplace; that is Matt's original,
unmodified upstream.

## Claude Code — the plugin

<canonical-block name="claude-code">

```
/plugin marketplace add Dlybeck/David-Skills
/plugin install david-skills@david-skills
```

</canonical-block>

Because this repository is private, GitHub authentication must already be available on the
machine. Add the marketplace once. To update a later release, refresh the catalog and then update
the qualified plugin:

```
/plugin marketplace update david-skills
/plugin update david-skills@david-skills
```

## Codex and other agents — skills.sh

The plugin is Claude Code only. Everywhere else,
[skills.sh](https://skills.sh) copies editable skill files into the project. Use the whole-set
form in `README.md`:

<canonical-block name="skills-sh-whole-set">

```bash
npx skills@latest add Dlybeck/David-Skills
```

Pick the skills and target agents you want. Make sure `setup` is included. Since the
repository is private, run `gh auth setup-git` first when the machine is not already
authenticated.

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

## The two routes are exclusive

The plugin is a managed, read-only bundle. skills.sh writes ordinary files the user owns and
edits. Installing both duplicates every selected skill, so always tell users to pick one.

## Upstream

[mattpocock/skills](https://github.com/mattpocock/skills) remains the methodology source and is
configured as the read-only `upstream` Git remote. It is mentioned for attribution and upstream
syncs, not as the installation target for David Skills.
