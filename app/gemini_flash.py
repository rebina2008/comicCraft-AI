import os
import warnings
import google.generativeai as genai

# Suppress deprecation warning
warnings.filterwarnings("ignore", category=FutureWarning)

api_key = os.getenv("GEMINI_API_KEY", "")
if api_key:
    genai.configure(api_key=api_key)

def generate_outline(prompt: str):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            f"Create a 5-panel comic outline based on: {prompt}. Return JSON list of 5 objects with keys: panel_number, panel_title, image_prompt, dialogue_or_narration."
        )
        import json
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
        return json.loads(text)
    except Exception as e:
        print(f"Outline generation error: {e}")
        return [
            {"panel_number": 1, "panel_title": "Introduction", "image_prompt": "character introduction scene", "dialogue_or_narration": "The story begins..."},
            {"panel_number": 2, "panel_title": "Rising Action", "image_prompt": "character looking shocked", "dialogue_or_narration": "Something happens!"},
            {"panel_number": 3, "panel_title": "Confrontation", "image_prompt": "intense conflict scene", "dialogue_or_narration": "A challenge appears."},
            {"panel_number": 4, "panel_title": "Climax", "image_prompt": "epic glowing action battle", "dialogue_or_narration": "The moment of truth!"},
            {"panel_number": 5, "panel_title": "Resolution", "image_prompt": "peaceful sunset scene", "dialogue_or_narration": "All is quiet again."}
        ]