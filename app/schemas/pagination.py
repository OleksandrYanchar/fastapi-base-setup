from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationSchema(BaseModel, Generic[T]):
    items: List[T]
    total: int
    offset: int
    limit: int
