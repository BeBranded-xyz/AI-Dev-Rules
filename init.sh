#!/usr/bin/env bash
# Bootstrap a project with this ruleset.
#
#   ./init.sh --dest ../my-project [--target claude|cursor|codex|both|all|<list>] [--name "My Project"] [--check "pnpm check"] [--force]
#   ./init.sh --dest ../my-project --update
#
# --target accepts one agent, "both" (claude,cursor, the default), "all"
# (claude,cursor,codex), or a comma-separated list such as "claude,codex".
#
# --update refreshes an existing project to the current ruleset. It overwrites
# only files the ruleset owns (rules, hooks, skills, testing catalogue, changelog,
# helper scripts), removes rule files that no longer exist upstream, adds any
# new template file that is missing, and NEVER touches project-owned files
# (PROJECT.md, TEST_PLAN.md, BACKLOG.md, CLAUDE.md, .env.example, registries,
# workflows, settings.json). It records the ruleset commit in
# .ruleset-version and prints what changed.
#
# What it does (idempotent; project-owned files are never overwritten unless --force):
#   - Cursor:      copies core/ modules/ languages/ platforms/ into <dest>/.cursor/rules/ (as .mdc, nested)
#   - Claude Code: converts the same rules into <dest>/.claude/rules/ (as .md; `globs` -> `paths`);
#                  rules that are conditional AND have no globs go to <dest>/.claude/rules-on-demand/
#                  copies claude/settings.json, hooks/, skills/ into <dest>/.claude/
#                  writes <dest>/CLAUDE.md from templates/CLAUDE.md
#   - Codex:       writes <dest>/AGENTS.md from templates/AGENTS.md with a generated index of the
#                  rule files; reuses .claude/ rules and skills when Claude is a target, otherwise
#                  installs the same converted rules and skills into <dest>/.agents/
#   - Every target: copies PROJECT.md, TEST_PLAN.md, registries, .env.example, PR template, workflows,
#                  renovate.json, docs/reference/testing-catalogue.md
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
dest=""; target="both"; name=""; check=""; force=0; update=0

usage() { sed -n '2,18p' "$0"; exit 1; }
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dest) dest="$2"; shift 2 ;;
    --target) target="$2"; shift 2 ;;
    --name) name="$2"; shift 2 ;;
    --check) check="$2"; shift 2 ;;
    --force) force=1; shift ;;
    --update) update=1; shift ;;
    -h|--help) usage ;;
    *) echo "Unknown argument: $1" >&2; usage ;;
  esac
done
[[ -z "$dest" ]] && { echo "--dest is required" >&2; usage; }
case "$target" in
  both) target_list="claude,cursor" ;;
  all) target_list="claude,cursor,codex" ;;
  *) target_list="$target" ;;
esac
targets=","
IFS=',' read -r -a requested <<< "$target_list,"
for t in "${requested[@]}"; do
  [[ "$t" =~ ^(claude|cursor|codex)$ ]] || {
    echo "--target must be claude, cursor, codex, both, all, or a comma-separated list of claude, cursor, codex" >&2; exit 1; }
  targets+="$t,"
done
has() { [[ "$targets" == *",$1,"* ]]; }
# Converted (.md) rules and skills live in .claude/ when Claude is a target; Codex reuses them.
agents_root=".claude"; has claude || agents_root=".agents"
mkdir -p "$dest"; dest="$(cd "$dest" && pwd)"
[[ -z "$name" ]] && name="$(basename "$dest")"

copied=0; skipped=0; updated=0; removed=0
added_list=(); updated_list=()
put() { # put <src> <dst>  project-owned file: never overwritten unless --force
  local src="$1" dst="$2"
  if [[ -e "$dst" && $force -eq 0 ]]; then skipped=$((skipped+1)); return; fi
  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"; copied=$((copied+1)); added_list+=("${dst#"$dest"/}")
}
put_owned() { # put_owned <src> <dst>  ruleset-owned file: overwritten on --update/--force when content differs
  local src="$1" dst="$2"
  if [[ -e "$dst" ]]; then
    if [[ $force -eq 0 && $update -eq 0 ]]; then skipped=$((skipped+1)); return; fi
    if cmp -s "$src" "$dst"; then skipped=$((skipped+1)); return; fi
    cp "$src" "$dst"; updated=$((updated+1)); updated_list+=("${dst#"$dest"/}"); return
  fi
  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"; copied=$((copied+1)); added_list+=("${dst#"$dest"/}")
}
# Remove rule files under <dir> that the ruleset no longer ships (renamed or deleted upstream).
prune_rules() { # prune_rules <dir> <ext>
  local dir="$1" ext="$2" f rel base
  [[ -d "$dir" ]] || return 0
  while IFS= read -r f; do
    rel="${f#"$dir"/}"; base="${rel%."$ext"}"
    [[ -f "$here/$base.mdc" ]] && continue
    rm -f "$f"; removed=$((removed+1)); echo "removed stale rule: ${f#"$dest"/}"
  done < <(find "$dir" -type f -name "*.$ext" \( -path "$dir/core/*" -o -path "$dir/modules/*" -o -path "$dir/languages/*" -o -path "$dir/platforms/*" \))
}

subst() { # subst <file>  replace {{PROJECT_NAME}} and {{pnpm check}} placeholders
  local f="$1"
  sed -i.bak -e "s/{{PROJECT_NAME}}/${name//\//\\/}/g" "$f"
  if [[ -n "$check" ]]; then sed -i.bak -e "s/{{pnpm check}}/${check//\//\\/}/g" "$f"; fi
  rm -f "$f.bak"
}

# Convert a .mdc (Cursor front-matter) into a Claude Code rule .md.
# Prints "always" | "paths" | "ondemand" on stdout after writing the file.
to_claude_rule() { # to_claude_rule <src.mdc> <dst.md>
  local src="$1" dst="$2"
  python3 - "$src" "$dst" <<'PY'
import re, sys
src, dst = sys.argv[1], sys.argv[2]
text = open(src).read()
m = re.match(r'^---\n(.*?)\n---\n(.*)$', text, re.S)
fm, body = (m.group(1), m.group(2)) if m else ("", text)
desc = re.search(r'^description:\s*(.+)$', fm, re.M)
always = re.search(r'^alwaysApply:\s*true', fm, re.M) is not None
globs = []
if 'globs:' in fm:
    for line in fm.split('globs:')[1].splitlines():
        mm = re.match(r'^\s*-\s*"?([^"#]+?)"?\s*(#.*)?$', line)
        if mm: globs.append(mm.group(1).strip())
        elif line.strip() and not line.startswith(' '): break
kind = "always" if always else ("paths" if globs else "ondemand")
out = ["---"]
if desc: out.append("description: " + desc.group(1).strip())
if kind == "paths":
    out.append("paths:")
    out += ["  - \"%s\"" % g for g in globs]
out.append("---")
open(dst, "w").write("\n".join(out) + "\n" + body)
print(kind)
PY
}

echo "Bootstrapping '$name' into $dest (target: $target)"

# --- Rules -------------------------------------------------------------------
rule_dirs=(core modules languages platforms)
ondemand_list=()
for d in "${rule_dirs[@]}"; do
  for f in "$here/$d"/*.mdc; do
    [[ -e "$f" ]] || continue
    base="$(basename "$f" .mdc)"
    if has cursor; then
      put_owned "$f" "$dest/.cursor/rules/$d/$base.mdc"
    fi
    if has claude || has codex; then
      tmp="$(mktemp)"
      kind="$(to_claude_rule "$f" "$tmp")"
      if [[ "$kind" == "ondemand" ]]; then
        put_owned "$tmp" "$dest/$agents_root/rules-on-demand/$d/$base.md"
        ondemand_list+=("$agents_root/rules-on-demand/$d/$base.md")
        rm -f "$dest/$agents_root/rules/$d/$base.md"
      else
        put_owned "$tmp" "$dest/$agents_root/rules/$d/$base.md"
        rm -f "$dest/$agents_root/rules-on-demand/$d/$base.md"
      fi
      rm -f "$tmp"
    fi
  done
done

if [[ $update -eq 1 ]]; then
  if has cursor; then prune_rules "$dest/.cursor/rules" mdc; fi
  if has claude || has codex; then
    prune_rules "$dest/$agents_root/rules" md; prune_rules "$dest/$agents_root/rules-on-demand" md
  fi
fi

# --- Claude Code harness -----------------------------------------------------
if has claude; then
  put "$here/claude/settings.json" "$dest/.claude/settings.json"
  if [[ $update -eq 1 ]] && ! cmp -s "$here/claude/settings.json" "$dest/.claude/settings.json"; then
    echo "note: .claude/settings.json differs from the ruleset version (kept yours). Diff with: diff $here/claude/settings.json $dest/.claude/settings.json"
  fi
  for h in "$here"/claude/hooks/*.sh; do put_owned "$h" "$dest/.claude/hooks/$(basename "$h")"; done
  chmod +x "$dest"/.claude/hooks/*.sh
  for s in "$here"/claude/skills/*/; do
    sname="$(basename "$s")"
    put_owned "$s/SKILL.md" "$dest/.claude/skills/$sname/SKILL.md"
  done
  [[ -n "$check" ]] && { printf '%s\n' "$check" > "$dest/.claude/check-command"; }
  put "$here/templates/CLAUDE.md" "$dest/CLAUDE.md"
  subst "$dest/CLAUDE.md"
  # (Re)generate the on-demand section at the end of CLAUDE.md; everything above it is project-owned.
  if [[ ${#ondemand_list[@]} -gt 0 ]]; then
    python3 - "$dest/CLAUDE.md" "${ondemand_list[@]}" <<'PY'
import re, sys
path, rules = sys.argv[1], sys.argv[2:]
s = open(path).read()
section = "## On-demand rules\n\nThese rules have no file pattern. Read them when `PROJECT.md` marks the module active or the task touches the topic:\n\n" + "\n".join("- @" + r for r in rules) + "\n"
if "## On-demand rules" in s:
    s = re.sub(r"## On-demand rules\n\n[^\n]*\n\n(?:- @[^\n]*\n?)*", section, s, count=1)
else:
    s = s.rstrip("\n") + "\n\n" + section
open(path, "w").write(s)
PY
  fi
fi

# --- Codex (AGENTS.md) -------------------------------------------------------
if has codex; then
  if ! has claude; then
    for s in "$here"/claude/skills/*/; do
      sname="$(basename "$s")"
      put_owned "$s/SKILL.md" "$dest/.agents/skills/$sname/SKILL.md"
    done
  fi
  if [[ ! -e "$dest/AGENTS.md" || $force -eq 1 ]]; then
    put "$here/templates/AGENTS.md" "$dest/AGENTS.md"
    subst "$dest/AGENTS.md"
    sed -i.bak -e "s#{{RULES_ROOT}}#$agents_root#g" "$dest/AGENTS.md" && rm -f "$dest/AGENTS.md.bak"
  else
    skipped=$((skipped+1))
  fi
  # (Re)generate the rule index at the end of AGENTS.md; everything above it is project-owned.
  python3 "$here/scripts/agents-index.py" "$dest" "$agents_root"
fi

# --- Shared project files ----------------------------------------------------
put "$here/PROJECT.md" "$dest/PROJECT.md"
put "$here/templates/TEST_PLAN.md" "$dest/TEST_PLAN.md"
put "$here/templates/BACKLOG.md" "$dest/BACKLOG.md"
put "$here/templates/.env.example" "$dest/.env.example"
put "$here/templates/FUNCTIONS_REGISTRY.md" "$dest/docs/FUNCTIONS_REGISTRY.md"
put "$here/templates/MIGRATIONS_CHANGELOG.md" "$dest/docs/MIGRATIONS_CHANGELOG.md"
put "$here/templates/FEATURE_FLAGS.md" "$dest/docs/FEATURE_FLAGS.md"
put "$here/templates/DEBT.md" "$dest/docs/DEBT.md"
put "$here/templates/RUNBOOK.md" "$dest/docs/RUNBOOK.md"
put "$here/templates/ADR_TEMPLATE.md" "$dest/docs/adr/0000-template.md"
put_owned "$here/docs/reference/testing-catalogue.md" "$dest/docs/reference/testing-catalogue.md"
put_owned "$here/CHANGELOG.md" "$dest/docs/reference/ruleset-changelog.md"
put "$here/templates/PULL_REQUEST_TEMPLATE.md" "$dest/.github/PULL_REQUEST_TEMPLATE.md"
put "$here/templates/renovate.json" "$dest/renovate.json"
for w in "$here"/templates/github/workflows/*.yml; do
  put "$w" "$dest/.github/workflows/$(basename "$w")"
done
for sc in "$here"/templates/scripts/*; do
  put_owned "$sc" "$dest/scripts/$(basename "$sc")"
done
chmod +x "$dest"/scripts/*.sh 2>/dev/null || true
for f in PROJECT.md TEST_PLAN.md BACKLOG.md .env.example docs/RUNBOOK.md; do
  [[ -f "$dest/$f" ]] && subst "$dest/$f"
done

# .gitignore essentials
gi="$dest/.gitignore"
touch "$gi"
for line in ".env" ".env.*" "!.env.example" ".DS_Store" "*.log" "coverage/" "test-results/" "playwright-report/"; do
  grep -qxF "$line" "$gi" || echo "$line" >> "$gi"
done

# Record which ruleset version the project is on.
previous_ruleset="$(sed -n 's/^ruleset=//p' "$dest/.ruleset-version" 2>/dev/null || true)"
ruleset_sha="$(git -C "$here" rev-parse --short HEAD 2>/dev/null || echo unknown)"
printf 'ruleset=%s\nupdated=%s\nsource=%s\n' "$ruleset_sha" "$(date -u +%Y-%m-%d)" "$here" > "$dest/.ruleset-version"

echo "Done: $copied added, $updated updated, $removed removed, $skipped left untouched. Ruleset $ruleset_sha recorded in .ruleset-version."
if [[ $update -eq 1 ]]; then
  echo "Ruleset transition: ${previous_ruleset:-unknown} -> $ruleset_sha. Read docs/reference/ruleset-changelog.md for migration steps."
  [[ ${#updated_list[@]} -gt 0 ]] && { echo "Updated:"; printf '  %s\n' "${updated_list[@]}"; }
  [[ ${#added_list[@]} -gt 0 ]] && { echo "Added (new in the ruleset, fill in):"; printf '  %s\n' "${added_list[@]}"; }
  cat <<EOF

After an update:
  1. Read docs/reference/ruleset-changelog.md and review the diff: git -C "$dest" diff --stat
  2. Open PROJECT.md section 9: tick any new language / platform / module the ruleset now offers.
  3. Run /test-plan (audit) so TEST_PLAN.md picks up new categories or tooling.
  4. Commit as: chore(rules): update ruleset to $ruleset_sha
EOF
  exit 0
fi
cat <<EOF

Next steps:
  1. Fill PROJECT.md (every {{PLACEHOLDER}}; tick active languages, platforms, modules).
  2. Add the check command to the project ($( [[ -n "$check" ]] && echo "$check" || echo "e.g. pnpm check / make check" )) and to PROJECT.md.
  3. Run /test-plan to fill TEST_PLAN.md and wire the CI workflows in .github/workflows/ (replace every {{...}}).
  4. Replace the remaining {{...}} placeholders: grep -rn '{{' --include='*.md' --include='*.yml' --include='*.example' .
EOF
