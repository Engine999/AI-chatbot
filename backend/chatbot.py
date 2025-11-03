from fastapi import FastAPI
from google import genai
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="C:\\Users\\dbswodyd99\\Desktop\\PTJ\\02.AI-chatbot\\AI-chatbot\\static\\.env")
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Engine을 출력하세요"
)

print(response.text)
