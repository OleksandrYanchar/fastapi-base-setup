import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import Integer, String, text
from sqlalchemy.orm import mapped_column

uuidpk = Annotated[
    uuid.UUID,
    mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
]

created_at = Annotated[
    datetime, mapped_column(server_default=text("TIMEZONE('utc', now())")),
]

unique_str_255 = Annotated[str, mapped_column(String(255), nullable=False, unique=True)]

optional_str_255 = Annotated[
    str, mapped_column(String(64), nullable=True, unique=False),
]

optional_int = Annotated[int, mapped_column(Integer, nullable=True, unique=False)]
