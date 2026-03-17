"""
Billing endpoints — Stripe subscriptions, checkout, webhooks.
"""

from fastapi import APIRouter, HTTPException, Request, Header
from pydantic import BaseModel
from typing import Optional
from enum import Enum

router = APIRouter()


class Plan(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class SubscriptionResponse(BaseModel):
    plan: Plan
    status: str
    current_period_end: Optional[str] = None
    cancel_at_period_end: bool = False


class CheckoutRequest(BaseModel):
    plan: Plan
    org_id: str


# ──────────────── Subscription Management ────────────────

@router.get("/subscription/{org_id}", response_model=SubscriptionResponse)
async def get_subscription(org_id: str):
    """Get current subscription details for an organization."""
    return {
        "plan": "pro",
        "status": "active",
        "current_period_end": "2024-02-01T00:00:00Z",
        "cancel_at_period_end": False,
    }


@router.post("/checkout")
async def create_checkout_session(data: CheckoutRequest):
    """Create a Stripe Checkout session for upgrading plan."""
    # In production:
    # 1. Look up Stripe price_id for the plan
    # 2. Create Stripe Checkout session
    # 3. Return session URL
    return {
        "checkout_url": "https://checkout.stripe.com/c/pay/cs_test_xxxxx",
        "session_id": "cs_test_xxxxx",
    }


@router.post("/portal/{org_id}")
async def create_customer_portal(org_id: str):
    """Create a Stripe Customer Portal session for self-service management."""
    # In production: look up Stripe customer_id, create portal session
    return {
        "portal_url": "https://billing.stripe.com/p/session/xxxxx",
    }


@router.post("/cancel/{org_id}")
async def cancel_subscription(org_id: str):
    """Cancel subscription at end of current billing period."""
    return {
        "message": "Subscription will be cancelled at end of billing period",
        "cancel_at_period_end": True,
    }


# ──────────────── Stripe Webhooks ────────────────

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    """
    Handle Stripe webhook events.

    Events handled:
    - checkout.session.completed → Activate subscription
    - invoice.paid → Record payment
    - invoice.payment_failed → Notify user, retry
    - customer.subscription.updated → Sync plan changes
    - customer.subscription.deleted → Downgrade to free
    """
    body = await request.body()

    # In production:
    # 1. Verify webhook signature with stripe.Webhook.construct_event()
    # 2. Parse event type
    # 3. Handle each event type

    return {"received": True}
