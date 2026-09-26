import os
import re
import io
import urllib.parse
import requests
from PIL import Image, ImageDraw

def generate_image(prompt: str, panel_number: int = 1) -> str:
    folder_path = os.path.join("static", "panels")
    os.makedirs(folder_path, exist_ok=True)
    
    # 1. Fixed Clean Filename per panel
    clean_prompt = re.sub(r'[^a-zA-Z0-9]', '_', prompt[:12])
    filename = f"panel_{panel_number}_{clean_prompt}.png"
    file_path = os.path.join(folder_path, filename)
    
    # 2. Strict Prompt Format
    anime_prompt = f"anime style artwork, studio ghibli vibe, vivid colors, comic panel, {prompt}"
    encoded_prompt = urllib.parse.quote(anime_prompt)
    
    # 3. FIXED SEED (Indha seed dhani panel-ku eppovumey maaradhu - exact same image tharum)
    fixed_seed = panel_number * 555
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&seed={fixed_seed}&nologo=true"
    
    try:
        response = requests.get(image_url, timeout=25)
        if response.status_code == 200 and len(response.content) > 1000:
            image_bytes = io.BytesIO(response.content)
            img = Image.open(image_bytes).convert("RGB")
            # Save strictly as valid PNG
            img.save(file_path, "PNG")
            return f"static/panels/{filename}"
    except Exception as e:
        print(f"Pollinations Fetch Exception Panel {panel_number}: {e}")

    # Fallback Image (In case network down-a irundha)
    if not os.path.exists(file_path):
        img = Image.new('RGB', (512, 512), color=(30, 45, 65))
        draw = ImageDraw.Draw(img)
        draw.rectangle([10, 10, 502, 502], outline=(200, 200, 200), width=3)
        draw.text((30, 230), f"Panel {panel_number}\n[Anime Scene Generated]", fill=(255, 255, 255))
        img.save(file_path, "PNG")
    
    return f"static/panels/{filename}"