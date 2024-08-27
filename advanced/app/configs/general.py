import os
from pydantic_settings import BaseSettings
from pydantic import validator, root_validator


class GeneralSettings(BaseSettings):
    SERVICE_NAME: str = "check-splitter"
    DEBUG: bool = False
    MEDIA_DIR: str

    @validator("DEBUG", pre=True)
    def validate_debug(cls, v):
        if isinstance(v, str):
            return v.lower() in ("1", "true", "yes", "on")
        return bool(v)

    @root_validator(pre=True)
    def create_media_dir(cls, values: dict[str, str]):
        media_dir = values.get("MEDIA_DIR")
        if media_dir and not os.path.exists(media_dir):
            try:
                os.makedirs(media_dir, exist_ok=True)
            except OSError as e:
                raise RuntimeError(f"Failed to create media directory: {e}")
        return values
