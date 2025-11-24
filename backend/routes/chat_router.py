# routes/chat_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..chat.chatbot import gemini_chat

router = APIRouter()

class ChatTurn(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    code: Optional[str] = ""
    history: Optional[List[ChatTurn]] = []

@router.post("/chat")
def chat(req: ChatRequest):
    stitched = ""

    if req.code:
        stitched += "/* 현재 C 코드 */\n" + req.code + "\n\n"

    if req.history:
        for t in req.history[-6:]:
            stitched += f"{t.role.upper()}: {t.content}\n"
        stitched += "\n"

    stitched += f"USER: {req.message}\nASSISTANT:"

    try:
        result = gemini_chat(stitched)
        return {"ok": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
