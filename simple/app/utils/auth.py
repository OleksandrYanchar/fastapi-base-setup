from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import Users
from app.repositories.users import users_repository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_pass):
    return pwd_context.verify(plain_password, hashed_pass)


async def verify_user_credentials(
    username: str, password: str, session: AsyncSession
) -> Users:
    user = await users_repository.get(session, username=username)

    if not user:
        user = await users_repository.get(session, email=username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user with this email or username dosent exist",
        )

    if not pwd_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return user


async def is_user_not_activated(user: Users):
    if user.is_activated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is activated",
        )
    else:
        return True
