#!/usr/bin/env node
// Copies package.json's version into both plugin manifests and package-lock.
// Runs as part of `npm run version`, immediately after `changeset version`.
// With --check it changes nothing and exits 1 if any version differs.

import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repo = join(dirname(fileURLToPath(import.meta.url)), "..");
const pluginPaths = [
  [".claude-plugin/plugin.json", join(repo, ".claude-plugin", "plugin.json")],
  [".codex-plugin/plugin.json", join(repo, ".codex-plugin", "plugin.json")],
];

const { name, version } = JSON.parse(
  readFileSync(join(repo, "package.json"), "utf8"),
);
if (typeof name !== "string" || typeof version !== "string") {
  console.error("package.json must contain string name and version fields.");
  process.exit(1);
}

const lockLabel = "package-lock.json";
const lockPath = join(repo, lockLabel);
const lock = JSON.parse(readFileSync(lockPath, "utf8"));
const lockRoot = lock.packages?.[""];

// Validate package identity before changing any file, so failures are transactional.
if (!lockRoot) {
  console.error(`${lockLabel} has no root package entry.`);
  process.exit(1);
}
if (lock.name !== name || lockRoot.name !== name) {
  console.error(
    `${lockLabel} package names are ${lock.name}/${lockRoot.name}, package.json is ${name}. Refusing to rewrite package identity.`,
  );
  process.exit(1);
}

const checkOnly = process.argv.includes("--check");
let versionsDiffer = false;

for (const [label, pluginPath] of pluginPaths) {
  const source = readFileSync(pluginPath, "utf8");
  const plugin = JSON.parse(source);

  if (plugin.version === version) {
    console.log(`${label} version is ${version} — already in sync`);
    continue;
  }

  versionsDiffer = true;
  if (checkOnly) {
    console.error(
      `${label} version is ${plugin.version}, package.json is ${version}. Run \`node scripts/sync-plugin-version.mjs\`.`,
    );
    continue;
  }

  // Rewrite only the version line, to keep the key order and formatting.
  const updated = source.replace(
    /("version"\s*:\s*")[^"]*(")/,
    `$1${version}$2`,
  );

  if (JSON.parse(updated).version !== version) {
    console.error(`Could not find a version field to replace in ${pluginPath}.`);
    process.exit(1);
  }

  writeFileSync(pluginPath, updated);
  console.log(`${label} version ${plugin.version} -> ${version}`);
}

const lockInSync = lock.version === version && lockRoot?.version === version;

if (lockInSync) {
  console.log(`${lockLabel} versions are ${version} — already in sync`);
} else {
  versionsDiffer = true;
  if (checkOnly) {
    console.error(
      `${lockLabel} root versions are ${lock.version}/${lockRoot?.version}, package.json is ${version}. Run \`node scripts/sync-plugin-version.mjs\`.`,
    );
  } else {
    const previous = `${lock.version}/${lockRoot.version}`;
    lock.version = version;
    lockRoot.version = version;
    writeFileSync(lockPath, `${JSON.stringify(lock, null, 2)}\n`);
    console.log(`${lockLabel} root versions ${previous} -> ${version}/${version}`);
  }
}

if (checkOnly && versionsDiffer) {
  process.exit(1);
}
