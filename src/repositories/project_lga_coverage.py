from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.project_lga_coverage import ProjectLgaCoverage


class LgaCoverageRepository(BaseRepository[ProjectLgaCoverage]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProjectLgaCoverage, session)