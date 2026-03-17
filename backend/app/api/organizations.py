"""
Organization (multi-tenancy) endpoints — CRUD, members, invites.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

router = APIRouter()


class Role(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class CreateOrgRequest(BaseModel):
    name: str
    slug: Optional[str] = None


class InviteMemberRequest(BaseModel):
    email: EmailStr
    role: Role = Role.MEMBER


class OrgResponse(BaseModel):
    id: str
    name: str
    slug: str
    plan: str
    member_count: int
    created_at: str


class MemberResponse(BaseModel):
    user_id: str
    email: str
    full_name: str
    role: Role
    joined_at: str


# ──────────────── Organization CRUD ────────────────

@router.post("/", response_model=OrgResponse, status_code=201)
async def create_organization(data: CreateOrgRequest):
    """Create a new organization. Creator becomes Owner."""
    return {
        "id": "org_456",
        "name": data.name,
        "slug": data.slug or data.name.lower().replace(" ", "-"),
        "plan": "free",
        "member_count": 1,
        "created_at": "2024-01-01T00:00:00Z",
    }


@router.get("/", response_model=list[OrgResponse])
async def list_organizations():
    """List all organizations the current user belongs to."""
    return [
        {
            "id": "org_456",
            "name": "Acme Inc",
            "slug": "acme-inc",
            "plan": "pro",
            "member_count": 5,
            "created_at": "2024-01-01T00:00:00Z",
        }
    ]


@router.get("/{org_id}", response_model=OrgResponse)
async def get_organization(org_id: str):
    """Get organization details."""
    return {
        "id": org_id,
        "name": "Acme Inc",
        "slug": "acme-inc",
        "plan": "pro",
        "member_count": 5,
        "created_at": "2024-01-01T00:00:00Z",
    }


# ──────────────── Member Management ────────────────

@router.get("/{org_id}/members", response_model=list[MemberResponse])
async def list_members(org_id: str):
    """List all members of an organization."""
    return [
        {
            "user_id": "user_123",
            "email": "owner@example.com",
            "full_name": "Org Owner",
            "role": "owner",
            "joined_at": "2024-01-01T00:00:00Z",
        }
    ]


@router.post("/{org_id}/invite", status_code=201)
async def invite_member(org_id: str, data: InviteMemberRequest):
    """Invite a new member to the organization via email."""
    # In production: check RBAC (only Owner/Admin can invite),
    # check plan limits, send invitation email
    return {
        "message": f"Invitation sent to {data.email}",
        "role": data.role,
    }


@router.delete("/{org_id}/members/{user_id}", status_code=204)
async def remove_member(org_id: str, user_id: str):
    """Remove a member from the organization. Owners cannot be removed."""
    return None
