from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.project_ward_coverage import ProjectWardCoverage


class WardCoverageRepository(BaseRepository[ProjectWardCoverage]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProjectWardCoverage, session)

    async def get_existing_ids(self, project_id: str, ids: list[str], field_name: str) -> set:
        """Get all the ids (wards) this project is currectly monitoring"""
        stmt = (
            select(getattr(self.model, field_name))
            .where(
                self.model.project_id == project_id,
                getattr(self.model, field_name).in_(ids)
            )
        )
        result = await self.session.execute(stmt)
        return {row[0] for row in result}

    async def get_existing_by_ward_ids(self, project_id: str, ids: set[str]) -> dict[str, str]:
        """
        Return mapping { ward_id: project_ward_coverage_id } for wards already covered by the project.
        """
        if not ids:
            return {}
        stmt = (
            select(self.model.ward_id, self.model.id)
            .where(self.model.project_id == project_id, self.model.ward_id.in_(ids))
        )
        result = await self.session.execute(stmt)
        return {row[0]: row[1] for row in result.all()}

    # async def get_lga_ids_for_wards(self, ids: set[str]) -> dict[str, str]:
    #     """Return mapping { ward_id : lga_id } for the provided ward ids."""
    #     if not ids:
    #         return {}
    #     stmt = select(self.model.id, self.model.lga_coverage_id).where(
    #         self.model.id.in_(ids))
    #     result = await self.session.execute(stmt)
    #     return {row[0]: row[1] for row in result.all()}

    async def get_ward_coverage(self, project_id: str, lga_coverage_id: str) -> list[ProjectWardCoverage]:
        stmt = (select(
            ProjectWardCoverage
        ).where(
            ProjectWardCoverage.project_id == project_id, ProjectWardCoverage.lga_coverage_id == lga_coverage_id
        ).options(
            selectinload(ProjectWardCoverage.ward)
        ))

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
