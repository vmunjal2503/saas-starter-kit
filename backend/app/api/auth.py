"""
Authentication endpoints — Register, Login, OAuth, Password Reset.
"""

from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.services.auth_service import AuthService

router = APIRouter()


# ──────────────── Request/Response Models ────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


# ──────────────── Endpoints ────────────────

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(data: RegisterRequest):
    """Register a new user account."""
    service = AuthService()

    # Check if user already exists
    existing = await service.get_user_by_email(data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    user = await service.create_user(
        email=data.email,
        password=data.password,
        full_name=data.full_name,
    )
    tokens = service.generate_tokens(user_id=str(user.id))

    # Send verification email (async, non-blocking)
    await service.send_verification_email(user)

    return tokens


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    """Authenticate with email and password."""
    service = AuthService()

    user = await service.authenticate(email=data.email, password=data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    tokens = service.generate_tokens(user_id=str(user.id))
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """Get new access token using refresh token."""
    service = AuthService()

    payload = service.verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    tokens = service.generate_tokens(user_id=payload["sub"])
    return tokens


@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest):
    """Send password reset email."""
    service = AuthService()
    await service.send_password_reset_email(data.email)

    # Always return success (don't reveal if email exists)
    return {"message": "If an account exists, a reset link has been sent"}


@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest):
    """Reset password using token from email."""
    service = AuthService()
    success = await service.reset_password(data.token, data.new_password)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    return {"message": "Password reset successfully"}


@router.get("/google")
async def google_oauth_redirect():
    """Redirect to Google OAuth consent screen."""
    service = AuthService()
    return {"url": service.get_google_oauth_url()}


@router.get("/google/callback", response_model=TokenResponse)
async def google_oauth_callback(code: str):
    """Handle Google OAuth callback and create/login user."""
    service = AuthService()
    user = await service.handle_google_callback(code)
    tokens = service.generate_tokens(user_id=str(user.id))
    return tokens
