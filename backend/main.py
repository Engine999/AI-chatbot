from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.routes.execute_router import router as execute_router
from backend.routes.analyze_router import router as analyze_router
from backend.routes.chat_router import router as chat_router

app = FastAPI()

app.include_router(execute_router)
app.include_router(analyze_router)
app.include_router(chat_router)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def root():
    return FileResponse("frontend/chat.html")
