from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.media import ResultMedia


class ResultMediaRepository(BaseRepository[ResultMedia]):
    """Repository class for managing media associated with election results"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ResultMedia, session)