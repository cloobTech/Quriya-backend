from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.project_lga_coverage import ProjectLgaCoverage


class LgaCoverageRepository(BaseRepository[ProjectLgaCoverage]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProjectLgaCoverage, session)

    async def get_existing_ids(self, project_id: str, ids: list[str], field_name: str) -> set:
        """Get all the ids (lgas) this project is currectly monitoring"""
        stmt = (
            select(getattr(self.model, field_name))
            .where(
                self.model.project_id == project_id,
                getattr(self.model, field_name).in_(ids)
            )
        )
        result = await self.session.execute(stmt)
        return {row[0] for row in result}

    async def get_existing_by_lga_ids(self, project_id: str, ids: set[str]) -> dict[str, str]:
        """
        Return mapping { lga_id: project_lga_coverage_id } for LGAs already covered by the project.
        """
        if not ids:
            return {}
        stmt = (
            select(self.model.lga_id, self.model.id)
            .where(self.model.project_id == project_id, self.model.lga_id.in_(ids))
        )
        result = await self.session.execute(stmt)
        return {row[0]: row[1] for row in result.all()}

    # async def get_state_ids_for_lgas(self, ids: set[str]) -> dict[str, str]:
    #     """Return mapping { lga_id: state_id } for the provided LGA ids."""
    #     if not ids:
    #         return {}
    #     stmt = select(self.model.id, self.model.state_coverage_id).where(
    #         self.model.id.in_(ids))
    #     result = await self.session.execute(stmt)
    #     return {row[0]: row[1] for row in result.all()}

    async def get_lga_coverage(self, project_id: str, state_coverage_id: str) -> list[ProjectLgaCoverage]:
        stmt = (select(
            ProjectLgaCoverage
        ).where(
            ProjectLgaCoverage.project_id == project_id, ProjectLgaCoverage.state_coverage_id == state_coverage_id
        ).options(
            selectinload(ProjectLgaCoverage.lga)
        ))

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
