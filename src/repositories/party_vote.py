from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base import BaseRepository
from src.models.party_vote import PartyVote


class PartyVoteRepository(BaseRepository[PartyVote]):
    """Repository class for managing party votes"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(PartyVote, session)
