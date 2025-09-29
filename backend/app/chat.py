from __future__ import annotations
from typing import AsyncGenerator
from fastapi import APIRouter, Depends, HTTPException
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .deps import get_current_user
from .db import get_db
from .models import Conversation, Message, User
from .schemas import ChatIn
from .config import get_settings

router = APIRouter(prefix="/chat", tags=["chat"])
settings = get_settings()

# Optional OpenAI
_client = None
if settings.openai_api_key:
    from openai import AsyncOpenAI

    _client = AsyncOpenAI(api_key=settings.openai_api_key)


async def _prep_conversation(
    session: AsyncSession, user: User, conv_id: str | None
) -> Conversation:
    if conv_id:
        conv = await session.get(Conversation, conv_id)
        if conv and conv.user_id == user.id:
            return conv
    conv = Conversation(user_id=user.id, title="New chat")
    session.add(conv)
    await session.commit()
    return conv


@router.post("")
async def chat(
    body: ChatIn, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)
):
    conv = await _prep_conversation(session, user, body.conversation_id)
    session.add(Message(conversation_id=conv.id, role="user", content=body.message))
    await session.commit()

    reply = "I'm connected to your calendar. Ask me to list events or create one like: “Help me add a new event called ‘Call with Andy’ at 3 PM tomorrow.”"
    session.add(Message(conversation_id=conv.id, role="assistant", content=reply))
    await session.commit()
    return {"conversation_id": str(conv.id), "reply": reply}


@router.post("/stream")
async def chat_stream(
    body: ChatIn, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)
):
    conv = await _prep_conversation(session, user, body.conversation_id)
    session.add(Message(conversation_id=conv.id, role="user", content=body.message))
    await session.commit()

    async def event_gen() -> AsyncGenerator[dict, None]:
        # Immediately tell the UI we're thinking
        yield {"event": "status", "data": "thinking"}

        if not _client:
            # Fallback demo stream
            for chunk in ["Let", "’s ", "set ", "this ", "up ", "together!"]:
                yield {"event": "message", "data": chunk}
                import asyncio

                await asyncio.sleep(0.1)
            yield {"event": "done", "data": ""}
            return

        sys_prompt = (
            "You are an AI calendar assistant. If the message asks to create an event, "
            "propose a short confirmation. Otherwise, answer helpfully. Keep replies short."
        )
        stream = await _client.chat.completions.create(
            model="gpt-4o-mini",
            stream=True,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": body.message},
            ],
        )
        collected = []
        async for part in stream:
            delta = part.choices[0].delta.content or ""
            if delta:
                collected.append(delta)
                yield {"event": "message", "data": delta}
        full = "".join(collected)
        # persist assistant message
        session.add(Message(conversation_id=conv.id, role="assistant", content=full))
        await session.commit()
        yield {"event": "done", "data": ""}

    return EventSourceResponse(event_gen())
