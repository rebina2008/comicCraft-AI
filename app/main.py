import os
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="ComicCraft")

# Favicon 404 handler
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return Response(status_code=204)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Routes import-ai application setup-ku appram call panrom
from app.routes import router
app.include_router(router)