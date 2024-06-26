from dotenv import load_dotenv
import os

load_dotenv()

MEDIA_DIR = os.getenv("MEDIA_DIR")
AVATARS_DIR = f"{MEDIA_DIR}avatars/"

os.makedirs(MEDIA_DIR, exist_ok=True)
os.makedirs(AVATARS_DIR, exist_ok=True)
