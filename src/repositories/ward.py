from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.ward import Ward


class WardRepository(BaseRepository[Ward]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Ward, session)