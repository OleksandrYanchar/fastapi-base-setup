import uuid

from pydantic import BaseModel


class CreateAuthorSchema(BaseModel):

    name: str


class UpdateAuthorSchema(BaseModel):
    id: uuid.UUID

    name: str


class AuthorSchema(BaseModel):
    id: uuid.UUID
    name: str
