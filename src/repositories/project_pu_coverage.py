from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.project_pu_coverage import ProjectPuCoverage


class PuCoverageRepository(BaseRepository[ProjectPuCoverage]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProjectPuCoverage, session)

    # async def get_existing_ids(self, project_id: str, ids: list[str], field_name: str) -> set:
    #     """Get all the [coverage ids (polling units)] this project is currectly monitoring"""
    #     stmt = (
    #         select(getattr(self.model, field_name))
    #         .where(
    #             self.model.project_id == project_id,
    #             getattr(self.model, field_name).in_(ids)
    #         )
    #     )
    #     result = await self.session.execute(stmt)
    #     return {row[0] for row in result}

    async def get_existing_ids(self, ids: set[str]) -> set[str]:
        """
        Return the subset of IDs that actually exist in the wards table.
        """
        if not ids:
            return set()

        stmt = select(self.model.id).where(self.model.id.in_(ids))
        result = await self.session.execute(stmt)
        return {row[0] for row in result}

    async def get_pu_coverage(
        self,
        project_id: str,
        ward_coverage_id: str,
        assigned_status: bool | None = None  # None=all, True=assigned, False=unassigned
    ) -> list[ProjectPuCoverage]:
        stmt = (
            select(ProjectPuCoverage)
            .where(
                ProjectPuCoverage.project_id == project_id,
                ProjectPuCoverage.ward_coverage_id == ward_coverage_id
            )
            .options(selectinload(ProjectPuCoverage.polling_unit))
        )

        if assigned_status is not None:
            if assigned_status:  # True = assigned
                stmt = stmt.where(ProjectPuCoverage.assignments != None)
            else:  # False = unassigned
                stmt = stmt.where(ProjectPuCoverage.assignments == None)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_existing_by_pu_ids(self, project_id: str, ids: set[str]) -> dict[str, str]:
        """
        Return mapping { pu_id: project_pu_coverage_id } for pus already covered by the project.
        """
        if not ids:
            return {}
        stmt = (
            select(self.model.pu_id, self.model.id)
            .where(self.model.project_id == project_id, self.model.pu_id.in_(ids))
        )
        result = await self.session.execute(stmt)
        return {row[0]: row[1] for row in result.all()}

    # async def get_ward_ids_for_pus(self, ids: set[str]) -> dict[str, str]:
    #     """Return mapping { pu_id : ward_id } for the provided ward ids."""
    #     if not ids:
    #         return {}
    #     stmt = select(self.model.id, self.model.ward_coverage_id).where(
    #         self.model.id.in_(ids))
    #     result = await self.session.execute(stmt)
    #     return {row[0]: row[1] for row in result.all()}
