# SaaS Starter Kit — Next.js + FastAPI + PostgreSQL

Production-ready SaaS boilerplate with authentication, multi-tenancy, Stripe billing, and role-based access control. Ship your SaaS in days, not months.

## Why I Built This

**The Problem:** Every SaaS application needs the same foundational features — user authentication, team/organization management, subscription billing, and role-based permissions. Founders and developers waste 2-3 months building these boring-but-critical features before they can write a single line of actual product code. And when they rush it, they end up with security vulnerabilities, billing bugs, and spaghetti auth logic.

**The Solution:** This starter kit gives you a production-grade foundation with JWT + OAuth authentication, multi-tenant organizations, Stripe subscriptions (checkout, portal, webhooks), and RBAC — all wired up and working. Fork it, swap in your product features, and launch in days instead of months.

**Built from building SaaS products** and seeing the same patterns repeated across dozens of projects. This captures the architecture I'd use if I were starting a new SaaS today — clean separation of concerns, type safety, and infrastructure-ready with Docker and Terraform.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Architecture                                 │
│                                                                     │
│  ┌──────────────────────┐         ┌──────────────────────────────┐  │
│  │   Frontend (Next.js) │         │    Backend (FastAPI)          │  │
│  │                      │  REST   │                              │  │
│  │  • React 18 + TS     │────────▶│  • JWT Auth + OAuth          │  │
│  │  • Tailwind CSS      │  API    │  • Multi-tenant data layer   │  │
│  │  • Shadcn/ui         │◀────────│  • Stripe subscriptions      │  │
│  │  • React Query       │         │  • RBAC (Admin/Member/View)  │  │
│  │  • Next Auth         │         │  • Rate limiting             │  │
│  └──────────────────────┘         └──────────────┬───────────────┘  │
│                                                  │                   │
│                                   ┌──────────────▼───────────────┐  │
│                                   │   PostgreSQL + Redis          │  │
│                                   │                              │  │
│                                   │  • Alembic migrations        │  │
│                                   │  • Row-level security        │  │
│                                   │  • Session caching           │  │
│                                   └──────────────────────────────┘  │
│                                                                     │
│  Infrastructure: Docker Compose │ Terraform (AWS) │ GitHub Actions  │
└─────────────────────────────────────────────────────────────────────┘
```

## Features

### Authentication & Authorization
- [x] JWT token auth with refresh tokens
- [x] Google OAuth integration
- [x] Role-based access control (Owner, Admin, Member, Viewer)
- [x] Email verification flow
- [x] Password reset with secure tokens

### Multi-Tenancy
- [x] Organization-based tenancy (shared database, tenant column isolation)
- [x] Automatic tenant scoping on all queries
- [x] Invite team members via email
- [x] Switch between organizations

### Billing (Stripe)
- [x] Subscription plans (Free, Pro, Enterprise)
- [x] Stripe Checkout integration
- [x] Webhook handling for payment events
- [x] Usage-based billing support
- [x] Customer portal for self-service

### Developer Experience
- [x] Hot reload (frontend + backend)
- [x] Alembic database migrations
- [x] OpenAPI docs auto-generated at `/docs`
- [x] Pre-configured linting (ESLint, Ruff)
- [x] Docker Compose for local development
- [x] CI/CD pipeline (GitHub Actions)

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS, Shadcn/ui |
| Backend | FastAPI, Python 3.12, SQLAlchemy 2.0, Pydantic v2 |
| Database | PostgreSQL 16, Redis (caching + sessions) |
| Auth | JWT + OAuth2 (Google), bcrypt |
| Payments | Stripe (Subscriptions, Checkout, Webhooks) |
| Infra | Docker, Terraform (AWS), GitHub Actions |

## Quick Start

```bash
# 1. Clone
git clone https://github.com/vmunjal2503/saas-starter-kit.git
cd saas-starter-kit

# 2. Set up environment
cp .env.example .env
# Edit .env with your database, Stripe, and OAuth credentials

# 3. Start with Docker
docker compose up -d

# 4. Run migrations
docker compose exec backend alembic upgrade head

# 5. Open
# Frontend: http://localhost:3000
# Backend API docs: http://localhost:8000/docs
```

## Project Structure

```
saas-starter-kit/
├── frontend/                  # Next.js application
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/             # Next.js pages
│   │   ├── hooks/             # Custom React hooks
│   │   └── lib/               # Utilities, API client, types
│   └── public/                # Static assets
├── backend/                   # FastAPI application
│   ├── app/
│   │   ├── api/               # Route handlers
│   │   ├── models/            # SQLAlchemy models
│   │   ├── services/          # Business logic
│   │   └── middleware/        # Auth, tenant, rate limiting
│   └── migrations/            # Alembic migrations
├── docker-compose.yml         # Local development setup
├── docker-compose.prod.yml    # Production setup
└── .github/workflows/         # CI/CD pipelines
```

## Environment Variables

See [.env.example](.env.example) for all required variables.

## Deployment

```bash
# Production build
docker compose -f docker-compose.prod.yml up -d

# Or deploy to AWS with Terraform
cd infra && terraform apply
```

---

Built by **Vikas Munjal** | Open source under MIT License
