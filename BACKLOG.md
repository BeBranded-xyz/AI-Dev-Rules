# Ruleset backlog

This file tracks work on the ruleset repository. Downstream projects receive
`templates/BACKLOG.md`, not this file.

## Decisions pending

None.

## Done

- Added the shared design system and its six approved supporting rules.
- Added validated configuration, authoritative business rules, preservation of
  existing work, external-content trust boundaries, and architecture enforcement.
- Added conditional data lifecycle and audit trail modules.
- Added local/CI ruleset checks, installer regression tests, and corrected broken
  maintenance references, missing activation fields, and missing checklists found
  by the checks.

- B-001: Unified mutation feedback policy in `modules/data-fetching.mdc`, with
  safe optimistic eligibility, confirmed sensitive writes, and concurrency tests
  required in consuming projects.
- Hardened and regression-tested Claude commit/write hooks; documented scope.
- Defined scoped adoption and legacy-gap tracking for existing projects.
- Added the ruleset changelog, consumer migration steps, distribution, and update
  version-transition reporting while preserving the application changelog.
