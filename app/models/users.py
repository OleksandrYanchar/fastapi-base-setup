from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.configs.db import Base
from app.models.annotes import unique_str_255, uuidpk


class Users(Base):
    __tablename__ = "users"

    id: Mapped[uuidpk]

    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    emalil: Mapped[unique_str_255]

    password: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)

    is_activated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    avatar: Mapped[str] = mapped_column(String, nullable=True)
