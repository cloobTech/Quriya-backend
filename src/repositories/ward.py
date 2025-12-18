from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.ward import Ward


class WardRepository(BaseRepository[Ward]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Ward, session)

    async def get_existing_ids(self, ids: set[str]) -> set[str]:
        """
        Return the subset of IDs that actually exist in the wards table.
        """
        if not ids:
            return set()

        stmt = select(self.model.id).where(self.model.id.in_(ids))
        result = await self.session.execute(stmt)
        return {row[0] for row in result}