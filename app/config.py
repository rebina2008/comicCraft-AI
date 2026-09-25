import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
HF_API_KEY = os.getenv("HF_API_KEY", "")

DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

GEMINI_FLASH_MODEL = os.getenv(
    "GEMINI_FLASH_MODEL",
    "gemini-1.5-flash"
)

GEMINI_PRO_MODEL = os.getenv(
    "GEMINI_PRO_MODEL",
    "gemini-1.5-pro"
)

HF_MODEL = os.getenv(
    "HF_MODEL",
    "runwayml/stable-diffusion-v1-5"
)


PANELS_DIR = BASE_DIR / "static" / "panels"
EXPORTS_DIR = BASE_DIR / "static" / "exports"

PANELS_DIR.mkdir(parents=True, exist_ok=True)

FLASH_MODEL = GEMINI_FLASH_MODEL
PRO_MODEL = GEMINI_PRO_MODEL
HF_TOKEN = HF_API_KEY