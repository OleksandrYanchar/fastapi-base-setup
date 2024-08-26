from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.logger import init_logger
from app.models.users import Users
from app.repositories.users import users_repository
from app.services.tokens import TokenService
from app.utils.db import get_async_session

logger = init_logger(__file__)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> Users:
    token_data = await TokenService.verify_token(token, "access")
    user = await users_repository.get(session, id=token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    logger.info(user.dict())
    return user
