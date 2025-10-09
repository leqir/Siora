from fastapi import APIRouter, Depends, Request
from starlette.responses import JSONResponse

router = APIRouter()

@router.get("/events")
async def get_events(request: Request):
    session = request.session
    if "user" not in session:
        return JSONResponse({"error": "unauthorized"}, status_code=401)
    # placeholder: ideally fetch from Google Calendar here
    return {"events": []}