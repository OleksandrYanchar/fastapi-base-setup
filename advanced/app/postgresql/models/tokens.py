from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.postgresql.models.base import BaseORM
from app.postgresql.models.annotes import created_at, uuidpk


class BlacklistedToken(BaseORM):
    __tablename__ = "blacklisted_tokens"

    id: Mapped[uuidpk]
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    blacklisted_on: Mapped[created_at]

    def __repr__(self):
        return f"<BlacklistedToken token={self.token}>"
