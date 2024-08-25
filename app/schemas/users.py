import uuid
from typing import Optional

from pydantic import BaseModel

from app.schemas.tokens import TokenSchema


class UserSchema(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True


class UserCreateInSchema(UserSchema):
    password: str

    class Config:
        from_attributes = True


class UserCreateOutSchema(UserSchema):
    password: str

    tokens: TokenSchema

    class Config:
        from_attributes = True


class UserDataSchema(UserSchema):
    id: uuid.UUID
    email: str
    is_activated: bool
    avatar: Optional[str]


class UserLoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class UserPasswordChangeSchema(BaseModel):
    old_password: str
    new_password1: str
    new_password2: str

    class Config:
        from_attributes = True


class UserPasswordResetSchema(BaseModel):
    new_password1: str
    new_password2: str

    class Config:
        from_attributes = True


class UpdateUserDataSchema(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True
