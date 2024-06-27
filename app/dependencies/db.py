from configs.db import engine
from sqlalchemy.ext.asyncio import async_sessionmaker

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with async_session_maker() as session:
        yield session
