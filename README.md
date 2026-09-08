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
  faithfully (`core/ai-workflow.mdc`). Hooks make the check command a hard
  gate before every commit.
- **Maximal testing by default**: all 72 test categories of the catalogue are
  required unless justified in the project's `TEST_PLAN.md`
  (`core/testing.mdc`). The goal is to break the program against tests until
  as few defects as possible reach production or human testing.
- **Engineering baseline**: size limits, architecture, type safety, error
  taxonomy, security, dependency policy, git workflow, documentation as a
  deliverable.
- **Per language, platform, and module rules** activated from `PROJECT.md`.

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
languages/                  Apply per language (globs)
  typescript, python, go, rust, php (incl. WordPress), swift,
  kotlin-android, react-native, sql, shell
platforms/                  Apply per platform (globs)
  nextjs, supabase, cloudflare-workers, webflow, vercel
modules/                    Apply when PROJECT.md marks them active
  database, auth, integrations, api-design, frontend, data-fetching, i18n, performance,
  background-jobs, observability, infra, releases, ai-features,
  maintenance, graphify
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
init.sh                     Bootstrap script
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

## Updating an existing project

```bash
cd rules && git pull
./init.sh --dest ../my-project --update
```

`--update` overwrites only what the ruleset owns: the rules in
`.cursor/rules/` and `.claude/rules/`, the hooks, the skills, the testing
catalogue, and the helper scripts. It removes rule files that no longer exist
upstream, adds new template files that the project does not have yet, and
never touches project-owned files (`PROJECT.md`, `TEST_PLAN.md`,
`BACKLOG.md`, `CLAUDE.md` above its on-demand section, `.env.example`,
registries, workflows, `.claude/settings.json`). The ruleset commit is
recorded in `.ruleset-version` so `/health-check` can tell when a project is
behind. Then review the diff, tick any new module in `PROJECT.md` section 9,
run `/test-plan` to audit, and commit as `chore(rules): update ruleset to <sha>`.

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
