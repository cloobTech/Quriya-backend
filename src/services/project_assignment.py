from src.unit_of_work.unit_of_work import UnitOfWork
from src.models.project_assigment import ProjectAssignment
from src.schemas.project_assignment import AssignPollingUnitToProjectMember
from src.core.exceptions import EntityNotFoundError, InvalidCoverageSelectionError
from src.utils.fetch_or_exists import fetch_or_exists
from src.models.project_member import ProjectMember
from src.validations.coverage import validate_location_existence


class ProjectAssignmentService:
    """Manage project assignments"""

    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def assign_polling_units_to_project_member(self, data: AssignPollingUnitToProjectMember, project_id: str) -> list[ProjectAssignment]:
        """Assign Polling Units to Project Member"""

        async with self.uow_factory as uow:
            # validate organization exists
            if not await fetch_or_exists(uow.election_project_repo, id=project_id, only_exists=True):
                raise EntityNotFoundError(
                    message="Election project not found",
                    details={"project_id": project_id}
                )
            project_member = await uow.election_project_member_repo.get_member_by_user_id(
                user_id=data.user_id,
                project_id=project_id)
            if not project_member:
                project_member = ProjectMember(user_id=data.user_id,
                                               election_project_id=project_id)
            await uow.election_project_member_repo.create(project_member)

            pu_ids = set(data.polling_unit_ids)  # Remove duplicates if any
            assignments = []
            
            await validate_location_existence(repo=uow.polling_unit_repo, ids=list(pu_ids))
        
            for pu_id in pu_ids:
                assignment = await uow.project_assignment_repo.create(
                    ProjectAssignment(
                        project_member_id=project_member.id,
                        polling_unit_id=pu_id
                    )
                )
                assignments.append(assignment)
            return assignments
