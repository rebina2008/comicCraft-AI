import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai
from dotenv import load_dotenv

from app.routes import router

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="ComicCraft")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)