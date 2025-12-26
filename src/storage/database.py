from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from models.base import Base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from pydantic import EmailStr
from models import customer, service_provider, admin
class DBstorage:
    def __init__(self, db_url: str = "sqlite+aiosqlite:///mysqlalchemy.db"):
        self.__engine = create_async_engine(db_url, echo=False)
        self.__session_maker = async_sessionmaker(self.__engine, expire_on_commit=False)

    async def create_table(self):
        """Creating a table in the database"""
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def drop_tables(self):
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)