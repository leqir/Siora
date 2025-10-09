from __future__ import annotations
import asyncio
from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from .db import Base, engine
from .config import get_settings
from .utils import verify_user_id
from .auth import router as auth_router
from .calendar_api import router as calendar_router
from .chat import router as chat_router
from .events import router as events_router

settings = get_settings()

app = FastAPI(title="AI Calendar Assistant (Backend)")

# ----------------------------
# ✅ CORS CONFIGURATION (MUST come BEFORE routers)
# ----------------------------
print("🟢 CORS configured for:", settings.frontend_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# ✅ SESSION MIDDLEWARE (handles cookies securely)
# ----------------------------
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    same_site="none",    # required for cross-site cookies
    https_only=True,     # required for SameSite=None
)

# ----------------------------
# ✅ ROUTERS (load after middleware)
# ----------------------------
app.include_router(auth_router)
app.include_router(calendar_router)
app.include_router(chat_router)
app.include_router(events_router)

# ----------------------------
# ✅ HEALTH CHECK
# ----------------------------
@app.get("/healthz")
async def healthz():
    return {"ok": True}

# ----------------------------
# ✅ DATABASE INIT
# ----------------------------
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ----------------------------
# ✅ ROOT ENDPOINT
# ----------------------------
@app.get("/")
async def root():
    return {"message": "Backend is running 🚀"}

# ----------------------------
# ✅ USER ATTACH MIDDLEWARE (optional auth header)
# ----------------------------
@app.middleware("http")
async def attach_user_from_header(request: Request, call_next):
    auth = request.headers.get("Authorization")
    if auth and auth.startswith("Bearer "):
        token = auth.split(" ", 1)[1]
        try:
            user_id = verify_user_id(token)
            request.state.user_id = user_id
        except Exception:
            request.state.user_id = None
    response = await call_next(request)
    return response
