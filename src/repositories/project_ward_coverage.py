from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.project_ward_coverage import ProjectWardCoverage


class WardCoverageRepository(BaseRepository[ProjectWardCoverage]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProjectWardCoverage, session)