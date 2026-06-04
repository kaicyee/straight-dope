"""FastAPI backend for Straight Dope."""

import asyncio
import json
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any

from . import storage
from .council import run_full_council, generate_conversation_title

app = FastAPI(title="Straight Dope API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateConversationRequest(BaseModel):
    pass


class SendMessageRequest(BaseModel):
    content: str


@app.get("/")
async def root():
    return {"status": "ok", "service": "Straight Dope API"}


@app.get("/api/conversations")
async def list_conversations():
    return storage.list_conversations()


@app.post("/api/conversations")
async def create_conversation(request: CreateConversationRequest):
    conversation_id = str(uuid.uuid4())
    return storage.create_conversation(conversation_id)


@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    conversation = storage.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return conversation


@app.post("/api/conversations/{conversation_id}/message/stream")
async def send_message_stream(conversation_id: str, request: SendMessageRequest):
    """Stream the 3-stage Straight Dope process via Server-Sent Events."""
    conversation = storage.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Session not found")

    is_first_message = len(conversation["messages"]) == 0

    async def event_generator():
        try:
            storage.add_user_message(conversation_id, request.content)

            title_task = None
            if is_first_message:
                title_task = asyncio.create_task(
                    generate_conversation_title(request.content)
                )

            # Stage 1: Advisors
            yield f"data: {json.dumps({'type': 'stage1_start'})}\n\n"
            stage1_results = await _run_stage1(request.content)
            yield f"data: {json.dumps({'type': 'stage1_complete', 'data': stage1_results})}\n\n"

            # Stage 2: Cross-examination
            yield f"data: {json.dumps({'type': 'stage2_start'})}\n\n"
            stage2_results = await _run_stage2(request.content, stage1_results)
            yield f"data: {json.dumps({'type': 'stage2_complete', 'data': stage2_results})}\n\n"

            # Stage 3: Chairman's verdict
            yield f"data: {json.dumps({'type': 'stage3_start'})}\n\n"
            stage3_result = await _run_stage3(request.content, stage1_results, stage2_results)
            yield f"data: {json.dumps({'type': 'stage3_complete', 'data': stage3_result})}\n\n"

            if title_task:
                title = await title_task
                storage.update_conversation_title(conversation_id, title)
                yield f"data: {json.dumps({'type': 'title_complete', 'data': {'title': title}})}\n\n"

            storage.add_assistant_message(
                conversation_id, stage1_results, stage2_results, stage3_result
            )

            yield f"data: {json.dumps({'type': 'complete'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


# Import stage functions here to keep main.py clean
from .council import (
    stage1_advisor_perspectives as _run_stage1,
    stage2_cross_examination as _run_stage2,
    stage3_chairman_verdict as _run_stage3,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
