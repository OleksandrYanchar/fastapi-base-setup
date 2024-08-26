from re import match

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.users import users_repository


async def validate_username(username: str, session: AsyncSession) -> str:
    """
    Asynchronously checks if given username is valid.

    Parameters:
    - Username: string to check.

    Returns:
    - Username if username is valid, otherwise raises an ValueError.
    """
    if await users_repository.get(session=session, username=username):
        raise ValueError("User with this username already exists")
    if len(username) < 4:
        raise ValueError("Username too short")
    if len(username) > 32:
        raise ValueError("Username too long")

    return username


async def validate_email(email: str, session: AsyncSession) -> str:
    """
    Asynchronously checks if given email is valid.

    Parameters:
    - email: string to check.

    Returns:
    - Email if email is valid, otherwise raises an ValueError.
    """
    # email validation pattern
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    # checking if passed email matches pattern
    if await users_repository.get(session=session, email=email):
        raise ValueError("User with this email already exists")
    if not match(pattern, email):
        raise ValueError("Invalid email format")
    return email


async def validate_password(password: str) -> bool:
    """
    Asynchronously checks if given email is valid.

    Parameters:
    - password: string to check.

    Returns:
    - Password if password is valid, otherwise raises an ValueError.
    """
    # checking if password ain't totaly numerical
    if password.isdigit():
        raise HTTPException(
            status_code=400, detail="Password can't be totaly numerical"
        )
    # checking if password's lens is greater or eaqual 8
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Your password is too short")
    return True
