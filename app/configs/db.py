import os
from typing import Any, Dict

import humps
from configs.general import DEBUG_MODE
from dotenv import load_dotenv
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr

load_dotenv()
"""Postgres database connection setup"""
DB_NAME = os.getenv("DB_NAME")
DB_PASS = os.getenv("DB_PASS")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

"""Redis connection setup"""
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"


# Create an asynchronous engine for the database
engine = create_async_engine(
    DATABASE_URL,
    echo=DEBUG_MODE,
    pool_size=10,
    max_overflow=10,
)


# Define a base class for the SQLAlchemy models
@as_declarative()
class Base:
    __name__: str

    # Define a method to automatically generate table names in snake_case
    @declared_attr
    def __tablename__(cls) -> str:
        return humps.depascalize(cls.__name__)

    # Define a method to convert the model instance to a dictionary
    def dict(self) -> Dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
