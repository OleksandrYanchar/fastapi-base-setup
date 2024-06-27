import uuid

from configs.db import Base
from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
