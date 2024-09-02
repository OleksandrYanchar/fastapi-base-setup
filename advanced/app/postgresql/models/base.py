from typing import Any, Dict
from sqlalchemy import MetaData, inspect
from sqlalchemy.ext.declarative import as_declarative, declared_attr
import humps

# Define shared metadata
metadata = MetaData()

@as_declarative(metadata=metadata)
class BaseORM:
    __name__: str

    # Automatically generate table names in snake_case
    @declared_attr
    def __tablename__(cls) -> str:
        return humps.depascalize(cls.__name__)

    # Convert the model instance to a dictionary
    def dict(self) -> Dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
