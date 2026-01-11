from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.member_ward_coverage import MemberWardCoverage
from src.repositories.base import BaseRepository


class MemberWardCoverageRepository(BaseRepository[MemberWardCoverage]):
    """Repository class for managing MemberWardCoverages."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(MemberWardCoverage, session)