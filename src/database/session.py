from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config.settings import get_settings
from database.models import Base

settings = get_settings()
DATABASE_URL = f"sqlite+aiosqlite:///{settings.PATH_TO_DB}"
engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSQLiteSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db() -> None:
    await engine.dispose()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSQLiteSessionLocal() as session:
        yield session

@asynccontextmanager
async def get_db_contextmanager() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSQLiteSessionLocal() as session:
        yield session

async def reset_sqlite_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
