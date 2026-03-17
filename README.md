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
- Sign up with email + password
- Log in with Google (OAuth)
- Forgot password → reset via email
- JWT tokens with automatic refresh (user stays logged in)

### Organizations (the "who's on your team?" part)
- Create an organization (your company/team)
- Invite people by email
- 4 roles: Owner, Admin, Member, Viewer
- Switch between multiple organizations

### Billing (the "how do they pay?" part)
- Free, Pro, and Enterprise plans
- Stripe Checkout (user clicks "Upgrade" → Stripe handles the payment page)
- Stripe Customer Portal (user manages their own subscription)
- Webhook handling (Stripe tells your app when payments succeed/fail)

### Developer Experience
- One command to start: `docker compose up -d`
- API docs auto-generated at `localhost:8000/docs`
- Hot reload — change code, see results instantly

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
│   ├── src/pages/             # Landing page, login, dashboard, settings
│   ├── src/components/        # Reusable UI pieces (sidebar, forms, modals)
│   ├── src/hooks/             # useAuth — handles login/logout state
│   └── src/lib/api.ts         # Talks to the backend API
│
├── backend/                   # The brain (FastAPI + Python)
│   ├── app/api/auth.py        # Login, signup, password reset, OAuth
│   ├── app/api/organizations.py  # Create teams, invite members, assign roles
│   ├── app/api/billing.py     # Stripe checkout, subscriptions, webhooks
│   ├── app/api/users.py       # User profile management
│   ├── app/models/user.py     # Database tables (User, Organization, Membership)
│   ├── app/services/auth_service.py  # JWT tokens, password hashing
│   └── app/middleware/rate_limit.py  # Prevents API abuse
│
├── docker-compose.yml         # Starts everything: frontend + backend + database + Redis
└── .env.example               # All the settings you need to configure
```

---

## Tech used

| What | Technology | Why |
|------|-----------|-----|
| Frontend | Next.js, React, TypeScript, Tailwind | Fast, type-safe, looks good |
| Backend | FastAPI, Python, SQLAlchemy | Fast API framework with auto-generated docs |
| Database | PostgreSQL | Reliable, handles everything a SaaS needs |
| Cache | Redis | Fast session storage and rate limiting |
| Payments | Stripe | Industry standard for SaaS billing |
| Auth | JWT + Google OAuth | Secure, stateless, users can log in with Google |

---

## Who is this for?

- Founders who want to launch a SaaS without building auth and billing from scratch
- Developers starting a new project who want a solid, modern architecture to build on
- Freelancers building SaaS products for clients (use this as your starting point)

---

Built by **Vikas Munjal** | Open source under MIT License
