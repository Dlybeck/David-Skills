# Private-marketplace plugin update semantics

Type: research
Status: resolved

## Question

When a Claude Code plugin is installed from a GitHub-sourced private marketplace
(`/plugin marketplace add DenaliAI-Automation/Denali-DEV` → `/plugin install denali-dev@denali-dev`),
what is the actual update behavior — against primary sources (docs.anthropic.com Claude Code
plugin docs, release notes), not memory?

Specifically:
1. Does Claude Code ever auto-update marketplace-added plugins, or is `/plugin marketplace
   update <name>` always manual? Is there any background refresh?
2. What exactly does `/plugin marketplace update` re-fetch — marketplace manifest only, or the
   plugin content snapshot too? Does an installed plugin's skill text refresh without an
   explicit reinstall (the "installs snapshot at install" trap in HANDOFF)?
3. What does upstream's official-marketplace listing (`mattpocock-skills`) get that a private
   marketplace doesn't — auto-update, discoverability, anything else?
4. Does the private-repo marketplace-add require `gh` auth, git credentials, or both — and
   which protocols (HTTPS/SSH) does it use? (SSH to GitHub is intermittently unreliable on
   this server — note if HTTPS is forced or selectable.)

Findings land on a throwaway `research/private-marketplace-update-semantics` branch as a
markdown file; the answer summary comes back here per the tracker's resolve convention.
Ticket 03 (sandboxed install test) and ticket 04 (nudge-hook design) both block on this.

## Answer

Full findings: `research/private-marketplace-update-semantics.md` on branch
`research/private-marketplace-update-semantics`.

1. **Auto-update is real but off by default for private/third-party marketplaces.** Claude
   Code checks for marketplace + plugin updates in the background ~0-10 min after session
   start, but only for marketplaces with auto-update enabled — official Anthropic marketplaces
   default to on, third-party (incl. private GitHub) default to off. `/plugin marketplace
   update` stays the reliable manual path unless someone flips the per-marketplace toggle.
2. **`/plugin marketplace update` only refreshes the catalog (`marketplace.json`), not plugin
   content.** Plugin content is a full snapshot copied into `~/.claude/plugins/cache/<mkt>/
   <plugin>/<version>/` at install/update time; it only refreshes when the *resolved version*
   changes (git SHA for unpinned git sources) via `/plugin update <plugin>` or auto-update. The
   "installs snapshot at install" trap is confirmed — this machine's own cache has two
   version-numbered copies of `denali-dev` (1.3.0 orphaned, 1.5.0 live) sitting side by side.
3. **Official vs. private:** auto-registration on first launch, auto-update-on-by-default, and
   richer Discover-tab metadata (Context cost, Last updated, upfront component list) are the
   three documented gaps; the Discover-tab browsing mechanism itself is identical either way.
4. **Auth/protocol:** manual commands accept either an HTTPS credential helper (`gh auth
   setup-git`) or SSH (`ssh-agent` + known_hosts) — GitHub `owner/repo` shorthand defaults to
   **SSH** unless `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` is set. Background auto-update pulls are
   HTTPS-credential-helper-blind (SSH-only for the pull itself; a failed pull re-clones using
   stored HTTPS creds, which can also time out) — directly relevant given this box's known SSH
   flakiness. **Caveat for ticket 03:** this machine's actual `denali-dev` marketplace entry is
   a local `directory` source (`/mnt/data/dlybeck/Denali-DEV`), not the GitHub-shorthand path
   the ticket names — the literal `/plugin marketplace add DenaliAI-Automation/Denali-DEV` flow
   has not yet been exercised here and should be ticket 03's first real test.
