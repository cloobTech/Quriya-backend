from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.repositories.base import BaseRepository
from src.models.project_member import ProjectMember
from src.models.enums import ElectionRole
from src.models.project_assigment import ProjectAssignment
from src.models.member_ward_coverage import MemberWardCoverage
from src.models.project_state_coverage import ProjectStateCoverage
from src.models.project_lga_coverage import ProjectLgaCoverage
from src.models.project_ward_coverage import ProjectWardCoverage
from src.models.project_pu_coverage import ProjectPuCoverage


class ProjectMemberRepository(BaseRepository[ProjectMember]):
    """Repository class for managing users as project members"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProjectMember, session)

    async def get_member_by_user_id(self, user_id: str, project_id: str) -> ProjectMember | None:
        project_member = await self.filter_one(user_id=user_id, election_project_id=project_id)
        if not project_member:
            return None
        return project_member

    async def list_by_project(
        self,
        project_id: str,
        role: ElectionRole | None = None,
    ) -> list[ProjectMember]:
        stmt = select(ProjectMember).where(
            ProjectMember.election_project_id == project_id
        ).options(
            selectinload(ProjectMember.user)
        )

        if role:
            stmt = stmt.where(ProjectMember.role == role)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_agents_with_assignments_and_location(
        self,
        project_id: str,
        role: ElectionRole = ElectionRole.FIELD_AGENT,
    ) -> list[ProjectMember]:

        stmt = (
            select(ProjectMember)
            .where(
                ProjectMember.election_project_id == project_id,
                ProjectMember.role == role
            )
            .options(
                selectinload(ProjectMember.user),

                selectinload(ProjectMember.state_coverage)
                .selectinload(ProjectStateCoverage.state),

                selectinload(ProjectMember.lga_coverage)
                .selectinload(ProjectLgaCoverage.lga),

                selectinload(ProjectMember.member_ward_coverage)
                .selectinload(MemberWardCoverage.ward_coverage)
                .selectinload(ProjectWardCoverage.ward),

                selectinload(ProjectMember.assignments)
                .selectinload(ProjectAssignment.pu_coverage)
                .selectinload(ProjectPuCoverage.polling_unit),
            )

        )

        result = await self.session.execute(stmt)
        return list(result.scalars().unique().all())
