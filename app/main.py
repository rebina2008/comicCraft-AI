import os
import random
import urllib.parse
import asyncio
import aiohttp
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.exporters import create_comic_pdf

app = FastAPI(title="ComicCraft AI")

os.makedirs("static/generated", exist_ok=True)
os.makedirs("static/exports", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204, headers={"Cache-Control": "public, max-age=31536000"})

async def download_single_panel(url: str, local_path: str, retries: int = 4):
    """
    Downloads an image using standard aiohttp request with intelligent backoff logic.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36"
    }
    
    timeout = aiohttp.ClientTimeout(total=40)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        for attempt in range(1, retries + 1):
            try:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        content = await resp.read()
                        if len(content) > 2000:  # Validate real image binary content
                            with open(local_path, "wb") as f:
                                f.write(content)
                            print(f"Successfully downloaded: {local_path}")
                            return True
                    print(f"Attempt {attempt}: Received status {resp.status}")
            except Exception as err:
                print(f"Attempt {attempt} exception: {err}")
            
            # Incremental delay between attempts to bypass rate limits
            await asyncio.sleep(attempt * 2)
            
    return False

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"show_preview": False, "error": None}
    )

@app.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    story_prompt: str = Form(""),
    characters: str = Form(""),
    story_tone: str = Form("Adventure"),
    setting: str = Form(""),
    art_style: str = Form("Comic"),
    num_panels: int = Form(5)
):
    try:
        clean_prompt = story_prompt.strip() if story_prompt else "Forest Magic Awakening"
        char_desc = characters.strip() if characters else "cute little girl, neat polished modern dress, innocent expression"
        title = clean_prompt[:30].title()
        
        run_seed = random.randint(100000, 999999)

        panel_details = [
            {
                "title": "Panel 1: The Magic Forest",
                "story": f"A breathtaking magical forest of {clean_prompt}.",
                "dialogue": f"Welcome to the enchanted forest of {clean_prompt}...",
                "prompt": f"american comic book page, classic Marvel DC artwork, detailed magical forest, bold ink outlines, retro comic shading, seed {run_seed}"
            },
            {
                "title": "Panel 2: Little Girl Enters",
                "story": f"A cute little girl steps into the deep woods.",
                "dialogue": "Wow, what a huge and beautiful forest!",
                "prompt": f"american comic book illustration, full body shot of a cute little girl, wearing neat elegant modest dress, polite polished look, walking into mystical woods, classic western graphic novel art style, seed {run_seed+1}"
            },
            {
                "title": "Panel 3: Discovering Artifact",
                "story": f"The little girl finds a glowing magical artifact.",
                "dialogue": "Look at this shining crystal! It looks magical!",
                "prompt": f"american comic book panel, graphic novel art, shot of a little girl in neat smart dress discovering a glowing crystal relic, surprised innocent expression, comic book line art, seed {run_seed+2}"
            },
            {
                "title": "Panel 4: Power Awakening",
                "story": f"Magic energy sparkles gently around the little girl.",
                "dialogue": "It feels warm and friendly!",
                "prompt": f"american comic book panel, adorable little girl empowered by magical glowing aura, wearing neat formal dress, dynamic shading, realistic comic proportions, seed {run_seed+3}"
            },
            {
                "title": "Panel 5: Happy Ending",
                "story": f"The little girl smiles happily with her new magic power.",
                "dialogue": "Yay! I made a new magical friend!",
                "prompt": f"american graphic novel portrait, cute close up face of a little girl, neat hair and elegant modest dress, cheerful innocent smile, dark ink shading, western comic art, seed {run_seed+4}"
            }
        ]

        panels = []
        for i in range(1, num_panels + 1):
            detail = panel_details[i - 1]
            prompt_text = detail["prompt"]
            
            encoded_prompt = urllib.parse.quote_plus(prompt_text)
            pollinations_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=512&model=flux&nologo=true"

            local_filename = f"panel_{run_seed}_{i}.jpg"
            local_filepath = os.path.join("static", "generated", local_filename)
            web_path = f"/static/generated/{local_filename}"

            # Strict sequential download with retry mechanism
            success = await download_single_panel(pollinations_url, local_filepath)
            
            # Wait 3 seconds before requesting the next image to strictly prevent Rate Limit (429)
            await asyncio.sleep(3.0)

            # Fallback path logic
            final_img_path = web_path if (success and os.path.exists(local_filepath)) else pollinations_url

            panels.append({
                "panel_number": i,
                "title": detail["title"],
                "story_text": detail["story"],
                "dialogue": detail["dialogue"],
                "image_path": final_img_path,
                "fallback_image": pollinations_url,
                "local_filepath": local_filepath
            })

        pdf_filename = f"comic_{run_seed}.pdf"
        output_pdf_path = os.path.join("static", "exports", pdf_filename)
        create_comic_pdf(title=title, panels=panels, output_path=output_pdf_path)

        return templates.TemplateResponse(
            request=request, 
            name="index.html", 
            context={
                "title": title, 
                "panels": panels, 
                "pdf_path": f"/static/exports/{pdf_filename}", 
                "show_preview": True, 
                "error": None
            }
        )

    except Exception as e:
        print(f"Generation Error: {e}")
        return templates.TemplateResponse(
            request=request, 
            name="index.html", 
            context={"show_preview": False, "error": str(e)}
        )

@app.get("/download-pdf")
async def download_pdf(file_path: str):
    clean_path = file_path.lstrip('/')
    if os.path.exists(clean_path):
        return FileResponse(
            path=clean_path, 
            filename=os.path.basename(clean_path), 
            media_type="application/pdf"
        )
    return {"error": "File not found"}