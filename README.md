# AI Development Rules

A reusable, project-agnostic set of engineering rules for building apps with AI
assistants (Cursor, Claude Code, etc.). Clone it into a new project, fill in one
identity file, and every rule applies without edits.

## How it works

- **`PROJECT.md`** is the only file with project-specific facts: what the project
  is, how it runs, the stack, conventions, structure, business invariants, public
  identifiers, and which rule modules are active.
- Every **`.mdc` rule** is written to be generic and defers to `PROJECT.md` for
  concrete details. A rule for a technology you don't use can be ignored.

## Usage

1. Copy these files into your project (e.g. into `.cursor/rules/` for the `.mdc`
   files, and `PROJECT.md` + `README` reference at the root — adapt to your tool).
2. Fill in **`PROJECT.md`**: replace every `{{PLACEHOLDER}}`, tick the active rule
   modules, delete sections that don't apply.
3. Keep `PROJECT.md` up to date in the same PR whenever the stack, structure, or a
   key decision changes. Never hardcode project facts back into the generic rules.
4. Never put secrets in `PROJECT.md` — only public identifiers.

## Files

| File | Scope | Applies |
|---|---|---|
| `PROJECT.md` | The identity sheet (fill this in) | — |
| `project-identity.mdc` | Points to `PROJECT.md`, explains the ruleset | always |
| `code-standards.mdc` | Size limits, architecture, naming, TypeScript, dead code | always |
| `security.mdc` | Secrets, authorization, validation, privacy | always |
| `github-workflow.mdc` | Git, commits, PRs, documentation | git/docs files |
| `observability.mdc` | Error tracking, tracing, structured logging | always (if a tool is configured) |
| `database.mdc` | Migrations, RLS, clients, queries | if relational DB |
| `auth.mdc` | Authentication & sessions | if user auth |
| `integrations.mdc` | Serverless functions, webhooks, third-party APIs, sync | if external services |
| `graphify.mdc` | Knowledge-graph tooling | if graphify is used |

The `alwaysApply` / `globs` front-matter in each `.mdc` controls when it loads in
Cursor. Tools that don't read front-matter (e.g. Claude Code) can treat them as
plain Markdown guidance.
