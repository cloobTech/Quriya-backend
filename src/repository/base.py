from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.base import Base
from pydantic import EmailStr


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    def add(self, session: AsyncSession, obj):
        session.add(obj)
    
    async def save(self, session: AsyncSession, obj = None):
        if obj:
            self.add(session, obj)
        await session.commit()
    
    async def get_by_location(self, session: AsyncSession, cls: Base):
        smtp = select(cls)
        result = await session.execute(smtp)
        return result.scalars().all()
    
    async def get_by_id(self, session: AsyncSession, cls: Base, object_id:str):
        result = await session.execute(select(cls).where(cls.id == object_id))
        return result.scalar_one_or_none()
    

    async def get_by_column_name(self, session: AsyncSession, cls: Base, column_name: str):
        column = getattr(cls, column_name,  None)
        if column is None:
            return (f"{column_name} not found in db")
        smtp = await session.execute(select(column))
        result = [row[0] for row in smtp.all()]
        return result
    
    async def update_info(self, session: AsyncSession, cls: Base, id: str, key: str, value):
        result = await self.get_by_id(session, cls, id)
        if not result:
            return ("Record not found in db")
        setattr(result, key, value)
        await session.commit()
        return result
    
    async def get_by_user_id(self, session: AsyncSession, cls: Base, user_id: str):
        result = await session.execute(select(cls).where(cls.user_id == user_id))
        return result.scalars().first()
    
    async def delete_by_id(self, session: AsyncSession, cls: Base, id: str):
        result = await self.get_by_id(session, cls, id)
        if not  result:
            return (f"{cls.__name__} with {id} not in DB")
        await session.delete(result)
        await session.commit()
        return result
    
    
    async def get_by_email(self, session, model, email: EmailStr):
        result = await session.execute(select(model).where(model.email == email))
        return result.scalar_one_or_none()
    
    async def verify(self, session: AsyncSession, cls: Base, token):
        result = await session.execute(select(cls).where(cls.reset_token == token))
        return result