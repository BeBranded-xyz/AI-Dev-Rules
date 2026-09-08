#!/usr/bin/env node
// License allowlist check (core/dependencies.mdc).
// Usage: pnpm licenses list --json | node scripts/check-licenses.mjs
// Exit 1 when any production dependency uses a license outside the allowlist.
// Extend ALLOWED or EXCEPTIONS in the project; every exception needs a reason.

import { readFileSync } from "node:fs";

const ALLOWED = new Set([
  "MIT", "ISC", "BSD-2-Clause", "BSD-3-Clause", "Apache-2.0", "0BSD",
  "CC0-1.0", "Unlicense", "MPL-2.0", "Python-2.0", "BlueOak-1.0.0", "CC-BY-4.0",
]);

// Package name -> reason. Keep this list short and reviewed.
const EXCEPTIONS = new Map([
  // ["some-package", "Vendor-approved commercial license, contract #123"],
]);

const raw = readFileSync(0, "utf8").trim();
if (!raw) {
  console.error("check-licenses: no input on stdin");
  process.exit(1);
}

// pnpm outputs { "<license>": [ { name, versions, ... }, ... ] }
const byLicense = JSON.parse(raw);
const violations = [];
for (const [license, packages] of Object.entries(byLicense)) {
  const expr = license.replace(/[()]/g, "");
  const ok = expr.split(/\s+(?:OR|AND)\s+/i).some((part) => ALLOWED.has(part.trim()));
  if (ok) continue;
  for (const pkg of packages) {
    if (EXCEPTIONS.has(pkg.name)) continue;
    violations.push(`${pkg.name}@${(pkg.versions ?? []).join(",")} -> ${license}`);
  }
}

if (violations.length > 0) {
  console.error("Disallowed licenses found:\n  " + violations.join("\n  "));
  console.error("\nAdd to ALLOWED (with team approval) or to EXCEPTIONS with a reason.");
  process.exit(1);
}
console.log(`check-licenses: ${Object.keys(byLicense).length} license type(s) checked, all allowed.`);
