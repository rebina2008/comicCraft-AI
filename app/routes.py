import os
import time
import traceback
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    style: str = Form(...)
):
    try:
        # Session ID to lock the exact same images for Preview and PDF
        session_id = int(time.time())

        full_prompt = (
            f"{prompt}\n"
            f"The main character is {character_name}. "
            f"The setting is a {setting}. "
            f"The tone is {tone}. The art style is {style}."
        )

        outline = generate_outline(full_prompt)

        if not outline or not isinstance(outline, list):
            outline = [
                {
                    "panel": i,
                    "title": f"Panel {i}",
                    "scene_description": f"Panel {i} scene for {prompt}",
                    "image_prompt": f"{style} style drawing of {character_name} in {setting}"
                } for i in range(1, 6)
            ]

        full_story = generate_story(outline)

        # Generate images and save with session_id
        images = [
            generate_image(
                prompt=panel.get("image_prompt", prompt), 
                panel_number=idx
            ) 
            for idx, panel in enumerate(outline, start=1)
        ]

        layout = build_comic_layout(images, full_story, outline)

        # PDF Export using the EXACT same layout images
        pdf_path = save_pdf(layout)
        web_pdf_path = "/" + pdf_path.replace("\\", "/")

        return templates.TemplateResponse(
            request=request, 
            name="comic_preview.html", 
            context={
                "layout": layout, 
                "pdf_path": web_pdf_path,
                "status_message": "Comic Successfully Created! 🎉"
            }
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download-pdf")
async def download_pdf(pdf_path: str = None):
    if pdf_path:
        clean_path = pdf_path.lstrip("/")
        if os.path.exists(clean_path):
            return FileResponse(
                path=clean_path, 
                filename="ComicCraft_Anime_Comic.pdf", 
                media_type="application/pdf"
            )
            
    default_pdf = os.path.join("static", "exports", "comic_export.pdf")
    if os.path.exists(default_pdf):
        return FileResponse(
            path=default_pdf, 
            filename="ComicCraft_Anime_Comic.pdf", 
            media_type="application/pdf"
        )
        
    raise HTTPException(status_code=404, detail="PDF file not found.")