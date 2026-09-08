# Technical Debt Register

> Every deliberate shortcut is logged here when it is taken, with a deadline
> (`core/maintenance.mdc`). Deadlines are enforced like `@deprecated` dates:
> past the deadline, the item blocks the next release until paid or
> re-negotiated with a new dated entry. Reviewed monthly.

Last updated: {{YYYY-MM-DD}}

## Open

| ID | Taken on | What was skipped or simplified | Why | Risk if unpaid | Removal plan | Owner | Deadline | Issue |
|---|---|---|---|---|---|---|---|---|
| D-001 | {{2026-01-15}} | {{Order export runs synchronously in the request}} | {{Ship MVP; volume < 100/day}} | {{Timeouts past ~1k orders}} | {{Move to background job, see background-jobs.mdc}} | {{name}} | {{2026-03-31}} | {{#42}} |

## Paid

| ID | Paid on | PR | Notes |
|---|---|---|---|
| | | | |

## Re-negotiated

| ID | Old deadline | New deadline | Approved by | Reason |
|---|---|---|---|---|
| | | | | |
