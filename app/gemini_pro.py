import os
import requests
import io
from PIL import Image, ImageDraw
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def generate_image(prompt, panel_number=1):
    panels_dir = os.path.join("static", "panels")
    os.makedirs(panels_dir, exist_ok=True)

    output_path = os.path.join(panels_dir, f"panel_{panel_number}.png")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # Endpoint 1: Nekos.best API (Timeout increased to 8s)
    try:
        api_url = "https://nekos.best/api/v2/neko"
        res = requests.get(api_url, headers=headers, timeout=8, verify=False)
        if res.status_code == 200:
            image_url = res.json()["results"][0]["url"]
            img_res = requests.get(image_url, headers=headers, timeout=8, verify=False)
            if img_res.status_code == 200 and len(img_res.content) > 3000:
                img = Image.open(io.BytesIO(img_res.content)).convert("RGB").resize((512, 512))
                img.save(output_path, "PNG")
                print(f"Panel {panel_number} Anime Image downloaded successfully!")
                return f"static/panels/panel_{panel_number}.png"
    except Exception as e:
        print(f"Nekos API failed for Panel {panel_number}: {e}")

    # Endpoint 2: Waifu.pics API Backup
    try:
        res = requests.get("https://api.waifu.pics/sfw/waifu", headers=headers, timeout=8, verify=False)
        if res.status_code == 200:
            image_url = res.json().get("url")
            img_res = requests.get(image_url, headers=headers, timeout=8, verify=False)
            if img_res.status_code == 200 and len(img_res.content) > 3000:
                img = Image.open(io.BytesIO(img_res.content)).convert("RGB").resize((512, 512))
                img.save(output_path, "PNG")
                print(f"Panel {panel_number} Backup Waifu Image downloaded successfully!")
                return f"static/panels/panel_{panel_number}.png"
    except Exception as e:
        print(f"Waifu API failed for Panel {panel_number}: {e}")

    # Endpoint 3: Unsplash Stream Fallback
    try:
        stream_url = f"https://loremflickr.com/512/512/anime,manga/all?lock={panel_number * 31}"
        img_res = requests.get(stream_url, headers=headers, timeout=8, verify=False)
        if img_res.status_code == 200 and len(img_res.content) > 3000:
            img = Image.open(io.BytesIO(img_res.content)).convert("RGB").resize((512, 512))
            img.save(output_path, "PNG")
            print(f"Panel {panel_number} Stream Image saved successfully!")
            return f"static/panels/panel_{panel_number}.png"
    except Exception as e:
        print(f"Stream API failed for Panel {panel_number}: {e}")

    return create_fallback_image(output_path, panel_number)


def create_fallback_image(path, panel_number):
    img = Image.new('RGB', (512, 512), color=(20, 25, 40))
    d = ImageDraw.Draw(img)
    d.rectangle([(12, 12), (500, 500)], outline=(0, 210, 255), width=6)
    d.text((180, 240), f"Anime Panel {panel_number}", fill=(255, 255, 255))
    img.save(path, "PNG")
    return f"static/panels/panel_{panel_number}.png"