# Migrations Changelog

> Human-readable history of every schema and data migration
> (`modules/database.mdc`). One entry per migration file, added in the same PR.
> Applied migrations are never modified; a correction is a new migration.

Last updated: {{YYYY-MM-DD}}

## Format

```
## YYYYMMDDHHMMSS_short_description
- Date: YYYY-MM-DD
- Type: schema | data | schema+data
- Tables: table_a, table_b
- Summary: what and why, 1-3 sentences
- Breaking: no | yes (expand/contract step N of M)
- Rollback: documented in header | rollbacks/YYYYMMDDHHMMSS_short_description.sql
- RLS: policies added/changed
- Types regenerated: yes
- PR: #123
```

## Entries

## {{20260101120000_create_orders}}
- Date: {{2026-01-01}}
- Type: schema
- Tables: {{orders, order_items}}
- Summary: {{Introduce orders with line items and pickup slot reference.}}
- Breaking: no
- Rollback: documented in header
- RLS: {{orders_select_own, orders_insert_own}}
- Types regenerated: yes
- PR: {{#1}}
