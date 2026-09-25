import os
import requests
import random
import time
from urllib.parse import quote

def generate_image(prompt: str, panel_index: int = 1) -> str:
    output_dir = os.path.join("static", "panels")
    os.makedirs(output_dir, exist_ok=True)

    unique_seed = random.randint(100000, 999999) + (panel_index * 77)
    timestamp = int(time.time() * 1000)

    # Clean & Format Anime Prompt
    clean_prompt = prompt.replace("\n", " ").strip()
    enhanced_prompt = f"masterpiece japanese anime artwork, anime girl character, {clean_prompt}, vibrant colors, highly detailed"
    encoded_prompt = quote(enhanced_prompt)

    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=768&seed={unique_seed}&nologo=true&model=turbo"

    filename = f"panel_{panel_index}_{timestamp}.jpg"
    filepath = os.path.join(output_dir, filename)

    try:
        time.sleep(1.0)
        headers = {'User-Agent': f'Mozilla/5.0 ComicCraft/{unique_seed}'}
        response = requests.get(image_url, headers=headers, timeout=20)

        if response.status_code == 200 and len(response.content) > 3000:
            with open(filepath, "wb") as f:
                f.write(response.content)
            return f"/static/panels/{filename}?v={timestamp}"
        else:
            return image_url

    except Exception as e:
        print(f"Panel {panel_index} Generation error: {e}")
        return image_url