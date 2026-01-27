from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.local_government_area import LGA
from src.models.ward import Ward
from src.models.project_pu_coverage import ProjectPuCoverage
from src.models.project_lga_coverage import ProjectLgaCoverage
from src.models.project_ward_coverage import ProjectWardCoverage
from src.models.project_state_coverage import ProjectStateCoverage
from src.models.polling_unit import PollingUnit
from src.models.project_assigment import ProjectAssignment
from src.models.result import Result
from src.models.project_member import ProjectMember
from src.schemas.project_coverage import PUQueryParams
from src.schemas.default import PaginationParams


class PuCoverageRepository(BaseRepository[ProjectPuCoverage]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProjectPuCoverage, session)

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
                stmt = stmt.where(ProjectPuCoverage.assignment != None)
            else:  # False = unassigned
                stmt = stmt.where(ProjectPuCoverage.assignment == None)

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

    async def get_pu_coverage_with_result_status_and_agents(
        self,
        project_id: str,
        filters: PUQueryParams,
        pagination: PaginationParams

    ):
        """Return list of ProjectPuCoverage with result status and agents loaded."""

        stmt = (
            select(ProjectPuCoverage.id)
            .where(ProjectPuCoverage.project_id == project_id)
            .order_by(ProjectPuCoverage.created_at.desc())

        )

        if filters.status:
            stmt = stmt.where(ProjectPuCoverage.status == filters.status)

        if filters.search:
            stmt = stmt.join(ProjectPuCoverage.polling_unit).where(
                PollingUnit.name.ilike(f"%{filters.search}%")
            )

        if filters.ward_id:
            stmt = stmt.join(
                ProjectPuCoverage.ward_coverage).where(
                ProjectWardCoverage.id == filters.ward_id
            )

        puc_ids, total = await self.paginate(stmt, limit=pagination.limit, offset=pagination.offset)
        if not puc_ids:
            return [], 0

        stmt = (
            select(ProjectPuCoverage)
            .where(ProjectPuCoverage.id.in_(puc_ids))
            .options(
                selectinload(ProjectPuCoverage.polling_unit),

                selectinload(ProjectPuCoverage.assignment).selectinload(
                    ProjectAssignment.member).selectinload(
                    ProjectMember.user
                ),

                selectinload(ProjectPuCoverage.polling_units_result)
                .selectinload(Result.incidents),

                selectinload(ProjectPuCoverage.ward_coverage).selectinload(
                    ProjectWardCoverage.ward),
                    
                # Ward coverage → LGA coverage → LGA
                selectinload(ProjectPuCoverage.ward_coverage)
                .selectinload(ProjectWardCoverage.lga_coverage)
                .selectinload(ProjectLgaCoverage.lga),

                # LGA coverage → State coverage → State
                selectinload(ProjectPuCoverage.ward_coverage)
                .selectinload(ProjectWardCoverage.lga_coverage)
                .selectinload(ProjectLgaCoverage.state_coverage)
                .selectinload(ProjectStateCoverage.state),

            ))

        pu_coverages = (await self.session.scalars(stmt)).unique().all()
        return list(pu_coverages), total
