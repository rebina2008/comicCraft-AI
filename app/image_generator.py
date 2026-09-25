import os
import requests
import random
import time
from urllib.parse import quote

def generate_image(prompt: str, panel_index: int = 1) -> str:
    # 1. Image சேமிக்க static/panels ஃபோல்டரை உருவாக்குதல்
    output_dir = os.path.join("static", "panels")
    os.makedirs(output_dir, exist_ok=True)

    unique_seed = random.randint(100000, 999999) + panel_index
    timestamp = int(time.time() * 1000)

    # 2. Anime Girl Character Prompts & Dynamic Camera Angles
    panel_framings = [
        "anime girl character intro, wide view, beautiful detailed background",
        "anime girl looking shocked close up face expression, dramatic lighting",
        "anime girl dynamic action pose, side profile movement",
        "anime girl magical power climax scene, glowing energy aura",
        "anime girl peaceful ending shot, scenic sunset background"
    ]
    
    current_framing = panel_framings[(panel_index - 1) % len(panel_framings)]

    # 3. Enhanced Prompt Formulation
    enhanced_prompt = f"masterpiece japanese anime artwork, anime girl character, {prompt}, {current_framing}, 8k quality, vibrant colors"
    encoded_prompt = quote(enhanced_prompt)

    # Pollinations / Stable Diffusion Engine URL
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=768&seed={unique_seed}&nologo=true&model=turbo"

    filename = f"panel_{panel_index}_{timestamp}.jpg"
    filepath = os.path.join(output_dir, filename)

    try:
        time.sleep(1.2) # Avoid batch cache
        headers = {'User-Agent': f'ComicCraftBot/{unique_seed}'}
        response = requests.get(image_url, headers=headers, timeout=20)

        if response.status_code == 200 and len(response.content) > 3000:
            with open(filepath, "wb") as f:
                f.write(response.content)
            return f"/static/panels/{filename}?v={timestamp}"
        else:
            return image_url

    except Exception as e:
        print(f"Image Error: {e}")
        return image_url