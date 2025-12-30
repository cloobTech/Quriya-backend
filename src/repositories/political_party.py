from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.political_party import PoliticalParty


class PoliticalPartyRepository(BaseRepository[PoliticalParty]):
    """Repository class for managing political parties"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(PoliticalParty, session)
