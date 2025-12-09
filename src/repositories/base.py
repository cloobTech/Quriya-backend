from typing import Generic, Sequence, Type, TypeVar, Optional
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError
from src.models.base import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository providing common database operations for models."""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, obj: ModelType) -> ModelType:
        """Create a new record."""
        
        self.session.add(obj)
        return obj

    async def get_by_id(self, id: str) -> Optional[ModelType]:
        """Retrieve a record by its ID."""
        result = await self.session.get(self.model, id)
        # if not result:
        #     raise NoResultFound(
        #         f"{self.model.__name__} with ID {id} not found")
        return result


    async def get_all(self) -> Sequence[ModelType]:
        """Fetch all records."""
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete(self, id: str, soft: bool = False) -> bool:
        """Delete a record by its ID. Supports soft delete if the model has 'is_deleted' attribute."""
        obj = await self.get_by_id(id)
        if not obj:
            return False

        if soft and hasattr(obj, "is_deleted"):
            setattr(obj, "is_deleted", True)
        else:
            await self.session.delete(obj)

        return True

    async def filter_by(self, **kwargs) -> Sequence[ModelType]:
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, id: str, filters: dict | None = None, data: dict | None = None) -> bool:
        if not data:
            return False

        IGNORE_LIST = [
            'id', 'created_at', 'updated_at'
        ]
        updated_dict = {}
        if data:
            updated_dict = {
                key: value for key, value in data.items() if key not in IGNORE_LIST
            }

        stmt = update(self.model).values(**updated_dict)
        if id:
            stmt = stmt.where(getattr(self.model, "id") == id)
        elif filters:
            stmt = stmt.filter_by(**filters)
        else:
            raise ValueError(
                "You must provide either id or filters to update.")

        await self.session.execute(stmt)
        return True

    async def exists(self, **kwargs) -> bool:
        stmt = select(func.count()).select_from(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        scalar_result = result.scalar()
        return scalar_result is not None and scalar_result > 0
