from datetime import timedelta

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auth.security import create_token, hash_password, verify_password
from config.settings import settings


router = APIRouter(prefix="/auth", tags=["auth"])

# Production note: replace with persistent user store.
USERS = {
    "admin@qai.local": {"password_hash": hash_password("Admin@123"), "role": "admin"},
    "service@qai.local": {"password_hash": hash_password("Service@123"), "role": "service"},
    "user@qai.local": {"password_hash": hash_password("User@123"), "role": "user"},
}


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: str


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    user = USERS.get(payload.email)
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    role = user["role"]
    access_token = create_token(
        payload.email, role, "access", timedelta(minutes=settings.jwt_access_token_exp_minutes)
    )
    refresh_token = create_token(
        payload.email, role, "refresh", timedelta(days=settings.jwt_refresh_token_exp_days)
    )
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, role=role)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest):
    from auth.security import decode_token

    decoded = decode_token(payload.refresh_token)
    if decoded.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    subject = decoded.get("sub")
    role = decoded.get("role", "user")
    access_token = create_token(
        subject, role, "access", timedelta(minutes=settings.jwt_access_token_exp_minutes)
    )
    refresh_token = create_token(
        subject, role, "refresh", timedelta(days=settings.jwt_refresh_token_exp_days)
    )
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, role=role)
