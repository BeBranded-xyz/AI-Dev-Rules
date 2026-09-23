# {{PROJECT_NAME}}

This project uses the shared AI development ruleset. Read in this order:

1. `@PROJECT.md` (the only file with project-specific facts)
2. `@TEST_PLAN.md` (status of every test category; maximal testing is the default)
3. `@BACKLOG.md` (what is still to do; add every discovery, close what you finish)
4. The rules in `.claude/rules/` (loaded automatically; core rules always apply,
   language / platform / module rules apply per `PROJECT.md` section 9)

## Non-negotiables

- Work per `.claude/rules/core/ai-workflow.md`: read `PROJECT.md` first, plan
  multi-file changes, write tests with the code, run the check command before
  reporting done, never claim an unrun verification.
- Check command: `{{pnpm check}}`. It must be green before any commit.
- Tests: the maximum the change allows, across the categories in
  `core/testing.md` ("what every change must add" is the floor). Bug fixes
  start with a failing regression test.
- Backlog: anything noticed but not done goes in `BACKLOG.md` in the same
  turn; close items you finish.
- Never touch production data or services from a development task.
- Never run destructive commands (reset, drop, force-push, mass delete)
  without explicit confirmation.
- Code, identifiers, comments, commits, and docs are in English.

## Commands

| Task | Command |
|---|---|
| Install | `{{pnpm install --frozen-lockfile}}` |
| Dev server | `{{pnpm dev}}` |
| Check (format + lint + typecheck + unit + integration) | `{{pnpm check}}` |
| E2E | `{{pnpm test:e2e}}` |
| DB migrate / reset / types | `{{pnpm db:migrate}}` / `{{pnpm db:reset}}` / `{{pnpm db:types}}` |
| Build | `{{pnpm build}}` |

## Skills

`/check`, `/test-plan`, `/new-migration`, `/new-function`, `/release`,
`/health-check` are available in `.claude/skills/`. Use them instead of
re-deriving the procedure.

## Hooks

- Pre-commit: blocks recognized `git commit` calls when the check command is
  missing, blank, or fails. Never bypass with `--no-verify`.
- Pre-write: blocks secret-like strings in code, docs, examples, and fixtures.
  These tool hooks complement CI; they do not cover other editors or shell writes.
