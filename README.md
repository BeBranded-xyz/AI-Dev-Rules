# AI Development Rules

A reusable, project-agnostic engineering ruleset for building software with AI
assistants (Claude Code, Cursor). Bootstrap it into a project, fill in one
identity file, and every rule applies without edits.

Everything in this repository is written in English and stays in English: code,
identifiers, comments, commits, and docs of the projects that use it are
maintained in English.

## What it enforces

- **How the AI works**: read `PROJECT.md` first, plan multi-file changes, write
  tests with the code, run the check command before claiming done, report
  faithfully (`core/ai-workflow.mdc`). Claude hooks block recognized commits
  when verification is missing or fails; CI remains the shared enforcement gate.
- **Maximal testing by default**: all 72 test categories of the catalogue are
  required unless justified in the project's `TEST_PLAN.md`
  (`core/testing.mdc`). The goal is to break the program against tests until
  as few defects as possible reach production or human testing.
- **Engineering baseline**: size limits, architecture, type safety, error
  taxonomy, security, dependency policy, git workflow, documentation as a
  deliverable.
- **Per language, platform, and module rules** activated from `PROJECT.md`.
- **Shared design system for UI projects**: reusable components, semantic
  tokens instead of hardcoded design values, documented variants and states,
  consistent icons, and automated checks (`modules/design-system.mdc`).

## Layout

```
PROJECT.md                  Identity sheet: the only file with project-specific facts
core/                       Always apply
  project-identity.mdc      Points to PROJECT.md, explains the ruleset
  ai-workflow.mdc           How the agent works: context, planning, definition of done
  code-standards.mdc        Size limits, architecture, naming, type safety, dead code
  error-handling.mdc        Error taxonomy, typed errors, reason codes, boundaries
  testing.mdc               Maximal testing: what every change must add, gates per stage
  security.mdc              Secrets, authorization, validation, privacy
  dependencies.mdc          Adding, pinning, updating, auditing dependencies
  github-workflow.mdc       Branches, commits, PRs, review, docs as deliverable
  maintenance.mdc           Maintenance and debt (on demand)
languages/                  Apply per language (globs)
  typescript, python, go, rust, php (incl. WordPress), swift,
  kotlin-android, react-native, sql, shell
platforms/                  Apply per platform (globs)
  nextjs, supabase, cloudflare-workers, webflow, vercel
modules/                    Apply when PROJECT.md marks them active
  database, auth, integrations, api-design, frontend, design-system, data-fetching, i18n, performance,
  background-jobs, observability, infra, releases, ai-features,
  data-lifecycle, audit-trail, graphify
templates/                  Files every project gets
  TEST_PLAN.md              All 72 test categories with status / tool / command / gate
  BACKLOG.md                The project's task backlog, updated at the end of every task
  CLAUDE.md                 Project entry point for Claude Code
  .env.example, PULL_REQUEST_TEMPLATE.md, renovate.json
  FUNCTIONS_REGISTRY.md, MIGRATIONS_CHANGELOG.md, FEATURE_FLAGS.md,
  DEBT.md, RUNBOOK.md, ADR_TEMPLATE.md
  github/workflows/         ci.yml (commit + PR gates), pre-production.yml, release.yml (actionlint-clean, pnpm defaults)
  scripts/                  check-licenses.mjs, watch-slo.sh used by the workflows
claude/                     Claude Code harness
  settings.json             Hooks wiring
  hooks/                    pre-commit-check, block-secrets, stop-reminder
  skills/                   /check, /test-plan, /new-migration, /new-function, /release, /health-check
docs/reference/
  testing-catalogue.md      The 72 categories and what each detects
CHANGELOG.md                Ruleset changes and consumer migration steps
init.sh                     Bootstrap script
tests/                      Ruleset integrity and installer regression tests
Makefile                    Local check entry point
.github/workflows/          CI for this ruleset itself
```

## Usage

```bash
git clone <this repo> rules
./rules/init.sh --dest ../my-project --target both --name "My Project" --check "pnpm check"
```

`--target` is `claude`, `cursor`, or `both`. The script never overwrites an
existing file (use `--force` to do so). It:

1. Copies the rules into `.cursor/rules/` (Cursor, `.mdc`) and/or converts them
   into `.claude/rules/` (Claude Code, `.md`, `globs` become `paths`). Conditional
   rules without a file pattern go to `.claude/rules-on-demand/` and are listed
   in `CLAUDE.md`.
2. Installs the Claude Code hooks and skills into `.claude/`.
3. Copies `PROJECT.md`, `TEST_PLAN.md`, the registries, `.env.example`, the PR
   template, the CI workflows, and `renovate.json`.

Then:

1. Fill **`PROJECT.md`**: every `{{PLACEHOLDER}}`, tick the active languages,
   platforms, and modules, delete sections that do not apply.
2. Make sure the project has a single **check command** (`pnpm check`,
   `make check`, `cargo make check`, `./gradlew check`) that runs format, lint,
   typecheck, unit, and integration tests. The pre-commit hook runs it.
3. Run **`/test-plan`** to fill `TEST_PLAN.md` and wire the CI workflows.
4. Keep `PROJECT.md` and `TEST_PLAN.md` current in the same PR as any change
   to the stack, structure, tooling, or a key decision.

## Adopting the ruleset in an existing project

Capture the current check results and inventory legacy gaps before remediation.
Installation does not authorize a full rewrite: apply rules to new/changed
behavior and affected dependencies, then plan other gaps in the backlog with
owners. Scoped temporary exceptions need a reason, expiry, and migration issue.
Existing failures remain failures; security and data integrity are not waived.
See `core/ai-workflow.mdc` for the adoption policy.

## Updating an existing project

```bash
cd rules && git pull
./init.sh --dest ../my-project --update
```

Before updating, note the installed SHA in `.ruleset-version` and review
[CHANGELOG.md](CHANGELOG.md), including the migration steps for intervening
changes. For a single-target project, pass `--target claude` or `--target cursor`.

`--update` overwrites only what the ruleset owns: the rules in
`.cursor/rules/` and `.claude/rules/`, the hooks, the skills, the testing
catalogue, the ruleset changelog (`docs/reference/ruleset-changelog.md`), and
the helper scripts. The application's own `CHANGELOG.md` is never replaced.
It removes rule files that no longer exist upstream, adds new template files that the project does not have yet, and
never touches project-owned files (`PROJECT.md`, `TEST_PLAN.md`,
`BACKLOG.md`, `CLAUDE.md` above its on-demand section, `.env.example`,
registries, workflows, `.claude/settings.json`). The ruleset commit is
recorded in `.ruleset-version` so `/health-check` can tell when a project is
behind. Then review the diff, tick any new module in `PROJECT.md` section 9,
run `/test-plan` to audit, and commit as `chore(rules): update ruleset to <sha>`.

The update output reports the previous/current installed SHA. This records the
installed files; review and record migration completion separately in
`PROJECT.md`. Review source changes to `.claude/settings.json` manually because
existing hook wiring is preserved.

## Hook scope and configuration

Configure a real verification command before committing through Claude:
`CHECK_COMMAND`, `.claude/check-command` (one non-empty line), or a supported
ecosystem check target. Missing/blank commands and failing verification block
recognized commits. Invalid hook payloads block with a diagnostic.

The write hook scans code, docs, fixtures, and examples for credential patterns;
use obvious placeholders even in examples. Hooks run only on their configured
Claude tools. They do not intercept other editors, shell-based file writes, Git
aliases, or all shell command spellings. Keep independent CI checks and secret
scanning enabled; these hooks are not a security sandbox.

## How the rules relate

- `core/` never contains project facts; when a rule needs one it says "see
  `PROJECT.md`".
- A language rule takes precedence over `code-standards.mdc` for naming and may
  override size limits with a documented reason (never above 2x, function
  limit never overridden).
- A platform rule layers on top of the module rules it touches (e.g.
  `platforms/supabase.mdc` on `modules/database.mdc`) and references them
  rather than repeating them.
- `core/testing.mdc` is the standard; language and platform rules name the
  tools; `TEST_PLAN.md` records the project's actual commands and status;
  `docs/reference/testing-catalogue.md` defines what each category detects.

## Front-matter

Every `.mdc` starts with `description`, optional `globs`, and `alwaysApply`.
Cursor reads these directly. For Claude Code, `init.sh` converts `globs` to
`paths`; rules with `alwaysApply: true` load on every request.

## Contributing to the ruleset

- Rules are prescriptive: every bullet is something an agent can obey or a
  reviewer can check.
- Keep each rule between roughly 120 and 220 lines; split rather than grow.
- Never add a project-specific fact; add a placeholder to `PROJECT.md` instead.
- Every rule ends with a checklist. Every language and module rule has a
  Testing section.
- Any change to requirements, activation, hooks, or distribution updates
  `CHANGELOG.md` in the same change, with affected projects, behavior changes,
  and actionable migration steps (or explicitly no migration required).
- Every new or changed rule states its scope, allowed exceptions (or that none
  apply), and verification method (automated check or an explicit review item).
- Reuse the authoritative rule by reference. Resolve contradictory requirements
  explicitly; do not silently add a competing rule in another module.
- Update the activation catalogue, references, and relevant installer tests with
  every rule addition, move, or removal.
- Rules about agent behavior require review scenarios as well as prose: check
  that existing work stays intact and that instructions in external content
  cannot grant authorization. Static tests cannot prove agent compliance.

## Checking this repository

Run `make check` with Bash, Python 3.9+, Make, and Git. The tests use Python's
standard library and temporary directories; they do not install packages or
contact external services. `PROJECT.md` remains the template for downstream
projects, not a filled identity sheet for this distribution repository.

Checks cover rule metadata and checklists, explicit backticked `.mdc` references,
activation catalogue completeness, shell syntax, all rule conversions, both
individual targets, repeat installation, invalid targets, and updates preserving
project customizations while refreshing owned rules and removing stale ones.
Hook tests cover missing/failed checks, command precedence, bypass flags, invalid
payloads, secret patterns across write/edit shapes, and safe placeholders.
The GitHub workflow runs the same command on Linux and macOS. Workflow changes
also require `actionlint .github/workflows/ruleset.yml`.

These tests intentionally use the standard library without an application
package or third-party test environment: this repository distributes documents
and a Bash installer. This is a repository-specific tooling choice, not a change
to the Python application rules distributed under `languages/`.

Review semantic consistency, rule applicability, and exceptions manually; the
static checker does not interpret every prose link or prove that agents obey
instructions. Add a regression test for every installer or conversion bug.
