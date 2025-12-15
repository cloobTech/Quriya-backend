from src.storage.database import Database
from src.models.user import User
from src.models.organization import Organization
from src.models.election_project import ElectionProject
from src.models.election_project_assigment import ElectionProjectAssignment
from src.models.election_project_member import ElectionProjectMember
from src.models.ward import Ward
from src.models.polling_unit import PollingUnit
from src.models.local_government_area import LGA
from src.models.state import State
from src.models.project_pu_coverage import ProjectPuCoverage
from src.models.project_lga_coverage import ProjectLgaCoverage
from src.models.project_ward_coverage import ProjectWardCoverage
from src.models.project_state_coverage import ProjectStateCoverage

__all__ = ['Database', 'User', 'Organization', 'ElectionProjectMember',
           'ElectionProjectAssignment', 'ElectionProject', 'PollingUnit', 'Ward', 'State',
           'LGA', "ProjectStateCoverage", "ProjectWardCoverage", "ProjectLgaCoverage", "ProjectPuCoverage"]

db = Database(db_uri="sqlite+aiosqlite:///./test.db")
