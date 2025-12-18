from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.project_lga_coverage import ProjectLgaCoverage


class LgaCoverageRepository(BaseRepository[ProjectLgaCoverage]):
    """Repository class for managing election monitoring projects"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProjectLgaCoverage, session)


    async def get_existing_ids(self, project_id: str, ids: list[str], field_name: str) -> set:
        """Get all the ids (lgas) this project is currectly monitoring"""
        stmt = (
            select(getattr(self.model, field_name))
            .where(
                self.model.project_id == project_id,
                getattr(self.model, field_name).in_(ids)
            )
        )
        result = await self.session.execute(stmt)
        return {row[0] for row in result}
