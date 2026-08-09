#!/usr/bin/env bash
set -Eeuo pipefail

repo="${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}"
event_name="${RELEASE_EVENT_NAME:?RELEASE_EVENT_NAME is required}"
event_sha="${RELEASE_EVENT_SHA:?RELEASE_EVENT_SHA is required}"
recovery_tag="${RELEASE_RECOVERY_TAG:-}"
: "${GH_TOKEN:?GH_TOKEN is required}"

case "$event_name" in
  push|workflow_dispatch)
    ;;
  *)
    echo "Release failed: unsupported workflow event $event_name" >&2
    exit 1
    ;;
esac

fail() {
  echo "Release failed: $*" >&2
  exit 1
}

valid_version() {
  [[ "$1" =~ ^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?(\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$ ]]
}

read_version() {
  node -p "require('./package.json').version"
}

validate_tag() {
  local candidate="$1"
  valid_version "$candidate" || fail "unsafe package version: $candidate"
  git check-ref-format "refs/tags/v${candidate}" >/dev/null ||
    fail "package version does not form a valid tag: v${candidate}"
}

make_release_notes() {
  local output="$1"
  RELEASE_VERSION="$version" RELEASE_NOTES="$output" node <<'NODE'
const fs = require("node:fs");

const version = process.env.RELEASE_VERSION;
const output = process.env.RELEASE_NOTES;
const changelog = fs.readFileSync("CHANGELOG.md", "utf8");
const heading = `## ${version}`;
const lines = changelog.split(/\r?\n/);
const start = lines.indexOf(heading);

if (start < 0) {
  fs.writeFileSync(output, `Release v${version}\n`);
  process.exit(0);
}

let end = lines.length;
for (let index = start + 1; index < lines.length; index += 1) {
  if (lines[index].startsWith("## ")) {
    end = index;
    break;
  }
}

const body = lines.slice(start + 1, end).join("\n").trim();
fs.writeFileSync(output, `${body || `Release v${version}`}\n`);
NODE
}

ensure_github_release() {
  if gh release view "$tag" --repo "$repo" >/dev/null 2>&1; then
    echo "GitHub Release $tag already exists."
    return
  fi

  local notes_file="${RUNNER_TEMP:?RUNNER_TEMP is required}/david-skills-${tag}.md"
  make_release_notes "$notes_file"
  gh release create "$tag" \
    --repo "$repo" \
    --verify-tag \
    --title "$tag" \
    --notes-file "$notes_file"
}

git fetch --prune --no-tags origin \
  "+refs/heads/main:refs/remotes/origin/main" \
  "+refs/heads/dev:refs/remotes/origin/dev"
git fetch --prune origin "+refs/tags/*:refs/tags/*"

main_sha="$(git rev-parse refs/remotes/origin/main)"
dev_sha="$(git rev-parse refs/remotes/origin/dev)"
checkout_sha="$(git rev-parse HEAD)"

if [[ "$main_sha" != "$event_sha" ]]; then
  echo "Main moved from $event_sha to $main_sha; a newer run will handle it."
  exit 0
fi
[[ "$checkout_sha" == "$event_sha" ]] ||
  fail "checked-out commit $checkout_sha does not match event commit $event_sha"

npm test
[[ -z "$(git status --porcelain=v1 --untracked-files=all)" ]] ||
  fail "the release checkout is not clean after testing"

shopt -s nullglob
changesets=()
for file in .changeset/*.md; do
  [[ "$file" == ".changeset/README.md" ]] || changesets+=("$file")
done

version="$(read_version)"
validate_tag "$version"
tag="v${version}"

# A manual dispatch is recovery-only and can never consume Changesets or move refs.
if [[ "$event_name" == "workflow_dispatch" ]]; then
  if [[ -n "$recovery_tag" ]]; then
    [[ "$recovery_tag" == v* ]] || fail "recovery tag must start with v"
    version="${recovery_tag#v}"
    validate_tag "$version"
    tag="v${version}"
  fi
  git show-ref --verify --quiet "refs/tags/$tag" ||
    fail "recovery tag $tag does not exist"
  tagged_sha="$(git rev-list -n 1 "$tag")"
  git merge-base --is-ancestor "$tagged_sha" "$main_sha" ||
    fail "recovery tag $tag is not part of current main history"
  ensure_github_release
  exit 0
fi

# Automatic recovery: the Git ref transaction succeeded but Release creation failed.
if (( ${#changesets[@]} == 0 )); then
  if git show-ref --verify --quiet "refs/tags/$tag"; then
    tagged_sha="$(git rev-list -n 1 "$tag")"
    if git merge-base --is-ancestor "$tagged_sha" "$main_sha"; then
      ensure_github_release
    else
      echo "No pending Changesets; $tag is not in current main history. Nothing to release."
    fi
  else
    echo "No pending Changesets; nothing to release."
  fi
  exit 0
fi

[[ "$dev_sha" == "$main_sha" ]] ||
  fail "origin/main and origin/dev must be aligned before release"

old_version="$version"
npm run version

version="$(read_version)"
validate_tag "$version"
tag="v${version}"
[[ "$version" != "$old_version" ]] ||
  fail "Changesets did not advance the package version from $old_version"
if git show-ref --verify --quiet "refs/tags/$tag"; then
  fail "$tag already exists"
fi

# Versioning changes manifests, the lockfile, and the changelog. Test that exact tree.
npm test

git add -A -- \
  .changeset \
  package.json \
  package-lock.json \
  CHANGELOG.md \
  .claude-plugin/plugin.json \
  .codex-plugin/plugin.json

git diff --quiet || {
  git diff --name-only >&2
  fail "versioning modified tracked files outside the release allowlist"
}
if [[ -n "$(git ls-files --others --exclude-standard)" ]]; then
  git ls-files --others --exclude-standard >&2
  fail "versioning created files outside the release allowlist"
fi
git diff --cached --quiet && fail "versioning produced no releasable changes"

while IFS= read -r path; do
  case "$path" in
    package.json|package-lock.json|CHANGELOG.md|\
    .claude-plugin/plugin.json|.codex-plugin/plugin.json)
      ;;
    .changeset/*.md)
      [[ "$path" != ".changeset/README.md" ]] ||
        fail "versioning unexpectedly changed .changeset/README.md"
      ;;
    *)
      fail "versioning unexpectedly staged $path"
      ;;
  esac
done < <(git diff --cached --name-only)

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git -c commit.gpgsign=false commit -m "chore: release $tag"
release_sha="$(git rev-parse HEAD)"
git merge-base --is-ancestor "$main_sha" "$release_sha" ||
  fail "release commit is not a fast-forward descendant of the promoted commit"
git -c tag.gpgSign=false tag -a "$tag" -m "$tag"

# Recheck after versioning and tests. Concurrent branch movement must fail safely.
git fetch --no-tags origin \
  "+refs/heads/main:refs/remotes/origin/main" \
  "+refs/heads/dev:refs/remotes/origin/dev"
[[ "$(git rev-parse refs/remotes/origin/main)" == "$main_sha" ]] ||
  fail "origin/main moved during release"
[[ "$(git rev-parse refs/remotes/origin/dev)" == "$main_sha" ]] ||
  fail "origin/dev moved during release"

git push --atomic \
  "--force-with-lease=refs/heads/main:$main_sha" \
  "--force-with-lease=refs/heads/dev:$main_sha" \
  origin \
  "$release_sha:refs/heads/main" \
  "$release_sha:refs/heads/dev" \
  "refs/tags/$tag:refs/tags/$tag"

ensure_github_release
