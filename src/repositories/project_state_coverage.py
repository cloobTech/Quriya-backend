from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.project_state_coverage import ProjectStateCoverage


class StateCoverageRepository(BaseRepository[ProjectStateCoverage]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProjectStateCoverage, session)