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


class ElectionProjectMemberStatus(StrEnum):
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



# class ProjectStatus(StrEnum):
#     """..."""
#     DRAFT = "draft"  # same as "not_started" for wards & Polling units
#     ONGOING = "ongoing"
#     COMPLETED = "completed"
#     SUSPENDED = "suspended"
#     CANCELED = "canceled"



