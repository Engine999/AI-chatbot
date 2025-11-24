# routes/analyze_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..chat.chatbot import gemini_analyze

router = APIRouter()

class AnalyzeRequest(BaseModel):
    code: str

def add_line_numbers(code: str) -> str:
    lines = code.split("\n")
    return "\n".join(f"{i+1}: {line}" for i, line in enumerate(lines))

@router.post("/analyze")
def analyze(req: AnalyzeRequest):
    try:
        numbered = add_line_numbers(req.code)
        result = gemini_analyze(numbered)
        return {"ok": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
