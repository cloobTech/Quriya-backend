from src.unit_of_work.unit_of_work import UnitOfWork
from src.models.project_member import ProjectMember
from src.schemas.election_project_member import AddMultipleProjectMembers
from src.core.exceptions import EntityNotFoundError
from src.utils.fetch_or_exists import fetch_or_exists


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
        


    # async def get_project_member(self, user_id: str, project_id: str) -> ProjectMember:
    #     async with self.uow_factory as uow:
    #         return await uow.election_project_member_repo.get_member_by_user_id(user_id=user_id, project_id=project_id)