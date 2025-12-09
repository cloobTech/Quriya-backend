from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.polling_unit import PollingUnit


class PollingRepository(BaseRepository[PollingUnit]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(PollingUnit, session)