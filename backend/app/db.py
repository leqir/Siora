from __future__ import annotations

import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


def _as_async_url(url: str) -> str:
    # Ensure SQLAlchemy async driver is used.
    # Railway gives postgresql://... possibly with ?sslmode=require
    if url.startswith("postgresql+asyncpg://"):
        return url
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://") :]
    return url.replace("postgresql://", "postgresql+asyncpg://", 1)


DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://localhost/placeholder")
ASYNC_DB_URL = _as_async_url(DATABASE_URL)

engine = create_async_engine(
    ASYNC_DB_URL,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
