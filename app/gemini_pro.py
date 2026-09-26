import os
from google import genai

def generate_story(outline: list) -> str:
    formatted_outline = "\n".join([f"[{i+1}]. {item}" for i, item in enumerate(outline)])
    
    prompt = f"""
You're a comic book writer.

Given the following panel breakdown, write a comic-style story with engaging narration and character dialogues for each panel.

Panel Outline:
{formatted_outline}

Guidelines:
- Use a fun and engaging tone, like an actual comic book.
- Include narration and clearly marked character lines.
- Keep each panel self-contained but part of a cohesive story.
"""
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error generating story: {str(e)}"