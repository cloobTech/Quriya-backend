from src.storage.database import Database
from src.models.user import User
from src.models.organization import Organization
from src.models.project import Project
from src.models.project_assigment import ProjectAssignment
from src.models.project_member import ProjectMember
from src.models.ward import Ward
from src.models.polling_unit import PollingUnit
from src.models.local_government_area import LGA
from src.models.state import State
from src.models.political_party import PoliticalParty
from src.models.project_pu_coverage import ProjectPuCoverage
from src.models.project_lga_coverage import ProjectLgaCoverage
from src.models.project_ward_coverage import ProjectWardCoverage
from src.models.project_state_coverage import ProjectStateCoverage
from src.models.party_vote import PartyVote
from src.models.result import Result
from src.models.media import ResultMedia
from src.models.incident import Incident


__all__ = ['Database', 'User', 'Organization', 'ProjectMember',
           'ProjectAssignment', 'Project', 'PollingUnit', 'Ward', 'State',
           'LGA', "ProjectStateCoverage", "ProjectWardCoverage", "ProjectLgaCoverage",
           "ProjectPuCoverage", "PoliticalParty", "PartyVote", "Result", "ResultMedia", "Incident"]

db = Database(db_uri="sqlite+aiosqlite:///./test.db")
