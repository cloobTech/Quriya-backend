from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.project_member import ProjectMember


class ProjectMemberRepository(BaseRepository[ProjectMember]):
    """Repository class for managing users as project members"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProjectMember, session)

    async def get_member_by_user_id(self, user_id: str, project_id: str) -> ProjectMember | None:
        project_member = await self.filter_one(user_id=user_id, election_project_id=project_id)
        if not project_member:
            return None
        return project_member
