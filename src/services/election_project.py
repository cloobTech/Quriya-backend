from src.unit_of_work.unit_of_work import UnitOfWork
from src.models.election_project import ElectionProject
from src.schemas.election import CreateElectionProject
from src.core.exceptions import EntityNotFoundError


class ElectionProjectService:
    """Manage election monitoring"""

    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def create_election_monitoring_project(self, data: CreateElectionProject) -> ElectionProject:
        """create a new project"""

        async with self.uow_factory as uow:
            org = await uow.organizations_repo.get_by_id(data.organization_id)
            if not org:
                raise EntityNotFoundError(
                    message=f"cannot find organization with this id - {data.organization_id}", details={"hello": "hi"})
            # we can later choose to make sure that only
            election_project = await uow.election_project_repo.create(ElectionProject(**data.model_dump()))
            # we can send an email or notification here
            return election_project
