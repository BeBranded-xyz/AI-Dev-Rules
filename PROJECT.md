# Project Identity

> **This is the only file that should contain project-specific facts.**
> Fill every `{{PLACEHOLDER}}` and delete any section that does not apply.
> All the `.mdc` rules in this repository are written to be project-agnostic and
> defer to this file for the concrete stack, identifiers, and conventions.
>
> Keep this file up to date in the same PR whenever the stack, structure, or a
> key decision changes. Never put secrets here (only public identifiers).

Last updated: {{YYYY-MM-DD}}

---

## 1. What this project is

- **Name**: {{PROJECT_NAME}}
- **One-line description**: {{What it does, for whom.}}
- **Domain / problem**: {{2-4 sentences. What problem it solves, the business
  context, what makes it non-trivial.}}
- **Status**: {{prototype | MVP | in production}}

## 2. How it runs

- **Primary runtime**: {{e.g. Next.js app (App Router) + serverless functions}}
- **Entry points**: {{e.g. web app at /, marketing site, mobile, CLI, cron jobs}}
- **Local dev command(s)**: {{e.g. `pnpm dev`, `supabase start`}}
- **Build / start**: {{e.g. `pnpm build` / `pnpm start`}}
- **Deployment target**: {{e.g. Vercel / Webflow Cloud / Fly.io / self-hosted}}
- **What triggers a deploy**: {{e.g. push to `main` auto-deploys}}

## 3. Tech stack

| Layer | Technology | Notes |
|---|---|---|
| App framework | {{Next.js 15}} | |
| UI | {{React 19, Tailwind}} | |
| Data fetching / cache | {{TanStack Query}} | |
| Validation | {{Zod}} | |
| Database | {{Supabase / Postgres}} | |
| Authentication | {{Better Auth / Supabase Auth / NextAuth / none}} | |
| File storage | {{Supabase Storage / S3 / none}} | |
| Serverless / backend logic | {{Supabase Edge Functions / API routes}} | |
| Email | {{Brevo / Resend / none}} | |
| Monitoring / errors | {{Sentry / none}} | |
| Other | {{...}} | |

## 4. Languages & conventions

- **Code, identifiers, comments**: {{English}}
- **Commit messages**: {{English, conventional commits}}
- **User-facing content (UI, emails)**: {{French}}
- **Internal docs**: {{French accepted}} — **Technical docs / READMEs**: {{English}}
- **Tone**: {{technical and factual}}
- **Emojis in code / commits / technical docs**: {{not allowed}}

## 5. Environments & domains

| Environment | URL / host | Notes |
|---|---|---|
| Production | {{https://example.com}} | |
| Preview / staging | {{...}} | |
| Local | {{http://localhost:3000}} | |

- **Mount path / base path** (if app is not at root): {{e.g. /app}}

## 6. Repository structure

```
{{paste the actual top-level folder tree here, with one-line descriptions.
Keep this in sync with the real structure — update in the same PR as a move.}}
```

- **Monorepo?**: {{No / Yes — workspaces: ...}}

## 7. Data & source of truth

- **Application database**: {{Supabase Postgres — owns: ...}}
- **External source of truth** (if any): {{Airtable / Stripe / none — owns: ...}}
- **Sync model** (if external SoT exists): {{one-way / bidirectional; trigger:
  webhook / cron; see the `integrations` rule for the generic safety rules}}

### Business invariants

> Hard rules that must never be violated by code or sync. These are the
> project-specific facts the generic rules refer to.

- {{e.g. A sales counter is monotonic — never decrement `quantity_sold`.}}
- {{e.g. Customer status ladder is upgrade-only: Prospect → Client → Ambassadeur.}}
- {{e.g. Cart reservations have a 15-min TTL and live only in the app DB.}}
- {{...}}

## 8. Public identifiers

> Non-secret identifiers the team needs. **Never put API keys or secrets here** —
> those live only in env vars / a secret manager.

| Key | Value |
|---|---|
| {{Supabase project ref}} | {{...}} |
| {{Region}} | {{e.g. eu-west (GDPR)}} |
| {{External base / account IDs}} | {{...}} |

## 9. Active rule modules

Tick the modules that apply so contributors (and AI) know which `.mdc` rules are
in force. A rule for a tech you don't use can be ignored.

- [ ] `database` — relational DB, migrations, RLS
- [ ] `auth` — authentication & session management
- [ ] `integrations` — external services, webhooks, sync, serverless functions
- [ ] `observability` — error tracking, tracing, structured logging
- [ ] `graphify` — knowledge-graph tooling (`graphify-out/`)

## 10. Reference documents

| Doc | Purpose |
|---|---|
| {{docs/architecture/decisions.md}} | {{Product/architecture decisions}} |
| {{docs/<schema>.md}} | {{Data model}} |
| {{...}} | {{...}} |

## 11. Key architecture decisions

- {{Why this DB / auth / deployment choice was made — 1-2 lines each.}}
- {{...}}

## 12. External systems — do not assume undocumented behavior

Rely on official docs only for these; do not extrapolate from other projects:

- {{e.g. Deployment platform routing & cache behavior}}
- {{e.g. Webhook payload structure & signature validation}}
- {{e.g. Third-party API rate limits & quotas}}
