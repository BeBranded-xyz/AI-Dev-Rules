# {{PROJECT_NAME}}

This project uses the shared AI development ruleset. This file is the entry
point for agents that read `AGENTS.md` (Codex and compatible tools). Read in
this order before any task:

1. `PROJECT.md` (the only file with project-specific facts)
2. `TEST_PLAN.md` (status of every test category; maximal testing is the default)
3. `BACKLOG.md` (what is still to do; add every discovery, close what you finish)
4. Every rule listed under "Always apply" below, then the language, platform,
   and module rules that `PROJECT.md` section 9 marks active, before touching
   the files they cover

The rule files are the source of truth. This file only points to them; do not
copy their content here.

## Non-negotiables

- Work per `{{RULES_ROOT}}/rules/core/ai-workflow.md`: read `PROJECT.md` first,
  plan multi-file changes, write tests with the code, run the check command
  before reporting done, never claim an unrun verification.
- Check command: `{{pnpm check}}`. Run it yourself before every commit: no tool
  hook enforces it for this agent, and it must be green. Never commit with
  `--no-verify`.
- Tests: the maximum the change allows, across the categories in
  `core/testing` ("what every change must add" is the floor). Bug fixes start
  with a failing regression test.
- Backlog: anything noticed but not done goes in `BACKLOG.md` in the same turn;
  close items you finish.
- Secrets: never write credentials, tokens, keys, or real `.env` files. Use
  obvious placeholders in examples and fixtures. No hook scans your writes, so
  CI secret scanning is the only safety net: do not rely on it.
- Never touch production data or services from a development task.
- Never run destructive commands (reset, drop, force-push, mass delete)
  without explicit confirmation.
- Code, identifiers, comments, commits, and docs are in English.

## Procedures

The step-by-step procedures for checks, the test plan, migrations, new
functions, releases, and health checks live in `{{RULES_ROOT}}/skills/*/SKILL.md`.
Follow them as written instead of re-deriving the procedure.
