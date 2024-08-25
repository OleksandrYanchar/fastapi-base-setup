import os

from dotenv import load_dotenv

load_dotenv()

MEDIA_DIR = os.getenv("MEDIA_DIR")
AVATARS_DIR = f"{MEDIA_DIR}/avatars"
os.makedirs(MEDIA_DIR, exist_ok=True)
os.makedirs(AVATARS_DIR, exist_ok=True)

DEBUG_MODE = True if os.getenv("DEBUG", "0").lower() in ("true", "1", "t") else False
