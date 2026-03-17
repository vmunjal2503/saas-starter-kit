"""
User management endpoints — Profile, Settings.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()


class UserProfile(BaseModel):
    id: str
    email: str
    full_name: str
    avatar_url: Optional[str] = None
    is_verified: bool
    created_at: str


class UpdateProfileRequest(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None


@router.get("/me", response_model=UserProfile)
async def get_current_user():
    """Get current authenticated user's profile."""
    # In production: extract user from JWT token via dependency injection
    return {
        "id": "user_123",
        "email": "user@example.com",
        "full_name": "Demo User",
        "avatar_url": None,
        "is_verified": True,
        "created_at": "2024-01-01T00:00:00Z",
    }


@router.patch("/me", response_model=UserProfile)
async def update_profile(data: UpdateProfileRequest):
    """Update current user's profile."""
    return {
        "id": "user_123",
        "email": "user@example.com",
        "full_name": data.full_name or "Demo User",
        "avatar_url": data.avatar_url,
        "is_verified": True,
        "created_at": "2024-01-01T00:00:00Z",
    }


@router.delete("/me", status_code=204)
async def delete_account():
    """Delete current user's account and all associated data."""
    # In production: soft delete, cancel subscriptions, cleanup data
    return None
