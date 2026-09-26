import json
import re
import os
from google import genai

def generate_outline(user_prompt: str) -> list:
    prompt = f"""
You are a professional AI comic planner.

Generate a strictly formatted JSON list containing 5 panel descriptions for a comic based on the story idea below:

STORY: "{user_prompt}"

Return ONLY a JSON array with objects containing these exact keys:
- "panel" (integer)
- "title" (string)
- "scene_description" (string)
- "image_prompt" (string)

Example valid format:
[
  {{
    "panel": 1,
    "title": "Title here",
    "scene_description": "Scene description here",
    "image_prompt": "Image prompt for text to image generator"
  }}
]
"""
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Using stable/supported model string
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
        )
        
        output_text = response.text.strip()

        json_match = re.search(r'\[.*\]', output_text, re.DOTALL)
        if json_match:
            output_text = json_match.group(0)

        panel_data = json.loads(output_text)

        if not isinstance(panel_data, list):
            return []

        cleaned_data = []
        for idx, panel in enumerate(panel_data, start=1):
            if isinstance(panel, dict):
                cleaned_data.append({
                    "panel": panel.get("panel", idx),
                    "title": panel.get("title", f"Panel {idx}"),
                    "scene_description": panel.get("scene_description", "A scene in the story."),
                    "image_prompt": panel.get("image_prompt", user_prompt)
                })

        return cleaned_data

    except Exception as e:
        print(f"Error in Gemini Flash Outline Generation: {str(e)}")
        # Dynamic fallback for 5 panels if API fails
        return [
            {
                "panel": i,
                "title": f"Panel {i}",
                "scene_description": f"Scene description for panel {i}",
                "image_prompt": f"Anime style illustration of {user_prompt}, panel {i}"
            } for i in range(1, 6)
        ]