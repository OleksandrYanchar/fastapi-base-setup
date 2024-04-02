from sqlalchemy.ext.asyncio import create_async_engine
from configs.db import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from typing import Any, Dict

import humps
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import as_declarative, declared_attr


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return humps.depascalize(cls.__name__)

    def dict(self) -> Dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
