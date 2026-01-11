from sqlalchemy.exc import NoResultFound
from src.models.organization import Organization
from src.models.organization import Organization
from src.schemas.organization import CreateOrganization
from src.unit_of_work.unit_of_work import UnitOfWork
from src.events.organization_events import OrganizationCreatedEvent
from src.core.exceptions import  EntityNotFoundError


class OrganizationService:
    """Service class for managing organizations."""

    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    # async def create_organization_with_admin(self, org_data: CreateOrganization, user_data: CreateUser) -> Tuple[Organization, User]:
    #     """Create a new organization."""
    #     async with self.uow_factory as uow:
    #         user = await uow.users_repo.filter_by(email=user_data.email)
    #         if user:
    #             raise UserAlreadyExistsError("user exist already")
    #         existing_org = await uow.organizations_repo.filter_one(slug=org_data.slug)
    #         if existing_org:
    #             raise EntityNotFoundError(
    #                 message="Organization with this slug already exist",
    #                 details={"organization_name": org_data.name,
    #                          "organization_slug": org_data.slug}
    #             )

    #         org = Organization(**org_data.model_dump())
    #         new_org = await uow.organizations_repo.create(org)
    #         user_data.organization_id = new_org.id
    #         user_data.role = UserRole.ORG_ADMIN
    #         admin_user = await uow.users_repo.create(User(**user_data.model_dump()))
    #         uow.collect_event(OrganizationCreatedEvent(
    #             admin_name=f"{admin_user.first_name} {admin_user.last_name}",
    #             organization_name=new_org.name,
    #             admin_email=admin_user.email,
    #             event_type="OrganizationCreated"
    #         ))
    #         return new_org, admin_user

    async def create_organization(self, org_data: CreateOrganization) -> Organization:
        existing_org = await self.uow_factory.organizations_repo.filter_one(name=org_data.name)
        if existing_org:
            raise EntityNotFoundError(
                message="Organization with this name already exist",
                details={"organization_name": org_data.name}
            )

        org = Organization(**org_data.model_dump())
        new_org = await self.uow_factory.organizations_repo.create(org)
        return new_org

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

    async def get_by_slug(self, org_slug: str) -> Organization:
        async with self.uow_factory as uow:
            try:
                org = await uow.organizations_repo.filter_one(slug=org_slug)
                if org is None:
                    raise EntityNotFoundError(
                        message=f"Organization with slug {org_slug} not found")
                return org
            except NoResultFound as e:
                raise EntityNotFoundError(message=str(e))
