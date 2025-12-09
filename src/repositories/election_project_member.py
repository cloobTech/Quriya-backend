from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.election_project_member import ElectionProjectMember



class ElectionProjectMemberRepository(BaseRepository[ElectionProjectMember]):
    """Repository class for managing users as project members"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ElectionProjectMember, session)