from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.repositories.user import UserRepository
from src.repositories.member_ward_coverage import MemberWardCoverageRepository
from src.repositories.organization import OrganizationRepository
from src.repositories.project import ProjectRepository
from src.repositories.project_member import ProjectMemberRepository
from src.repositories.ward import WardRepository
from src.repositories.polling_unit import PollingRepository
from src.repositories.state import StateRepository
from src.repositories.local_government_area import LgaRepository
from src.repositories.project_pu_coverage import PuCoverageRepository
from src.repositories.project_ward_coverage import WardCoverageRepository
from src.repositories.project_state_coverage import StateCoverageRepository
from src.repositories.project_lga_coverage import LgaCoverageRepository
from src.repositories.project_assignment import ProjectAssignmentRepository
from src.repositories.media import ResultMediaRepository
from src.repositories.result import ResultRepository
from src.repositories.party_vote import PartyVoteRepository
from src.repositories.political_party import PoliticalPartyRepository
from src.events.bus import event_bus
from src.events.base import DomainEvent
from src.core.exceptions import UniqueViolationError


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.event_bus = event_bus
        self._pending_events: List[DomainEvent] = []

        # --- Repositories ---
        self.users_repo = UserRepository(session)
        self.organizations_repo = OrganizationRepository(session)
        self.election_project_repo = ProjectRepository(session)
        self.election_project_member_repo = ProjectMemberRepository(
            session)
        self.ward_repo = WardRepository(
            session)
        self.polling_unit_repo = PollingRepository(
            session)
        self.lga_repo = LgaRepository(session)
        self.state_repo = StateRepository(session)
        self.pu_coverage_repo = PuCoverageRepository(session)
        self.ward_coverage_repo = WardCoverageRepository(session)
        self.lga_coverage_repo = LgaCoverageRepository(session)
        self.state_coverage_repo = StateCoverageRepository(session)
        self.project_assignment_repo = ProjectAssignmentRepository(session)
        self.result_media_repo = ResultMediaRepository(session)
        self.result_repo = ResultRepository(session)
        self.party_vote_repo = PartyVoteRepository(session)
        self.political_party_repo = PoliticalPartyRepository(session)
        self.member_ward_coverage_repo = MemberWardCoverageRepository(session)

    def collect_event(self, event: DomainEvent) -> None:
        self._pending_events.append(event)

    async def __aenter__(self):
        await self.session.begin()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:

        try:
            if exc_type is not None:
                await self.session.rollback()
                self._pending_events.clear()
                await self.session.close()
                return

            await self.session.commit()
        # except IntegrityError as e:
        #     print(exc_type, exc, tb)
        #     await self.session.rollback()
        #     self._pending_events.clear()
        #     raise UniqueViolationError("Duplicate record") from e
        except Exception:
            await self.session.rollback()
            self._pending_events.clear()
            raise
        finally:
            await self.session.close()

        # publish only if event_bus exists
        if self.event_bus is not None:
            for ev in self._pending_events:
                await self.event_bus.publish(ev)

        self._pending_events.clear()
