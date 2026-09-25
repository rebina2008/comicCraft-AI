import os
import traceback
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

try:
    from app.gemini_flash import generate_outline
    from app.gemini_pro import generate_story
    from app.image_generator import generate_image
    from app.layout_builder import build_comic_layout
    from app.exporters import save_pdf
except ImportError:
    from gemini_flash import generate_outline
    from gemini_pro import generate_story
    from image_generator import generate_image
    from layout_builder import build_comic_layout
    from exporters import save_pdf

app = FastAPI(title="ComicCraft AI")

# Create necessary static directories
os.makedirs("static/panels", exist_ok=True)
os.makedirs("static/exports", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Renders the Home Page input form"""
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    prompt: str = Form(...),
    story_details: str = Form(""),
    character_name: str = Form(""),
    setting: str = Form("City"),
    tone: str = Form("Dramatic"),
    style: str = Form("Anime")
):
    """
    Main pipeline:
    1. Enrich user prompt
    2. Generate structured 5-panel outline via Gemini Flash
    3. Generate detailed narration & dialogue via Gemini Pro
    4. Generate 5 unique anime panel images
    5. Build combined layout dictionary
    6. Export layout into PDF file
    7. Render preview page
    """
    try:
        # Enriched prompt combining user form parameters
        enriched_prompt = f"Title: {prompt}. Plot: {story_details}. Main Character: {character_name}. Setting: {setting}. Tone: {tone}. Style: {style}."

        # 1. Step 1: Generate Outline
        outline = generate_outline(enriched_prompt)
        if not outline or not isinstance(outline, list):
            outline = []

        # 2. Step 2: Generate Full Story Narration & Dialogues
        full_story = generate_story(outline)

        # Default panel descriptions if Gemini outline fails
        default_scenes = [
            f"Panel 1: Wide shot introduction of anime girl {character_name} in {setting}",
            f"Panel 2: Emotion shot of anime girl {character_name} discovering a mystery",
            f"Panel 3: Anime girl {character_name} facing an intense dynamic battle conflict",
            f"Panel 4: Power climax scene with glowing magical aura burst around anime girl {character_name}",
            f"Panel 5: Peaceful sunset view with anime girl {character_name} looking at horizon"
        ]

        # 3. Step 3: Generate 5 Unique Anime Panel Images
        images = []
        for i in range(5):
            panel_num = i + 1
            panel_prompt = ""
            
            if i < len(outline) and isinstance(outline[i], dict):
                panel_prompt = outline[i].get("image_prompt", "")
            
            if not panel_prompt:
                panel_prompt = default_scenes[i]

            final_image_prompt = f"{panel_prompt}, anime girl {character_name}, setting {setting}, {style} style"

            # Call generator with panel_index for camera framing variations
            img_url = generate_image(final_image_prompt, panel_index=panel_num)
            images.append(img_url)

        # 4. Step 4: Build Layout Dictionary
        layout = build_comic_layout(images, full_story, outline)

        # 5. Step 5: Save PDF using Exporters Module
        pdf_file_path = save_pdf(layout)

        # 6. Step 6: Determine Template Name
        template_name = "comic_preview.html"
        if not os.path.exists("templates/comic_preview.html") and os.path.exists("templates/preview.html"):
            template_name = "preview.html"

        return templates.TemplateResponse(
            request=request,
            name=template_name,
            context={
                "layout": layout,
                "prompt": prompt,
                "pdf_path": pdf_file_path
            }
        )

    except Exception as e:
        error_details = traceback.format_exc()
        return HTMLResponse(
            content=f"<pre style='color:red;'>Generation Error:\n{error_details}</pre>",
            status_code=500
        )


@app.get("/download-pdf")
async def download_pdf(pdf_path: str):
    """Route to directly download generated PDF file"""
    if os.path.exists(pdf_path):
        return FileResponse(
            pdf_path, 
            filename="ComicCraft_Story.pdf", 
            media_type="application/pdf"
        )
    return HTMLResponse("<h2 style='color:red;'>PDF File Not Found</h2>", status_code=404)


@app.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf_path: str = ""):
    """Export confirmation page route"""
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={"pdf_path": pdf_path}
    )