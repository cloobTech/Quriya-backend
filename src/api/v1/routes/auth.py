from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.api.v1.dependencies import get_uow
from src.schemas.organization import CreateOrganizationWithAdmin
from src.auth.services import AuthService
from src.auth.schemas import TokenResponse, Login
from src.unit_of_work.unit_of_work import UnitOfWork


router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def create_organization(org: CreateOrganizationWithAdmin, uow: UnitOfWork = Depends(get_uow)):
    auth = AuthService(uow)
    response = await auth.onboard_organization_with_admin(
        org.organization, org.admin_user
    )

    return response


@router.post('/login', response_model=TokenResponse)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), uow: UnitOfWork = Depends(get_uow)):
    """Handle Logging in a user"""

    credentials = Login(email=user_credentials.username,
                        password=user_credentials.password)

    auth = AuthService(uow)
    response = await auth.login(credentials)
    return response
