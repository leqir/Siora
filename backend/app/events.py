from fastapi import APIRouter, Depends, Request
from starlette.responses import JSONResponse

# Import or define verify_user_id
from app.utils.auth import verify_user_id  # Adjust the import path as needed

router = APIRouter()

@router.get("/events")
async def list_events(request: Request):
    cookie = request.cookies.get("session")
    if not cookie:
        print("⚠️ No session cookie received!")
        return {"error": "unauthorized"}, 401
    try:
        user_id = verify_user_id(cookie)
        print("✅ User verified:", user_id)
        return {"events": []}
    except Exception as e:
        print("❌ Token invalid:", e)
        return {"error": "unauthorized"}, 401