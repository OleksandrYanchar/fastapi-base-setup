from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.logger import init_logger
from app.models.users import Users
from app.repositories.users import users_repository
from app.schemas.users import UserCreateInSchema, UserCreateOutSchema
from app.services.email import verify_email_sender
from app.services.tokens import TokenService
from app.utils.auth import get_password_hash, verify_user_credentials
from app.utils.validators import validate_email, validate_password, validate_username

logger = init_logger(__file__)


class AuthService:
    @staticmethod
    async def create_user(
        user_request: UserCreateInSchema, request: Request, session: AsyncSession
    ) -> UserCreateOutSchema:

        try:
            validate_password(user_request.password)

            await validate_email(user_request.email, session)
            await validate_username(user_request.username, session)

            user_request.password = get_password_hash(user_request.password)
            obj_in = UserCreateInSchema(**user_request.dict())

            # Create the new user in the database
            new_user = await users_repository.create(session, obj_in)

            # Send verification email
            await verify_email_sender.send_email(
                new_user, request, "send-verification.html"
            )

            # Create JWT tokens for the new user
            tokens = await TokenService.create_jwt_tokens(new_user)

            return UserCreateOutSchema(**new_user.dict(), tokens=tokens)

        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except HTTPException as e:
            # Re-raise HTTP exceptions to be handled appropriately
            raise e
        except Exception as e:
            logger.error(f"Error during user registration: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during user registration.",
            )

    @staticmethod
    async def email_verification(token: str, session: AsyncSession):
        try:
            # Remove any whitespace or newline characters from the token string
            token = token.strip()
            # Verify the token and extract data
            token_data = await TokenService.verify_token(token, "access_token")

            user_id = str(token_data.user_id)
            logger.debug(
                f"Decoded token data: {token_data}"
            )  # Log the token data for debugging

            # Log the user_id before attempting to retrieve the user
            logger.debug(f"Attempting to retrieve user with user_id: {user_id}")

            # Retrieve user from the database
            user = await users_repository.get(session, id=user_id)
            if user is None:
                logger.error(f"User not found for user_id: {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if user.is_activated:
                logger.info(f"User {user_id} already activated.")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User is already activated",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Update user activation status
            user = await users_repository.update(
                session, db_obj=user, obj_in={"is_activated": True}
            )
            return {"username": user.username, "is_active": user.is_activated}

        except HTTPException as e:
            # Re-raise HTTP exceptions to be handled appropriately
            raise e
        except Exception as e:
            logger.error(f"Verification error: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error occurred during email verification.",
            )

    @staticmethod
    async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm, session: AsyncSession
    ):
        try:
            user = await verify_user_credentials(
                form_data.username, form_data.password, session
            )
            tokens = await TokenService.create_jwt_tokens(
                user
            )  # Await the async function call
            return tokens
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Verification error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error occurred during verifying credentials",
            )

    @staticmethod
    async def resend_verification_email(request: Request, user: Users):
        try:
            await verify_email_sender.send_email(
                [user.email], request, "send-verification.html"
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Verification error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error occurred during email verification",
            )
