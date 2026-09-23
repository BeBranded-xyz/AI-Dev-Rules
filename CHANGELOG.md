# Ruleset changelog

This changelog describes the shared ruleset, not any consuming application's
releases. Installed commits are recorded in `.ruleset-version`. Entries remain
under Unreleased until committed/released; the installed SHA is the precise
version reference. Do not imply that uncommitted edits have a released version.

## Unreleased

### New requirements

- Shared design system: semantic tokens, reusable components, explicit variants
  and states, catalogue, consistent icons, and automated enforcement.
- Validated configuration boundaries, authoritative business rule ownership,
  architecture dependency checks, preservation of existing work, and protection
  against instructions embedded in external content.
- Optional `data-lifecycle` and `audit-trail` modules, activated according to the
  project's persistent data and sensitive operations.
- Scoped adoption for existing projects: baseline findings and planned migration,
  with documented temporary legacy exceptions and no blanket rewrite.
- Ruleset integrity, installation, update, and hook regression tests via
  `make check`, with Linux/macOS CI.

### Behavior changes

- `modules/data-fetching.mdc` owns the mutation feedback policy. Optimistic UI
  requires predictable results, low risk, and reliable rollback. Money,
  permissions, destructive/irreversible actions, scarce-resource reservations,
  and unpredictable output wait for server confirmation. Offline replay follows
  the same restrictions; rollback must preserve newer successful writes.
- Claude's pre-commit hook now blocks recognized commits when the check command
  is absent, empty, whitespace-only, or failing, and blocks malformed hook input
  or an inaccessible verification directory. Verification logs are private
  temporary files, removed on exit.
- The write hook scans docs, examples, and fixtures as well as code. Malformed
  payloads or decoding failures block writes. Placeholder examples remain valid;
  credential-shaped example values must be replaced with obvious placeholders.
- `init.sh` distributes this file as `docs/reference/ruleset-changelog.md`,
  refreshes it on update, and prints the previous/current installed SHA.
  It never overwrites the application's own `CHANGELOG.md`.

### Migration for consuming projects

1. Before updating, record `.ruleset-version`, read the source ruleset changelog
   for intervening changes, and capture the project's current check results.
   If the installed SHA is unavailable, compare installed files with the source
   rather than assuming a clean or fully migrated state.
2. Configure and run the real verification command. For Claude, store it on one
   line in `.claude/check-command` or supply `CHECK_COMMAND`; the documented
   ecosystem fallbacks remain available. A no-op is not a valid verification.
3. Run `init.sh --dest <project> --target <installed-target> --update` and review
   the diff and the installed ruleset changelog. Pass the target explicitly when
   the project uses only Claude or only Cursor.
4. Existing `PROJECT.md`, `TEST_PLAN.md`, workflows, registries, and Claude
   settings are preserved. Manually add applicable new module entries and the
   configuration, architecture, governance, and adoption fields from the template.
   Check hook wiring against the source settings; update does not merge it for you.
5. Classify existing mutations using the new feedback policy. Prioritize money,
   permissions, destructive operations, reservations, and unsafe offline queues;
   add pending/confirmation tests and overlapping-write rollback coverage.
6. Replace credential-shaped examples with placeholders. Keep repository/CI secret
   scanning enabled: Claude hooks do not cover shell writes, other editors, or
   every possible command spelling and are not a security sandbox.
7. Inventory unrelated legacy gaps in `BACKLOG.md`/`docs/DEBT.md`, with owners and
   scoped migration steps. Apply rules to the changed scope without rewriting
   the entire project. Report existing failing checks honestly.
8. Run the project check and relevant tests, audit `TEST_PLAN.md`, and record the
   source/target SHA plus migration completion in `PROJECT.md`. The installed SHA
   records file distribution, not proof that every migration has been completed.

### Corrections

- Fixed stale maintenance rule references, missing rule activation metadata,
  and missing checklists detected by the integrity checks.

## Historical baseline

Changes before this changelog are documented by Git history. No release dates
or version numbers have been reconstructed. Use the installed SHA to determine
which baseline a consuming project actually has.
