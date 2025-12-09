from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.api.v1.dependencies import get_auth_service
from src.schemas.organization import CreateOrganizationWithAdmin
from src.auth.services import AuthService
from src.auth.schemas import TokenResponse, Login


router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def create_organization(org: CreateOrganizationWithAdmin, auth: AuthService = Depends(get_auth_service)):
    response = await auth.register_organization(
        org.organization, org.admin_user
    )

    return response


@router.post('/login', response_model=TokenResponse)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), auth: AuthService = Depends(get_auth_service)):
    """Handle Logging in a user"""

    credentials = Login(email=user_credentials.username,
                        password=user_credentials.password)

    response = await auth.login(credentials)
    return response
