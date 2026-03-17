"""
Authentication service — JWT tokens, password hashing, OAuth.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
import os


class AuthService:
    """Handles authentication, token generation, and password management."""

    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
    ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """Hash a plain-text password."""
        return self.pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        """Verify a plain-text password against its hash."""
        return self.pwd_context.verify(plain, hashed)

    def generate_tokens(self, user_id: str) -> dict:
        """Generate access + refresh token pair."""
        now = datetime.now(timezone.utc)

        access_token = jwt.encode(
            {
                "sub": user_id,
                "type": "access",
                "exp": now + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE),
                "iat": now,
            },
            self.SECRET_KEY,
            algorithm=self.ALGORITHM,
        )

        refresh_token = jwt.encode(
            {
                "sub": user_id,
                "type": "refresh",
                "exp": now + timedelta(days=self.REFRESH_TOKEN_EXPIRE),
                "iat": now,
            },
            self.SECRET_KEY,
            algorithm=self.ALGORITHM,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": self.ACCESS_TOKEN_EXPIRE * 60,
        }

    def verify_access_token(self, token: str) -> Optional[dict]:
        """Verify and decode an access token."""
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("type") != "access":
                return None
            return payload
        except JWTError:
            return None

    def verify_refresh_token(self, token: str) -> Optional[dict]:
        """Verify and decode a refresh token."""
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("type") != "refresh":
                return None
            return payload
        except JWTError:
            return None

    async def get_user_by_email(self, email: str):
        """Look up user by email. Returns None if not found."""
        # In production: query database
        return None

    async def create_user(self, email: str, password: str, full_name: str):
        """Create a new user account."""
        # In production: insert into database
        class MockUser:
            id = "user_new"
            email = email
            full_name = full_name
        return MockUser()

    async def authenticate(self, email: str, password: str):
        """Authenticate user with email and password."""
        # In production: look up user, verify password
        return None

    async def send_verification_email(self, user):
        """Send email verification link."""
        # In production: generate token, send email
        pass

    async def send_password_reset_email(self, email: str):
        """Send password reset email if user exists."""
        # In production: generate reset token, send email
        pass

    async def reset_password(self, token: str, new_password: str) -> bool:
        """Reset password using a valid reset token."""
        # In production: verify token, update password
        return True

    def get_google_oauth_url(self) -> str:
        """Get Google OAuth consent URL."""
        client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        redirect_uri = os.getenv("BACKEND_URL", "http://localhost:8000") + "/api/auth/google/callback"
        return (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&redirect_uri={redirect_uri}"
            f"&response_type=code&scope=openid%20email%20profile"
        )

    async def handle_google_callback(self, code: str):
        """Exchange OAuth code for user info and create/login user."""
        # In production: exchange code for tokens, get user info, upsert user
        class MockUser:
            id = "user_google"
        return MockUser()
