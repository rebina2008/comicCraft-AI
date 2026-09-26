import os
import re

def sanitize_filename(prompt: str) -> str:
    clean = re.sub(r'[^a-zA-Z0-9]', '_', prompt[:20])
    return f"{clean}.png"

def generate_image(prompt: str, filename: str = None):
    if not filename:
        filename = sanitize_filename(prompt)
    
    # Note: Replace this placeholder or initialize diffusers pipe locally
    # pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    # image = pipe(prompt).images[0]
    
    path = f"static/panels/{filename}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Temporary blank/mock image generation if PyTorch GPU is limited
    from PIL import Image
    img = Image.new('RGB', (512, 512), color=(73, 109, 137))
    img.save(path)
    
    return path