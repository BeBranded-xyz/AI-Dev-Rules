# Test Plan

> Status of every test category from `docs/reference/testing-catalogue.md`.
> Every category is **required by default** (`core/testing.mdc`). Status is one of:
> `active` (tool + command + gate filled in), `planned YYYY-MM-DD` (blocking after
> that date), or `N/A: <reason>` (must be accepted by a reviewer).
> Gates: `commit` | `pr` | `pre-prod` | `deploy` | `prod`.

Last updated: {{YYYY-MM-DD}}
Owner: {{name}}

## Check command

`{{pnpm check}}` runs: {{format, lint, typecheck, unit, integration}}.

## Coverage and mutation thresholds

| Layer | Coverage target | Coverage floor | Mutation score floor |
|---|---|---|---|
| Business logic / data access | 100% lines and branches | 95% | 80% |
| Handlers / components | 100% | 85% | 70% |
| UI glue | as high as the framework allows | 70% | 60% |

Floors only go up; the target is always the maximum. Edit here and in the CI
config in the same PR. Tests that cannot be written yet are listed in
`BACKLOG.md` under "Missing tests".


## Foundations

| # | Category | Status | Tool | Command | Gate | Notes |
|---|---|---|---|---|---|---|
| 1 | Static Analysis | {{active}} | | | | |
| 2 | Unit Tests | {{active}} | | | | |
| 3 | Property-Based Testing | {{active}} | | | | |
| 4 | Mutation Testing | {{active}} | | | | |
| 5 | Component / Module Tests | {{active}} | | | | |
| 6 | Integration Tests | {{active}} | | | | |
| 7 | API Tests | {{active}} | | | | |
| 8 | Contract Tests | {{active}} | | | | |
| 9 | End-to-End (E2E) Tests | {{active}} | | | | |
| 10 | UI / Frontend Tests | {{active}} | | | | |
| 11 | Visual Regression Testing | {{active}} | | | | |
| 12 | Accessibility Testing | {{active}} | | | | |
| 13 | Regression Testing | {{active}} | | | | |
| 14 | Smoke Tests | {{active}} | | | | |
| 15 | Sanity Tests | {{active}} | | | | |

## Performance Testing

| # | Category | Status | Tool | Command | Gate | Notes |
|---|---|---|---|---|---|---|
| 16 | Load Testing | {{active}} | | | | |
| 17 | Stress Testing | {{active}} | | | | |
| 18 | Spike Testing | {{active}} | | | | |
| 19 | Soak / Endurance Testing | {{active}} | | | | |
| 20 | Scalability Testing | {{active}} | | | | |

## Reliability Testing

| # | Category | Status | Tool | Command | Gate | Notes |
|---|---|---|---|---|---|---|
| 21 | Failure Injection | {{active}} | | | | |
| 22 | Timeout Testing | {{active}} | | | | |
| 23 | Retry Testing | {{active}} | | | | |
| 24 | Failover Testing | {{active}} | | | | |
| 25 | Recovery Testing | {{active}} | | | | |
| 26 | Disaster Recovery Testing | {{active}} | | | | |
| 27 | Chaos Engineering | {{active}} | | | | |

## Security Testing

| # | Category | Status | Tool | Command | Gate | Notes |
|---|---|---|---|---|---|---|
| 28 | SAST | {{active}} | | | | |
| 29 | DAST | {{active}} | | | | |
| 30 | Dependency Security Testing | {{active}} | | | | |
| 31 | Authentication Testing | {{active}} | | | | |
| 32 | Authorization Testing | {{active}} | | | | |
| 33 | Injection Testing | {{active}} | | | | |
| 34 | Web Security Testing | {{active}} | | | | |
| 35 | Secret Scanning | {{active}} | | | | |
| 36 | Penetration Testing | {{active}} | | | | |

## Advanced Bug Detection

| # | Category | Status | Tool | Command | Gate | Notes |
|---|---|---|---|---|---|---|
| 37 | Fuzz Testing | {{active}} | | | | |
| 38 | Differential Testing | {{active}} | | | | |

## Database Testing

| # | Category | Status | Tool | Command | Gate | Notes |
|---|---|---|---|---|---|---|
| 39 | Database Tests | {{active}} | | | | |
| 40 | Migration Testing | {{active}} | | | | |

## Concurrency Testing

| # | Category | Status | Tool | Command | Gate | Notes |
|---|---|---|---|---|---|---|
| 41 | Race Condition Testing | {{active}} | | | | |
| 42 | Deadlock Testing | {{active}} | | | | |
| 43 | Idempotency Testing | {{active}} | | | | |

## Compatibility Testing

| # | Category | Status | Tool | Command | Gate | Notes |
|---|---|---|---|---|---|---|
| 44 | Browser Testing | {{active}} | | | | |
| 45 | Device Testing | {{active}} | | | | |
| 46 | Operating System Testing | {{active}} | | | | |
| 47 | Responsive Testing | {{active}} | | | | |

## Internationalization

| # | Category | Status | Tool | Command | Gate | Notes |
|---|---|---|---|---|---|---|
| 48 | Localization Testing | {{active}} | | | | |
| 49 | Date / Time Testing | {{active}} | | | | |
| 50 | Currency / Number Testing | {{active}} | | | | |

## Deployment Testing

| # | Category | Status | Tool | Command | Gate | Notes |
|---|---|---|---|---|---|---|
| 51 | Installation Testing | {{active}} | | | | |
| 52 | Upgrade Testing | {{active}} | | | | |
| 53 | Rollback Testing | {{active}} | | | | |
| 54 | Configuration Testing | {{active}} | | | | |

## Business Testing

| # | Category | Status | Tool | Command | Gate | Notes |
|---|---|---|---|---|---|---|
| 55 | Acceptance Testing | {{active}} | | | | |
| 56 | User Acceptance Testing (UAT) | {{active}} | | | | |
| 57 | Business Logic Testing | {{active}} | | | | |

## Human Testing

| # | Category | Status | Tool | Command | Gate | Notes |
|---|---|---|---|---|---|---|
| 58 | Exploratory Testing | {{active}} | | | | |
| 59 | Usability Testing | {{active}} | | | | |

## Production Testing & Monitoring

| # | Category | Status | Tool | Command | Gate | Notes |
|---|---|---|---|---|---|---|
| 60 | Error Monitoring | {{active}} | | | | |
| 61 | Logging | {{active}} | | | | |
| 62 | Metrics Monitoring | {{active}} | | | | |
| 63 | Distributed Tracing | {{active}} | | | | |
| 64 | Real User Monitoring (RUM) | {{active}} | | | | |
| 65 | Synthetic Monitoring | {{active}} | | | | |
| 66 | Uptime Monitoring | {{active}} | | | | |
| 67 | Business KPI Monitoring | {{active}} | | | | |

## Release Safety

| # | Category | Status | Tool | Command | Gate | Notes |
|---|---|---|---|---|---|---|
| 68 | Feature Flags | {{active}} | | | | |
| 69 | Canary Deployment | {{active}} | | | | |
| 70 | Blue/Green Deployment | {{active}} | | | | |
| 71 | Shadow Traffic | {{active}} | | | | |
| 72 | Automated Rollback | {{active}} | | | | |

## Human testing (after all automated gates are green)

| Activity | Cadence | Last run | Findings logged in |
|---|---|---|---|
| Exploratory session | every release | {{date}} | {{issues label}} |
| Usability test | {{quarterly}} | {{date}} | {{doc}} |
| UAT sign-off | every release | {{date}} | {{doc}} |
| Penetration test | before major launch + yearly | {{date}} | {{doc}} |
