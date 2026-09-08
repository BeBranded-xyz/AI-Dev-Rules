#!/usr/bin/env bash
# PreToolUse hook (matcher: Bash). Blocks `git commit` unless the project's
# check command passes. Exit 2 = block the tool call and feed stderr to the
# agent. Any other failure of this script itself is non-blocking (exit 0) so a
# broken hook never silently stops all work; it prints a warning instead.
#
# The check command is resolved, in order, from:
#   1. $CHECK_COMMAND
#   2. .claude/check-command (one line)
#   3. package.json "check" script -> pnpm/npm/yarn/bun check
#   4. Makefile target "check" -> make check
#   5. Cargo.toml -> cargo fmt --check && cargo clippy -D warnings && cargo test
#   6. go.mod -> go vet ./... && go test ./...
#   7. pyproject.toml -> ruff check . && pyright && pytest
#   8. build.gradle.kts -> ./gradlew check
set -uo pipefail

input="$(cat)"
command="$(printf '%s' "$input" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null || true)"

# Only act on real commits (not --amend of message, not log/diff/status).
if ! printf '%s' "$command" | grep -Eq '(^|[;&|[:space:]])git[[:space:]]+(-C[[:space:]]+[^[:space:]]+[[:space:]]+)?commit([[:space:]]|$)'; then
  exit 0
fi

if printf '%s' "$command" | grep -Eq -- '--no-verify|-n([[:space:]]|$)'; then
  echo "Blocked: never bypass the check with --no-verify (core/ai-workflow.mdc)." >&2
  exit 2
fi

root="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$root" || exit 0

resolve_check() {
  if [[ -n "${CHECK_COMMAND:-}" ]]; then echo "$CHECK_COMMAND"; return; fi
  if [[ -f .claude/check-command ]]; then head -n1 .claude/check-command; return; fi
  if [[ -f package.json ]] && grep -q '"check"' package.json; then
    if [[ -f pnpm-lock.yaml ]]; then echo "pnpm check"; return; fi
    if [[ -f bun.lockb || -f bun.lock ]]; then echo "bun run check"; return; fi
    if [[ -f yarn.lock ]]; then echo "yarn check"; return; fi
    echo "npm run check"; return
  fi
  if [[ -f Makefile ]] && grep -Eq '^check:' Makefile; then echo "make check"; return; fi
  if [[ -f Cargo.toml ]]; then echo "cargo fmt --check && cargo clippy --all-targets -- -D warnings && cargo test"; return; fi
  if [[ -f go.mod ]]; then echo "gofmt -l . | (! grep .) && go vet ./... && go test -race ./..."; return; fi
  if [[ -f pyproject.toml ]]; then echo "ruff format --check . && ruff check . && pyright && pytest"; return; fi
  if [[ -f build.gradle.kts || -f build.gradle ]]; then echo "./gradlew check"; return; fi
  echo ""
}

check="$(resolve_check)"
if [[ -z "$check" ]]; then
  echo "Warning: no check command found (set CHECK_COMMAND or .claude/check-command). Commit allowed but unverified." >&2
  exit 0
fi

echo "Running check before commit: $check" >&2
if bash -c "$check" >/tmp/claude-check.log 2>&1; then
  exit 0
fi

echo "Blocked: check command failed ($check). Fix the failures before committing. Last 60 lines:" >&2
tail -n 60 /tmp/claude-check.log >&2
exit 2
