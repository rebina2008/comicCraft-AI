import os
import json
from google import genai

def get_client():
    """Fetches API key safely without crashing server at startup."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")
    return genai.Client(api_key=api_key)

def generate_comic_story(prompt: str) -> dict:
    """Generates a structured 5-panel comic outline using Gemini."""
    system_instruction = """
    You are an expert comic book story writer. Given a prompt, return a valid JSON object with:
    - "title": A catchy title for the comic
    - "panels": A list of 5 objects, each having:
        - "panel_number": int (1 to 5)
        - "title": panel scene heading
        - "description": visual prompt description
        - "dialogue": text spoken in the panel
    Return ONLY pure JSON.
    """

    try:
        client = get_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Create a 5-panel comic outline based on this idea: {prompt}",
            config={"system_instruction": system_instruction}
        )

        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)

    except Exception as e:
        print(f"Error in Gemini Flash Outline Generation: {e}")
        # Fallback response so application stays alive
        return {
            "title": "ComicCraft AI Adventure",
            "panels": [
                {
                    "panel_number": i,
                    "title": f"Panel {i}",
                    "description": f"Scene {i} for prompt: {prompt}",
                    "dialogue": "..."
                } for i in range(1, 6)
            ]
        }