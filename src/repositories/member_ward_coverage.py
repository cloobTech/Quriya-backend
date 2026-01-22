from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.member_ward_coverage import MemberWardCoverage
from src.repositories.base import BaseRepository


class MemberWardCoverageRepository(BaseRepository[MemberWardCoverage]):
    """Repository class for managing MemberWardCoverages."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(MemberWardCoverage, session)


    async def get_ward_coverage_by_member_and_ward_coverage_id(self, member_id: str, ward_coverage_id: str) -> MemberWardCoverage | None:
        stmt = select(MemberWardCoverage).where(
            MemberWardCoverage.member_id == member_id,
            MemberWardCoverage.ward_coverage_id == ward_coverage_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()