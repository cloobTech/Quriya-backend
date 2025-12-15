from src.unit_of_work.unit_of_work import UnitOfWork
from src.models.election_project_member import ElectionProjectMember
from src.schemas.election_project_member import AddElectionProjectMember
from src.core.exceptions import EntityNotFoundError


class ElectionProjectMemberService:
    """manage users attached an election monitoring project"""

    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def add_member_to_election_project(self):
        async with self.uow_factory as uow:
            pass
