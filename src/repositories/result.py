from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.result import Result


class ResultRepository(BaseRepository[Result]):
    """Repository class for managing election results"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Result, session)
