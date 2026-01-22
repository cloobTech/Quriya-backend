from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.project_state_coverage import ProjectStateCoverage


class StateCoverageRepository(BaseRepository[ProjectStateCoverage]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProjectStateCoverage, session)

    async def get_existing_ids(self, project_id: str, ids: list[str], field_name: str) -> set:
        """Get all the ids (states) this project is currectly monitoring"""
        stmt = (
            select(getattr(self.model, field_name))
            .where(
                self.model.project_id == project_id,
                getattr(self.model, field_name).in_(ids)
            )
        )
        result = await self.session.execute(stmt)
        return {row[0] for row in result}


    async def get_existing_by_state_ids(self, project_id: str, ids: set[str]) -> dict[str, str]:
        """
        Return mapping { state_id: project_state_coverage_id } for LGAs already covered by the project.
        """
        if not ids:
            return {}
        stmt = (
            select(self.model.state_id, self.model.id)
            .where(self.model.project_id == project_id, self.model.state_id.in_(ids))
        )
        result = await self.session.execute(stmt)
        return {row[0]: row[1] for row in result.all()}
    


    async def get_state_coverage(self, project_id: str) -> list[ProjectStateCoverage]:
        stmt = (select(
            ProjectStateCoverage
        ).where(
            ProjectStateCoverage.project_id == project_id
        ).options(
            selectinload(ProjectStateCoverage.state)
        ))

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
