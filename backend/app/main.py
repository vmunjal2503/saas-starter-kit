"""
SaaS Starter Kit — FastAPI Backend
Multi-tenant SaaS application with auth, billing, and RBAC.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, users, organizations, billing, health
from app.middleware.rate_limit import RateLimitMiddleware

app = FastAPI(
    title="SaaS Starter Kit API",
    description="Production-ready SaaS backend with auth, multi-tenancy, and Stripe billing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ──────────────── CORS ────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────── Rate Limiting ────────────────
app.add_middleware(RateLimitMiddleware, requests_per_minute=60)

# ──────────────── Routes ────────────────
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(organizations.router, prefix="/api/organizations", tags=["Organizations"])
app.include_router(billing.router, prefix="/api/billing", tags=["Billing"])
