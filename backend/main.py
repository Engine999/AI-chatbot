from fastapi import FastAPI
from backend.routes.execute_router import router as execute_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
import sys

app = FastAPI()

app.include_router(execute_router)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def root_page():
    return FileResponse("frontend/chat.html")