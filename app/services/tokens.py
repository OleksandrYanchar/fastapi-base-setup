from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_SECRET,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET,
)
from app.configs.logger import init_logger
from app.models.users import Users
from app.repositories.tokens import TokensRepository, token_repository
from app.repositories.users import users_repository
from app.schemas.tokens import (
    RefreshTokenRequestSchema,
    TokenPayloadSchema,
    TokenSchema,
)

logger = init_logger(__file__)


class TokenService:
    @staticmethod
    async def create_jwt_tokens(user: Users) -> TokenSchema:
        token_payload = TokenPayloadSchema(
            user_id=str(user.id),
            username=user.username,
            is_activated=user.is_activated,
        )

        to_encode = token_payload.dict()
        access_token_expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": access_token_expire})
        encoded_access = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

        refresh_token_expire = datetime.utcnow() + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )
        to_encode.update({"exp": refresh_token_expire})
        encoded_refresh = jwt.encode(to_encode, REFRESH_SECRET, algorithm=ALGORITHM)

        return TokenSchema(
            access_token=encoded_access,
            refresh_token=encoded_refresh,
            token_type="bearer",
        )

    @staticmethod
    async def verify_token(token: str, token_type: str) -> TokenPayloadSchema:
        secret = REFRESH_SECRET if token_type == "refresh_token" else SECRET
        try:
            payload = jwt.decode(token, secret, algorithms=[ALGORITHM])

            user_id: str = payload.get("user_id")
            username: Optional[str] = payload.get("username")

            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token does not contain user_id.",
                )

            return TokenPayloadSchema(user_id=user_id, username=username)

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The token has expired. Please refresh your token.",
            )
        except JWTError as e:
            logger.error(f"JWT decoding error: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials.",
            )

    @staticmethod
    async def is_token_blacklisted(token: str, session: AsyncSession) -> bool:

        return await TokensRepository.is_token_blacklisted(token, session)

    @staticmethod
    async def blacklist_token(token: str, session: AsyncSession):
        try:
            await token_repository.create(session, obj_in={"token": token})
        except Exception as e:
            await session.rollback()
            logger.error(f"Error blacklisting token: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error occurred during token blacklisting.",
            )

    @staticmethod
    async def refresh_token(
        refresh_token_request: RefreshTokenRequestSchema,
        session: AsyncSession,
    ):
        try:
            refresh_token = refresh_token_request.token
            if await TokenService.is_token_blacklisted(refresh_token, session):
                raise HTTPException(status_code=400, detail="Token is blacklisted")

            payload = await TokenService.verify_token(refresh_token, "refresh_token")

            user = await users_repository.get(session, id=payload.user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            tokens = await TokenService.create_jwt_tokens(user)
            await TokenService.blacklist_token(refresh_token, session)
            return tokens

        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error refreshing token: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error occurred during token refreshing",
            )
