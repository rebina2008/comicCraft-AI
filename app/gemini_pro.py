import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def generate_story(outline: list) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return ""

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        outline_text = ""
        for i, item in enumerate(outline):
            desc = item.get("scene_description", "") if isinstance(item, dict) else ""
            outline_text += f"Panel {i+1}: {desc}\n"

        prompt = f"""
        Write a 1-sentence narrative story for each of these 5 anime comic panels:
        {outline_text}

        STRICT FORMAT:
        Panel 1: [Short story for panel 1]
        ---
        Panel 2: [Short story for panel 2]
        ---
        Panel 3: [Short story for panel 3]
        ---
        Panel 4: [Short story for panel 4]
        ---
        Panel 5: [Short story for panel 5]
        """

        response = model.generate_content(prompt)
        if response and response.text:
            return response.text
    except Exception as e:
        print(f"Gemini Pro Error: {e}")

    return ""