from sqlalchemy.exc import NoResultFound
from typing import Tuple
from src.models.organization import Organization
from src.models.enums import UserRole
from src.models.user import User
from src.models.organization import Organization
from src.schemas.organization import CreateOrganization
from src.schemas.user import CreateUser
from src.unit_of_work.unit_of_work import UnitOfWork
from src.events.organization_events import OrganizationCreatedEvent
from src.core.exceptions import UserAlreadyExistsError, EntityNotFoundError


class OrganizationService:
    """Service class for managing organizations."""

    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def create_organization_with_admin(self, org_data: CreateOrganization, user_data: CreateUser) -> Tuple[Organization, User]:
        """Create a new organization."""
        async with self.uow_factory as uow:
            user = await uow.users_repo.filter_by(email=user_data.email)
            if user:
                raise UserAlreadyExistsError("user exist already")
            org = Organization(**org_data.model_dump())
            new_org = await uow.organizations_repo.create(org)
            user_data.organization_id = new_org.id
            user_data.role = UserRole.ORG_ADMIN
            admin_user = await uow.users_repo.create(User(**user_data.model_dump()))
            uow.collect_event(OrganizationCreatedEvent(
                admin_name=f"{admin_user.first_name} {admin_user.last_name}",
                organization_name=new_org.name,
                admin_email=admin_user.email,
                event_type="OrganizationCreated"
            ))
            return new_org, admin_user

    async def get_org(self, org_id: str) -> Organization:
        """Get organization by Id"""
        async with self.uow_factory as uow:
            try:
                org = await uow.organizations_repo.get_by_id(org_id)
                if org is None:
                    raise EntityNotFoundError(
                        message=f"Organization with id {org_id} not found")
                return org
            except NoResultFound as e:
                raise EntityNotFoundError(message=str(e))
