from src.unit_of_work.unit_of_work import UnitOfWork
from src.models.project import Project
# from src.models.user import User
from src.schemas.election_project import CreateProject
from src.core.exceptions import EntityNotFoundError
# from src.models.enums import UserRole


class ProjectService:
    """Manage election monitoring"""

    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def create_election_monitoring_project(self, data: CreateProject, organization_id: str, createdby_user_id: str) -> Project:
        """create a new project"""

        async with self.uow_factory as uow:
            org = await uow.organizations_repo.get_by_id(organization_id)
            if not org:
                raise EntityNotFoundError(
                    message=f"cannot find organization with this id - {organization_id}", details={"hello": "hi"})
            # we can later choose to make sure that only
            election_project = await uow.election_project_repo.create(Project(**data.model_dump(), organization_id=organization_id,
                                                                              createdby_user_id=createdby_user_id,))
            # we can send an email or notification here
            return election_project

    async def get_organization_projects(self, organization_id: str) -> list[Project]:

        async with self.uow_factory as uow:
            projects = await uow.election_project_repo.filter_by(organization_id=organization_id)
            return projects

    async def get_organization_project(self, project_id: str) -> Project:

        async with self.uow_factory as uow:
            project = await uow.election_project_repo.get_by_id(project_id)
            if project is None:
                raise EntityNotFoundError(
                    message=f"cannot find project with this id - {project_id}", details={"project_id": project_id})
            return project
