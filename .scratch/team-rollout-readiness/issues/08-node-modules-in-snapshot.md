# Trim the plugin snapshot (node_modules + internal dirs)

Type: task
Status: ready-for-agent

## Question

The installed plugin snapshot ships far more than the plugin. Two observations:

- Ticket 03's sandbox (GitHub source): snapshot is **29M, of which 27M is `node_modules`**
  (84 packages — the changeset/dev tooling). A fresh clone has none, so the marketplace/install
  pipeline materializes it. The snapshot also carries every internal dir: `.scratch`,
  `.agents`, `.out-of-scope`, `.github`, `HANDOFF.md`, full `docs/`.
- David's real install (directory-source marketplace): the snapshot copies the working
  directory **wholesale, ignoring `.gitignore`** — his personal `/teach` workspace
  (`MISSION.md`, `NOTES.md`, `lessons/`, `assets/`) is sitting in his plugin cache. Proof the
  pipeline does no git-aware filtering at all.

1. Find the mechanism (does marketplace validation or plugin install run `npm install` when
   `package.json` is present at the plugin root? what filtering, if any, does the snapshot
   copy apply?) — cite the doc or observed behavior.
2. Decide the fix: an ignore/files mechanism in the plugin manifest if one exists, moving dev
   tooling out of the plugin root, or accepting the bloat with a note. Prefer the smallest
   change that keeps `npm run version` working for David. Cover the internal dirs, not just
   `node_modules`, if the mechanism allows.
3. Verify with a re-run of ticket 03's sandbox sequence: snapshot should shrink to roughly the
   skills + hooks + manifests (~2M), and a directory-source install should no longer swallow
   gitignored personal files.

Not rollout-blocking for a private team repo (installers are teammates), but 27M of dev
dependencies plus the whole internal tracker in every cache is noise, and the
ignores-.gitignore behavior is a footgun worth closing before anyone reuses this pattern on
a less-private repo.

## Answer

(resolution pending)
