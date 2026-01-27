from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, or_
from sqlalchemy.orm import selectinload
from src.repositories.base import BaseRepository
from src.models.project_member import ProjectMember
from src.models.enums import ElectionRole, ProjectMemberStatus
from src.models.project_assigment import ProjectAssignment
from src.models.member_ward_coverage import MemberWardCoverage
from src.models.project_state_coverage import ProjectStateCoverage
from src.models.project_lga_coverage import ProjectLgaCoverage
from src.models.project_ward_coverage import ProjectWardCoverage
from src.models.project_pu_coverage import ProjectPuCoverage
from src.models.user import User
from src.schemas.default import PaginationParams
from src.schemas.project_member import AgentQueryParams


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
        pagination: PaginationParams,
        filters: AgentQueryParams,
        role: ElectionRole = ElectionRole.FIELD_AGENT,

    ) -> tuple[list[ProjectMember], int]:

        base_stmt = (
            select(ProjectMember.id)
            .join(ProjectMember.user)
            .where(
                ProjectMember.election_project_id == project_id,
                ProjectMember.role == role
            )

            .order_by(ProjectMember.created_at.desc())

        )

        if filters.status:
            base_stmt = base_stmt.where(ProjectMember.status == filters.status)

        if filters.search:
            q = f"%{filters.search}%"
            base_stmt = base_stmt.where(
                or_(
                    User.first_name.ilike(q),
                    User.last_name.ilike(q),
                    User.email.ilike(q),
                )
            )

        if filters.state_id:
            base_stmt = base_stmt.join(ProjectMember.state_coverage).where(
                ProjectStateCoverage.id == filters.state_id
            )

        if filters.lga_id:
            base_stmt = base_stmt.join(ProjectMember.lga_coverage).where(
                ProjectLgaCoverage.id == filters.lga_id
            )

        if filters.ward_id:
            base_stmt = base_stmt.join(ProjectMember.member_ward_coverage).where(
                MemberWardCoverage.ward_coverage_id == filters.ward_id
            )

        member_ids, total = await self.paginate(base_stmt, limit=pagination.limit, offset=pagination.offset)
        # return result, total
        if not member_ids:
            return [], 0
        stmt = (
            select(ProjectMember)
            .where(ProjectMember.id.in_(member_ids))
            # .where(ProjectMember.id.in_([m.id for m in member_ids]))
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

        members = (await self.session.scalars(stmt)).unique().all()

        return list(members), total

    async def agent_statistics(
        self,
        project_id: str,

    ):
        """
        Returns stats for agents in a project:
        - total_agents
        - breakdown by status
        - total wards assigned
        - total polling units assigned
         """

        pm = ProjectMember
        pa = ProjectAssignment
        pu = ProjectPuCoverage

        stmt = (
            select(
                # func.count(pm.id).label("total_agents"),
                func.count(func.distinct(pm.id)).label("total_agents"),
                func.count(func.distinct(case(
                    (pm.status == ProjectMemberStatus.ACTIVE, pm.id), else_=None))).label("active_agents"),
                func.count(func.distinct(case(
                    (pm.status == ProjectMemberStatus.INVITED, pm.id), else_=None))).label("invited_agents"),
                func.count(func.distinct(case(
                    (pm.status == ProjectMemberStatus.SUSPENDED, pm.id), else_=None))).label("suspended_agents"),
                func.count(func.distinct(case(
                    (pm.status == ProjectMemberStatus.DEACTIVATED, pm.id), else_=None))).label(
                    "deactivated_agents"),
                func.count(func.distinct(case(
                    (pm.status == ProjectMemberStatus.IDLE, pm.id), else_=None))).label(
                    "idle_agents"),
                func.count(func.distinct(pa.pu_coverage_id)
                           ).label("total_pus_assigned"),
            )
            .outerjoin(pa, pm.id == pa.project_member_id)  # join assignments
            .where(pm.election_project_id == project_id, pm.role == ElectionRole.FIELD_AGENT)
        )

        result = await self.session.execute(stmt)
        stats = result.one()

        total_pus = await self.session.scalar(
            select(func.count(pu.id)).where(pu.project_id == project_id)
        )

        return stats, total_pus
