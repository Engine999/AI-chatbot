# backend/routes/execute_router.py
from fastapi import APIRouter
from pydantic import BaseModel
from backend.chat.execute import execute_c

router = APIRouter(prefix="/execute", tags=["execute"])

class ExecRequest(BaseModel):
    code: str

class ExecResponse(BaseModel):
    stdout: str
    stderr: str
    exit_code: int
    time_ms: int

@router.post("", response_model=ExecResponse)
def execute(req: ExecRequest):
    result = execute_c(req.code)
    return ExecResponse(**result)
