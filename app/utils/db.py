from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.configs.db import engine

async_session_maker = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def get_async_session():
    async with async_session_maker() as session:
        yield session
