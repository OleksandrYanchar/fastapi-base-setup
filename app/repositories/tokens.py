from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.logger import init_logger
from app.models.tokens import BlacklistedToken
from app.repositories.base import BaseRepository
from app.schemas.tokens import RefreshTokenRequestSchema

logger = init_logger(__file__)


class TokensRepository(
    BaseRepository[
        BlacklistedToken, RefreshTokenRequestSchema, RefreshTokenRequestSchema
    ]
):
    @staticmethod
    async def is_token_blacklisted(token: str, db: AsyncSession) -> bool:
        result = await db.execute(
            select(BlacklistedToken).filter(BlacklistedToken.token == token)
        )
        return result.scalars().first() is not None


token_repository = TokensRepository(BlacklistedToken)
