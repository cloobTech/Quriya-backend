from enum import StrEnum


class UserRole(StrEnum):
    """User roles within the system"""
    SUPER_ADMIN = "super_admin"  # Platform administrators
    ORG_ADMIN = "org_admin"      # Organization administrators
    STAFF = "staff"
    ORG_OWNER = "organization_owner"


class ElectionRole(StrEnum):
    """user's role in a particular election project"""
    FIELD_AGENT = "field_agent"
    OBSERVER = "observer"
    SUPERVISOR = "supervisor"
    WARD_COORDINATOR = "ward_coordinator"
    LGA_COORDINATOR = "lga_coordinator"
    STATE_COORDINATOR = "state_coordinator"
    NATIONAL_COORDINATOR = "national_coordinator"


class ProjectMemberStatus(StrEnum):
    INVITED = "invited"
    ACTIVE = "active"
    REMOVED = "removed"


class UserStatus(StrEnum):
    """Status of user accounts"""
    PENDING_ACTIVATION = "pending_activation"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"
    IDLE = "idle"


class OrganizationType(StrEnum):
    """Types of organizations using the platform"""
    ELECTION_OBSERVER = "election_observer"
    POLITICAL_PARTY = "political_party"
    NGO = "ngo"
    CIVIL_SOCIETY = "civil_society"
    ELECTORAL_BODY = "electoral_body"


class OrganizationStatus(StrEnum):
    """Status of organizations"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"


class SubscriptionTier(StrEnum):
    """Subscription tiers for organizations"""
    FREE_TRIAL = "free_trial"
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class ElectionStatus(StrEnum):
    DRAFT = "draft"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    CANCELED = "canceled"


class ElectionType(StrEnum):
    PRESIDENTIAL = "presidential"
    GUBERNATORIAL = "gubernatorial"
    SENATORIAL = "senatorial"
    FEDERAL_HOUSE_OF_ASSEMBLY = "federal_house_of_assembly"
    STATE_HOUSE_OF_ASSEMBLY = "state_house_of_assembly"
    LOCAL_GOVERNMENT = "local_government"
    WARD = "ward"
    COUNCILLORSHIP = "councillorship"
    OTHERS = "others"


class ResultStatus(StrEnum):
    PENDING_REVIEW = "pending_review"
    VERIFIED = "verified"
    REJECTED = "rejected"


class MediaType(StrEnum):
    RESULT_SHEET = "result_sheet"
    INCIDENT_PHOTO = "incident_photo"
    ENVIRONMENT = "environment"
    OTHER = "other"
