from datetime import datetime, timezone
from src.services.organization import OrganizationService
from src.services.user import UserService
from src.schemas.user import CreateUser
from src.schemas.organization import CreateOrganization
from src.auth.security import hash_password, verify_password, retrive_token
from src.auth.schemas import Login, TokenResponse
from src.core.exceptions import InvalidCredentialsError


class AuthService:
    """Service class for managing organizations."""

    def __init__(self, org_service: OrganizationService, user_service: UserService) -> None:
        self.org_service = org_service
        self.user_service = user_service

    async def register_organization(self, org_data: CreateOrganization, user_data: CreateUser) -> TokenResponse:
        """Register a new Organization"""
        if user_data.password:
            user_data.password = hash_password(user_data.password)
        _, admin_user = await self.org_service.create_organization_with_admin(org_data, user_data)

        token = retrive_token(admin_user)

        return TokenResponse(
            token=token,
            message="Organization successfully created"
        )

    async def login(self, login_details: Login) -> TokenResponse:
        """Login User"""
        user = await self.user_service.get_user_by_email(
            login_details.email)
        if user is None or not verify_password(user, login_details.password):
            raise InvalidCredentialsError("Invalid Credentials")
        # check user status
        # check email verification
        user.last_login = datetime.now(timezone.utc)
        token = retrive_token(user)

        return TokenResponse(
            token=token,
        )
