from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.logger import init_logger
from app.dependencies.auth import get_current_user
from app.models.users import Users
from app.schemas.tokens import RefreshTokenRequestSchema, TokenSchema
from app.schemas.users import UserCreateInSchema, UserCreateOutSchema
from app.services.tokens import TokenService
from app.services.users.auth import AuthService
from app.utils.db import get_async_session

logger = init_logger(__file__)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/signup", response_model=UserCreateOutSchema)
async def create_user(
    user_request: UserCreateInSchema,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> UserCreateOutSchema:
    return await AuthService.create_user(user_request, request, session)


@router.get("/verification")
async def email_verification(
    token: str, session: AsyncSession = Depends(get_async_session)
):
    return await AuthService.email_verification(token, session)


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    return await AuthService.login_for_access_token(form_data, session)


@router.post("/token/refresh", response_model=TokenSchema)
async def refresh_token(
    refresh_token_request: RefreshTokenRequestSchema,
    session: AsyncSession = Depends(get_async_session),
):
    return await TokenService.refresh_token(refresh_token_request, session)


@router.post("/resend-verification")
async def resend_verification_email(
    request: Request, user: Users = Depends(get_current_user)
):
    await AuthService.resend_verification_email(request, user)
    return {"detail": "Verification email was sent"}
