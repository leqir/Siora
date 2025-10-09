from __future__ import annotations
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine
from .db import Base, engine
from .config import get_settings
from .auth import router as auth_router
from .calendar_api import router as calendar_router
from .chat import router as chat_router
from .events import router as events_router

from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
import os

settings = get_settings()
app = FastAPI(title="AI Calendar Assistant (Backend)")


# CORS so the Next.js frontend can call us
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    same_site="none",    # ✅ required for cross-site cookies
    https_only=True,     # ✅ required for SameSite=None
)


@app.get("/healthz")
async def healthz():
    return {"ok": True}


@app.on_event("startup")
async def on_startup():
    # Create tables if they don't exist (simple and fine for this project)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
@app.get("/")
async def root():
    return {"message": "Backend is running 🚀"}

# Routers
app.include_router(auth_router)
app.include_router(calendar_router)
app.include_router(chat_router)
app.include_router(events_router)
