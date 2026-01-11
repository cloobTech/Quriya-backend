from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.models.base import Base


class Database:
    """Database class for managing connections and operations."""

    # __engine = None
    # __session_maker = None

    def __init__(self, db_uri: str):
        """Initialize the database storage class"""
        self.__engine = create_async_engine(db_uri, echo=True)
        self.__session_maker = async_sessionmaker(
            self.__engine, expire_on_commit=False)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Create and return a session object"""
        async with self.__session_maker() as session:
            yield session

    async def create_tables(self) -> None:
        """Create all tables in the database"""
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self) -> None:
        """Drop all tables in the database (use with caution)"""
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def cleanup(self) -> None:
        """Cleanup database resources"""
        await self.__engine.dispose()
