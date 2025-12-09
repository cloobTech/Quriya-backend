from sqlalchemy.ext.asyncio import AsyncSession
from src.models.organization import Organization
from src.repositories.base import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):
    """Repository class for managing organizations."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Organization, session)
