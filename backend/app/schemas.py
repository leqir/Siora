from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserOut(BaseModel):
    id: str
    email: EmailStr
    name: str | None = None
    picture_url: str | None = None


class ChatIn(BaseModel):
    conversation_id: str | None = None
    message: str


class ChatOut(BaseModel):
    conversation_id: str
    reply: str


class EventCreate(BaseModel):
    summary: str = Field(..., description="Event title")
    start_iso: str = Field(..., description="RFC3339 datetime, e.g., 2025-10-01T15:00:00+10:00")
    end_iso: str


class EventOut(BaseModel):
    id: str
    summary: str | None = None
    start_iso: str | None = None
    end_iso: str | None = None
    status: str | None = None
