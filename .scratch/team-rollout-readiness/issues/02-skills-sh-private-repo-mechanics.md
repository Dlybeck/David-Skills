# skills.sh private-repo install mechanics (the Codex triple-check)

Type: research
Status: resolved

## Question

`.agents/install-block.md` admits the skills.sh route (`npx skills@latest add
DenaliAI-Automation/Denali-DEV --skill=<name>`) is **not verified end-to-end against a private
org repo**. David's Codex test machine is a pain to use, so this ticket must triple-check the
route before ticket 05 asks him to touch it:

1. How does the `skills` npm package fetch a repo — `git clone` (HTTPS or SSH?), GitHub API,
   tarball? Read the actual package source/docs, don't guess.
2. What auth does a **private** org repo require for that fetch path — ambient `gh` auth, git
   credential helper, SSH key, a token env var? What's the failure mode when auth is missing?
3. Does `npx skills update <name>` work against a private source once installed?
4. **Local dry-run** (allowed: this stays inside David's user on this machine): run the install
   into a throwaway temp project dir and record exactly what happens — success, prompts, or
   the precise error. This is the closest desk-check to the real Codex machine.
5. Produce the step-by-step checklist ticket 05 will hand David — including the auth
   preconditions to verify on the Codex machine *before* running anything.

Findings land on a throwaway `research/skills-sh-private-repo` branch as a markdown file; the
answer summary comes back here per the tracker's resolve convention. Ticket 05 blocks on this.

## Answer

Fetch mechanism: `git clone --depth 1 [--branch <ref>]` over an HTTPS URL built from
`owner/repo` (`simple-git`, shells out to system `git`); GitHub-API/tarball fast paths are
hard-allowlisted to a handful of Vercel-owned repos and never apply to us. Auth is three-tier:
ambient git credential helper over HTTPS → `gh repo clone` fallback → one direct
`git@github.com:...` SSH clone with `BatchMode=yes`. On this machine (`gh auth setup-git`
already wired), tier 1 succeeded outright in every dry run — SSH was never touched.
`npx skills update` reuses the identical clone+auth path, verified working end-to-end.

**Headline, non-auth finding**: the canonical documented command
(`.agents/install-block.md`'s `--skill=<name>`, equals syntax) is **silently broken** — the
CLI's arg parser only recognizes `--skill <name>` (space-separated) and falls through to
installing *every* skill in the repo when given the `=` form. Reproduced identically against
both `main` and `dev`. `.agents/install-block.md` and `README.md` need the `=` dropped before
ticket 05 runs, or David's one Codex-machine visit installs all 38 skills instead of `setup`.

Also confirmed: `main` still carries the pre-rename skill set (no `setup` skill exists there
yet) — ticket 05's checklist must target `DenaliAI-Automation/Denali-DEV#dev` until `dev` is
promoted.

Full findings, cited source lines, trimmed dry-run transcripts, and the Codex-machine
checklist (auth pre-flight, exact command, expected output, failure-mode table): see
`research/skills-sh-private-repo.md` on branch `research/skills-sh-private-repo`.
