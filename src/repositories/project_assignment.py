from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.project_assigment import ProjectAssignment


class ProjectAssignmentRepository(BaseRepository[ProjectAssignment]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProjectAssignment, session)