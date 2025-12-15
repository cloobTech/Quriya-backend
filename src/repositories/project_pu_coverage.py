from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.project_pu_coverage import ProjectPuCoverage


class PuCoverageRepository(BaseRepository[ProjectPuCoverage]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProjectPuCoverage, session)