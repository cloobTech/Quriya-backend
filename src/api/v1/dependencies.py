from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.unit_of_work.unit_of_work import UnitOfWork
from src.storage import db
from src.services.organization import OrganizationService
from src.services.user import UserService
from src.auth.services import AuthService
from src.auth.security import verify_access_token
from src.models.user import User
from src.schemas.user import UserRole
from src.core.exceptions import PermissionDeniedError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with db.get_session() as session:
        yield session


def get_uow(session: AsyncSession = Depends(get_session)):
    return UnitOfWork(session)


def get_auth_service(uow_factory=Depends(get_uow)):
    org_service = OrganizationService(uow_factory)
    user_service = UserService(uow_factory)

    return AuthService(
        org_service=org_service,
        user_service=user_service
    )


def get_user_service(uow: UnitOfWork = Depends(get_uow)):
    return UserService(uow)


def get_org_service(uow: UnitOfWork = Depends(get_uow)):
    return OrganizationService(uow)


# async def get_current_user(token: str = Depends(oauth2_scheme), user_service: UserService = Depends(get_user_service)) -> User:
#     credential_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                           detail="Could not validate User token", headers={"WWW-Authenticate": "Bearer"})
#     payload: dict = verify_access_token(token, credential_exceptions)
#     current_user = await user_service.uow_factory.users_repo.get_by_id(payload['user_id'])
#     if not current_user:
#         raise credential_exceptions
#     return current_user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    uow: UnitOfWork = Depends(get_uow),
) -> User:
    credential_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_access_token(token, credential_exceptions)

    async with uow:
        user = await uow.users_repo.get_by_id(payload["user_id"])

    if not user:
        raise credential_exceptions

    return user


def require_role(*allowed_roles: UserRole):
    async def org_checker(
        current_user=Depends(get_current_user),
    ):
        # Super admin bypass
        if current_user.role == UserRole.SUPER_ADMIN:
            return current_user

        # Normal org users
        if current_user.role not in allowed_roles:
            raise PermissionDeniedError(
                details={
                    "recommendation": f"check if user has one of the following roles - [{allowed_roles}]"
                }
            )

        return current_user

    return org_checker


def require_role_in_org(*allowed_roles: UserRole):
    async def org_checker(
        current_user=Depends(get_current_user),
        org_id: str = Path(...)
    ):
        # Super admin bypass
        if current_user.role == UserRole.SUPER_ADMIN:
            return current_user

        # Normal org users
        if current_user.role not in allowed_roles:
            raise PermissionDeniedError()

        if current_user.organization_id != org_id:
            raise PermissionDeniedError()

        return current_user

    return org_checker


# def require_project_role(*allowed_roles):
#     async def checker(
#         current_user = Depends(get_current_user),
#         project_id: str = Path(...),
#         member_service: ProjectMemberService = Depends(...)
#     ):
#         member = await member_service.get_member(project_id, current_user.id)
#         if not member or member.role not in allowed_roles:
#             raise HTTPException(403, "Not permitted")
#         return member

#     return checker
