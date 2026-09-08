# Runbook

> Operational procedures for {{PROJECT_NAME}}. Every alert in the error
> tracker or monitoring links to a section here. Updated whenever an incident
> reveals a missing step (`core/maintenance.mdc`).

Last updated: {{YYYY-MM-DD}}

## Contacts and escalation

| Role | Who | Reach |
|---|---|---|
| On-call | {{name}} | {{channel}} |
| Escalation | {{name}} | {{channel}} |
| Vendor support | {{platform}} | {{link}} |

## Dashboards and tools

| What | Where |
|---|---|
| Error tracker | {{url}} |
| Logs | {{url}} |
| Metrics / uptime | {{url}} |
| Deploys | {{url}} |
| Feature flags | {{url}} / `FEATURE_FLAGS.md` |

## Alerts -> procedure

| Alert | Severity | First checks | Procedure |
|---|---|---|---|
| Error rate > {{1%}} on {{surface}} | page | Recent deploy? Upstream status? | [Rollback](#rollback) |
| Webhook signature failures | high | Provider rotated secret? Attack? | [Rotate webhook secret](#rotate-a-secret) |
| Sync failures > {{threshold}} | high | Provider rate limit? Schema drift? | [Replay sync](#replay-a-sync) |
| DB pool saturation | page | Long queries? Missing index? | [DB pressure](#database-pressure) |
| Uptime check failing | page | DNS? TLS? Platform incident? | [Outage](#outage) |

## Procedures

### Rollback
1. {{deploy command --rollback}} or redeploy the previous tag.
2. Confirm smoke tests pass on the rolled-back version.
3. Open an incident issue; link the failing release.

### Rotate a secret
1. Generate the new value in the provider.
2. Set it in the secret store for every environment.
3. Redeploy; verify the consumer works; revoke the old value.
4. Record the rotation date in `PROJECT.md` section 8 notes.

### Replay a sync
{{steps}}

### Database pressure
{{steps: identify with pg_stat_activity, kill, add index via migration}}

### Outage
{{steps}}

### Restore from backup
{{steps, including the last drill date and result}}

## Kill switches

| Flag | Effect | Where to flip |
|---|---|---|
| {{disable_checkout}} | {{Shows maintenance notice on checkout}} | {{url}} |

## Post-incident

Every page-level incident gets a blameless write-up within 5 working days:
timeline, root cause, what detected it, what did not, action items with owners
and dates, and the regression test that now covers it.
