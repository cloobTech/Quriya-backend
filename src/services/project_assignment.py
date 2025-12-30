from src.unit_of_work.unit_of_work import UnitOfWork
from src.models.project_assigment import ProjectAssignment
from src.schemas.project_assignment import AssignPollingUnitToProjectMember
from src.core.exceptions import EntityNotFoundError
from src.utils.fetch_or_exists import fetch_or_exists


class ProjectAssignmentService:
    """Manage project assignments"""

    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def assign_polling_units_to_project_member(self, data: AssignPollingUnitToProjectMember, project_id: str) -> list[ProjectAssignment]:
        """Assign Polling Units to Project Member"""

        async with self.uow_factory as uow:
            if not await fetch_or_exists(uow.election_project_repo, id=project_id, only_exists=True):
                raise EntityNotFoundError(
                    message="Election project not found",
                    details={"project_id": project_id}
                )
            project_member = await uow.election_project_member_repo.get_member_by_user_id(
                user_id=data.user_id,
                project_id=project_id)
            if not project_member:
                raise EntityNotFoundError(
                    message="Project member not found",
                    details={
                        "user_id": data.user_id,
                        "project_id": project_id
                    }
                )
            pu_ids = set(data.polling_unit_ids)  # Remove duplicates if any
            assignments = []
            for pu_id in pu_ids:
                assignment = await uow.project_assignment_repo.create(
                    ProjectAssignment(
                        project_member_id=project_member.id,
                        polling_unit_id=pu_id
                    )
                )
                assignments.append(assignment)
            return assignments
