import math
from src.unit_of_work.unit_of_work import UnitOfWork
from src.models.project_member import ProjectMember
from src.schemas.project_member import AddMultipleProjectMembers, ProjectMemberResponse, ProjectAgentResponse, AssignmentResponse
from src.core.exceptions import EntityNotFoundError
from src.utils.fetch_or_exists import fetch_or_exists
from src.models.enums import ElectionRole
from src.schemas.default import PaginationParams, PaginatedResponse, Meta


class ProjectMemberService:
    """manage users attached an election monitoring project"""

    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def add_members_to_election_project(self, data: AddMultipleProjectMembers, project_id: str) -> list[ProjectMember]:
        async with self.uow_factory as uow:
            if not await fetch_or_exists(uow.election_project_repo, id=project_id, only_exists=True):
                raise EntityNotFoundError(
                    message="Election project not found",
                    details={"project_id": project_id}
                )
            members = [
                ProjectMember(
                    **member.model_dump(), election_project_id=project_id)
                for member in data.members
            ]

            if not members:
                raise EntityNotFoundError(message="No members to add")
            await uow.election_project_member_repo.bulk_create(members)
            return members

    async def get_project_members(self, project_id: str, role: ElectionRole | None = None) -> list[ProjectMemberResponse]:
        """Get project members"""
        async with self.uow_factory as uow:
            members = await uow.election_project_member_repo.list_by_project(project_id=project_id, role=role)
            return [
                ProjectMemberResponse.model_validate(member)
                for member in members
            ]

    async def get_agents_with_assignments_and_location(self, project_id: str,
                                                       pagination: PaginationParams):
        async with self.uow_factory as uow:
            members, total = await uow.election_project_member_repo.list_agents_with_assignments_and_location(project_id=project_id, pagination=pagination)

            result = [
                {
                    "id": str(member.id),
                    "user_id": str(member.user_id),
                    "role": member.role.value,
                    "status": member.status.value,
                    "updated_at": member.updated_at,
                    "user": {
                        "id": str(member.user.id),
                        "email": member.user.email,
                        "name": member.user.full_name,
                    },
                    "state_coverage": {
                        "id": str(member.state_coverage.id),
                        "name": member.state_coverage.state.name,

                    } if member.state_coverage else None,
                    "lga_coverage": {
                        "id": str(member.lga_coverage.id),
                        "name": member.lga_coverage.lga.name,

                    } if member.lga_coverage else None,
                    "wards": [
                        {"name": ward.ward_coverage.ward.name, "ward_coverage_id": ward.ward_coverage_id} for ward in member.member_ward_coverage
                    ],
                    "polling_units": [
                        {"name": pu.pu_coverage.polling_unit.name, "formatted_address": pu.pu_coverage.polling_unit.formatted_address, "code": pu.pu_coverage.polling_unit.code} for pu in member.assignments
                    ]
                }
                for member in members

            ]

            meta = Meta(
                page=pagination.page,
                page_size=pagination.page_size,
                total=total,
                total_pages=math.ceil(total / pagination.page_size),
            )

            return PaginatedResponse(
                data=result,
                meta=meta

            )

    async def get_agent_statistics(self, project_id: str):
        async with self.uow_factory as uow:
            stats, total_pus = await uow.election_project_member_repo.agent_statistics(
                project_id=project_id
            )

            return {
                "total_agents": stats.total_agents or 0,
                "active_agents": stats.active_agents or 0,
                "invited_agents": stats.invited_agents or 0,
                "suspended_agents": stats.suspended_agents or 0,
                "deactivated_agents": stats.deactivated_agents or 0,
                "idle_agents": stats.idle_agents or 0,
                "total_pus_assigned": stats.total_pus_assigned or 0,
                "total_pus_in_project": total_pus or 0,
            }
