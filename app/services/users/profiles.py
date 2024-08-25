from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.users import users_repository
from app.schemas.pagination import PaginationSchema
from app.schemas.users import UserDataSchema


class UsersProfileService:

    @staticmethod
    async def get_profile_by_username(
        username: str, session: AsyncSession
    ) -> UserDataSchema:
        user = await users_repository.get(session, username=username)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="The user with this username does not exist in the system",
            )
        return UserDataSchema(**user.dict())

    @staticmethod
    async def get_all_users(
        session: AsyncSession, offset: int, limit: int
    ) -> PaginationSchema:
        users, total = await users_repository.get_multi(
            session, offset=offset, limit=limit
        )

        result_users = [UserDataSchema(**user.dict()) for user in users]
        return PaginationSchema(
            total=total, items=result_users, offset=offset, limit=limit
        )
