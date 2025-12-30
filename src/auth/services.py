from src.services.organization import OrganizationService
from src.services.user import UserService
from src.schemas.user import CreateUser
from src.schemas.organization import CreateOrganization
from src.auth.security import hash_password, verify_password, retrive_token
from src.auth.schemas import Login, TokenResponse
from src.core.exceptions import InvalidCredentialsError
from src.unit_of_work.unit_of_work import UnitOfWork
from src.events.organization_events import OrganizationCreatedEvent


class AuthService:
    """Service class for managing organizations."""

    def __init__(
        self,
        uow_factory: UnitOfWork,

    ):
        self.uow_factory = uow_factory
        self.org_service = OrganizationService(uow_factory)
        self.user_service = UserService(uow_factory)

    async def onboard_organization_with_admin(self, org_data: CreateOrganization, user_data: CreateUser) -> TokenResponse:
        """onboard organization with admin"""
        async with self.uow_factory as uow:
            org = await self.org_service.create_organization(org_data)
            user_data.organization_id = org.id
            if user_data.password:
                user_data.password = hash_password(user_data.password)
            admin_user = await self.user_service.create_org_admin(user_data)

            token = retrive_token(admin_user)

            uow.collect_event(
                OrganizationCreatedEvent(
                    admin_name=f"{admin_user.first_name} {admin_user.last_name}",
                    organization_name=org.name,
                    admin_email=admin_user.email,
                    event_type="OrganizationCreated",
                )
            )

            return TokenResponse(
                token=token,
                message="Organization successfully created"
            )

    async def login(self, login_details: Login) -> TokenResponse:
        """Login User"""
        async with self.uow_factory:
            user = await self.user_service.get_user_by_email(
                login_details.email)
            if user is None or not verify_password(user, login_details.password):
                raise InvalidCredentialsError("Invalid Credentials")
            # check user status
            await self.user_service.update_last_login(user.id)
            token = retrive_token(user)

            return TokenResponse(
                token=token,
            )
