from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.image_generator import generate_image
from app.pdf_generator import create_comic_pdf

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    # Updated syntax compatible with all Jinja2 / FastAPI versions
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/generate")
async def generate_comic(request: Request, prompt: str = Form(...)):
    print(f"\n--- Generating Comic for Prompt: {prompt} ---")
    
    # 5 Story panels structure
    panels_data = [
        {"panel": 1, "narration": f"Panel 1: {prompt}", "dialogue": "Let's begin the anime adventure!"},
        {"panel": 2, "narration": "Panel 2: The journey unfolds in a mysterious world.", "dialogue": "Look at what's ahead!"},
        {"panel": 3, "narration": "Panel 3: A sudden wave of magical energy appears.", "dialogue": "We must stand our ground!"},
        {"panel": 4, "narration": "Panel 4: Power gathers for the ultimate moment.", "dialogue": "Unleash the power!"},
        {"panel": 5, "narration": "Panel 5: Peace is restored in the anime realm.", "dialogue": "We did it!"}
    ]

    # Generate images for all 5 panels
    for item in panels_data:
        p_num = item["panel"]
        print(f"Triggering image generation for Panel {p_num}...")
        image_path = generate_image(prompt, panel_number=p_num)
        item["image"] = f"/{image_path}"

    # Generate PDF
    pdf_filename = create_comic_pdf(panels_data)

    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={
            "panels": panels_data,
            "pdf_url": f"/download/{pdf_filename}"
        }
    )

@app.get("/download/{filename}")
async def download_pdf(filename: str):
    file_path = os.path.join("static", filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='application/pdf')
    return {"error": "File not found"}