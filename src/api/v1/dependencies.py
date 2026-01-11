from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.unit_of_work.unit_of_work import UnitOfWork
from src.storage import db
from src.services.organization import OrganizationService
from src.services.user import UserService
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


def get_user_service(uow: UnitOfWork = Depends(get_uow)):
    return UserService(uow)


def get_org_service(uow: UnitOfWork = Depends(get_uow)):
    return OrganizationService(uow)


async def get_current_org(
    org_slug: str = Path(...),
    org_service: OrganizationService = Depends(get_org_service),
):
    org = await org_service.get_by_slug(org_slug)
    return org


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


def require_role_in_org(*allowed_roles: UserRole):
    async def org_checker(
        current_user=Depends(get_current_user),
        organization_id: str = Path(...)
    ):
        # Super admin bypass
        if current_user.role == UserRole.SUPER_ADMIN:
            return current_user

        # Normal org users
        if current_user.role not in allowed_roles:
            raise PermissionDeniedError(
                message="You do not have permission to perform this action",
                details={"user_id": current_user.id, "organization_id": organization_id}
            )

        if current_user.organization_id != organization_id:
            raise PermissionDeniedError(
                message="You do not have permission to perform this operation on this organization",
                details={"user_id": current_user.id, "organization_id": organization_id}
            )

        return current_user

    return org_checker


def validate_organization_route(current_user: User = Depends(get_current_user), organization_id: str = Path(...)) -> None:
    if current_user.organization_id != organization_id:
        raise PermissionDeniedError(
            message="You do not have permission to perform this operation on this organization",
            details={"user_id": current_user.id,
                     "organization_id": organization_id}
        )
