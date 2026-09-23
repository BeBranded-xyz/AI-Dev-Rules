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
- **Check command** (format + lint + typecheck + unit + integration; must be
  green before any commit): {{`pnpm check`}}
- **Build / start**: {{e.g. `pnpm build` / `pnpm start`}}
- **Deployment target**: {{e.g. Vercel / Webflow Cloud / Fly.io / self-hosted}}
- **What triggers a deploy**: PR merged into protected `main` -> impact analysis
  -> required checks -> affected units only (see delivery plan below).

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
| Background jobs | {{Vercel cron / Cloudflare cron / BullMQ / Inngest / none}} | |
| Feature flags | {{PostHog / Flagship / env-based / none}} | |
| Release tooling | {{release-please / changesets / semantic-release}} | |
| LLM provider (if the product calls LLMs) | {{Anthropic / none}} | {{data retention setting, region}} |
| Other | {{...}} | |

## 4. Languages & conventions

- **Code, identifiers, comments**: {{English}}
- **Commit messages**: {{English, conventional commits}}
- **User-facing content (UI, emails)**: {{French}}
- **Internal docs**: {{French accepted}} — **Technical docs / READMEs**: {{English}}
- **Tone**: {{technical and factual}}
- **Emojis in code / commits / technical docs**: {{not allowed}}
- **Size limit overrides** (see `code-standards.mdc`; never above 2x, function
  limit never overridden): {{none}}
- **Documented size-limit exemptions** (file paths): {{generated types, ...}}

### Design system (projects with a UI)

- **Token source and generated outputs**: {{paths; generation command}}
- **Shared components / package and public API**: {{paths / import entry point}}
- **Styling approach**: {{Tailwind / CSS modules / native styling / other}}
- **Component catalogue**: {{Storybook or equivalent; path / command}}
- **Supported themes**: {{light / dark / brand themes}}
- **Icon library and custom assets**: {{library; central asset path}}
- **Design system documentation / exceptions**: {{path}}
- **Enforcement and visual verification commands**: {{commands; see TEST_PLAN.md}}

## 5. Environments & domains

| Environment | URL / host | Notes |
|---|---|---|
| Production | {{https://example.com}} | |
| Preview / staging | {{...}} | |
| Local | {{http://localhost:3000}} | |

- **Mount path / base path** (if app is not at root): {{e.g. /app}}

### CI/CD and deployment plan

- **Delivery plan and dependency graph**: {{document path; review before implementation}}
- **Required checks / main branch protection**: {{check names / PR merge policy}}
- **Affected-unit selector and tests**: {{command / test command}}
- **Deployment state**: {{per unit/environment: last successful SHA and artifact store}}
- **Ordering, concurrency, failure, and rollback**: {{runbook sections}}
- **Hosting auto-deploy filters / CI ownership**: {{one owner per unit/environment}}

| Deployable unit | Source and shared inputs | Target / deployment owner | Build / verify / deploy | Rollback |
|---|---|---|---|---|
| {{web / API / worker / migrations}} | {{paths and transitive dependencies}} | {{environment / hosting or CI}} | {{commands}} | {{artifact / procedure}} |

## 6. Repository structure

```
{{paste the actual top-level folder tree here, with one-line descriptions.
Keep this in sync with the real structure — update in the same PR as a move.}}
```

- **Monorepo?**: {{No / Yes — workspaces: ...}}

### Configuration and architecture

- **Validated configuration boundaries**: {{server / client / worker paths}}
- **Module owners, public APIs, allowed dependency graph**: {{document path}}
- **Architecture enforcement command and exceptions**: {{command / document}}

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

### Domain ownership and data governance

- **Authoritative business rule implementations**: {{domain -> owner / module}}
- **State transitions and policy contracts**: {{document / schema paths}}
- **Data lifecycle inventory**: {{category -> owner, stores, retention, deletion SLA}}
- **Deletion, archival, and restore procedures**: {{runbook sections}}
- **Audit event catalogue and storage**: {{document / schema / sink}}
- **Audit access, retention, and failure policy**: {{roles / duration / behavior}}

## 8. Public identifiers

> Non-secret identifiers the team needs. **Never put API keys or secrets here** —
> those live only in env vars / a secret manager.

| Key | Value |
|---|---|
| {{Supabase project ref}} | {{...}} |
| {{Region}} | {{e.g. eu-west (GDPR)}} |
| {{External base / account IDs}} | {{...}} |

## 9. Active rules

Core rules always apply (`core/`): project identity, AI workflow, code
standards, security, error handling, testing, dependencies, git workflow.
Tick everything else that applies so contributors and AI load the right rules.
A rule for a tech you don't use is ignored.

**Languages** (`languages/`)
- [ ] `typescript`
- [ ] `python`
- [ ] `go`
- [ ] `rust`
- [ ] `php` (incl. WordPress)
- [ ] `swift` (iOS / macOS)
- [ ] `kotlin-android` (native Android)
- [ ] `react-native` (Expo)
- [ ] `sql`
- [ ] `shell`

**Platforms** (`platforms/`)
- [ ] `nextjs`
- [ ] `supabase`
- [ ] `cloudflare-workers`
- [ ] `webflow`
- [ ] `vercel`

**Modules** (`modules/`)
- [ ] `database` — relational DB, migrations, RLS
- [ ] `data-lifecycle` — retention, archival, deletion propagation, safe restores (persistent user or business data)
- [ ] `audit-trail` — durable, access-controlled history of sensitive operations
- [ ] `auth` — authentication & session management
- [ ] `integrations` — external services, webhooks, sync, serverless functions
- [ ] `api-design` — REST/RPC conventions, error envelope, versioning, OpenAPI
- [ ] `frontend` — components, accessibility, Core Web Vitals, design tokens
- [ ] `design-system` — shared components, semantic tokens, themes, catalogue, icons, enforcement (required for projects with a UI)
- [ ] `data-fetching` — fast reads, safe optimistic updates, confirmed sensitive writes, one data layer
- [ ] `i18n` — locales, dates/times, currencies, RTL
- [ ] `performance` — budgets, caching, load testing
- [ ] `background-jobs` — crons, queues, workers
- [ ] `observability` — error tracking, tracing, structured logging
- [ ] `infra` — CI/CD, Docker, IaC, environments
- [ ] `deployments` — planned CI/CD, PR-to-main triggers, affected units, deployment state
- [ ] `releases` — versioning, changelog, flags, progressive delivery
- [ ] `ai-features` — the product calls LLMs
- [ ] `maintenance` — monthly ritual, debt register (recommended for every project past MVP)
- [ ] `graphify` — knowledge-graph tooling (`graphify-out/`)

**Testing**: maximal by default (`core/testing.mdc`). Status per category is
tracked in `TEST_PLAN.md`; every category is required unless justified there.

## 10. Reference documents

| Doc | Purpose |
|---|---|
| `TEST_PLAN.md` | Status, tooling, command, and gate for every test category |
| `BACKLOG.md` | Everything still to do; nothing lives only in a chat or a head |
| `docs/FUNCTIONS_REGISTRY.md` | Every function, route, webhook, job |
| `docs/MIGRATIONS_CHANGELOG.md` | Human-readable migration history |
| `docs/FEATURE_FLAGS.md` | Flags with removal dates |
| `docs/DEBT.md` | Deliberate shortcuts with deadlines |
| `docs/RUNBOOK.md` | Alerts, procedures, kill switches |
| `docs/adr/` | Architecture decision records |
| {{docs/<schema>.md}} | {{Data model}} |
| {{...}} | {{...}} |

### Ruleset adoption (existing projects)

- **Baseline date and check results**: {{date / report path / existing failures}}
- **Legacy gaps and migration plan**: {{BACKLOG.md / docs/DEBT.md references}}
- **Scoped temporary exceptions**: {{rule, files, owner, reason, expiry, issue}}
- **Ruleset migration review**: {{source and target SHA / reviewed changelog entries}}

## 11. Key architecture decisions

- {{Why this DB / auth / deployment choice was made — 1-2 lines each.}}
- {{...}}

## 12. Budgets and thresholds

| Budget | Value |
|---|---|
| p95 latency, API reads / writes | {{200 ms / 500 ms}} |
| Page weight / JS bundle (initial) | {{< 1 MB / < 200 kB gz}} |
| Core Web Vitals | LCP < 2.5 s, INP < 200 ms, CLS < 0.1 |
| DB query p95 | {{50 ms}} |
| Job duration max | {{5 min}} |
| Error rate alert / canary rollback | {{1% over 5 min}} |
| Coverage / mutation floors | see `TEST_PLAN.md` |

## 13. Secrets and access (dates only, never values)

| Secret | Where it lives | Last rotated | Rotation cadence |
|---|---|---|---|
| {{DATABASE_URL}} | {{platform secret store}} | {{YYYY-MM-DD}} | {{6 months}} |

## 14. External systems — do not assume undocumented behavior

Rely on official docs only for these; do not extrapolate from other projects:

- {{e.g. Deployment platform routing & cache behavior}}
- {{e.g. Webhook payload structure & signature validation}}
- {{e.g. Third-party API rate limits & quotas}}
