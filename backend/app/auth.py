from __future__ import annotations
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .config import get_settings
from .db import get_db
from .models import User
from .utils import sign_user_id
from starlette.responses import JSONResponse
import os

router = APIRouter(prefix="/auth", tags=["auth"])

settings = get_settings()

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile https://www.googleapis.com/auth/calendar.events",
        "prompt": "consent",
        "access_type": "offline",
        "include_granted_scopes": "true",
    },
)

@router.get("/login")
async def login(request: Request):
    redirect_uri = settings.google_redirect_uri
    print("Redirecting to:", redirect_uri)  # confirm it
    return await oauth.google.authorize_redirect(request, redirect_uri)



@router.get("/callback")
async def callback(request: Request, session: AsyncSession = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {e.error}")

    # id_token gives basic profile
    userinfo = token.get("userinfo")
    if not userinfo:
        # If using Authlib < 1.3, parse id_token manually:
        userinfo = await oauth.google.parse_id_token(request, token)

    email = userinfo["email"]
    name = userinfo.get("name")
    picture = userinfo.get("picture")

    # find or create user
    existing = await session.scalar(select(User).where(User.email == email))
    if existing:
        user = existing
    else:
        user = User(email=email, name=name, picture_url=picture)
        session.add(user)

    # Store refresh/access tokens (prefer refresh; access will be refreshed when needed)
    user.picture_url = picture or user.picture_url
    user.name = name or user.name
    user.google_refresh_token = token.get("refresh_token") or user.google_refresh_token
    user.google_access_token = token.get("access_token")
    expires_in = token.get("expires_in")
    if expires_in:
        user.google_token_expiry = datetime.now(timezone.utc) + timedelta(seconds=int(expires_in))
    user.google_scope = token.get("scope")

    await session.commit()

    # Set signed session cookie with user.id (30 days)
    # Set signed session cookie with user.id (30 days)
    session_token = sign_user_id(str(user.id))
    resp = RedirectResponse(url=f"{settings.frontend_origin}/connected")
    resp.set_cookie(
        "session",
        value=session_token,
        max_age=60 * 60 * 24 * 30,  # 30 days
        httponly=True,
        secure=True,                # must be True if you're using https on Vercel
        samesite="none",            # allow cross-domain cookie
    )

    print("✅ Setting session cookie for user:", user.email)
    print("Frontend redirecting to:", settings.frontend_origin)

    return resp




@router.post("/logout")
async def logout():
    resp = RedirectResponse(url=f"{settings.frontend_origin}/logged-out")
    resp.delete_cookie("session")
    return resp
