from fastapi import FastAPI
from backend.routes.execute_router import router as execute_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
import sys

app = FastAPI()

app.include_router(execute_router)






from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# 1) .env 로드
load_dotenv(dotenv_path=r"C:\Users\dbswodyd99\Desktop\PTJ\02.AI-chatbot\AI-chatbot\static\.env")
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY가 설정되지 않았습니다. .env를 확인하세요.")

# 2) Gemini 클라이언트 / 시스템 지시문
client = genai.Client(api_key=api_key)
system_instruction = (
    "당신은 C 코드 학습용 리뷰어입니다. 절대 전체 정답 코드를 제공하지 마세요. "
    "문제가 되는 Line을 명시하세요."
)

# 3) FastAPI 앱
#app = FastAPI(title="AI-chatbot (Gemini)")

# 필요 시 외부에서 접근할 프론트가 따로 있으면 CORS 허용
# 같은 서버에서 정적 서빙할 거면 없어도 됨(아래 줄 주석 유지 가능)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],   # 배포 시 도메인으로 제한 권장
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# 4) 요청 스키마
class AnalyzeRequest(BaseModel):
    code: str

# 5) API: /analyze
@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    try:
        resp = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=req.code,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,
                max_output_tokens=512,
            ),
        )
        return {"ok": True, "result": resp.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# (위에 AnalyzeRequest 아래에 이어서)

from typing import List, Optional
from pydantic import BaseModel

class ChatTurn(BaseModel):
    role: str        # "user" | "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    code: Optional[str] = ""
    history: Optional[List[ChatTurn]] = []

@app.post("/chat")
def chat(req: ChatRequest):
    # 간단 프롬프트 결합
    stitched = ""
    if req.code:
        stitched += "/* 현재 C 코드 */\n" + req.code + "\n\n"
    if req.history:
        for t in req.history[-6:]:
            stitched += f"{t.role.upper()}: {t.content}\n"
        stitched += "\n"
    stitched += f"USER: {req.message}\nASSISTANT:"

    try:
        resp = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=stitched,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,
                max_output_tokens=512,
            ),
        )
        return {"ok": True, "result": resp.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 6) 정적 파일 서빙 (Same-Origin으로 프론트 제공)
#app.mount("/", StaticFiles(directory="static", html=True), name="static")


app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def root_page():
    return FileResponse("frontend/chat.html")