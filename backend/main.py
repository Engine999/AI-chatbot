from fastapi import FastAPI
from google import genai
from dotenv import load_dotenv
import os
import sys

app = FastAPI()

@app.get("/") 
def main_page():
    return 
