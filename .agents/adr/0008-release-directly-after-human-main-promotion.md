# Release directly after the human main promotion

## Context

This is a private personal repository with a human-gated `main` branch. A generated version pull
request adds another approval loop without adding a meaningful decision: David already makes the
release decision by promoting the tested `dev` tip to `main`.

Changesets remain useful as small, reviewable records of release intent and as deterministic input
for version and changelog generation. The pull-request automation around them is not useful here.

## Decision

The Release workflow runs after David promotes `dev` to `main` and does not create a pull request.
It:

1. requires remote `main`, remote `dev`, and the triggering commit to be identical;
2. tests the promoted tree;
3. consumes any pending Changesets and synchronizes all version surfaces;
4. tests the resulting versioned tree;
5. creates one mechanical release commit and an annotated version tag;
6. atomically pushes that commit to both `main` and `dev` together with the tag; and
7. creates a GitHub Release from the matching changelog section.

The atomic push is the workflow's only exception to the human-only `main` rule. It uses the tested,
pinned workflow and may change only the Changesets, changelog, package files, lockfile, and plugin
versions. It refuses to proceed after concurrent branch movement.

The release commit must be a fast-forward descendant of the promoted commit. Exact expected-old
leases turn the atomic push into a compare-and-swap operation, so even branch deletion or a
concurrent force-reset makes the transaction fail instead of overwriting the newer remote state.

GitHub-token pushes do not recursively start another workflow run. If the Git ref transaction
succeeds but GitHub Release creation fails, `workflow_dispatch` provides an idempotent recovery path
that can create a missing Release only for an existing tag reachable from current `main`. A manual
dispatch cannot consume a Changeset or move any Git ref.

## Consequences

- Releases require no version or release pull request.
- `main` and `dev` stay aligned after the mechanical version commit.
- The human promotion remains the only release approval.
- Pending Changesets are mandatory for a new version; a run without one is a no-op except for safe
  recovery of a missing GitHub Release.
