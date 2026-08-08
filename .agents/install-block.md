# The canonical install block

One install story, one wording. `README.md`, `.changeset/*`, and every page under `docs/` must say **this** and nothing else. Change it here first, then propagate.

This is Denali's private fork of [mattpocock/skills](https://github.com/mattpocock/skills), shipped as its own plugin (`denali-dev`) from its own single-plugin marketplace baked into this repo. It is **not** in Claude Code's official marketplace — that listing (`mattpocock-skills`) is Matt's original, unmodified upstream. Installing that instead of this fork gets you the vanilla skills, without `setup`'s local-markdown tracker, the plugin-root hook that blocks any push or PR into `main`, or any other Denali-specific change.

## Claude Code — the plugin

<canonical-block name="claude-code">

```
/plugin marketplace add DenaliAI-Automation/Denali-DEV
/plugin install denali-dev@denali-dev
```

No official-marketplace shortcut exists for a private fork — add the marketplace once, then install from it. To pick up a new version later, run `/plugin marketplace update denali-dev` (or reinstall).

</canonical-block>

## Codex, and other agents — skills.sh

The plugin is Claude Code only. Everywhere else, [skills.sh](https://skills.sh) copies editable skill files into the project. Use the whole-set form on `README.md`:

<canonical-block name="skills-sh-whole-set">

```bash
npx skills@latest add DenaliAI-Automation/Denali-DEV
```

Pick the skills you want, and which coding agents to install them on. **The installer lets you choose which skills to take — make sure `setup` is one of them.** This repo is private — have `gh`/git auth for the `DenaliAI-Automation` org already set up locally (`gh auth setup-git` wires the HTTPS credential helper the clone uses first), or the clone step fails. Verified end-to-end against this private repo 2026-08-08 under org-owner auth; a plain org member's auth is still unproven. Note the flag is `--skill <name>` with a space — the `--skill=<name>` equals form is silently ignored by the CLI and installs every skill.

</canonical-block>

…and the single-skill form wherever one skill is named on its own. Note that **`docs/` pages are not a consumer of this block**: see [writing-docs.md](./writing-docs.md).

<canonical-block name="skills-sh-one-skill">

```bash
npx skills@latest add DenaliAI-Automation/Denali-DEV --skill <name>
```

```bash
npx skills@latest update <name>
```

</canonical-block>

`skills@latest` is the pinned spelling in all three. The pages under `docs/` used to carry their own copy of these commands; those blocks are deleted rather than corrected, because the site renders the install commands itself — this fork does not currently publish docs pages anywhere they'd render that widget, so treat any surviving `docs/` install snippet as dead and delete it on sight rather than fixing it.

## The two routes are exclusive

The plugin is a managed, read-only bundle you subscribe to. skills.sh writes files you own and edit. Installing both leaves the user with every skill twice — always say "pick one".

## Not the install story

Matt's original, [mattpocock/skills](https://github.com/mattpocock/skills), is what this repo forked from and still tracks read-only via the `upstream` git remote (`git fetch upstream && git merge upstream/main`). It's in Claude Code's official marketplace (`claude plugins install mattpocock-skills`) and installable via `npx skills@latest add mattpocock/skills` — the unmodified original, not this fork. Don't point Denali engineers at it by mistake; it's mentioned here only for anyone who wants Matt's version specifically, or is pulling upstream changes into this fork.
