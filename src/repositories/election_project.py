from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.election_project import ElectionProject


class ElectionProjectRepository(BaseRepository[ElectionProject]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ElectionProject, session)
