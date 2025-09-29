from __future__ import annotations
from datetime import datetime, timezone
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .deps import get_current_user
from .config import get_settings
from .models import User, CalendarEvent
from .db import get_db

router = APIRouter(prefix="/calendar", tags=["calendar"])

TOKEN_URL = "https://oauth2.googleapis.com/token"
EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/primary/events"

settings = get_settings()


async def ensure_access_token(user: User, session: AsyncSession) -> str:
    # If token exists and not expired, use it
    if user.google_access_token and user.google_token_expiry:
        if user.google_token_expiry > datetime.now(timezone.utc):
            return user.google_access_token

    if not user.google_refresh_token:
        raise HTTPException(status_code=400, detail="Google not connected (no refresh token)")

    data = {
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "grant_type": "refresh_token",
        "refresh_token": user.google_refresh_token,
    }
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(TOKEN_URL, data=data)
        r.raise_for_status()
        tok = r.json()

    user.google_access_token = tok["access_token"]
    expires_in = tok.get("expires_in", 3600)
    user.google_token_expiry = datetime.now(timezone.utc) + timedelta(seconds=int(expires_in))
    await session.commit()
    return user.google_access_token


@router.get("/events")
async def list_events(
    time_min: str | None = Query(None, description="RFC3339, default now"),
    time_max: str | None = Query(None, description="RFC3339, default +7 days"),
    q: str | None = Query(None, description="Search query"),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    from datetime import timedelta

    access_token = await ensure_access_token(user, session)

    if not time_min:
        time_min = datetime.now(timezone.utc).isoformat()
    if not time_max:
        time_max = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()

    params = {
        "timeMin": time_min,
        "timeMax": time_max,
        "singleEvents": "true",
        "orderBy": "startTime",
    }
    if q:
        params["q"] = q

    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(EVENTS_URL, params=params, headers=headers)
        r.raise_for_status()
        data = r.json()

    # Optionally cache basic fields in DB (best-effort)
    items_out = []
    for ev in data.get("items", []):
        start_iso = (ev.get("start", {}) or {}).get("dateTime") or (ev.get("start", {}) or {}).get(
            "date"
        )
        end_iso = (ev.get("end", {}) or {}).get("dateTime") or (ev.get("end", {}) or {}).get("date")
        items_out.append(
            {
                "id": ev["id"],
                "summary": ev.get("summary"),
                "start_iso": start_iso,
                "end_iso": end_iso,
                "status": ev.get("status"),
            }
        )
    return {"events": items_out}


@router.post("/events")
async def create_event(
    payload: dict,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """
    Expected payload:
      {
        "summary": "...",
        "start_iso": "2025-10-01T15:00:00+10:00",
        "end_iso":   "2025-10-01T16:00:00+10:00"
      }
    """
    required = {"summary", "start_iso", "end_iso"}
    if not required.issubset(payload):
        raise HTTPException(status_code=422, detail="Missing required fields")

    access_token = await ensure_access_token(user, session)
    headers = {"Authorization": f"Bearer {access_token}"}
    body = {
        "summary": payload["summary"],
        "start": {"dateTime": payload["start_iso"]},
        "end": {"dateTime": payload["end_iso"]},
    }

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(EVENTS_URL, headers=headers, json=body)
        r.raise_for_status()
        ev = r.json()

    # Best-effort store
    ce = CalendarEvent(
        user_id=user.id,
        google_event_id=ev["id"],
        summary=ev.get("summary"),
        start_iso=(ev.get("start", {}) or {}).get("dateTime"),
        end_iso=(ev.get("end", {}) or {}).get("dateTime"),
        status=ev.get("status"),
    )
    session.add(ce)
    await session.commit()

    return {
        "ok": True,
        "event": {
            "id": ev["id"],
            "summary": ev.get("summary"),
            "start_iso": ce.start_iso,
            "end_iso": ce.end_iso,
            "status": ce.status,
        },
    }
