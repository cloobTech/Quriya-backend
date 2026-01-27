from typing import Generic, Sequence, Type, TypeVar, Optional
from sqlalchemy import func, select, update, exists
from sqlalchemy.ext.asyncio import AsyncSession
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

    async def bulk_create(self, data: list[ModelType]):
        """Create multiple data db record"""

        self.session.add_all(data)

    async def get_by_id(self, id: str) -> Optional[ModelType]:
        """Retrieve a record by its ID."""
        result = await self.session.get(self.model, id)

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

    async def filter_by(self, **kwargs) -> list[ModelType]:
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def filter_one(self, **kwargs) -> Optional[ModelType]:
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return result.scalars().first()

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

    async def exists(self, **kwargs) -> bool | None:
        stmt = select(
            exists().where(
                *[getattr(self.model, k) == v for k, v in kwargs.items()]
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def all_ids_exist(self, ids: list[str]) -> bool:
        if not ids:
            return True  # or False, depending on your rule

        stmt = (
            select(func.count())
            .select_from(self.model)
            .where(self.model.id.in_(ids))  # type: ignore[attr-defined]
        )

        result = await self.session.execute(stmt)
        count = result.scalar_one()

        return count == len(set(ids))

    async def paginate(self,
                       stmt,
                       *,
                       offset: int,
                       limit: int) -> tuple[list[ModelType], int]:
        """Fetch records with pagination."""
        count_stmt = select(func.count()).select_from(
            stmt.distinct().subquery())
        total = await self.session.scalar(count_stmt) or 0
        result = await self.session.scalars(
            stmt.distinct().offset(offset).limit(limit)
        )
        return list(result.all()), total
