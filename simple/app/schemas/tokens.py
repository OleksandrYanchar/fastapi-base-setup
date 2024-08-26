from typing import Optional

from pydantic import BaseModel


class TokenPayloadSchema(BaseModel):
    user_id: str
    username: Optional[str] = None
    is_activated: Optional[bool] = None
    is_staff: Optional[bool] = None


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequestSchema(BaseModel):
    token: str
