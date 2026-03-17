# SaaS Starter Kit

**A ready-to-use foundation for building SaaS products — authentication, team management, Stripe billing, and permissions are already built. Just add your product features.**

---

## What is this?

Every SaaS app needs the same boring stuff before you can build the actual product:

- ✅ User signup/login (email + Google OAuth)
- ✅ Teams & organizations (invite members, assign roles)
- ✅ Subscription billing (Stripe checkout, invoices, cancel/upgrade)
- ✅ Permissions (who can see/edit what)
- ✅ API with documentation

This starter kit has all of that working. Fork it, add your product features, and launch.

```
┌─────────────────┐         ┌─────────────────┐
│   Next.js        │  REST   │   FastAPI        │
│   Frontend       │────────▶│   Backend        │
│                  │  API    │                  │
│  Landing page    │◀────────│  Auth (JWT+OAuth)│
│  Dashboard       │         │  Organizations   │
│  Settings        │         │  Stripe billing  │
│  Billing page    │         │  Role permissions │
└─────────────────┘         └────────┬─────────┘
                                     │
                            ┌────────▼─────────┐
                            │  PostgreSQL       │
                            │  + Redis          │
                            └──────────────────┘
```

---

## What problem does this solve?

**Without this:** You spend 2-3 months building login flows, password resets, team invitations, Stripe webhooks, and role-based permissions — before writing a single line of your actual product. Or you rush it and end up with security holes and billing bugs.

**With this:** All the infrastructure is done. The auth works. Stripe is wired up. Permissions are in place. You start building your actual product on day one.

---

## What's already built?

### Authentication (the "who are you?" part)
- Sign up with email + password (passwords hashed with `bcrypt`, 12 salt rounds)
- Log in with Google (OAuth 2.0 authorization code flow)
- Forgot password → reset via email (time-limited token, single-use)
- JWT tokens with automatic refresh (access token: 15min, refresh token: 7 days, rotated on use)

### Organizations (the "who's on your team?" part)
- Create an organization (your company/team)
- Invite people by email (invitation token with 48h expiry)
- 4 roles: Owner, Admin, Member, Viewer — enforced at the API level via dependency injection
- Switch between multiple organizations (JWT contains active `org_id`)

### Billing (the "how do they pay?" part)
- Free, Pro, and Enterprise plans
- Stripe Checkout (user clicks "Upgrade" → redirected to Stripe-hosted payment page → webhook confirms)
- Stripe Customer Portal (user manages their own subscription — cancel, upgrade, payment method)
- Webhook handling (`checkout.session.completed`, `invoice.paid`, `customer.subscription.deleted`)

### Developer Experience
- One command to start: `docker compose up -d`
- API docs auto-generated at `localhost:8000/docs` (Swagger UI from FastAPI)
- Hot reload — change code, see results instantly (both frontend and backend)

---

## Technical architecture

### Auth flow
```
User submits email + password
     │
     ▼
Backend verifies credentials (bcrypt.checkpw)
     │
     ▼
Issues JWT access token (15min) + refresh token (7 days)
     │                                    │
     ▼                                    ▼
Stored in httpOnly cookie           Stored in Redis
(XSS-safe, not accessible           (server can revoke
 from JavaScript)                    on logout/password change)
     │
     ▼
Every API request: middleware extracts JWT → verifies signature → injects user into request
     │
     ▼
Token expired? Frontend auto-calls /auth/refresh → gets new access token (transparent to user)
```

### Permission model
```python
# Roles are hierarchical: Owner > Admin > Member > Viewer
# Enforced via FastAPI dependency injection:

@router.delete("/projects/{id}")
async def delete_project(
    user: User = Depends(require_role(Role.ADMIN))  # Only Admin+ can delete
):
    ...

# Role checks happen before your endpoint code runs.
# Wrong role → 403 Forbidden, your code never executes.
```

### Stripe webhook flow
```
Stripe sends POST /api/billing/webhook
     │
     ▼
Verify signature (stripe.Webhook.construct_event) — rejects tampered payloads
     │
     ▼
Switch on event type:
  ├── checkout.session.completed → Activate subscription, update org plan
  ├── invoice.paid → Extend billing period, log payment
  ├── invoice.payment_failed → Notify org owner, grace period starts
  └── customer.subscription.deleted → Downgrade org to free plan
```

### Database schema
```
┌──────────┐       ┌─────────────────────┐       ┌──────────────┐
│  users   │       │ organization_members │       │ organizations│
├──────────┤       ├─────────────────────┤       ├──────────────┤
│ id (PK)  │──┐    │ id (PK)             │    ┌──│ id (PK)      │
│ email    │  └───▶│ user_id (FK)        │    │  │ name         │
│ password │       │ org_id (FK)    ◀────┼────┘  │ plan         │
│ name     │       │ role (enum)         │       │ stripe_id    │
│ oauth_id │       │ invited_at          │       │ created_at   │
└──────────┘       └─────────────────────┘       └──────────────┘
```

---

## Key design decisions

- **JWT + Redis, not sessions** — Stateless auth that scales horizontally. Any backend instance can verify a token without hitting the database. Redis stores refresh tokens for revocation (logout invalidates all sessions).
- **Refresh token rotation** — Every time a refresh token is used, a new one is issued and the old one is invalidated. Prevents replay attacks if a refresh token is stolen.
- **Role-based access via dependency injection** — Permissions are enforced as FastAPI `Depends()`, not decorators. This makes them composable and testable. `require_role(Role.ADMIN)` is a reusable dependency.
- **Stripe webhooks, not polling** — The app never asks Stripe "did they pay?" — Stripe pushes events. Webhook signature verification prevents spoofed payment confirmations.
- **Multi-tenancy via org_id** — Every query is scoped to the user's active organization. Middleware injects `org_id` from the JWT. No data leaks between organizations.
- **Rate limiting per IP** — Redis-backed sliding window rate limiter on all API endpoints. Prevents brute-force login attacks and API abuse. Default: 100 req/min.

---

## How to use it

```bash
# 1. Clone
git clone https://github.com/vmunjal2503/saas-starter-kit.git
cd saas-starter-kit

# 2. Configure
cp .env.example .env
# Add your Stripe keys, database URL, and Google OAuth credentials

# 3. Start
docker compose up -d

# 4. Open
# Your app:    http://localhost:3000
# API docs:    http://localhost:8000/docs
```

---

## How is the code organized?

```
saas-starter-kit/
├── frontend/                  # What the user sees (Next.js + React + Tailwind)
│   ├── src/pages/             # Landing page, login, dashboard, settings, billing
│   ├── src/components/        # Reusable UI: sidebar, forms, modals, toast notifications
│   ├── src/hooks/useAuth.ts   # Auth hook: login/logout state, auto token refresh
│   └── src/lib/api.ts         # Axios client with JWT interceptor (auto-attaches token, handles 401 → refresh)
│
├── backend/                   # The brain (FastAPI + Python)
│   ├── app/api/auth.py        # Login, signup, OAuth callback, password reset, token refresh
│   ├── app/api/organizations.py  # CRUD, invite members, assign roles, switch active org
│   ├── app/api/billing.py     # Stripe checkout session, customer portal, webhook handler
│   ├── app/api/users.py       # Profile management, avatar upload, change password
│   ├── app/models/user.py     # SQLAlchemy models: User, Organization, OrganizationMember
│   ├── app/services/auth_service.py  # JWT create/verify, bcrypt hashing, OAuth token exchange
│   └── app/middleware/rate_limit.py  # Redis sliding window rate limiter (100 req/min per IP)
│
├── docker-compose.yml         # Starts everything: frontend + backend + PostgreSQL + Redis
└── .env.example               # All the settings you need to configure
```

---

## Tech stack

| What | Technology | Why |
|------|-----------|-----|
| Frontend | Next.js, React, TypeScript, Tailwind | SSR for landing page SEO, type-safe, utility-first CSS |
| Backend | FastAPI, Python, SQLAlchemy | Async-first, auto-generated OpenAPI docs, dependency injection |
| Database | PostgreSQL | ACID transactions, JSONB for flexible fields, proven at scale |
| Cache | Redis | Sub-ms reads for rate limiting, session storage, refresh token revocation |
| Payments | Stripe | PCI-compliant, webhook-driven, handles 135+ currencies |
| Auth | JWT + Google OAuth | Stateless tokens scale horizontally, OAuth reduces signup friction |

---

## Who is this for?

- Founders who want to launch a SaaS without building auth and billing from scratch
- Developers starting a new project who want a solid, modern architecture to build on
- Freelancers building SaaS products for clients (use this as your starting point)

---

Built by **Vikas Munjal** | Open source under MIT License
