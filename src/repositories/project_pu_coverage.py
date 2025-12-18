from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.project_pu_coverage import ProjectPuCoverage


class PuCoverageRepository(BaseRepository[ProjectPuCoverage]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProjectPuCoverage, session)

    async def get_existing_ids(self, project_id: str, ids: list[str], field_name: str) -> set:
        """Get all the [coverage ids (polling units)] this project is currectly monitoring"""
        stmt = (
            select(getattr(self.model, field_name))
            .where(
                self.model.project_id == project_id,
                getattr(self.model, field_name).in_(ids)
            )
        )
        result = await self.session.execute(stmt)
        return {row[0] for row in result}
