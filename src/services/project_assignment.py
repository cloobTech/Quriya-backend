from src.unit_of_work.unit_of_work import UnitOfWork
from src.models.project import Project
from src.models.project_assigment import ProjectAssignment
from src.models.project_member import ProjectMember
from src.models.member_ward_coverage import MemberWardCoverage
from src.schemas.project_assignment import AssignPollingUnitToProjectMember
from src.core.exceptions import EntityNotFoundError
from src.utils.fetch_or_exists import fetch_or_exists
from src.utils.agent_code import generate_agent_code
from src.validations.coverage import validate_location_existence


class ProjectAssignmentService:
    """Manage project assignments"""

    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def assign_polling_units_to_project_member(self, data: AssignPollingUnitToProjectMember, project_id: str) -> list[ProjectAssignment]:
        """Assign Polling Units to Project Member"""

        async with self.uow_factory as uow:
            # validate organization exists
            # validate project exists
            project = await fetch_or_exists(uow.election_project_repo, id=project_id)
            if not isinstance(project, Project):
                raise TypeError(
                    f"Expected 'Project', got '{type(project).__name__}'")
            if not project:
                raise EntityNotFoundError(
                    message="Election project not found",
                    details={"project_id": project_id}
                )
            project_member = await uow.election_project_member_repo.get_member_by_user_id(
                user_id=data.user_id,
                project_id=project_id)
            if not project_member:
                agent_code = generate_agent_code(project=project)
                project_member = ProjectMember(user_id=data.user_id,
                                               election_project_id=project_id, state_coverage_id=data.state_coverage_id,
                                               lga_coverage_id=data.lga_coverage_id, agent_code=agent_code)

            existing_ward_coverage = await uow.member_ward_coverage_repo.get_ward_coverage_by_member_and_ward_coverage_id(
                member_id=project_member.id, ward_coverage_id=data.ward_coverage_id
            )
            if existing_ward_coverage is None:
                ward = MemberWardCoverage(
                    ward_coverage_id=data.ward_coverage_id, member_id=project_member.id)

# ...........................................................................................>>....>>>>>>>>>>>>>>>>>>>>>>>>
            await uow.election_project_member_repo.create(project_member)
            await uow.member_ward_coverage_repo.create(ward)

            pu_ids = set(data.pu_coverage_ids)  # Remove duplicates if any
            assignments = []

            await validate_location_existence(repo=uow.pu_coverage_repo, ids=list(pu_ids))

            for pu_id in pu_ids:
                assignment = await uow.project_assignment_repo.create(
                    ProjectAssignment(
                        project_member_id=project_member.id,
                        pu_coverage_id=pu_id
                    )
                )
                assignments.append(assignment)
            return assignments
