from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
# Currently Project Assignment is more of Polling Unit Assignment
from src.models.project_assigment import ProjectAssignment



class ProjectAssignmentRepository(BaseRepository[ProjectAssignment]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProjectAssignment, session)

    # async def list_by_member_with_location_hierarchy(self, member_id: str):
    #     """Get assignments with full location hierarchy in ONE query"""

    #     stmt = select(ProjectAssignment).where(
    #         ProjectAssignment.project_member_id == member_id
    #     ).options(
    #         selectinload(ProjectAssignment.polling_unit)
    #         .selectinload(PollingUnit.ward)
    #         .selectinload(Ward.lga)
    #         .selectinload(LGA.state)
    #     )

    #     result = await self.session.execute(stmt)

    #     return list(result.scalars().all())
