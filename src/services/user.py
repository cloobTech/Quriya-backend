from src.schemas.user import CreateUser
from src.models.user import User
from src.models.organization import Organization
from src.unit_of_work.unit_of_work import UnitOfWork
# from src.events.user_events import UserCreatedEvent
from src.core.exceptions import UserAlreadyExistsError, UniqueViolationError, EntityNotFoundError, PermissionDeniedError
from typing import Tuple


class UserService:
    """Service class for managing users."""

    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def create_user(self, user_data: CreateUser) -> User:
        """Create a new user.

        Args:
            user_data (CreateUser): Data required to create a new user.

        Returns:
            User: The created user instance.
        """
        try:
            async with self.uow_factory as uow:
                user = await uow.users_repo.filter_by(email=user_data.email)
                if user:
                    raise UserAlreadyExistsError(message="user's email exist already in the database", details={
                        "recommendation": "ask user to provide a different email"
                    })
                if user_data.organization_id is None:
                    raise ValueError("organization_id cannot be None")
                org = await uow.organizations_repo.get_by_id(user_data.organization_id)
                if org is None:
                    raise EntityNotFoundError(message=f"Organisation with {user_data.organization_id} ID  could not be found", details={
                        "recommendation": "make sure you are passing the correct organization_id"
                    })
                if org.id != user_data.admin_organization_id:
                    raise PermissionDeniedError(
                        message=f"Access denied: only an admin belonging to this organization - {org.name} can add users."
                    )

                user = User(**user_data.model_dump())
                created_user = await uow.users_repo.create(user)
                # uow.collect_event(UserCreatedEvent(email=created_user.email, first_name=created_user.first_name,
                #                                    last_name=created_user.last_name, event_type="UserCreated"))
            return created_user

        except UniqueViolationError:
            raise UserAlreadyExistsError(
                "User with this email already exists.")

    async def user_profile(self, user_id: str) -> Tuple[User, Organization]:
        async with self.uow_factory as uow:
            user = await uow.users_repo.get_by_id(user_id)
            if user is None:
                raise EntityNotFoundError(
                    f"User with id {user_id} does not exist.")
            org = await uow.organizations_repo.get_by_id(user.organization_id)
            if org is None:
                raise EntityNotFoundError(
                    f"Couldn't fetch user's Organisation")

            return user, org

    async def get_user_by_email(self, email: str):
        async with self.uow_factory as uow:
            user = await uow.users_repo.get_user_by_email(email)
            if user is None:
                raise EntityNotFoundError(
                    f"User with this ({email}) does not exist.")
            return user
