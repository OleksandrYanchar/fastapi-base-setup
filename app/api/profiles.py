from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.logger import init_logger
from app.dependencies.auth import get_current_user
from app.models.users import Users
from app.schemas.pagination import PaginationSchema
from app.schemas.users import UserDataSchema
from app.services.users.profiles import UsersProfileService
from app.utils.db import get_async_session

logger = init_logger(__file__)

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)


@router.get("/me", response_model=UserDataSchema)
async def get_my_profile(
    user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await UsersProfileService.get_profile_by_username(user.username, session)


@router.get("/all", response_model=PaginationSchema[UserDataSchema])
async def get_all_profiles(
    offset: int = Query(default=0),
    limit: int = Query(default=2),
    session: AsyncSession = Depends(get_async_session),
) -> PaginationSchema[UserDataSchema]:
    return await UsersProfileService.get_all_users(
        session=session, offset=offset, limit=limit
    )


@router.get("/{username}", response_model=UserDataSchema)
async def get_profile_by_username(
    username: str, session: AsyncSession = Depends(get_async_session)
):
    return await UsersProfileService.get_profile_by_username(username, session)
