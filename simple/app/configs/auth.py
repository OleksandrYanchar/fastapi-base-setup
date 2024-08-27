import os

from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("SECRET")
REFRESH_SECRET = os.getenv("REFRESH_SECRET")
ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

REFRESH_TOKEN_EXPIRE_DAYS = REFRESH_TOKEN_EXPIRE_MINUTES * 24 * 7