import os
import re
from PIL import Image

def generate_image(prompt: str, panel_number: int = 1) -> str:
    # Safe filename creation
    clean_prompt = re.sub(r'[^a-zA-Z0-9]', '_', prompt[:15])
    filename = f"panel_{panel_number}_{clean_prompt}.png"
    
    path = f"static/panels/{filename}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Mock Image creation (Solid colored panel with text fallback)
    img = Image.new('RGB', (512, 512), color=(50, 80, 120))
    img.save(path)
    
    return path